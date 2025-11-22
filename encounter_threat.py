from dataclasses import dataclass, field
from typing import List, Dict, Tuple

from models import Enemy, Character, BuildKey
from mobility import enemy_threat_vs_party, engagement_factor
from dice_math import (
    enemy_TTK_vs_party,
    enemy_DPR_vs_party,
    damage_stats_to_avg_char_for_party,
    dodge_fail_prob,
)
from parties import iter_parties_for_tier


# ---- Basic structures ----

@dataclass
class EncounterEnemySlot:
    """One enemy type and how many copies on a tile."""
    name: str
    count: int = 1


@dataclass
class EncounterTile:
    """A single tile's worth of enemies."""
    name: str
    enemies: List[EncounterEnemySlot]


@dataclass
class Encounter:
    """
    A full encounter that may have multiple tiles.

    We will score each tile independently; cross-tile interactions are ignored
    (matching your "95% of fights" assumption).
    """
    name: str
    level: int  # you can still use this if you want to map to tiers
    tiles: List[EncounterTile]


PLAYER_COUNTS = (1, 2, 3, 4)
TIERS = ("tier1", "tier2", "tier3")
BLEED_BONUS = 2.0  # +2 damage per bleed trigger


def _compute_bleed_rates_for_tile(
    tile: "EncounterTile",
    party: List[Character],
    enemies_by_name: Dict[str, Enemy],
) -> Tuple[Dict[str, float], Dict[str, float]]:
    """
    For this tile and party, compute:

      lambda_apply[name]: expected # of Bleed applications per activation
                          by enemies with this name (all copies)
      lambda_trig[name]:  expected # of trigger-capable hits per activation
                          by enemies with this name (all copies)

    Counts are respected: if a slot has count > 1, we scale rates accordingly.
    """
    P = len(party)
    if P == 0:
        return {}, {}

    def avg_p_not_dodge(enemy: Enemy) -> float:
        """Average P(not dodged) for this enemy vs the party."""
        if not enemy.dodge_difficulty or enemy.dodge_difficulty <= 0:
            return 1.0
        return sum(
            dodge_fail_prob(c.dodge_dice, enemy.dodge_difficulty)
            for c in party
        ) / P

    lambda_apply: Dict[str, float] = {}
    lambda_trig: Dict[str, float] = {}

    for slot in tile.enemies:
        enemy = enemies_by_name.get(slot.name)
        if enemy is None:
            continue

        p_not_dodge = avg_p_not_dodge(enemy)

        lam_apply_e = 0.0
        lam_trig_e = 0.0

        for action in enemy.actions:
            base_damage = action.damage
            dmg_type = action.damage_type

            # Trigger capacity: damaging hits this action would land
            E_base, p_damage_event = damage_stats_to_avg_char_for_party(
                base_damage=base_damage,
                damage_type=dmg_type,
                dodge_difficulty=enemy.dodge_difficulty,
                party=party,
            )
            targets = min(P, action.max_targets)

            # Bleed application: if this action can apply Bleed, it does so
            # whenever it is NOT dodged (blocking doesn't stop Bleed).
            if action.apply_bleed and enemy.can_bleed:
                lam_apply_e += p_not_dodge * targets

            # Trigger capacity: any damaging hit *could* trigger Bleed if present.
            lam_trig_e += p_damage_event * targets

        # Scale by repeat and by how many copies of this enemy are on the tile
        lam_apply_e *= enemy.repeat * slot.count
        lam_trig_e *= enemy.repeat * slot.count

        lambda_apply[slot.name] = lambda_apply.get(slot.name, 0.0) + lam_apply_e
        lambda_trig[slot.name] = lambda_trig.get(slot.name, 0.0) + lam_trig_e

    return lambda_apply, lambda_trig


def _compute_bleed_synergy_for_tile(
    tile: "EncounterTile",
    party: List[Character],
    enemies_by_name: Dict[str, Enemy],
) -> Dict[str, float]:
    """
    Returns extra Bleed DPR per enemy *name* on this tile vs this party.

    Steps:
      1) lambda_apply[name], lambda_trig[name] per enemy name (scaled by counts).
      2) total_apply  = sum lambda_apply[name]
         total_trig   = sum lambda_trig[name]
         triggers_tot = min(total_apply, total_trig)
      3) Distribute triggers back to Bleed appliers proportional to their
         apply rate: triggers_n = (lambda_apply[n]/total_apply)*triggers_tot
      4) extra_bleed_dpr[name] = BLEED_BONUS * triggers_n
    """
    lambda_apply, lambda_trig = _compute_bleed_rates_for_tile(
        tile, party, enemies_by_name
    )

    total_apply = sum(lambda_apply.values())
    total_trig = sum(lambda_trig.values())
    triggers_tot = min(total_apply, total_trig)

    extra: Dict[str, float] = {}

    if total_apply <= 0.0 or triggers_tot <= 0.0:
        # No Bleed applications or no one can ever trigger them
        return extra

    for name, lam_app in lambda_apply.items():
        if lam_app <= 0.0:
            continue
        # This enemy name gets credit for this share of total triggers
        triggers_n = (lam_app / total_apply) * triggers_tot
        extra[name] = BLEED_BONUS * triggers_n

    return extra


# ---- Threat for a single tile vs a single party ----

def tile_threat_vs_party(
    tile: EncounterTile,
    party: List[Character],
    enemies_by_name: Dict[str, Enemy],
) -> float:
    """
    Threat of a single tile vs a single party:

      base = sum( T_enemy ) over all instances on this tile,
      where T_enemy = DPR_effective * TTK * engagement_factor

    plus special mechanics, all restricted to THIS TILE:

      - Phalanx: each Phalanx spawns 3 Phalanx Hollows on death
      - Necromancer: each Necro can summon ~min(3, round(L_N)) Skeleton Soldiers
      - Black Hollow Mage: each Mage can resurrect up to min(S, round(L_B))
        skeleton-type enemies from THIS TILE (S = number of skeleton instances here).
    """
    if not party:
        return 0.0

    base = 0.0

    # Counters / collections for special behavior (per tile)
    num_necros = 0
    num_bhm = 0
    num_phalanx = 0
    skeleton_slots: List[EncounterEnemySlot] = []

    # Precompute Bleed synergy DPR adjustments for this tile+party
    extra_bleed_dpr_by_name = _compute_bleed_synergy_for_tile(tile, party, enemies_by_name)

    # 1) Base threat and classification for this tile
    for slot in tile.enemies:
        enemy = enemies_by_name.get(slot.name)
        if enemy is None:
            continue

        # Effective DPR = base DPR (no Bleed) + synergy Bleed DPR (if any)
        dpr_base = enemy_DPR_vs_party(enemy, party, include_bleed=False)
        dpr_eff = dpr_base + extra_bleed_dpr_by_name.get(slot.name, 0.0)

        ttk = enemy_TTK_vs_party(enemy, party)
        eng = engagement_factor(enemy, party)

        if dpr_eff > 0.0 and ttk > 0.0 and eng > 0.0:
            base += slot.count * dpr_eff * ttk * eng

        # Specials
        n_lower = enemy.name.lower()
        if enemy.name == "Necromancer":
            num_necros += slot.count
        elif enemy.name == "Black Hollow Mage":
            num_bhm += slot.count
        elif enemy.name == "Phalanx":
            num_phalanx += slot.count

        # Skeleton-type enemies for Black Hollow Mage synergy
        if "skeleton" in n_lower and enemy.name != "Black Hollow Mage":
            skeleton_slots.append(slot)

    # ---- Phalanx: each one becomes 3 Phalanx Hollows on death ----

    extra_phalanx = 0.0
    if num_phalanx > 0:
        ph_hollow = enemies_by_name.get("Phalanx Hollow")
        if ph_hollow is not None:
            T_hollow = enemy_threat_vs_party(ph_hollow, party)
            extra_phalanx = num_phalanx * 3.0 * T_hollow

    # ---- Necromancer: summons Skeleton Soldiers (per tile) ----

    extra_necro = 0.0
    if num_necros > 0:
        necro = enemies_by_name.get("Necromancer")
        skel_soldier = enemies_by_name.get("Skeleton Soldier")

        if necro is not None and skel_soldier is not None:
            L_N = enemy_TTK_vs_party(necro, party)  # Necro lifetime in activations
            if L_N > 0 and L_N < float("inf"):
                # Each activation can summon 1, up to 3 active at once on this tile.
                k = min(3, max(0, int(round(L_N))))
                T_ss = enemy_threat_vs_party(skel_soldier, party)
                extra_necro = num_necros * k * T_ss

    # ---- Black Hollow Mage: resurrects skeleton-type enemies (on this tile) ----

    extra_bhm = 0.0
    if num_bhm > 0 and skeleton_slots:
        bhm = enemies_by_name.get("Black Hollow Mage")
        if bhm is not None:
            # Total skeleton instances on this tile
            S = sum(slot.count for slot in skeleton_slots)

            # Average skeleton threat vs this party, weighted by count
            total_skel_threat = 0.0
            for slot in skeleton_slots:
                e_skel = enemies_by_name.get(slot.name)
                if e_skel is None:
                    continue
                total_skel_threat += slot.count * enemy_threat_vs_party(e_skel, party)

            if S > 0 and total_skel_threat > 0.0:
                avg_T_skel = total_skel_threat / S

                L_B = enemy_TTK_vs_party(bhm, party)  # BH Mage lifetime in activations
                if L_B > 0 and L_B < float("inf"):
                    # Each activation can resurrect 1 skeleton from this tile;
                    # can't resurrect more lifetimes than there are skeleton instances.
                    extra_lifetimes_per_bhm = min(S, max(0, int(round(L_B))))
                    extra_bhm = num_bhm * extra_lifetimes_per_bhm * avg_T_skel

    return base + extra_phalanx + extra_necro + extra_bhm


# ---- Threat profiles for tiles across tiers/player counts ----

def compute_tile_threat_profile_all_tiers(
    tile: EncounterTile,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[BuildKey, Character],
) -> Dict[str, Dict[str, float]]:
    """
    For this tile, compute an average threat vs all parties for:
      tier1, tier2, tier3  x  1-4 players.

    Returns:
      {
        "tier1": {"p1": val, "p2": val, "p3": val, "p4": val},
        "tier2": {...},
        "tier3": {...},
      }
    """
    result: Dict[str, Dict[str, float]] = {}

    for tier_name in TIERS:
        tier_profile: Dict[str, float] = {}
        for P in PLAYER_COUNTS:
            parties = list(iter_parties_for_tier(P, tier_name, builds))
            if not parties:
                tier_profile[f"p{P}"] = 0.0
                continue

            vals = [
                tile_threat_vs_party(tile, party, enemies_by_name)
                for party in parties
            ]
            tier_profile[f"p{P}"] = sum(vals) / len(vals)

        result[tier_name] = tier_profile

    return result


def compute_encounter_threat_profile_all_tiers(
    encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[BuildKey, Character],
) -> Dict[str, Dict[str, float]]:
    """
    For each tier (tier1–tier3) and player count (1–4), compute the average
    encounter threat over all parties of that tier.

    Encounter threat vs a party = sum of tile_threat_vs_party over all tiles.
    """
    result: Dict[str, Dict[str, float]] = {}

    for tier_name in TIERS:
        tier_profile: Dict[str, float] = {}

        for P in PLAYER_COUNTS:
            parties = list(iter_parties_for_tier(P, tier_name, builds))
            if not parties:
                tier_profile[f"p{P}"] = 0.0
                continue

            vals = []
            for party in parties:
                total_for_party = 0.0
                for tile in encounter.tiles:
                    total_for_party += tile_threat_vs_party(
                        tile, party, enemies_by_name
                    )
                vals.append(total_for_party)

            tier_profile[f"p{P}"] = sum(vals) / len(vals)

        result[tier_name] = tier_profile

    return result


def encounter_threat_for_level_and_party_size(
    encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[BuildKey, Character],
    P: int,
) -> float:
    """
    Average threat of this encounter vs all parties of size P
    at this encounter's level (1->tier1, 2->tier2, 3->tier3).
    """
    level_to_tier = {1: "tier1", 2: "tier2", 3: "tier3"}
    tier_name = level_to_tier.get(encounter.level, "tier1")

    parties = list(iter_parties_for_tier(P, tier_name, builds))
    if not parties:
        return 0.0

    vals = []
    for party in parties:
        total = 0.0
        for tile in encounter.tiles:
            total += tile_threat_vs_party(tile, party, enemies_by_name)
        vals.append(total)

    return sum(vals) / len(vals)


def compute_encounter_threat_profile_all_tiers(
    encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[BuildKey, Character],
) -> Dict[str, Dict[str, float]]:
    """
    Compute encounter-level threat vs all tiers and player counts.

    For each tier and player count:
      - Iterate all parties for that tier
      - For each party, sum tile_threat_vs_party over all tiles in encounter
      - Average over parties

    Returns:
      {
        "tier1": {"p1": val, "p2": val, "p3": val, "p4": val},
        "tier2": {...},
        "tier3": {...}
      }
    """
    tiers = ("tier1", "tier2", "tier3")
    result: Dict[str, Dict[str, float]] = {}

    for tier_name in tiers:
        tier_profile: Dict[str, float] = {}
        for P in (1, 2, 3, 4):
            parties = list(iter_parties_for_tier(P, tier_name, builds))
            if not parties:
                tier_profile[f"p{P}"] = 0.0
                continue

            # For each party, sum threat across tiles
            encounter_vals = []
            for party in parties:
                total_for_party = 0.0
                for tile in encounter.tiles:
                    total_for_party += tile_threat_vs_party(
                        tile, party, enemies_by_name
                    )
                encounter_vals.append(total_for_party)

            tier_profile[f"p{P}"] = sum(encounter_vals) / len(encounter_vals)

        result[tier_name] = tier_profile

    return result