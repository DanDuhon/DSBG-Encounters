import sys

from builds import build_all_builds
from threat_profiles import build_enemy_threat_json
from models import EncounterSpec, EncounterEnemySpec
from encounters import generate_alternatives, LEVEL_TO_TIER

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py <enemies.csv> <output_enemies.json>")
        raise SystemExit(1)

    csv_path = sys.argv[1]
    out_path = sys.argv[2]

    builds = build_all_builds()
    enemies = build_enemy_threat_json(csv_path, out_path, builds=builds)
    print(f"Wrote enemies with tiered threat profiles to {out_path}")

    # Example: "No Safe Haven"
    no_safe_haven = EncounterSpec(
        name="No Safe Haven",
        level=1,
        enemies=[
            EncounterEnemySpec(enemy_name="Snow Rat", count=2, tile=1),
            EncounterEnemySpec(enemy_name="Engorged Zombie", count=1, tile=2),
        ],
    )

    tier_name = LEVEL_TO_TIER[no_safe_haven.level]
    alts = generate_alternatives(
        no_safe_haven,
        enemies,
        tier_name,
        max_candidates=3,
        max_tries=20000,
        threat_tolerance=0.2,
    )

    print("Example alternatives for 'No Safe Haven':")
    for i, alt in enumerate(alts, start=1):
        print(f"Alternative {i}: distance={alt['distance']:.3f}")
        for slot in alt["assignment"]:
            print(f"  Tile {slot['tile']}: {slot['enemy']}")
        print(f"  Threat: {alt['threat']}")
        print()

if __name__ == "__main__":
    main()
