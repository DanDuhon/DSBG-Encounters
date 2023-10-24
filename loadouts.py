from itertools import product
from os import path
from json import dump
from random import shuffle

from armor import armor
from hand_items import handItems
from attacks import attacks


baseFolder = path.dirname(__file__)

lenArmor = len(armor)

expectedDamageBlock = dict()
for x in range(5):
    expectedDamageBlock[x] = dict()
    for y in range(2, 10):
        expectedDamageBlock[x][y] = 0

expectedDamageResist = dict()
for x in range(5):
    expectedDamageResist[x] = dict()
    for y in range(2, 10):
        expectedDamageResist[x][y] = 0

# Because we're attacking enemies with every possible result of
# a weapon's damage rolls, I want to make sure each weapon gets
# equal representation.  Find a number that can be divided by
# all weapon results evenly.  That's how many results we want
# to apply for each weapon.
attackResults = sorted(list(set([len([d for d in product(*attack.damage)]) for attack in attacks])), reverse=True)
rounds = attackResults[0]
for a in attackResults[1:]:
    if a != 0 and rounds % a != 0:
        rounds = rounds * a

allAttacks = []
# A weapon's attack
for attack in attacks:
    # Each roll inside that attack (multiple for repeats)
    for i, roll in enumerate(attack.damage):
        attackResults = [max([0, sum(a) + attack.damageMod]) for a in product(*attack.damage[i])]
        totalResults = attackResults * int(rounds / len(attackResults))
        shuffle(totalResults)
        # Each possible result of the roll
        for result in totalResults:
            allAttacks.append((result, attack.damageBonus, attack.magic, attack.ignoreArmor, attack.poison, attack.bleed))

# Randomize the order of the attacks.
shuffle(allAttacks)

with open(baseFolder + "\\attacks.json", "w") as enemyFile:
    dump(allAttacks, enemyFile)

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

            for x in range(5):
                dodgeMod[x] = 1 if all([not a.canDodge, not mh.canDodge, not oh.canDodge]) else 1 - (sum([1 for do in product(*(a.dodge + mh.dodge + oh.dodge)) if sum(do) >= x]) / len(list(product(*(a.dodge + mh.dodge + oh.dodge)))))
                for y in range(2, 10):
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
