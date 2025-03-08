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

# Sort the dict so we can just load it in and not sort it later.
coreSets = {"Painted World of Ariamis", "The Sunless City", "Tomb of Giants", "Dark Souls The Board Game"}
v2Expansions = {"Painted World of Ariamis", "The Sunless City", "Tomb of Giants"}
encounters = dict(sorted(encounters.items(), key=lambda x: (
    1 if encounters[x]["level"] == 4 else 0,
    0 if encounters[x]["expansion"] in coreSets and encounters[x]["expansion"] in v2Expansions else 1,
    0 if encounters[x]["expansion"] in v2Expansions else 1,
    1 if encounters[x]["expansion"] == "Executioner Chariot" else 0,
    encounters[x]["expansion"],
    encounters[x]["level"],
    encounters[x]["name"])))

with open(baseFolder + "\\dsbg_shuffle_encounters.json", "w") as efd:
    dump(encounters, efd)
