import json
import csv

INPUT_JSON = "output_enemies.json"
OUTPUT_CSV = "output_enemies.csv"

def main():
    # Load the JSON file
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        enemies = json.load(f)

    rows = []

    for enemy in enemies:
        name = enemy.get("name", "")
        threat_profile = enemy.get("threat_profile", {})

        # threat_profile is a dict like {"tier1": {"p1": ..., "p2": ...}, ...}
        for tier, players in threat_profile.items():
            # players is a dict like {"p1": value, "p2": value, ...}
            for p_key, value in players.items():
                # Only process keys that look like "p1", "p2", etc.
                if not p_key.startswith("p"):
                    continue
                try:
                    player_num = int(p_key[1:])
                except ValueError:
                    # Skip any weird keys that don't have a number after 'p'
                    continue

                rows.append({
                    "name": name,
                    "tier": tier,
                    "player_num": player_num,
                    "threat": value,
                })

    # Write rows to CSV
    fieldnames = ["name", "tier", "player_num", "threat"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
