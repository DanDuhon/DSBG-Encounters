import math
from typing import List, Dict

from models import Enemy, Character
from dice_math import (
    choose_baseline_attack,
    enemy_DPR_vs_party,
    enemy_TTK_vs_party,
)

# ---- Tile / movement constants ----

# Avg character start ↔ enemy spawn distance ≈ 1.8357
TILE_AVG_DISTANCE = 2.0   # d0, in node steps
TILE_DIAMETER = 4.0       # max shortest path on this tile

# Floor on relative speed so we don't assume perfect, infinite kiting
REL_SPEED_FLOOR = 0.25    # in node-steps per enemy activation
SHIFT_KITE_BONUS = 0.5
PUSH_KITE_BONUS_NO_ENEMY_PUSH  = 0.5
PUSH_KITE_BONUS_VS_PUSH_ENEMY = 0.25
FROSTBITE_KITE_PENALTY = 0.5  # per enemy that can frostbite
STAGGER_KITE_PENALTY_PER_ATTACK = 0.25  # per attack a stagger-capable enemy pressures
MAX_KITE_SPEED   = 3.0


def char_kite_speed_vs_enemy(char: Character, enemy: Enemy) -> float:
    """
    Effective kiting speed (node steps per enemy activation) this character
    contributes vs this enemy, based on:

      - primary attack range
      - primary attack Shift / Push
      - enemy being ranged/leap or melee
      - enemy Push
      - enemy attaching Frostbite / Stagger (stamina/mobility pressure)
      - hero move 2 (before OR after attack, not both).
    """
    # If enemy is ranged or leap, we assume kiting doesn't really deny attacks.
    if enemy.is_ranged_or_leap:
        return 0.0

    atk = choose_baseline_attack(char, enemy)
    primary_range = atk.max_range
    has_shift = getattr(atk, "shift", False)
    has_push_attack = getattr(atk, "push", False)

    # --- Base kiting speed ignoring statuses ---

    if enemy.has_push:
        # Enemy can push; melee heroes have a hard time escaping
        if primary_range == 0:
            v_char = 0.0
        elif primary_range == 1:
            v_char = 1.0
        else:  # primary_range >= 2
            v_char = 2.0
    else:
        # Melee enemy, no push
        if primary_range == 0:
            v_char = 1.0     # sometimes successful hit-and-run
        elif primary_range == 1:
            v_char = 1.5
        else:  # primary_range >= 2
            v_char = 2.0     # ranged kiting

    # --- Shift bonus: free reposition stapled onto your main attack ---

    if has_shift:
        v_char += SHIFT_KITE_BONUS

    # --- Hero Push bonus: you can shove melee enemies away ---

    if has_push_attack:
        if enemy.has_push:
            v_char += PUSH_KITE_BONUS_VS_PUSH_ENEMY
        else:
            v_char += PUSH_KITE_BONUS_NO_ENEMY_PUSH

    # --- Frostbite & Stagger on characters (enemy statuses) ---

    # If the enemy can frostbite, occasionally your stamina for movement/dodge
    # is suppressed; treat as a small mobility penalty.
    if enemy.can_frostbite:
        v_char -= FROSTBITE_KITE_PENALTY

    # Stagger makes each attack cost +1 stamina; abstract as a penalty
    # proportional to how many attacks this build normally uses.
    if enemy.can_stagger:
        n_attacks = max(1, len(char.attacks))
        v_char -= STAGGER_KITE_PENALTY_PER_ATTACK * n_attacks

    # Clamp
    if v_char < 0.0:
        v_char = 0.0
    if v_char > MAX_KITE_SPEED:
        v_char = MAX_KITE_SPEED

    return v_char


def engagement_components(enemy: Enemy, party: List[Character]) -> Dict[str, float]:
    """
    Compute all the internal pieces used for engagement_factor so we can debug:
      - v_hero_party
      - R_eff
      - d_to_close
      - rel_speed_raw, rel_speed_eff
      - L (TTK)
      - t_engage
      - engagement_factor

    engagement_factor is modeled as:
        f = L / (L + t_engage)
    where:
        L = enemy_TTK_vs_party(enemy, party)
        t_engage = time (in activations) to first attack,
                   based on distance, enemy move, and party kiting speed.
    """
    comps: Dict[str, float] = {}

    if not party:
        comps.update(
            v_hero_party=0.0,
            R_eff=float(enemy.range_behavior or 0),
            d_to_close=0.0,
            rel_speed_raw=0.0,
            rel_speed_eff=0.0,
            L=0.0,
            t_engage=0.0,
            engagement_factor=0.0,
        )
        return comps

    # Party-level kiting speed (already accounts for Shift/Push/Frostbite/Stagger)
    v_hero_party = (
        sum(char_kite_speed_vs_enemy(c, enemy) for c in party) / len(party)
    )

    # Enemy effective move; frostbite from party can slow it
    party_has_frostbite = any(
        atk.apply_frostbite
        for c in party
        for atk in c.attacks
    )

    if party_has_frostbite:
        m_enemy = max(0.0, enemy.move_speed - 1.0)  # "move 1 fewer node"
    else:
        m_enemy = enemy.move_speed

    # Effective range: leapers can effectively reach anywhere on the tile
    if enemy.has_leap:
        R_eff = TILE_DIAMETER
    else:
        R_eff = float(enemy.range_behavior or 0)

    d0 = TILE_AVG_DISTANCE
    d_to_close = max(0.0, d0 - R_eff)

    # Relative speed (enemy closing minus party kiting).
    rel_speed_raw = m_enemy - v_hero_party

    # If party can kite in principle, don't assume perfect play forever.
    if rel_speed_raw <= 0.0:
        rel_speed_eff = REL_SPEED_FLOOR
    else:
        rel_speed_eff = rel_speed_raw

    # TTK vs this party (in activations)
    L = enemy_TTK_vs_party(enemy, party)
    if L <= 0.0 or not (L < float("inf")):
        t_engage = 0.0
        factor = 0.0
    else:
        t_engage = d_to_close / rel_speed_eff
        # Smoother fraction of life spent attacking:
        #   f = L / (L + t_engage)
        factor = L / (L + t_engage) if t_engage >= 0.0 else 1.0

    comps.update(
        v_hero_party=v_hero_party,
        R_eff=R_eff,
        d_to_close=d_to_close,
        rel_speed_raw=rel_speed_raw,
        rel_speed_eff=rel_speed_eff,
        L=L,
        t_engage=t_engage,
        engagement_factor=factor,
    )
    return comps


def engagement_factor(enemy: Enemy, party: List[Character]) -> float:
    """Public API used by the rest of the code."""
    return engagement_components(enemy, party)["engagement_factor"]


def enemy_threat_vs_party(enemy: Enemy, party: List[Character]) -> float:
    """
    Threat(party) = DPR * TTK * engagement_factor

    Where engagement_factor encodes how often the enemy actually gets to apply
    its attack pattern vs this party, on a single-tile 13-node board.
    """
    dpr = enemy_DPR_vs_party(enemy, party)
    ttk = enemy_TTK_vs_party(enemy, party)
    eng = engagement_factor(enemy, party)

    # If party can't hurt the enemy (TTK = inf), or enemy can't hurt the party (DPR = 0),
    # or it never engages (eng = 0), treat threat as 0, not NaN.
    if not math.isfinite(ttk) or dpr <= 0.0 or eng <= 0.0:
        return 0.0

    return dpr * ttk * eng
