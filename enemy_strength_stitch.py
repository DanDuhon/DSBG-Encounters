from json import load
from os import path, listdir

from enemies import enemies


baseFolder = path.dirname(__file__)

for enemy in enemies:
    enemy.damageDone = {1: 0, 2: 0, 3: 0, 4: 0}
    for enemyFile in listdir(baseFolder + "\\enemies"):
        if "0" in enemyFile and enemy.name in enemyFile:
            if enemy.name == "Mimic" and ("Voracious" in enemyFile or "Hungry" in enemyFile):
                continue
            with open(path.join(baseFolder + "\\enemies", enemyFile)) as efd:
                ed = load(efd)
            enemy.deaths = ed["deaths"]

        if "0" not in enemyFile or enemy.name not in enemyFile:
            continue
        if enemy.name == "Mimic" and ("Voracious" in enemyFile or "Hungry" in enemyFile):
            continue
        with open(path.join(baseFolder + "\\enemies", enemyFile)) as ef:
            e = load(ef)
        enemy.damageDone[1] += e["damageDone"]["1"]
        enemy.damageDone[2] += e["damageDone"]["2"]
        enemy.damageDone[3] += e["damageDone"]["3"]
        enemy.damageDone[4] += e["damageDone"]["4"]
    print(enemy.name + "_1_" + str(enemy.damageDone[1]) + "_" + str(enemy.deaths))
    print(enemy.name + "_2_" + str(enemy.damageDone[2]) + "_" + str(enemy.deaths))
    print(enemy.name + "_3_" + str(enemy.damageDone[3]) + "_" + str(enemy.deaths))
    print(enemy.name + "_4_" + str(enemy.damageDone[4]) + "_" + str(enemy.deaths))
input()