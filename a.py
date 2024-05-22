from json import load, dump
from os import path
from pathlib import Path


baseFolder = path.dirname(__file__)
encounterPath = Path(baseFolder + "\\encounters")
mimics = {34,47,48}
invaders = {35,36,37,38,39,40,41,42,43,44,45,46,47,48}
maxInvaders = 0

try:
    for encounter in encounterPath.glob("**/*.json"):
        print(encounter.stem)
        if "all_encounters" in encounter.stem:
            continue

        with open(encounter) as ef:
            e = load(ef)

        for alt in [alt for alt in e["alternatives"] if "Phantoms" in alt]:
            toDelete = []
            x = len(e["alternatives"][alt])
            for a in e["alternatives"][alt]:
                if len(set(a) & mimics) > 1:
                    toDelete.append(a)
                elif len(set(a) & invaders) > maxInvaders:
                    maxInvaders = len(set(a) & invaders)
            e["alternatives"][alt] = [a for a in e["alternatives"][alt] if a not in toDelete]
            if x - len(toDelete) != len(e["alternatives"][alt]):
                pass

        with open(encounter) as ef:
            dump(e, ef)

except Exception as ex:
    input(ex)
    raise
