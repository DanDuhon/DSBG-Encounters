from json import load
from os import path, listdir

from enemies import enemies


baseFolder = path.dirname(__file__)

for enemy in enemies:
    with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.index(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json") as efd:
        ed = load(efd)
    enemy.deaths = ed["deaths"]
    enemy.damageDone = {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}, 4: {1: 0, 2: 0, 3: 0}}
    for enemyFile in listdir(baseFolder + "\\enemies"):
        if (enemy.name not in enemyFile
            or enemy.name == "Mimic" and ("Voracious" in enemyFile or "Hungry" in enemyFile)
            or enemy.name == "Hollow Soldier" and "Large" in enemyFile
            or enemy.name == "Skeleton Soldier" and "Giant" in enemyFile
            or enemy.name == "Skeleton Archer" and "Giant" in enemyFile
            or enemy.name == "Phalanx" and "Hollow" in enemyFile):
            continue
        
        with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.index(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json") as ef:
            e = load(ef)
        for tier in range(1, 4):
            enemy.damageDone[1][tier] += e["damageDone"]["1"][str(tier)]
            enemy.damageDone[2][tier] += e["damageDone"]["2"][str(tier)]
            enemy.damageDone[3][tier] += e["damageDone"]["3"][str(tier)]
            enemy.damageDone[4][tier] += e["damageDone"]["4"][str(tier)]
    print(enemy.name + "1_1_" + str(enemy.damageDone[1][1]) + "_" + str(enemy.deaths["1"]))
    print(enemy.name + "1_2_" + str(enemy.damageDone[2][1]) + "_" + str(enemy.deaths["1"]))
    print(enemy.name + "1_3_" + str(enemy.damageDone[3][1]) + "_" + str(enemy.deaths["1"]))
    print(enemy.name + "1_4_" + str(enemy.damageDone[4][1]) + "_" + str(enemy.deaths["1"]))
    print(enemy.name + "2_1_" + str(enemy.damageDone[1][2]) + "_" + str(enemy.deaths["2"]))
    print(enemy.name + "2_2_" + str(enemy.damageDone[2][2]) + "_" + str(enemy.deaths["2"]))
    print(enemy.name + "2_3_" + str(enemy.damageDone[3][2]) + "_" + str(enemy.deaths["2"]))
    print(enemy.name + "2_4_" + str(enemy.damageDone[4][2]) + "_" + str(enemy.deaths["2"]))
    print(enemy.name + "3_1_" + str(enemy.damageDone[1][3]) + "_" + str(enemy.deaths["3"]))
    print(enemy.name + "3_2_" + str(enemy.damageDone[2][3]) + "_" + str(enemy.deaths["3"]))
    print(enemy.name + "3_3_" + str(enemy.damageDone[3][3]) + "_" + str(enemy.deaths["3"]))
    print(enemy.name + "3_4_" + str(enemy.damageDone[4][3]) + "_" + str(enemy.deaths["3"]))
input()