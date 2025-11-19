from itertools import product
from math import comb
from typing import List, Dict

from models import Character, Attack, Enemy

# ---------- Dice definitions ----------

DICE_FACES: Dict[str, List[int]] = {
    "black":  [0, 1, 1, 1, 2, 2],
    "blue":   [1, 1, 2, 2, 2, 3],
    "orange": [1, 2, 2, 3, 3, 4],
    # dodge die is implicit: 0,0,0,1,1,1 -> success p = 0.5
}

# ---------- New dodge + block rules ----------

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
    """
    New rules: roll dodge AND block/resist.
    If dodge succeeds => 0 damage, else damage reduced by block/resist.
    """
    if damage_type == "physical":
        def_dice = char.block_phys_dice
    else:
        def_dice = char.block_magic_dice

    p_fail = dodge_fail_prob(char.dodge_dice, dodge_difficulty)
    e_block = expected_block_damage(base_damage, def_dice)
    return p_fail * e_block


def expected_damage_to_avg_char_for_party(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    party: List[Character],
) -> float:
    vals = [
        expected_damage_to_char(base_damage, damage_type, dodge_difficulty, c)
        for c in party
    ]
    return sum(vals) / len(vals)


def expected_attack_damage_vs_enemy(atk: Attack, enemy: Enemy) -> float:
    """Expected damage this attack deals to this enemy in one use."""
    defense = enemy.armor if atk.damage_type == "physical" else enemy.resist

    if not atk.dice:
        raw_vals = [atk.flat_mod]
    else:
        face_lists = [DICE_FACES[d] for d in atk.dice]
        raw_vals = [sum(faces) + atk.flat_mod for faces in product(*face_lists)]

    vals = [max(0, v - defense) for v in raw_vals]
    return sum(vals) / len(vals)


def choose_baseline_attack(char: Character, enemy: Enemy) -> Attack:
    """
    Pick a sustainable attack to use for TTK calculations.
    v1: prefer low-stamina attacks, ignore range/shaft positioning.
    """
    candidates = [a for a in char.attacks if a.stamina_cost <= 1]
    if not candidates:
        candidates = char.attacks
    return max(
        candidates,
        key=lambda atk: expected_attack_damage_vs_enemy(atk, enemy)
    )


def enemy_DPR_vs_party(enemy: Enemy, party: List[Character]) -> float:
    P = len(party)
    total = 0.0
    for action in enemy.actions:
        per_char = expected_damage_to_avg_char_for_party(
            base_damage=action.damage,
            damage_type=action.damage_type,
            dodge_difficulty=enemy.dodge_difficulty,
            party=party,
        )
        targets = min(P, action.max_targets)
        total += per_char * targets
    if enemy.repeat > 1:
        total *= enemy.repeat
    return total


def team_DPS_vs_party(enemy: Enemy, party: List[Character]) -> float:
    total = 0.0
    for c in party:
        atk = choose_baseline_attack(c, enemy)
        total += expected_attack_damage_vs_enemy(atk, enemy)
    return total


def enemy_TTK_vs_party(enemy: Enemy, party: List[Character]) -> float:
    dps = team_DPS_vs_party(enemy, party)
    if dps <= 0:
        return float("inf")
    return enemy.hp / dps


def enemy_threat_vs_party(enemy: Enemy, party: List[Character]) -> float:
    """
    Threat(party) = DPR(party) * TTK(party)
    """
    dpr = enemy_DPR_vs_party(enemy, party)
    ttk = enemy_TTK_vs_party(enemy, party)
    return dpr * ttk
