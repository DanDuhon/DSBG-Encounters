from itertools import product, chain, combinations
from statistics import mean

from armor import armor
from hand_items import handItems


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

loadoutsCombos = chain(
    product(armor, product([h for h in handItems if h.twoHanded], [h for h in handItems if h.canUseWithTwoHanded])),
    product(armor, combinations([h for h in handItems if not h.twoHanded], 2)))

loadouts = []

for l in loadoutsCombos:
    loadouts.append({
        "block": sum([means[die] for die in l[0].block + l[1][0].block + l[1][1].block]) + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod]),
        "blockRoll": [[v + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod]) for v in b] for b in l[0].block + l[1][0].block + l[1][1].block],
        "resist": sum([means[die] for die in l[0].resist + l[1][0].resist + l[1][1].resist]) + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod]),
        "resistRoll": [[v + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod]) for v in b] for b in l[0].resist + l[1][0].resist + l[1][1].resist],
        "dodge": 0 if not all([l[0].canDodge, l[1][0].canDodge, l[1][1].canDodge]) else (l[0].dodge + l[1][0].dodge + l[1][1].dodge),
        "dodgeBonus": l[0].dodgeBonus,
        "immunities": l[0].immunities | l[1][0].immunities | l[1][1].immunities
    })

# Overall dodge modifier for the following dodge difficulties.
# Used for enemies that inflict Stagger or Frostbite.
dodgeMod = {
    1: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 1]) / len(list(product(*l["dodge"]))))) for l in loadouts]),
    2: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 2]) / len(list(product(*l["dodge"]))))) for l in loadouts]),
    3: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 3]) / len(list(product(*l["dodge"]))))) for l in loadouts]),
    4: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 4]) / len(list(product(*l["dodge"]))))) for l in loadouts])
}

# Winged Knight gets a bonus against blocks of 3 or higher.
expectedBlock3Plus = sum([1 for l in loadouts if l["block"] >= 3]) / len(loadouts)