from json import load, dump
from os import path, listdir

from enemies import enemies


baseFolder = path.dirname(__file__)

encounters = {}

for encounterFile in listdir(baseFolder + "\\combine"):
    with open(path.join(baseFolder + "\\combine", encounterFile)) as efl:
        e = load(efl)
    encounters[e["name"]] = e

with open(baseFolder + "\\encounters.json", "w") as efd:
    dump(encounters, efd)
