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

behaviorCount = {
    "Armorer Dennis": 5,
    "Artorias": 13,
    "Asylum Demon": 9,
    "Black Dragon Kalameet": 13,
    "Black Knight": 9,
    "Boreal Outrider Knight": 8,
    "Crossbreed Priscilla": 13,
    "Dancer of the Boreal Valley": 13,
    "Executioner's Chariot": 13,
    "Fencer Sharron": 7,
    "Gaping Dragon": 13,
    "Gargoyle": 8,
    "Gravelord Nito": 13,
    "Great Grey Wolf Sif": 14,
    "Guardian Dragon": 10,
    "Heavy Knight": 9,
    "Hungry Mimic": 7,
    "Invader Brylex": 5,
    "Kirk, Knight of Thorns": 5,
    "Longfinger Kirk": 5,
    "Maldron the Assassin": 5,
    "Maneater Mildred": 5,
    "Manus, Father of the Abyss": 14,
    "Marvelous Chester": 5,
    "Melinda the Butcher": 5,
    "Old Dragonslayer": 8,
    "Old Iron King": 12,
    "Oliver the Collector": 7,
    "Ornstein & Smough": 20,
    "Paladin Leeroy": 5,
    "Sir Alonne": 13,
    "Smelter Demon": 13,
    "Stray Demon": 13,
    "The Four Kings": 20,
    "The Last Giant": 16,
    "The Pursuer": 8,
    "Titanite Demon": 8,
    "Voracious Mimic": 7,
    "Vordt of the Boreal Valley": 17,
    "Winged Knight": 8,
    "Xanthous King Jeremiah": 5
}

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
    "physical": 21,
    "armor resist1": 22,
    "damage health1": 23,
    "damage health2": 24
}

try:
    a = len((list(enemyPath.glob("**/*.json"))))

    for i, enemy in enumerate(enemyPath.glob("**/*.json")):
        print(str((i/a)*100)[:6] + "%", end="\r")

        if "dsbg_shuffle" in enemy.stem:
            continue
        
        with open(enemy) as ef:
            e = load(ef)

        if "Ornstein" in enemy.stem or "Smough" in enemy.stem:
            baseName = "Ornstein & Smough"
            behaviorName = enemy.stem[enemy.stem.index(" - ")+3:]
        elif " - " in enemy.stem:
            baseName = enemy.stem[:enemy.stem.index(" - ")]
            behaviorName = enemy.stem[enemy.stem.index(" - ")+3:]
        else:
            baseName = enemy.stem
            behaviorName = ""

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

    keysToDelete = []
    for baseName in behaviorExport:
        for charCnt in behaviorExport[baseName]:
            for key in behaviorExport[baseName][charCnt]:
                for defKeyJson in behaviorExport[baseName][charCnt][key]:
                    if (
                        len(behaviorExport[baseName][charCnt].get(str(float(key)-0.1), {}).get(defKeyJson, {}))
                        + len(behaviorExport[baseName][charCnt][key][defKeyJson])
                        + len(behaviorExport[baseName][charCnt].get(str(float(key)+0.1), {}).get(defKeyJson, {}))
                        ) != behaviorCount.get(baseName, 1):
                        keysToDelete.append((baseName, charCnt, key, defKeyJson))

    for k in keysToDelete:
        del behaviorExport[k[0]][k[1]][k[2]][k[3]]

    keysToDelete = []
    for baseName in behaviorExport:
        for charCnt in behaviorExport[baseName]:
            for key in behaviorExport[baseName][charCnt]:
                if len(behaviorExport[baseName][charCnt][key]) == 0:
                    keysToDelete.append((baseName, charCnt, key))

    for k in keysToDelete:
        del behaviorExport[k[0]][k[1]][k[2]]

    print("")

    for key in behaviorExport:
        with open(baseFolder + "\\enemy_variants\\dsbg_shuffle_difficulty_" + key + ".json", "w") as enemyFile:
            dump(behaviorExport[key], enemyFile)

except Exception as ex:
    input(ex)
    raise
