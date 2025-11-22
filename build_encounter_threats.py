import json
from typing import Dict

from enemies_io import load_enemies_from_csv, id_to_enemy_name
from builds import build_all_builds
from encounter_threat import (
    Encounter,
    EncounterTile,
    EncounterEnemySlot,
    compute_tile_threat_profile_all_tiers,
    compute_encounter_threat_profile_all_tiers,
)

def load_encounters_from_json(path: str) -> Dict[str, Encounter]:
    """
    Expected JSON:
      {
        "No Safe Haven": {
          "level": 1,
          "tiles": {
            "1": {
                "enemies": [26, 5],
                "spawns": []
                },
            "2": {
                "enemies": [17],
                "spawns": []
                }
          }
        },
        ...
      }
    """
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    encs: Dict[str, Encounter] = {}
    for enc_name, enc_data in raw.items():
        tiles = []
        for t in enc_data["tiles"]:
            slots = [
                EncounterEnemySlot(name=id_to_enemy_name[s], count=(enc_data["tiles"][t]["enemies"] + enc_data["tiles"][t]["spawns"]).count(s))
                for s in enc_data["tiles"][t]["enemies"] + enc_data["tiles"][t]["spawns"]
            ]
            tiles.append(EncounterTile(name=t, enemies=slots))
        encs[enc_name] = Encounter(
            name=enc_name,
            level=enc_data["level"],
            tiles=tiles,
        )
    return encs


def main():
    enemies = load_enemies_from_csv("enemies.csv")
    enemies_by_name = {e.name: e for e in enemies}
    builds = build_all_builds()
    encounters = load_encounters_from_json("encounters.json")

    # Per-tile threat profiles
    tile_profiles: Dict[str, Dict[str, Dict[str, float]]] = {}

    # Per-encounter threat profiles
    encounter_profiles: Dict[str, Dict[str, Dict[str, float]]] = {}

    for enc in encounters.values():
        print("Processing " + enc.name)
        
        # Tiles
        for tile in enc.tiles:
            if tile.name not in tile_profiles:
                tile_profiles[tile.name] = compute_tile_threat_profile_all_tiers(
                    tile, enemies_by_name, builds
                )

        # Encounter
        encounter_profiles[enc.name] = compute_encounter_threat_profile_all_tiers(
            enc, enemies_by_name, builds
        )

    with open("output_tiles.json", "w", encoding="utf-8") as f:
        json.dump(tile_profiles, f, indent=2)

    with open("output_encounters.json", "w", encoding="utf-8") as f:
        json.dump(encounter_profiles, f, indent=2)


if __name__ == "__main__":
    main()