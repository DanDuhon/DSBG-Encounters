from itertools import product
from math import comb
from typing import List, Dict, Tuple

from models import Character, Attack, Enemy

# ---------- Dice definitions ----------

DICE_FACES: Dict[str, List[int]] = {
    "black":  [0, 1, 1, 1, 2, 2],
    "blue":   [1, 1, 2, 2, 2, 3],
    "orange": [1, 2, 2, 3, 3, 4],
    # dodge die is implicit: 0,0,0,1,1,1 -> success p = 0.5
}




def damage_stats_to_char(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    char: Character,
) -> Tuple[float, float]:
    """
    Return (E_damage, p_damage_event) for an enemy attack vs a single character,
    BEFORE bleed/poison bonuses.

    - E_damage: expected post-mitigation damage
    - p_damage_event: probability that damage > 0
    """
    if base_damage <= 0:
        return 0.0, 0.0

    if damage_type == "physical":
        def_dice = char.block_phys_dice
    else:
        def_dice = char.block_magic_dice

    # Dodge: probability of failing dodge
    p_fail = dodge_fail_prob(char.dodge_dice, dodge_difficulty)

    if not def_dice:
        # No block/resist dice
        d = float(base_damage)
        return p_fail * d, p_fail if base_damage > 0 else 0.0

    # Enumerate defense dice outcomes
    face_lists = [DICE_FACES[d] for d in def_dice]
    total_outcomes = 0
    sum_dmg_given_not_dodge = 0.0
    p_pos_given_not_dodge = 0.0

    for faces in product(*face_lists):
        block_val = sum(faces)
        dmg = max(0, base_damage - block_val)
        total_outcomes += 1
        sum_dmg_given_not_dodge += dmg
        if dmg > 0:
            p_pos_given_not_dodge += 1

    if total_outcomes == 0:
        return 0.0, 0.0

    E_given_not = sum_dmg_given_not_dodge / total_outcomes
    p_pos_given_not = p_pos_given_not_dodge / total_outcomes

    E = p_fail * E_given_not
    p_event = p_fail * p_pos_given_not
    return E, p_event


def damage_stats_to_avg_char_for_party(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    party: List[Character],
) -> Tuple[float, float]:
    """
    Average (E_damage, p_damage_event) across all characters in the party.
    """
    if not party:
        return 0.0, 0.0

    Es = []
    Ps = []
    for c in party:
        E, p = damage_stats_to_char(base_damage, damage_type, dodge_difficulty, c)
        Es.append(E)
        Ps.append(p)
    return sum(Es) / len(Es), sum(Ps) / len(Ps)


def dodge_fail_prob(n_dodge: int, difficulty: int) -> float:
    """
    Probability that the player FAILS the dodge check.
    Each dodge die: 0,0,0,1,1,1 -> p(success) = 0.5
    """
    if n_dodge <= 0:
        return 1.0
    p_fail = 0.0
    for k in range(0, min(difficulty, n_dodge + 1)):
        p_fail += comb(n_dodge, k) * (0.5 ** n_dodge)
    return p_fail


def expected_block_damage(base_damage: int, def_dice: List[str]) -> float:
    """
    Expected damage after rolling defense dice (block or resist).
    """
    if base_damage <= 0:
        return 0.0
    if not def_dice:
        return float(base_damage)

    face_lists = [DICE_FACES[d] for d in def_dice]
    total_damage = 0.0
    total_outcomes = 0

    for faces in product(*face_lists):
        block_val = sum(faces)
        dmg = max(0, base_damage - block_val)
        total_damage += dmg
        total_outcomes += 1

    return total_damage / total_outcomes


def expected_damage_to_char(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    char: Character,
) -> float:
    E, _ = damage_stats_to_char(base_damage, damage_type, dodge_difficulty, char)
    return E


def expected_damage_to_avg_char_for_party(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    party: List[Character],
) -> float:
    E, _ = damage_stats_to_avg_char_for_party(base_damage, damage_type, dodge_difficulty, party)
    return E


def damage_stats_vs_enemy(atk: Attack, enemy: Enemy) -> Tuple[float, float]:
    """
    Return (E_damage, p_damage_event) for this character attack vs this enemy,
    including ignore_armor, bleed, poison.

    This is per use of the attack, in steady state.
    """
    if atk.damage_type == "physical":
        defense = 0 if atk.ignore_armor else enemy.armor
    else:
        defense = enemy.resist

    if not atk.dice:
        # Flat-only attack
        raw_vals = [atk.flat_mod]
    else:
        face_lists = [DICE_FACES[d] for d in atk.dice]
        raw_vals = [sum(faces) + atk.flat_mod for faces in product(*face_lists)]

    total_outcomes = len(raw_vals)
    if total_outcomes == 0:
        return 0.0, 0.0

    sum_dmg = 0.0
    count_pos = 0
    for raw in raw_vals:
        dmg = max(0, raw - defense)
        sum_dmg += dmg
        if dmg > 0:
            count_pos += 1

    E_base = sum_dmg / total_outcomes
    p_event = count_pos / total_outcomes

    # Bleed/poison vs enemy: same steady-state logic as enemy→char
    extra_bleed = 2.0 * p_event if atk.apply_bleed else 0.0
    extra_poison = 1.0 * p_event if atk.apply_poison else 0.0

    E_total = E_base + extra_bleed + extra_poison
    return E_total, p_event


def expected_attack_damage_vs_enemy(atk: Attack, enemy: Enemy) -> float:
    E, _ = damage_stats_vs_enemy(atk, enemy)
    return E


def choose_baseline_attack(char: Character, enemy: Enemy) -> Attack:
    """
    Representative 'primary' attack for this character vs this enemy,
    chosen as the attack with the highest total DPR contribution
    (expected damage per use * repeat).
    """
    if not char.attacks:
        raise ValueError(f"Character {char.cls_name} has no attacks defined")

    def dpr_score(atk: Attack) -> float:
        per_use = expected_attack_damage_vs_enemy(atk, enemy)
        return atk.repeat * per_use

    return max(char.attacks, key=dpr_score)


def enemy_DPR_vs_party(enemy: Enemy, party: List[Character], include_bleed: bool = True) -> float:
    """
    Total expected damage this enemy does in one activation vs this party,
    including bleed/poison bonuses on its attacks (steady-state).
    """
    P = len(party)
    if P == 0:
        return 0.0

    # Does the party have at least one stagger-capable sustainable attack?
    party_has_stagger = any(
        atk.apply_stagger
        for c in party
        for atk in c.attacks
    )

    total = 0.0
    for action in enemy.actions:
        base_damage = action.damage

        # Stagger from party: treat as -1 damage to all attacks if they can
        # keep the enemy staggered often. (Upper-bound approximation.)
        if party_has_stagger:
            base_damage = max(0, base_damage - 1)

        damage_type = action.damage_type
        E_base, p_event = damage_stats_to_avg_char_for_party(
            base_damage=base_damage,
            damage_type=damage_type,
            dodge_difficulty=enemy.dodge_difficulty,
            party=party,
        )

        targets = min(P, action.max_targets)

        # Poison: +1 per damaging hit (end-of-turn tick).
        extra_poison = 0.0
        if action.apply_poison and enemy.can_poison:
            extra_poison = 1.0 * p_event

        # Bleed: only add if include_bleed=True
        extra_bleed = 0.0
        if include_bleed and action.apply_bleed and enemy.can_bleed:
            # (Use your existing per-enemy approximation here, e.g. 2 * p_event)
            extra_bleed = 2.0 * p_event * targets

        total += (E_base * targets) + extra_poison + extra_bleed

    if enemy.repeat > 1:
        total *= enemy.repeat

    return total


def team_DPS_vs_party(enemy: Enemy, party: List[Character]) -> float:
    """
    Total expected DPS the party deals to this enemy in one activation,
    assuming each Character performs all of their sustainable attacks.
    """
    total = 0.0
    for c in party:
        for atk in c.attacks:
            per_use = expected_attack_damage_vs_enemy(atk, enemy)
            total += atk.repeat * per_use
    return total


def enemy_TTK_vs_party(enemy: Enemy, party: List[Character]) -> float:
    dps = team_DPS_vs_party(enemy, party)
    if dps <= 0:
        return float("inf")
    return enemy.hp / dps
