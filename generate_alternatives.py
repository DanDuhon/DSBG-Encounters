import json
import random
from collections import Counter
from typing import List, Dict, Tuple

from enemies_io import (
    load_enemies_from_csv,
    enemy_ids,
    id_to_enemy_name,
)
from encounters_io import (
    load_encounters_from_json,
    ENEMY_SLOTS_BY_ENCOUNTER,
    ORIGINAL_ENEMIES_BY_ENCOUNTER,
    ENEMY_ENCOUNTER_BY_ENEMY_NAME,
)
from builds import build_all_builds, BuildKey
from encounter_threat import Encounter, EncounterTile, EncounterEnemySlot, tile_threat_vs_party
from mobility import enemy_threat_vs_party
from parties import iter_parties_for_tier
from models import Character, Enemy


PLAYER_COUNTS = (1, 2, 3, 4)
LEVEL_TO_TIER = {1: "tier1", 2: "tier2", 3: "tier3"}

# Only use "regular" enemies (1–33) in alternatives (no invaders/mimics)
REGULAR_ENEMY_IDS = [eid for eid in enemy_ids.values() if eid <= 33]

BASE_GAME_EXPANSION = "Dark Souls The Board Game"
SUNLESS_EXPANSION = "The Sunless City"

# Enemies that exist in both Dark Souls TBG and The Sunless City
SHARED_SUNLESS_BASE_ENEMY_NAMES = {
    "Crossbow Hollow",
    "Hollow Soldier",
    "Sentinel",
    "Silver Knight Greatbowman",
    "Silver Knight Swordsman",
}


# ---- Scoring helpers ----

def encounter_threat_for_level_and_party_size(
    encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[Tuple[str, str, int], Character],
    P: int,
) -> float:
    """
    Average threat of this encounter vs all parties of size P
    at this encounter's level (1->tier1, 2->tier2, 3->tier3).
    """
    tier_name = LEVEL_TO_TIER.get(encounter.level, "tier1")
    parties = list(iter_parties_for_tier(P, tier_name, builds))
    if not parties:
        return 0.0

    vals: List[float] = []
    for party in parties:
        total_for_party = 0.0
        for tile in encounter.tiles:
            total_for_party += tile_threat_vs_party(tile, party, enemies_by_name)
        vals.append(total_for_party)

    return sum(vals) / len(vals)


def compute_threat_order_for_original(
    encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[BuildKey, Character],
    P: int,
    original_ids: List[int],
) -> List[int]:
    """
    Compute a threat-based ordering of the original enemy list for this
    encounter and party size P.

    Steps:
      1) For each unique enemy name in original_ids, compute its average
         threat vs all parties of this tier + player count.
      2) Assign that average threat to each position in original_ids.
      3) Return indices 0..N-1 sorted by descending threat (ties keep
         original order).
    """
    tier_name = LEVEL_TO_TIER.get(encounter.level, "tier1")
    parties = list(iter_parties_for_tier(P, tier_name, builds))
    if not parties:
        # No parties? Just keep original order.
        return list(range(len(original_ids)))

    # 1) Average threat per enemy NAME (not per instance)
    unique_names = {id_to_enemy_name[eid] for eid in original_ids}
    avg_threat_by_name: Dict[str, float] = {}

    for name in unique_names:
        enemy = enemies_by_name[name]
        vals = [enemy_threat_vs_party(enemy, party) for party in parties]
        avg_threat_by_name[name] = sum(vals) / len(vals) if vals else 0.0

    # 2) Per-position score (instances of same enemy share the same score)
    scores = [avg_threat_by_name[id_to_enemy_name[eid]] for eid in original_ids]

    # 3) Indices sorted by descending threat; ties keep earlier index first
    order = sorted(
        range(len(original_ids)),
        key=lambda i: (-scores[i], i),
    )
    return order


def _tile_instance_counts(encounter: Encounter) -> List[int]:
    """
    Return total number of enemy *instances* per tile (respecting slot.count).
    E.g. for No Safe Haven: [2, 1, 0]
    """
    counts: List[int] = []
    for tile in encounter.tiles:
        n = sum(slot.count for slot in tile.enemies)
        counts.append(n)
    return counts


def build_candidate_encounter_from_ids(
    base_encounter: Encounter,
    candidate_ids: List[int],
    id_to_name: Dict[int, str],
) -> Encounter:
    """
    Build a new Encounter with the same tile structure as base_encounter,
    but using candidate_ids as the enemy IDs, assigned sequentially across tiles.

    Tile i gets exactly the same number of enemies as in base_encounter;
    within each tile we aggregate duplicates into EncounterEnemySlot(name, count).
    """
    tile_sizes = _tile_instance_counts(base_encounter)
    total_slots = sum(tile_sizes)
    if len(candidate_ids) != total_slots:
        raise ValueError(
            f"candidate_ids length {len(candidate_ids)} "
            f"does not match total enemy slots {total_slots}"
        )

    tiles: List[EncounterTile] = []
    idx = 0
    for base_tile, size in zip(base_encounter.tiles, tile_sizes):
        ids_for_tile = candidate_ids[idx:idx + size]
        idx += size

        counts_by_name: Counter = Counter(id_to_name[eid] for eid in ids_for_tile)
        slots = [
            EncounterEnemySlot(name=name, count=count)
            for name, count in counts_by_name.items()
        ]
        tiles.append(EncounterTile(name=base_tile.name, enemies=slots))

    return Encounter(
        name=base_encounter.name,
        level=base_encounter.level,
        tiles=tiles,
    )


# ---- Alternative generation ----

def generate_candidate_id_lists_for_encounter(
    base_encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[Tuple[str, str, int], Character],
    P: int,
    pool_ids: List[int],
    base_ids: List[int],
    *,
    tolerance: float = 0.20,
    max_candidates: int = 500,
    max_samples: int = 50000,
    rng: random.Random = random,
) -> List[List[int]]:
    """
    Randomly sample candidate enemy ID lists for this encounter and party size P.

    Keep candidates whose average threat (vs all parties of that tier+P) is
    within `tolerance` of the original encounter's threat.

    Returns a list of candidate ID lists (each of length len(base_ids)).
    """
    # Baseline encounter threat for this party size
    base_threat = encounter_threat_for_level_and_party_size(
        base_encounter, enemies_by_name, builds, P
    )

    if base_threat <= 0.0:
        # Degenerate case: use absolute difference instead of relative later
        use_relative = False
    else:
        use_relative = True

    tile_sizes = _tile_instance_counts(base_encounter)
    n_slots = sum(tile_sizes)
    if n_slots != len(base_ids):
        raise ValueError(
            f"ORIGINAL_ENEMIES length {len(base_ids)} does not match tile slots {n_slots}"
        )

    seen_multisets = set()
    kept: List[List[int]] = []

    for attempt in range(max_samples):
        # Sample with replacement from pool_ids
        cand_ids = [rng.choice(pool_ids) for _ in range(n_slots)]

        # Avoid duplicates by multiset
        key = tuple(sorted(cand_ids))
        if key in seen_multisets:
            continue
        seen_multisets.add(key)

        # Skip the original; we'll add it separately later
        if sorted(cand_ids) == sorted(base_ids):
            continue

        # Build candidate encounter and score it
        cand_enc = build_candidate_encounter_from_ids(base_encounter, cand_ids, id_to_enemy_name)
        cand_threat = encounter_threat_for_level_and_party_size(
            cand_enc, enemies_by_name, builds, P
        )

        if use_relative and base_threat > 0.0:
            rel_diff = abs(cand_threat - base_threat) / base_threat
            ok = rel_diff <= tolerance
        else:
            abs_diff = abs(cand_threat - base_threat)
            ok = abs_diff <= 1e-6  # essentially equal

        if ok:
            kept.append(cand_ids)
            if len(kept) >= max_candidates:
                break

    return kept


def group_candidates_by_expansion(
    candidates: List[List[int]],
) -> Dict[str, List[List[int]]]:
    """
    Group candidate ID lists by their expansion combination string:

      expansions = sorted unique expansions of the enemies in the list
      key = ",".join(expansions)

    For lineups that only use Dark Souls TBG enemies from the shared set
    (Crossbow Hollow, Hollow Soldier, Sentinel, Silver Knight Greatbowman,
     Silver Knight Swordsman), we ALSO add an entry where
    "Dark Souls The Board Game" is replaced by "The Sunless City".
    """
    grouped: Dict[str, List[List[int]]] = {}

    for ids_ in candidates:
        names = [id_to_enemy_name[eid] for eid in ids_]

        expansions = set()
        base_game_names = []  # names whose expansion is exactly BASE_GAME_EXPANSION

        for name in names:
            exp = ENEMY_ENCOUNTER_BY_ENEMY_NAME.get(name)
            if not exp:
                continue
            expansions.add(exp)
            if exp == BASE_GAME_EXPANSION:
                base_game_names.append(name)

        # Base key
        base_key = ",".join(sorted(expansions)) if expansions else ""
        grouped.setdefault(base_key, []).append(ids_)

        # ----- Sunless alias logic -----

        # Only consider aliasing if the lineup uses the base game at all
        if BASE_GAME_EXPANSION not in expansions:
            continue

        if not base_game_names:
            continue

        # ALL base-game enemies in this lineup must be from the shared list.
        # If there's ANY base-game enemy not in the shared set (e.g. Large Hollow Soldier
        # or some other DS-only unit), we cannot re-label this as Sunless City.
        if not all(name in SHARED_SUNLESS_BASE_ENEMY_NAMES for name in base_game_names):
            continue

        # At least one of the shared enemies is actually present (this will always
        # be true given the check above, but keeping the intent explicit).
        if not any(name in SHARED_SUNLESS_BASE_ENEMY_NAMES for name in base_game_names):
            continue

        # Build the alias expansion set: replace "Dark Souls TBG" with "The Sunless City"
        alias_expansions = set(expansions)
        alias_expansions.discard(BASE_GAME_EXPANSION)
        alias_expansions.add(SUNLESS_EXPANSION)

        # If nothing actually changed (e.g. we somehow already had that combo), skip
        if alias_expansions == expansions:
            continue

        alias_key = ",".join(sorted(alias_expansions))
        grouped.setdefault(alias_key, []).append(ids_)

    return grouped


def build_alternative_json_for_encounter_and_party(
    encounter_name: str,
    encounter: Encounter,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[Tuple[str, str, int], Character],
    P: int,
    *,
    tolerance: float = 0.20,
    max_candidates: int = 500,
    max_samples: int = 50000,
    rng_seed: int = 12345,
) -> Dict:
    """
    Generate the JSON structure for <EncounterName><P>.json:

      {
        "enemySlots": [...],
        "alternatives": { "Exp1,Exp2": [[ids...], ...], ... },
        "original": [orig_ids...]
      }
    """
    if encounter_name not in ENEMY_SLOTS_BY_ENCOUNTER:
        raise KeyError(f"No enemySlots entry for encounter '{encounter_name}'")

    if encounter_name not in ORIGINAL_ENEMIES_BY_ENCOUNTER:
        raise KeyError(f"No ORIGINAL_ENEMIES entry for encounter '{encounter_name}'")

    enemy_slots = ENEMY_SLOTS_BY_ENCOUNTER[encounter_name]
    original_ids = ORIGINAL_ENEMIES_BY_ENCOUNTER[encounter_name]

    rng = random.Random(rng_seed)

    candidates = generate_candidate_id_lists_for_encounter(
        base_encounter=encounter,
        enemies_by_name=enemies_by_name,
        builds=builds,
        P=P,
        pool_ids=REGULAR_ENEMY_IDS,
        base_ids=original_ids,
        tolerance=tolerance,
        max_candidates=max_candidates,
        max_samples=max_samples,
        rng=rng,
    )

    # --- NEW: compute threat-based order from the ORIGINAL lineup ---

    threat_order = compute_threat_order_for_original(
        encounter=encounter,
        enemies_by_name=enemies_by_name,
        builds=builds,
        P=P,
        original_ids=original_ids,
    )

    def reorder(ids_list: List[int]) -> List[int]:
        if len(ids_list) != len(threat_order):
            # Safety fallback; should not happen
            return ids_list
        return [ids_list[i] for i in threat_order]

    # Apply to candidates and original for display
    display_candidates = [reorder(cand) for cand in candidates]
    display_original = reorder(original_ids)

    # Group candidates + original by expansion (with Sunless alias logic)
    grouped = group_candidates_by_expansion(display_candidates + [display_original])

    return {
        "enemySlots": enemy_slots,
        "alternatives": grouped,
        "original": display_original,
    }


def apply_difficulty_order(ids_list: List[int], order: List[int]) -> List[int]:
    """
    Reorder ids_list according to a difficultyOrder permutation.

    order[k] = index in ids_list that should appear at position k in the output.
    E.g. ids = [A,B,C], order=[1,2,0] -> [B,C,A].
    """
    if not order or len(order) != len(ids_list):
        # Fallback: leave as-is if lengths don't match
        return ids_list
    return [ids_list[i] for i in order]


# ---- Main entrypoint ----

def main():
    # Load core data
    enemies = load_enemies_from_csv("enemies.csv")
    enemies_by_name = {e.name: e for e in enemies}
    builds = build_all_builds()
    encounters = load_encounters_from_json("encounters.json")

    # For now, generate alternatives just for "No Safe Haven" for all party sizes 1–4
    encounter_name = "Painted Passage"
    if encounter_name not in encounters:
        raise KeyError(f"Encounter '{encounter_name}' not found in encounters.json")

    encounter = encounters[encounter_name]

    for P in PLAYER_COUNTS:
        data = build_alternative_json_for_encounter_and_party(
            encounter_name=encounter_name,
            encounter=encounter,
            enemies_by_name=enemies_by_name,
            builds=builds,
            P=P,
            tolerance=0.10,       # tweak to tighten/loosen matching
            max_candidates=1000,   # max alts to keep
            max_samples=50000,    # how many random samples to try
            rng_seed=12345 + P,   # different seed per party size
        )
        out_name = f"{encounter_name}{P}.json"
        with open(out_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        print(f"Wrote {out_name} with {sum(len(v) for v in data['alternatives'].values())} alternatives")


if __name__ == "__main__":
    main()
