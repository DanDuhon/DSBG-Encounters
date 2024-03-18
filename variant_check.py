from json import load, dump
from os import path
from pathlib import Path


baseFolder = path.dirname(__file__)
enemyPath = Path(baseFolder + "\\enemy_variants")

enemies = {}
enemyDiffs = {}
defenses = {"armor1", "armor2", "resist1", "resist2", "health1", "health2", "health3", "health4"}

try:
    a = len((list(enemyPath.glob("**/*.json"))))

    for enemy in enemyPath.glob("**/*.json"):
        if " - " in enemy.name:
            continue
        with open(enemy) as ef:
            e = load(ef)
            
        enemies[enemy.stem] = {1: {}, 2: {}, 3: {}, 4: {}}
        enemyDiffs[enemy.stem] = {1: {}, 2: {}, 3: {}, 4: {}}

        for charCnt in range(1, 5):
            for key in e[str(charCnt)]:
                for val in e[str(charCnt)][key]:
                    defKey = tuple(sorted(tuple(defenses & set(val))))
                    if defKey not in enemies[enemy.stem][charCnt]:
                        enemies[enemy.stem][charCnt][defKey] = set()

                    enemies[enemy.stem][charCnt][defKey].add(int(key))

    for i, enemy in enumerate(enemyPath.glob("**/*.json")):
        print(str((i/a)*100)[:6] + "%", end="\r")
        if " - " not in enemy.name:
            continue
        with open(enemy) as ef:
            e = load(ef)

        baseName = enemy.stem[:enemy.stem.index(" - ")]
        behaviorName = enemy.stem[enemy.stem.index(" - ")+3:]

        if baseName not in enemies:
            enemies[baseName] = {1: {}, 2: {}, 3: {}, 4: {}}
            enemyDiffs[baseName] = {1: {}, 2: {}, 3: {}, 4: {}}

        for charCnt in range(1, 5):
            for key in e[str(charCnt)]:
                for val in e[str(charCnt)][key]:
                    defKey = tuple(sorted(tuple(defenses & set(val))))
                    if defKey not in enemies[baseName][charCnt]:
                        enemies[baseName][charCnt][defKey] = {}

                    if behaviorName not in enemies[baseName][charCnt][defKey]:
                        enemies[baseName][charCnt][defKey][behaviorName] = set()

                    enemies[baseName][charCnt][defKey][behaviorName].add(int(key))

    overallDifficultiesList = []

    for enemy in enemies:
        for charCnt in enemies[enemy]:
            for defense in enemies[enemy][charCnt]:
                if type(enemies[enemy][charCnt][defense]) == dict:
                    if defense not in enemyDiffs[enemy][charCnt]:
                        enemyDiffs[enemy][charCnt][defense] = {}
                    difficulties = [enemies[enemy][charCnt][defense][key] for key in enemies[enemy][charCnt][defense]]
                    # Pull out all the difficulties that exist for all behavior variants for this enemy.
                    enemyDiffs[enemy][charCnt][defense]["difficulties"] = set(difficulties[0].intersection(*difficulties[1:]))
                else:
                    difficulties = [enemies[enemy][charCnt][defense] for _ in enemies[enemy][charCnt][defense]]

                overallDifficultiesList.append(set(difficulties[0].intersection(*difficulties[1:])))

    overallDifficulties = set(overallDifficultiesList[0].intersection(*overallDifficultiesList[1:]))

    with open(baseFolder + "\\enemy_variants\\_difficulty.json", "w") as enemyFile:
        dump({
            "overall": list(overallDifficulties),
            "enemy": dict(sorted(enemies[baseName][2].items())),
            "3": dict(sorted(enemies[baseName][3].items())),
            "4": dict(sorted(enemies[baseName][4].items()))}, enemyFile)

except Exception as ex:
    input(ex)
    raise
