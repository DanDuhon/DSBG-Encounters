from json import load, dump
from os import path, listdir


baseFolder = path.dirname(__file__)

encounters = {}

for encounterFile in listdir(baseFolder + "\\combine"):
    with open(path.join(baseFolder + "\\combine", encounterFile)) as efl:
        e = load(efl)
    if not e:
        continue
    encounters[e["name"]] = e

with open(baseFolder + "\\dsbg_shuffle_encounters.json", "w") as efd:
    dump(encounters, efd)
