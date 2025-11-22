from enemies_io import load_enemies_from_csv
from builds import build_all_builds
from encounter_threat import (
    Encounter,
    EncounterEnemySlot,
    compute_encounter_threat_profile_all_tiers,
)

csv_path = "enemies.csv"
enemies = load_enemies_from_csv(csv_path)
enemies_by_name = {e.name: e for e in enemies}
builds = build_all_builds()

enc = Encounter(
    name="Skeleton Party",
    level=1,
    enemies=[
        EncounterEnemySlot("Necromancer", 1),
        EncounterEnemySlot("Skeleton Soldier", 2),
        EncounterEnemySlot("Black Hollow Mage", 1),
    ],
)

profile = compute_encounter_threat_profile_all_tiers(enc, enemies_by_name, builds)
print(profile)