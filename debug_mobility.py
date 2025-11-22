import sys
from typing import Dict, List

from builds import build_all_builds
from enemies_io import load_enemies_from_csv
from parties import iter_parties_for_tier
from mobility import engagement_components
from dice_math import enemy_DPR_vs_party, enemy_TTK_vs_party
from models import Enemy, Character, BuildKey


def pick_enemies(enemies: List[Enemy], names: List[str]) -> List[Enemy]:
    """Pick enemies by name if provided; otherwise first few with actions."""
    by_name: Dict[str, Enemy] = {e.name: e for e in enemies}
    selected: List[Enemy] = []

    for name in names:
        e = by_name.get(name)
        if e:
            selected.append(e)
        else:
            print(f"[warn] enemy {name!r} not found in CSV")

    if selected:
        return selected

    # fallback: first 5 with at least one action
    selected = [e for e in enemies if e.actions][:5]
    if not selected and enemies:
        selected = enemies[:5]
    return selected


def build_sample_parties(builds: Dict[BuildKey, Character]) -> Dict[int, List[Character]]:
    """
    Build one sample party per player count for tier1,
    using the first party returned by iter_parties_for_tier.
    """
    sample_parties: Dict[int, List[Character]] = {}
    for P in (1, 2, 3, 4):
        parties = iter_parties_for_tier(P, "tier1", builds)
        if parties:
            sample_parties[P] = parties[0]
    return sample_parties


def main():
    if len(sys.argv) < 2:
        print("Usage: python debug_mobility.py <enemies.csv> [ENEMY_NAME ...]")
        raise SystemExit(1)

    csv_path = sys.argv[1]
    enemy_names = sys.argv[2:]  # optional

    builds = build_all_builds()
    enemies = load_enemies_from_csv(csv_path)

    selected_enemies = pick_enemies(enemies, enemy_names)
    sample_parties = build_sample_parties(builds)

    if not sample_parties:
        print("No sample parties could be built (check builds / tiers).")
        raise SystemExit(1)

    for enemy in selected_enemies:
        print(f"\n=== {enemy.name} ===")
        print(
            f"  move_speed={enemy.move_speed}, "
            f"range_behavior={enemy.range_behavior}, "
            f"has_push={enemy.has_push}, "
            f"has_leap={enemy.has_leap}, "
            f"is_ranged_or_leap={enemy.is_ranged_or_leap}"
        )

        for P, party in sample_parties.items():
            comps = engagement_components(enemy, party)
            dpr = enemy_DPR_vs_party(enemy, party)
            ttk = enemy_TTK_vs_party(enemy, party)
            threat = dpr * ttk * comps["engagement_factor"]

            party_desc = ", ".join(f"{c.cls_name}({c.tier})" for c in party)

            print(f"  -- vs tier1 {P}-player party --")
            print(f"     party: {party_desc}")
            print(f"     v_hero_party      = {comps['v_hero_party']:.3f}")
            print(f"     R_eff             = {comps['R_eff']:.3f}")
            print(f"     d_to_close        = {comps['d_to_close']:.3f}")
            print(f"     rel_speed_raw     = {comps['rel_speed_raw']:.3f}")
            print(f"     rel_speed_eff     = {comps['rel_speed_eff']:.3f}")
            print(f"     L (TTK)           = {comps['L']:.3f}")
            print(f"     t_engage          = {comps['t_engage']:.3f}")
            print(f"     engagement_factor = {comps['engagement_factor']:.3f}")
            print(f"     DPR               = {dpr:.3f}")
            print(f"     Threat            = {threat:.3f}")
        print()


if __name__ == "__main__":
    main()