from itertools import product, chain, combinations
from statistics import mean

from armor import armorTiers
from hand_items import handItemTiers
from attacks import weaponRange


b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)
means = {
    b: mean(b),
    u: mean(u),
    o: mean(o),
    d: mean(d)
}

loadouts = {
    1: [],
    2: [],
    3: []
}

dodgeMod = {
    1: {},
    2: {},
    3: {}
}

loadoutLookup = {1: {}, 2: {}, 3: {}}
x=0
for tier in range(1, 4):
    loadoutsCombos = chain(
        product(armorTiers[tier], product([h for h in handItemTiers[tier] if h.twoHanded], [h for h in handItemTiers[tier] if h.canUseWithTwoHanded])),
        product(armorTiers[tier], combinations([h for h in handItemTiers[tier] if not h.twoHanded], 2)))

    for i, l in enumerate(loadoutsCombos):
        # This is to speed things up for testing.
        # if i > 100:
        #     break
        loadouts[tier].append({
            "block": sum([means[die] for die in l[0].block + l[1][0].block + l[1][1].block]) + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod]),
            "blockRoll": [[v + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod]) for v in b] for b in l[0].block + l[1][0].block + l[1][1].block],
            "resist": sum([means[die] for die in l[0].resist + l[1][0].resist + l[1][1].resist]) + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod]),
            "resistRoll": [[v + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod]) for v in b] for b in l[0].resist + l[1][0].resist + l[1][1].resist],
            "dodge": 0 if not all([l[0].canDodge, l[1][0].canDodge, l[1][1].canDodge]) else (l[0].dodge + l[1][0].dodge + l[1][1].dodge),
            "dodgeBonus": l[0].dodgeBonus,
            "immunities": l[0].immunities | l[1][0].immunities | l[1][1].immunities
        })

        maxRange = max([weaponRange.get(l[1][0].name, 0), weaponRange.get(l[1][1].name, 0)])
        block = sum([means[die] for die in l[0].block + l[1][0].block + l[1][1].block]) + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod])
        blockArmorOnly = sum([means[die] for die in l[0].block]) + sum([l[0].blockMod])
        resist = sum([means[die] for die in l[0].resist + l[1][0].resist + l[1][1].resist]) + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod])
        dodge = (0,) if not all([l[0].canDodge, l[1][0].canDodge, l[1][1].canDodge]) else tuple(l[0].dodge + l[1][0].dodge + l[1][1].dodge)

        if tuple([block, resist, dodge, maxRange, blockArmorOnly]) in loadoutLookup[tier]:
            loadoutLookup[tier][tuple([block, resist, dodge, maxRange, blockArmorOnly])] += 1
        else:
            loadoutLookup[tier][tuple([block, resist, dodge, maxRange, blockArmorOnly])] = 1
            x += 1

    # Overall dodge modifier for the following dodge difficulties.
    # Used for enemies that inflict Stagger or Frostbite.
    dodgeMod[tier] = {
        0: 1,
        1: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 1]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
        2: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 2]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
        3: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 3]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
        4: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 4]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
        5: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 5]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
        6: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 6]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]])
    }

# Winged Knight gets a bonus against blocks of 3 or higher.
expectedBlock = {}
expectedResist = {}
for x in range(2, 14):
    expectedBlock[x] = {
        1: 1 - (sum([1 for l in loadouts[1] if l["block"] >= x]) / len(loadouts[1])),
        2: 1 - (sum([1 for l in loadouts[2] if l["block"] >= x]) / len(loadouts[2])),
        3: 1 - (sum([1 for l in loadouts[3] if l["block"] >= x]) / len(loadouts[3]))
        }
    expectedResist[x] = {
        1: 1 - (sum([1 for l in loadouts[1] if l["resist"] >= x]) / len(loadouts[1])),
        2: 1 - (sum([1 for l in loadouts[2] if l["resist"] >= x]) / len(loadouts[2])),
        3: 1 - (sum([1 for l in loadouts[3] if l["resist"] >= x]) / len(loadouts[3]))
        }