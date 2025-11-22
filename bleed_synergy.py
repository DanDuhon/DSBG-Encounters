from typing import List, Dict, Tuple
from models import Enemy, Character
from dice_math import (
    damage_stats_to_avg_char_for_party,
    dodge_fail_prob,
)

BLEED_BONUS = 2.0  # +2 damage per trigger


def compute_bleed_rates_for_encounter(
    enemies: List[Enemy],
    party: List[Character],
) -> Tuple[Dict[Enemy, float], Dict[Enemy, float]]:
    """
    For a given encounter (list of enemies) and a party:

      lambda_apply[e]: expected # of Bleed applications per activation by enemy e
      lambda_trig[e]:  expected # of 'trigger-capable' hits per activation by e
                       (damaging hits that could trigger Bleed if target is bleeding)

    These are encounter-specific; we don't compute damage here, just rates.
    """
    P = len(party)
    if P == 0:
        return {e: 0.0 for e in enemies}, {e: 0.0 for e in enemies}

    # Precompute average P(not dodge) for this enemy vs the party
    def avg_p_not_dodge(enemy: Enemy) -> float:
        if not enemy.dodge_difficulty or enemy.dodge_difficulty <= 0:
            return 1.0
        return sum(
            dodge_fail_prob(c.dodge_dice, enemy.dodge_difficulty)
            for c in party
        ) / P

    lambda_apply: Dict[Enemy, float] = {}
    lambda_trig: Dict[Enemy, float] = {}

    for e in enemies:
        p_not_dodge = avg_p_not_dodge(e)

        lam_apply_e = 0.0
        lam_trig_e = 0.0

        for action in e.actions:
            base_damage = action.damage
            dmg_type = action.damage_type

            # Trigger capacity: damaging hits this action would land
            E_base, p_damage_event = damage_stats_to_avg_char_for_party(
                base_damage=base_damage,
                damage_type=dmg_type,
                dodge_difficulty=e.dodge_difficulty,
                party=party,
            )
            targets = min(P, action.max_targets)

            # Bleed application: if this action can apply Bleed, it does so
            # whenever it is NOT dodged (blocking doesn't stop Bleed).
            if action.apply_bleed and e.can_bleed:
                lam_apply_e += p_not_dodge * targets

            # Trigger capacity: any damaging hit *could* trigger Bleed if present.
            lam_trig_e += p_damage_event * targets

        # Account for enemy.repeat
        lam_apply_e *= e.repeat
        lam_trig_e *= e.repeat

        lambda_apply[e] = lam_apply_e
        lambda_trig[e] = lam_trig_e

    return lambda_apply, lambda_trig


def compute_bleed_synergy_for_encounter(
    enemies: List[Enemy],
    party: List[Character],
) -> Dict[Enemy, float]:
    """
    Returns extra Bleed DPR per enemy for this encounter vs this party.

    Steps:
      1) Compute lambda_apply[e] and lambda_trig[e] for all enemies.
      2) total_apply  = sum_e lambda_apply[e]
         total_trig   = sum_e lambda_trig[e]
         triggers_tot = min(total_apply, total_trig)
      3) Distribute triggers back to Bleed appliers proportional to their
         apply rate: triggers_e = (lambda_apply[e]/total_apply)*triggers_tot
      4) extra_bleed_dpr[e] = BLEED_BONUS * triggers_e
    """
    lambda_apply, lambda_trig = compute_bleed_rates_for_encounter(enemies, party)

    total_apply = sum(lambda_apply.values())
    total_trig = sum(lambda_trig.values())
    triggers_tot = min(total_apply, total_trig)

    extra: Dict[Enemy, float] = {e: 0.0 for e in enemies}

    if total_apply <= 0.0 or triggers_tot <= 0.0:
        # No Bleed applications or no one can ever trigger them
        return extra

    for e in enemies:
        lam_e = lambda_apply[e]
        if lam_e <= 0.0:
            continue
        # enemy e gets credit for this share of total triggers
        triggers_e = (lam_e / total_apply) * triggers_tot
        extra[e] = BLEED_BONUS * triggers_e

    return extra