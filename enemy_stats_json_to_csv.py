import json
import csv

json_filepath = "enemy_stats.json"
csv_filepath = "enemy_stats.csv"

with open(json_filepath, "r") as f:
    data = json.load(f)
    
headers = [
    "Enemy Name",
    "Tier 1 STK",
    "Tier 1 DPS",
    "Tier 2 STK",
    "Tier 2 DPS",
    "Tier 3 STK",
    "Tier 3 DPS"
]

with open(csv_filepath, 'w', newline='') as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(headers)
    
    for enemy_name, stats in data.items():
        row = [
            enemy_name,
            stats["1"]["stk"],
            stats["1"]["dps"],
            stats["2"]["stk"],
            stats["2"]["dps"],
            stats["3"]["stk"],
            stats["3"]["dps"]
        ]
        writer.writerow(row)
