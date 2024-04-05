from json import load, dump
from os import path
from pathlib import Path


baseFolder = path.dirname(__file__)
enemyPath = Path(baseFolder + "\\enemy_variants")

enemies = {}
enemyDiffs = {}
enemyExport = {}
behaviorExport = {}
defenses = {"armor1", "armor2", "resist1", "resist2", "health1", "health2", "health3", "health4"}

modIdLookup = {
    "dodge1": 1,
    "dodge2": 2,
    "damage1": 3,
    "damage2": 4,
    "damage3": 5,
    "damage4": 6,
    "armor1": 7,
    "armor2": 8,
    "resist1": 9,
    "resist2": 10,
    "health1": 11,
    "health2": 12,
    "health3": 13,
    "health4": 14,
    "repeat": 15,
    "magic": 16,
    "bleed": 17,
    "frostbite": 18,
    "poison": 19,
    "stagger": 20,
    "physical": 21
}

try:
    a = len((list(enemyPath.glob("**/*.json"))))

    # for enemy in enemyPath.glob("**/*.json"):
    #     if " - " in enemy.name or "dsbg_shuffle" in enemy.name:
    #         continue
    #     with open(enemy) as ef:
    #         e = load(ef)
            
    #     enemies[enemy.stem] = {1: {}, 2: {}, 3: {}, 4: {}}
    #     enemyDiffs[enemy.stem] = {1: {}, 2: {}, 3: {}, 4: {}}
    #     enemyExport[enemy.stem] = {1: [], 2: [], 3: [], 4: []}

        # for charCnt in range(1, 5):
        #     for key in e[str(charCnt)]:
        #         for val in e[str(charCnt)][key]:
        #             defKey = tuple(sorted(tuple(defenses & set(val))))
        #             if defKey not in enemies[enemy.stem][charCnt]:
        #                 enemies[enemy.stem][charCnt][defKey] = set()

        #             enemies[enemy.stem][charCnt][defKey].add(float(key))

    for i, enemy in enumerate(enemyPath.glob("**/*.json")):
        print(str((i/a)*100)[:6] + "%", end="\r")
        # if " - " not in enemy.name:
        #     continue
        with open(enemy) as ef:
            e = load(ef)

        if " - " in enemy.stem:
            baseName = enemy.stem[:enemy.stem.index(" - ")]
            behaviorName = enemy.stem[enemy.stem.index(" - ")+3:]
        else:
            baseName = enemy.stem
            behaviorName = "default"

        if baseName not in behaviorExport:
            behaviorExport[baseName] = {1: {}, 2: {}, 3: {}, 4: {}}

        for charCnt in range(1, 5):
            for key in e[str(charCnt)]:
                for val in e[str(charCnt)][key]:
                    defKey = tuple(sorted(tuple(defenses & set(val))))
                    defKeyJson = ",".join([str(modIdLookup[m]) for m in defKey])
                    valJson = [modIdLookup[v] for v in val]

                    if key not in behaviorExport[baseName][charCnt]:
                        behaviorExport[baseName][charCnt][key] = {}

                    if defKeyJson not in behaviorExport[baseName][charCnt][key]:
                        behaviorExport[baseName][charCnt][key][defKeyJson] = {}

                    if behaviorName not in behaviorExport[baseName][charCnt][key][defKeyJson]:
                        behaviorExport[baseName][charCnt][key][defKeyJson][behaviorName] = []

                    behaviorExport[baseName][charCnt][key][defKeyJson][behaviorName].append(valJson)

    print("")

    # overallDifficultiesList = []

    # for enemy in enemies:
    #     for charCnt in enemies[enemy]:
    #         if type([enemies[enemy][charCnt][k] for k in enemies[enemy][charCnt]][0]) == dict:
    #             diffsToCombine = []

    #             for defense in enemies[enemy][charCnt]:
    #                 if defense not in enemyDiffs[enemy][charCnt]:
    #                     enemyDiffs[enemy][charCnt][defense] = {}
                        
    #                 difficulties = [enemies[enemy][charCnt][defense][key] for key in enemies[enemy][charCnt][defense]]

    #                 # Pull out all the difficulties that exist for all behavior variants for this enemy.
    #                 enemyDiffs[enemy][charCnt][defense]["difficulties"] = set(difficulties[0].intersection(*difficulties[1:]))
    #                 diffsToCombine.append(enemyDiffs[enemy][charCnt][defense]["difficulties"])

    #             enemyDiffs[enemy][charCnt]["difficulties"] = sorted(list(set(diffsToCombine[0].union(*diffsToCombine[1:]))))
    #             enemyExport[enemy][charCnt] = sorted(list(enemyDiffs[enemy][charCnt]["difficulties"]))
    #             overallDifficultiesList.append(enemyDiffs[enemy][charCnt]["difficulties"])
    #         else:
    #             difficulties = [enemies[enemy][charCnt][defense] for defense in enemies[enemy][charCnt]]
    #             enemyDiffs[enemy][charCnt]["difficulties"] = list(set(difficulties[0].union(*difficulties[1:])))
    #             enemyExport[enemy][charCnt] = sorted(list(enemyDiffs[enemy][charCnt]["difficulties"]))

    #             overallDifficultiesList.append(set(difficulties[0].union(*difficulties[1:])))

    # overallDifficulties = set(overallDifficultiesList[0].intersection(*overallDifficultiesList[1:]))

    with open(baseFolder + "\\dsbg_shuffle_difficulty.json", "w") as enemyFile:
        dump(behaviorExport, enemyFile)

except Exception as ex:
    input(ex)
    raise
