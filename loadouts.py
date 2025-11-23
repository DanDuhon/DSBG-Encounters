from itertools import product, chain, combinations
from statistics import mean

from armor import armorByName
from hand_items import handItemsByName
from attacks import weaponRange, weaponRangeBoss
from builds import builds as classBuilds


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

partySizes = sorted({
    partySize
    for classBuild in classBuilds.values()
    for partySize in classBuild.keys()
})

tiers = sorted({
    tier
    for classBuild in classBuilds.values()
    for partyDict in classBuild.values()
    for tier in partyDict.keys()
})

loadouts = {
    partySize: {tier: [] for tier in tiers}
    for partySize in partySizes
}

dodgeMod = {
    partySize: {tier: {} for tier in tiers}
    for partySize in partySizes
}

loadoutLookup = {
    True: {
        partySize: {tier: {} for tier in tiers}
        for partySize in partySizes
    },
    False: {
        partySize: {tier: {} for tier in tiers}
        for partySize in partySizes
    },
}


# Helper to turn a name into either an armor or hand-item object.
def _lookup_item(name):
    """Return the armor/hand-item object for the given name.

    Prefers armorByName, falls back to handItemByName.
    """
    if name in armorByName:
        return armorByName[name]
    return handItemsByName[name]


# Build loadouts for each party size and tier.
unique_signature_count = 0

for partySize in partySizes:
    for tier in tiers:
        for className, partyDict in classBuilds.items():
            tierDict = partyDict[partySize]

            armors = []
            handItems = []
            itemNames = tierDict[tier]
            
            for name in itemNames:
                item = _lookup_item(name)

                if name in armorByName:
                    armors.append(item)
                else:
                    handItems.append(item)

            twoHanders = [h for h in handItems if getattr(h, "twoHanded", False)]
            offHands = [h for h in handItems if getattr(h, "canUseWithTwoHanded", False)]
            oneHanders = [h for h in handItems if not getattr(h, "twoHanded", False)]

            loadoutsCombos = chain(
                product(armors, product(twoHanders, offHands)) if twoHanders and offHands else [],
                product(armors, combinations(oneHanders, 2)) if len(oneHanders) >= 2 else [],
            )

            for armorObj, (mainHand, offHand) in loadoutsCombos:
                totalBlockMod = armorObj.blockMod + mainHand.blockMod + offHand.blockMod
                totalResistMod = armorObj.resistMod + mainHand.resistMod + offHand.resistMod

                blockDice = armorObj.block + mainHand.block + offHand.block
                resistDice = armorObj.resist + mainHand.resist + offHand.resist

                block = sum(means[die] for die in blockDice) + totalBlockMod
                blockRoll = [
                    [v + totalBlockMod for v in die]
                    for die in blockDice
                ]

                resist = sum(means[die] for die in resistDice) + totalResistMod
                resistRoll = [
                    [v + totalResistMod for v in die]
                    for die in resistDice
                ]

                canDodgeAll = (
                    getattr(armorObj, "canDodge", False)
                    and getattr(mainHand, "canDodge", False)
                    and getattr(offHand, "canDodge", False)
                )

                dodge_value = (
                    0
                    if not canDodgeAll
                    else (armorObj.dodge + mainHand.dodge + offHand.dodge)
                )

                loadouts[partySize][tier].append(
                    {
                        "block": block,
                        "blockRoll": blockRoll,
                        "resist": resist,
                        "resistRoll": resistRoll,
                        "dodge": dodge_value,
                        "dodgeBonus": armorObj.dodgeBonus,
                        "immunities": (
                            armorObj.immunities
                            | mainHand.immunities
                            | offHand.immunities
                        ),
                    }
                )

                maxRange = max(
                    weaponRange.get(mainHand.name, 0),
                    weaponRange.get(offHand.name, 0),
                )
                maxRangeBoss = max(
                    weaponRangeBoss.get(mainHand.name, 0),
                    weaponRangeBoss.get(offHand.name, 0),
                )

                blockArmorOnly = (
                    sum(means[die] for die in armorObj.block) + armorObj.blockMod
                )
                resistArmorOnly = (
                    sum(means[die] for die in armorObj.resist) + armorObj.resistMod
                )

                dodge_for_key = (
                    (0,)
                    if not canDodgeAll
                    else tuple(armorObj.dodge + mainHand.dodge + offHand.dodge)
                )
                dodgeArmorOnly = (
                    (0,)
                    if not canDodgeAll
                    else tuple(armorObj.dodge)
                )

                # For enemies with ambush
                ambushKey = (
                    block,
                    resist,
                    dodge_for_key,
                    maxRange,
                    blockArmorOnly,
                    resistArmorOnly,
                    dodgeArmorOnly,
                )
                ambushLookup = loadoutLookup[True][partySize][tier]
                if ambushKey in ambushLookup:
                    ambushLookup[ambushKey] += 1
                else:
                    ambushLookup[ambushKey] = 1
                    unique_signature_count += 1

                # Everybody else
                normalKey = (
                    block,
                    resist,
                    dodge_for_key,
                    maxRange,
                    maxRangeBoss,
                )
                normalLookup = loadoutLookup[False][partySize][tier]
                if normalKey in normalLookup:
                    normalLookup[normalKey] += 1
                else:
                    normalLookup[normalKey] = 1
                    unique_signature_count += 1

        # After we've built all loadouts for this partySize/tier, compute
        # the dodge modifiers used by various enemies.
        current_loadouts = loadouts[partySize][tier]

        dodgeMod[partySize][tier] = {0: 1}
        for difficulty in range(1, 7):
            dodgeMod[partySize][tier][difficulty] = mean(
                [
                    1 if l["dodge"] == 0 else (1- (sum(
                        1 for outcome in product(*l["dodge"])if sum(outcome) >= difficulty)
                        / len(list(product(*l["dodge"])))
                        )
                    )
                    for l in current_loadouts
                ]
            )

# Winged Knight gets a bonus against blocks of 3 or higher.
expectedBlock = {partySize: {} for partySize in partySizes}
expectedResist = {partySize: {} for partySize in partySizes}

for partySize in partySizes:
    for threshold in range(2, 14):
        expectedBlock[partySize][threshold] = {}
        expectedResist[partySize][threshold] = {}
        for tier in tiers:
            current_loadouts = loadouts[partySize][tier]
            if not current_loadouts:
                expectedBlock[partySize][threshold][tier] = 1
                expectedResist[partySize][threshold][tier] = 1
                continue

            expectedBlock[partySize][threshold][tier] = 1 - (
                sum(1 for l in current_loadouts if l["block"] >= threshold)
                / len(current_loadouts)
            )
            expectedResist[partySize][threshold][tier] = 1 - (
                sum(1 for l in current_loadouts if l["resist"] >= threshold)
                / len(current_loadouts)
            )