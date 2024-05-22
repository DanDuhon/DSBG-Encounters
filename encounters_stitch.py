from json import load, dump
from os import path, listdir


baseFolder = path.dirname(__file__)

encounters = {}

for encounterFile in listdir(baseFolder + "\\combine"):
    with open(path.join(baseFolder + "\\combine", encounterFile)) as efl:
        e = load(efl)
    if not e:
        continue
    if e["name"] not in encounters:
        encounters[e["name"]] = {
            "name": e["name"],
            "expansion": e["expansion"],
            "level": e["level"],
            "expansionCombos": {1: [], 2: [], 3: [], 4: []}
        }
    encounters[e["name"]]["expansionCombos"][int(encounterFile[-6])] = e["expansionCombos"]

with open(baseFolder + "\\dsbg_shuffle_encounters.json", "w") as efd:
    dump(encounters, efd)
