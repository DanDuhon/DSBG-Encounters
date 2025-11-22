import json

from enemies_io import load_enemies_from_csv
from builds import build_all_builds
from encounters_io import load_encounters_from_json
from encounter_threat import (
    compute_tile_threat_profile_all_tiers,
    compute_encounter_threat_profile_all_tiers,
)


def main():
    enemies = load_enemies_from_csv("enemies.csv")
    enemies_by_name = {e.name: e for e in enemies}
    builds = build_all_builds()
    encounters = load_encounters_from_json("encounters.json")

    tile_scores = {}
    encounter_scores = {}

    for enc_name, enc in encounters.items():
        # per-tile profiles
        for i, tile in enumerate(enc.tiles, start=1):
            key = f"{enc_name}::Tile{i}"
            tile_scores[key] = compute_tile_threat_profile_all_tiers(
                tile, enemies_by_name, builds
            )

        # encounter profiles
        encounter_scores[enc_name] = compute_encounter_threat_profile_all_tiers(
            enc, enemies_by_name, builds
        )

    with open("output_tile_scores.json", "w", encoding="utf-8") as f:
        json.dump(tile_scores, f, indent=2)

    with open("output_encounter_scores.json", "w", encoding="utf-8") as f:
        json.dump(encounter_scores, f, indent=2)


if __name__ == "__main__":
    main()