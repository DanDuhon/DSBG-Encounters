from json import load
from os import path
from pathlib import Path


baseFolder = path.dirname(__file__)
enemyPath = Path(baseFolder + "\\enemies")

enemies = {}
baselineDiff = {}
allEnemies = []

for enemy in enemyPath.glob("**/*.json"):
    baseName = enemy.stem[:enemy.stem.index(" (") if " (" in enemy.stem else len(enemy.stem)]
    if baseName not in enemies:
        enemies[baseName] = set()
    with open(enemy) as ef:
        e = load(ef)
    for charCnt in range(1, 5):
        for tier in range(1, 4):
            diff = (e["damageDone"][str(charCnt)][str(tier)] + e["bleedDamage"][str(charCnt)][str(tier)]) / e["deaths"][str(tier)]
            if (baseName, charCnt, tier) not in baselineDiff:
                baselineDiff[(baseName, charCnt, tier)] = diff
                enemies[baseName].add(enemy.stem + "_" + str(charCnt) + "_" + str(tier) + "_" + str(diff) +  "_1.0")
                allEnemies.append(enemy.stem + "\t" + str(charCnt) + "\t" + str(tier) + "\t" + str(diff) +  "\t1.0")
            else:
                if diff/baselineDiff[(baseName, charCnt, tier)] <= 1.0:
                    pass
                enemies[baseName].add(enemy.stem + "_" + str(charCnt) + "_" + str(tier) + "_" + str(diff) + "_" + str(diff/baselineDiff[(baseName, charCnt, tier)]))
                allEnemies.append(enemy.stem + "\t" + str(charCnt) + "\t" + str(tier) + "\t" + str(diff) + "\t" + str(diff/baselineDiff[(baseName, charCnt, tier)]))

    with open(baseFolder + "\\enemies_output\\" + baseName + ".txt", "w") as out:
        out.write("\n".join(enemies[baseName]))

with open(baseFolder + "\\enemies_output\\allEnemies.txt", "w") as out:
    out.write("\n".join(allEnemies))