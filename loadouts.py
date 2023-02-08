from itertools import product
from os import path
from json import dump

from armor import armor
from hand_items import handItems


baseFolder = path.dirname(__file__)

lenArmor = len(armor)

expectedDamageBlock = dict()
for x in range(1, 3):
    expectedDamageBlock[x] = dict()
    for y in range(2, 7):
        expectedDamageBlock[x][y] = 0

expectedDamageResist = dict()
for x in range(1, 3):
    expectedDamageResist[x] = dict()

dodgeMod = dict()

for i, a in enumerate(armor):
    loadouts = {}
    print(a.name)
    for mh in handItems:
        if not mh.name:
            continue
        for oh in handItems:
            if oh.twoHanded or mh == oh or (mh.twoHanded and not oh.canUseWithTwoHanded) or (not mh.twoHanded and oh is None):
                continue

            for x in range(1, 3):
                dodgeMod[x] = 1 if all([not a.canDodge, not mh.canDodge, not oh.canDodge]) else 1 - (sum([1 for do in product(*(a.dodge + mh.dodge + oh.dodge)) if sum(do) >= x]) / len(list(product(*(a.dodge + mh.dodge + oh.dodge)))))
                for y in range(2, 7):
                    expectedDamageBlock[x][y] = a.expectedDamageBlock[x][y]
                    expectedDamageResist[x][y] = a.expectedDamageResist[x][y]
            
            loadoutKey = frozenset([a.name, mh.name, oh.name])

            if loadoutKey not in loadouts:
                loadouts[loadoutKey] = {
                    "expected damage block": expectedDamageBlock,
                    "expected damage resist": expectedDamageResist,
                    "dodge mod": {k: dodgeMod[k] for k in dodgeMod},
                    "immunities": ["bleed" if any(["bleed" in mh.immunities, "bleed" in oh.immunities, "bleed" in a.immunities]) else None, "poison" if any(["poison" in mh.immunities, "poison" in oh.immunities, "poison" in a.immunities]) else None],
                    "dodge bonus": None if any([not a.canDodge, not mh.canDodge, not oh.canDodge]) else a.dodgeBonus
                    }
                    
    with open(baseFolder + "\\loadouts\\" + a.name + ".json", "w") as loadoutsFile:
        dump({str(k): loadouts[k] for k in loadouts}, loadoutsFile)
