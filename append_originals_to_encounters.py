from os import path
from json import load, dump


baseFolder = path.dirname(__file__)

with open(path.join(baseFolder + "\\encounters", "all_encounters.json")) as aef:
    allEncounters = load(aef)

for encounter in allEncounters:
    for i in range(1, 5):
        print(encounter + str(i))

        with open(path.join(baseFolder + "\\encounters", encounter + str(i) + ".json")) as ef:
            e = load(ef)

        enemies = []
        for tile in allEncounters[encounter]["tiles"]:
            enemies += allEncounters[encounter]["tiles"][tile]["enemies"] + allEncounters[encounter]["tiles"][tile]["spawns"]

        e["original"] = enemies
                
        with open(baseFolder + "\\encounters\\" + encounter + str(i) + ".json", "w") as encountersFile:
            dump(e, encountersFile)