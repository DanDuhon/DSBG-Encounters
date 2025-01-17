from json import load, dump
from os import path
from pathlib import Path


baseFolder = path.dirname(__file__)
enemyPath = Path(baseFolder + "\\enemies")

enemies = {}
baselineDiff = {}
allEnemies = []
baseNames = set()

behaviorCount = {
    "Armorer Dennis": 5,
    "Artorias": 13,
    "Asylum Demon": 9,
    "Black Dragon Kalameet": 13,
    "Black Knight": 9,
    "Boreal Outrider Knight": 8,
    "Crossbreed Priscilla": 13,
    "Dancer of the Boreal Valley": 13,
    "Executioner's Chariot": 16,
    "Fencer Sharron": 7,
    "Gaping Dragon": 13,
    "Gargoyle": 8,
    "Gravelord Nito": 13,
    "Great Grey Wolf Sif": 14,
    "Guardian Dragon": 13,
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
    "The Pursuer": 11,
    "Titanite Demon": 8,
    "Voracious Mimic": 7,
    "Vordt of the Boreal Valley": 17,
    "Winged Knight": 8,
    "Xanthous King Jeremiah": 5
}

try:
    a = len((list(enemyPath.glob("**/*.json"))))

    for i, enemy in enumerate(enemyPath.glob("**/*.json")):
        # if "Asylum Demon" not in enemy.stem:
        #     continue
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

                diff = e["damageDone"][str(charCnt)][str(tier)] / e["deaths"][str(tier)]
                if diff == 0:
                    continue

                if (baseName, charCnt, tier) not in baselineDiff:
                    baselineDiff[(baseName, charCnt, tier)] = diff
                else:
                    roundTarget = 5 + behaviorCount.get(baseName if "-" not in baseName else baseName[:baseName.index(" - ")], 0)
                    d = round((diff/baselineDiff[(baseName, charCnt, tier)]) * 100)
                    diffChange = (roundTarget * round(d / roundTarget)) / 100

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

except Exception as ex:
    print(enemy)
    input(ex)
    raise
