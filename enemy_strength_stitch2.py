from json import load, dump
from os import path
from pathlib import Path
from math import ceil


baseFolder = path.dirname(__file__)
enemyPath = Path(baseFolder + "\\enemies")

enemies = {}
baselineDiff = {}
allEnemies = []
baseNames = set()

try:
    a = len((list(enemyPath.glob("**/*.json"))))

    for i, enemy in enumerate(enemyPath.glob("**/*.json")):
        print(str((i/a)*100)[:6] + "%", end="\r")
        baseName = enemy.stem[:enemy.stem.rfind(" (") if " (" in enemy.stem else len(enemy.stem)]
        baseNames.add(baseName)
        if baseName not in enemies:
            enemies[baseName] = {1: {}, 2: {}, 3: {}, 4: {}}
        with open(enemy) as ef:
            e = load(ef)
        for charCnt in range(1, 5):
            for tier in range(1, 4):
                if " (" in enemy.stem and tier < 3:
                    continue

                diff = (e["damageDone"][str(charCnt)][str(tier)] + e["bleedDamage"][str(charCnt)][str(tier)]) / e["deaths"][str(tier)]

                if (baseName, charCnt, tier) not in baselineDiff:
                    baselineDiff[(baseName, charCnt, tier)] = diff
                else:
                    # I want to group everything in groups of 20%, so round up to the nearest even tenth.
                    diffChange = (ceil((round(diff/baselineDiff[(baseName, charCnt, tier)], 1) * 10) / 2.0) * 2) / 10

                    if diffChange <= 1.0:
                        continue

                    if diffChange not in enemies[baseName][charCnt]:
                        enemies[baseName][charCnt][diffChange] = [tuple(enemy.name.replace(baseName, "").replace(" ('", "").replace("')", "").replace("',)", "").replace(".json", "").split("', '"))]
                    else:
                        enemies[baseName][charCnt][diffChange].append(tuple(enemy.name.replace(baseName, "").replace(" ('", "").replace("')", "").replace("',)", "").replace(".json", "").split("', '")))

    for baseName in list(baseNames):
        with open(baseFolder + "\\enemy_variants\\" + baseName + ".json", "w") as enemyFile:
            dump({
                "1": dict(sorted(enemies[baseName][1].items())),
                "2": dict(sorted(enemies[baseName][2].items())),
                "3": dict(sorted(enemies[baseName][3].items())),
                "4": dict(sorted(enemies[baseName][4].items()))}, enemyFile)

        # with open(baseFolder + "\\enemies_output\\" + baseName + ".txt", "w") as out:
        #     out.write("\n".join(enemies[baseName]))

    # with open(baseFolder + "\\enemies_output\\allEnemies.txt", "w") as out:
    #     out.write("\n".join(allEnemies))

except Exception as ex:
    input(ex)
    raise
