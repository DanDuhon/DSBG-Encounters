from json import load, dump
from os import path
from pathlib import Path
from math import ceil
from enemies import enemiesDict


baseFolder = path.dirname(__file__)
enemyPath = Path(baseFolder + "\\enemies")

baselineDiff = {}
compare = {}

try:
    l = len((list(enemyPath.glob("**/*.json"))))

    for i, enemy in enumerate(enemyPath.glob("**/*.json")):
        print(str((i/l)*100)[:6] + "%", end="\r")
        baseName = enemy.stem[:enemy.stem.rfind(" (") if " (" in enemy.stem else len(enemy.stem)]
        if baseName not in enemiesDict:
            continue
        if baseName not in compare:
            compare[baseName] = {e: {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0} for e in enemiesDict if "(" not in e}
        with open(enemy) as ef:
            e = load(ef)
        for charCnt in range(1, 5):
            diff = (e["damageDone"][str(charCnt)]["3"] / e["deaths"]["3"]) * 100
            if diff == 0:
                continue

            if (baseName, charCnt, 3) not in baselineDiff:
                baselineDiff[(baseName, charCnt, 3)] = diff
            else:
                # I want to group everything in groups of 20%, so round up to the nearest even tenth.
                diffChange = (ceil((round(diff/baselineDiff[(baseName, charCnt, 3)], 1) * 10) / 2.0) * 2) / 10

                if diffChange <= 1.0:
                    continue

                for a in compare[baseName]:
                    if enemiesDict[baseName].difficultyTiers[3]["difficulty"][charCnt] >= enemiesDict[a].difficultyTiers[3]["difficulty"][charCnt]:
                        continue
                    if diff >= enemiesDict[a].difficultyTiers[3]["difficulty"][charCnt] and (compare[baseName][a][charCnt] == 0 or compare[baseName][a][charCnt] > diffChange):
                        compare[baseName][a][charCnt] = diffChange

    with open(baseFolder + "\\enemy_compare.json", "w") as out:
        dump(compare, out)

    compareOut = "|  | " + " | ".join(e for e in compare) + " |\n|" + (" :---: |" * (len(compare) + 1))
    for e in compare:
        compareOut += "\n| " + e + " | "
        for ee in compare[e]:
            compareOut += (
                (str(int(round((compare[e][ee][1] - 1) * 100))) if compare[e][ee][1] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][2] - 1) * 100))) if compare[e][ee][2] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][3] - 1) * 100))) if compare[e][ee][3] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][4] - 1) * 100))) if compare[e][ee][4] - 1 > 0 else "") + " | ")

    with open(baseFolder + "\\enemy_compare_wiki_all.json", "w") as out:
        out.write(compareOut)

    compareOut = "|  | " + " | ".join(e for e in compare if enemiesDict[e].expansion in {"Dark Souls The Board Game", "The Sunless City"}) + " |\n|" + (" :---: |" * (len([e for e in compare if enemiesDict[e].expansion in {"Dark Souls The Board Game", "The Sunless City"}]) + 1))
    for e in [e for e in compare if enemiesDict[e].expansion in {"Dark Souls The Board Game", "The Sunless City"}]:
        compareOut += "\n| " + e + " | "
        for ee in compare[e]:
            if enemiesDict[ee].expansion not in {"Dark Souls The Board Game", "The Sunless City"}:
                continue
            compareOut += (
                (str(int(round((compare[e][ee][1] - 1) * 100))) if compare[e][ee][1] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][2] - 1) * 100))) if compare[e][ee][2] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][3] - 1) * 100))) if compare[e][ee][3] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][4] - 1) * 100))) if compare[e][ee][4] - 1 > 0 else "") + " | ")

    with open(baseFolder + "\\enemy_compare_wiki_tsc.json", "w") as out:
        out.write(compareOut)

    compareOut = "|  | " + " | ".join(e for e in compare if enemiesDict[e].expansion == "Painted World of Ariamis") + " |\n|" + (" :---: |" * (len([e for e in compare if enemiesDict[e].expansion == "Painted World of Ariamis"]) + 1))
    for e in [e for e in compare if enemiesDict[e].expansion == "Painted World of Ariamis"]:
        compareOut += "\n| " + e + " | "
        for ee in compare[e]:
            if enemiesDict[ee].expansion != "Painted World of Ariamis":
                continue
            compareOut += (
                (str(int(round((compare[e][ee][1] - 1) * 100))) if compare[e][ee][1] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][2] - 1) * 100))) if compare[e][ee][2] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][3] - 1) * 100))) if compare[e][ee][3] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][4] - 1) * 100))) if compare[e][ee][4] - 1 > 0 else "") + " | ")

    with open(baseFolder + "\\enemy_compare_wiki_pwa.json", "w") as out:
        out.write(compareOut)

    compareOut = "|  | " + " | ".join(e for e in compare if enemiesDict[e].expansion == "Tomb of Giants") + " |\n|" + (" :---: |" * (len([e for e in compare if enemiesDict[e].expansion == "Tomb of Giants"]) + 1))
    for e in [e for e in compare if enemiesDict[e].expansion == "Tomb of Giants"]:
        compareOut += "\n| " + e + " | "
        for ee in compare[e]:
            if enemiesDict[ee].expansion != "Tomb of Giants":
                continue
            compareOut += (
                (str(int(round((compare[e][ee][1] - 1) * 100))) if compare[e][ee][1] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][2] - 1) * 100))) if compare[e][ee][2] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][3] - 1) * 100))) if compare[e][ee][3] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][4] - 1) * 100))) if compare[e][ee][4] - 1 > 0 else "") + " | ")

    with open(baseFolder + "\\enemy_compare_wiki_tog.json", "w") as out:
        out.write(compareOut)

    compareOut = "|  | " + " | ".join(e for e in compare if enemiesDict[e].expansion == "Darkroot") + " |\n|" + (" :---: |" * (len([e for e in compare if enemiesDict[e].expansion == "Darkroot"]) + 1))
    for e in [e for e in compare if enemiesDict[e].expansion == "Darkroot"]:
        compareOut += "\n| " + e + " | "
        for ee in compare[e]:
            if enemiesDict[ee].expansion != "Darkroot":
                continue
            compareOut += (
                (str(int(round((compare[e][ee][1] - 1) * 100))) if compare[e][ee][1] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][2] - 1) * 100))) if compare[e][ee][2] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][3] - 1) * 100))) if compare[e][ee][3] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][4] - 1) * 100))) if compare[e][ee][4] - 1 > 0 else "") + " | ")

    with open(baseFolder + "\\enemy_compare_wiki_dr.json", "w") as out:
        out.write(compareOut)

    compareOut = "|  | " + " | ".join(e for e in compare if enemiesDict[e].expansion == "Iron Keep") + " |\n|" + (" :---: |" * (len([e for e in compare if enemiesDict[e].expansion == "Iron Keep"]) + 1))
    for e in [e for e in compare if enemiesDict[e].expansion == "Iron Keep"]:
        compareOut += "\n| " + e + " | "
        for ee in compare[e]:
            if enemiesDict[ee].expansion != "Iron Keep":
                continue
            compareOut += (
                (str(int(round((compare[e][ee][1] - 1) * 100))) if compare[e][ee][1] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][2] - 1) * 100))) if compare[e][ee][2] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][3] - 1) * 100))) if compare[e][ee][3] - 1 > 0 else "")
                + ("/" + str(int(round((compare[e][ee][4] - 1) * 100))) if compare[e][ee][4] - 1 > 0 else "") + " | ")

    with open(baseFolder + "\\enemy_compare_wiki_ik.json", "w") as out:
        out.write(compareOut)

except Exception as ex:
    print(enemy)
    input(ex)
    raise
