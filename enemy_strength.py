from json import load, dump
from os import path
from enemies import enemies
from loadouts import loadoutLookup
from itertools import product
from statistics import mean
from time import sleep


baseFolder = path.dirname(__file__)

b = [0, 1, 1, 1, 2, 2]
u = [1, 1, 2, 2, 2, 3]
o = [1, 2, 2, 3, 3, 4]
d = [0, 0, 0, 1, 1, 1]

# Based on how many nodes an enemy can reach
# using their move plus range for a particular attack.
# Infinite range enemies all have reach 4 (move 0 range 4).
# Multiply expected damage by this amount for an attack's
# reach. This gives us expected damage across all possible
# configurations on an otherwise empty tile.
reachMod = {
    "regular": {
        0: 0.07692307692307693,
        1: 0.44970414201183434,
        2: 0.8224852071005917,
        3: 0.9763313609467456,
        4: 1
    },
    "invader": {
        0: 0.07692307692307693,
        1: 0.44970414201183434,
        2: 0.8224852071005917,
        3: 0.9763313609467456,
        4: 1
    },
    "mini boss": {
        0: 0.07692307692307693,
        1: 0.44970414201183434,
        2: 0.8224852071005917,
        3: 0.9763313609467456,
        4: 1
    },
    "main boss": {
        0: 0.0384615384615385,
        1: 0.2582417582,
        2: 0.5412087912,
        3: 0.7637362637,
        4: 1
    },
    "mega boss": {
        0: 0.04,
        1: 0.2704,
        2: 0.5648,
        3: 0.8336,
        4: 1
    },
    # Middle node is inaccessible.
    "Executioner's Chariot": {
        0: 0.0416666666666667,
        1: 0.2638888889,
        2: 0.52,
        3: 0.8194444444,
        4: 1
    },
    # OIK only has 3 nodes he can be on and only 19 accessible nodes.
    "Old Iron King": {
        0: 0.0526315789473684,
        1: 0.3157894736842105,
        2: 0.7017543859649123,
        3: 0.8947368421052632,
        4: 1
    }
}

# Node attacks get a damage multiplier based on how likely
# it is that it'll hit multiple characters based on all
# possible configurations on an otherwise empty tile.
# The keys are the number of characters (1 character would be 1 mod).
# Chance of another character being on the target's node: 1/13.
# For 3 players, it's 2 * (1/13) + the chance both are there: (1/13) * (1/13).
# For 4 players, it's 3 * (1/13) + the different ways two could be there: 3 * ((1/13) * (1/13))
nodeAttackMod = {
    2: 1.07692307692307693,
    3: 1.1538461538461538,
    4: 1.2485207100591715
}


def arc_damage_mod(nodesAttacked, megaBoss):
    nodes = 28 if megaBoss else 16
    return {
        1: 1,
        2: 1 + (nodesAttacked / nodes),
        3: 1 + (((nodesAttacked / nodes) * 2) + ((nodesAttacked / nodes) * (nodesAttacked / nodes))),
        4: 1 + (((nodesAttacked / nodes) * 3) + (((nodesAttacked / nodes) * (nodesAttacked / nodes)) * 3))
        }


# This will be used to help calculate expected bleed damage from
# potential bleed damage.  Since any enemy can proc bleed once it
# has been applied, one piece of the puzzle we need is how often
# we can expect any enemy to be able to make an attack.
# This only needs to be run when the regular enemies actually change.
# reachSum = 0
# reachDiv = 0
# for enemy in enemies:
#     if enemy.enemyType == "regular" and not enemy.modified:
#         for _ in range(enemy.numberOfModels):
#             for i in range(len(enemy.attacks)):
#                 reachSum += reachMod[enemy.enemyType][max([0, min([4, sum(enemy.move[:i+1]) + sum(enemy.attackRange[:i+1]) - (1 if enemy.windup else 0)])])]
#                 reachDiv += 1
# meanReachMod = reachSum / reachDiv
# input(meanReachMod)

# Output of the above here to hardcode elsewhere.
meanReachMod = 0.7714069147635578

try:
    tier = 3

    # Calculate enemy offense.
    print("Enemy offense tier " + str(tier))
    for x, loadout in enumerate(loadoutLookup[tier]):
        print(str((x/len(loadoutLookup[tier]))*100)[:6] + "%", end="\r")
        block = loadout[0]
        resist = loadout[1]
        multiplier = loadoutLookup[tier][loadout]
        for enemy in enemies:
            if tier < 3 and enemy.modified:
                continue
            totalAttacks = 0
            damagingAttacks = 0
            bleedDamage1 = 0
            bleedDamage2 = 0
            bleedDamage3 = 0
            bleedDamage4 = 0
            damageDone1 = []
            damageDone2 = []
            damageDone3 = []
            damageDone4 = []
            poisonAdded = False
            
            # For each enemy attack, calculate the expected
            # damage the enemy would do to this loadout.
            # Everything gets multiplied by two decimals.
            # One represents the reach concept - how likely
            # the enemy is to be in range to attack at all.
            # The second represents character dodge - how
            # likely the attack is to be dodged.
            for i in range(len(enemy.attacks)):
                if enemy.attacks[i] == 0:
                    continue
                totalAttacks += multiplier
                reach = reachMod["Executioner's Chariot" if "Executioner's Chariot" in enemy.name else "Old Iron King" if "Old Iron King" in enemy.name else enemy.enemyType][max([0, min([4, sum(enemy.move[:i+1]) + sum(enemy.attackRange[:i+1]) - (1 if enemy.windup else 0)])])]
                dodge = 1 if loadout[2] == (0,) else (1 - (sum([1 for do in product(*loadout[2]) if sum(do) >= enemy.dodge]) / len(list(product(*loadout[2])))))

                # This is the effect of Calamity, see below for more details.
                if "Black Dragon Kalameet" in enemy.name:
                    dodge -= 0.1528822055

                # This is the effect of Corrosion
                # Average chance of pulling Corrosive Ooze across the fight
                # Pre-heatup chance: (1/6) * (20/46)
                # Post-heatup chance: (2/7) * (26/46)
                if "Gaping Dragon" in enemy.name and enemy.attackType[i] == "physical":
                    addedDamage = 0.2339544513
                # This is the effect of Calamity
                # Average chance of pulling Mark of Calamity across the fight
                # Pre-heatup chance: (1/6) * (16/38)
                # Post-heatup chance: (1/7) * (22/38)
                elif "Black Dragon Kalameet" in enemy.name:
                    addedDamage = 0.1528822055
                # The horse still damages you if you completely block/resist it.
                elif "Executioner's Chariot" in enemy.name and enemy.attacks[i] > 0:
                    addedDamage = min([1, (block if enemy.attackType[i] == "physical" else resist) / enemy.attacks[i]])
                else:
                    addedDamage = 0
                    
                if not poisonAdded:
                    poison1 = (((2 if enemy.id else 1) if enemy.attackEffect and "poison" in enemy.attackEffect[i] else 0)
                        * reach
                        * dodge)
                    poison2 = (((2 if enemy.id else 1) if enemy.attackEffect and "poison" in enemy.attackEffect[i] else 0)
                        * reach
                        * dodge
                        * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                        * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[2] if enemy.nodesAttacked[i] > 0 else 1))
                    poison3 = (((2 if enemy.id else 1) if enemy.attackEffect and "poison" in enemy.attackEffect[i] else 0)
                        * reach
                        * dodge
                        * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                        * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[3] if enemy.nodesAttacked[i] > 0 else 1))
                    poison4 = (((2 if enemy.id else 1) if enemy.attackEffect and "poison" in enemy.attackEffect[i] else 0)
                        * reach
                        * dodge
                        * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                        * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[4] if enemy.nodesAttacked[i] > 0 else 1))
                    
                    if poison1 > 0.0 or poison2 or poison3 > 0.0 or poison4 > 0.0:
                        poisonAdded = True

                bleedDamage1 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge)
                bleedDamage2 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[2] if enemy.nodesAttacked[i] > 0 else 1))
                bleedDamage3 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[3] if enemy.nodesAttacked[i] > 0 else 1))
                bleedDamage4 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[4] if enemy.nodesAttacked[i] > 0 else 1))
                
                expectedDamage1 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    ) + poison1) * multiplier
                expectedDamage2 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[2] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison2) * multiplier
                expectedDamage3 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[3] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison3) * multiplier
                expectedDamage4 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[4] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison4) * multiplier
                
                if loadout[0] < 3 and any([expectedDamage1 == 0.0, expectedDamage2 == 0.0, expectedDamage3 == 0.0, expectedDamage4 == 0.0]):
                    pass

                damagingAttacks += dodge * multiplier
                    
                damageDone1.append(expectedDamage1)
                damageDone2.append(expectedDamage2)
                damageDone3.append(expectedDamage3)
                damageDone4.append(expectedDamage4)

            # Need to cut these in half because all regular enemy attacks get doubled
            # to better reflect how they work over two turns.
            enemy.totalAttacks[tier] += totalAttacks / (2 if enemy.id else 1)
            enemy.damagingAttacks[tier] += damagingAttacks / (2 if enemy.id else 1)
            enemy.damageDone1[tier] += sum([d for d in damageDone1]) / (2 if enemy.id else 1)
            enemy.damageDone2[tier] += sum([d for d in damageDone2]) / (2 if enemy.id else 1)
            enemy.damageDone3[tier] += sum([d for d in damageDone3]) / (2 if enemy.id else 1)
            enemy.damageDone4[tier] += sum([d for d in damageDone4]) / (2 if enemy.id else 1)
            enemy.bleedDamage1[tier] += bleedDamage1 / (2 if enemy.id else 1)
            enemy.bleedDamage2[tier] += bleedDamage2 / (2 if enemy.id else 1)
            enemy.bleedDamage3[tier] += bleedDamage3 / (2 if enemy.id else 1)
            enemy.bleedDamage4[tier] += bleedDamage4 / (2 if enemy.id else 1)
            
    # (Damaging attacks / total attacks) * average enemy reach
    # This is the % that bleed will be procced.  The attack has
    # to be made (reach), and then do damage.
    bleedProc = {}

    if "regular" in set([enemy.enemyType for enemy in enemies]):
        bleedProc["regular"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if enemy.enemyType == "regular"])) * meanReachMod
    if "Armorer Dennis" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Armorer Dennis"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Armorer Dennis" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Armorer Dennis" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Fencer Sharron" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Fencer Sharron"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Fencer Sharron" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Fencer Sharron" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Invader Brylex" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Invader Brylex"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Invader Brylex" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Invader Brylex" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Kirk, Knight of Thorns" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Kirk, Knight of Thorns"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Kirk, Knight of Thorns" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Kirk, Knight of Thorns" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Longfinger Kirk" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Longfinger Kirk"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Longfinger Kirk" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Longfinger Kirk" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Maldron the Assassin" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Maldron the Assassin"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Maldron the Assassin" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Maldron the Assassin" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Maneater Mildred" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Maneater Mildred"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Maneater Mildred" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Maneater Mildred" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Marvelous Chester" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Marvelous Chester"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Marvelous Chester" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Marvelous Chester" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Melinda the Butcher" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Melinda the Butcher"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Melinda the Butcher" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Melinda the Butcher" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Oliver the Collector" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Oliver the Collector"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Oliver the Collector" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Oliver the Collector" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Paladin Leeroy" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Paladin Leeroy"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Paladin Leeroy" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Paladin Leeroy" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Xanthous King Jeremiah" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Xanthous King Jeremiah"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Xanthous King Jeremiah" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Xanthous King Jeremiah" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Hungry Mimic" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Hungry Mimic"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Hungry Mimic" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Hungry Mimic" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Voracious Mimic" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Voracious Mimic"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Voracious Mimic" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Voracious Mimic" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod
    if "Old Dragonslayer" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Old Dragonslayer1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name])) * 0.845044378698225 * 1 # Mean reach and arc attack mods for Old Dragonslayer
        bleedProc["Old Dragonslayer2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name])) * 0.845044378698225 * 1.296875 # Mean reach and arc attack mods for Old Dragonslayer
        bleedProc["Old Dragonslayer3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name])) * 0.845044378698225 * 1.794921875 # Mean reach and arc attack mods for Old Dragonslayer
        bleedProc["Old Dragonslayer4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Dragonslayer" in enemy.name])) * 0.845044378698225 * 2.494140625 # Mean reach and arc attack mods for Old Dragonslayer
    if "Asylum Demon" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Asylum Demon1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name])) * 0.527284681130835 * 1 # Mean reach and arc attack mods for Asylum Demon
        bleedProc["Asylum Demon2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name])) * 0.527284681130835 * 1.28472222222222 # Mean reach and arc attack mods for Asylum Demon
        bleedProc["Asylum Demon3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name])) * 0.527284681130835 * 1.75911458333333 # Mean reach and arc attack mods for Asylum Demon
        bleedProc["Asylum Demon4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Asylum Demon" in enemy.name])) * 0.527284681130835 * 2.42317708333333 # Mean reach and arc attack mods for Asylum Demon
    if "Boreal Outrider Knight" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Boreal Outrider Knight1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name])) * 0.736316568047337 * 1 # Mean reach and arc attack mods for Boreal Outrider Knight
        bleedProc["Boreal Outrider Knight2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name])) * 0.736316568047337 * 1.3515625 # Mean reach and arc attack mods for Boreal Outrider Knight
        bleedProc["Boreal Outrider Knight3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name])) * 0.736316568047337 * 1.88037109375 # Mean reach and arc attack mods for Boreal Outrider Knight
        bleedProc["Boreal Outrider Knight4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Boreal Outrider Knight" in enemy.name])) * 0.736316568047337 * 2.58642578125 # Mean reach and arc attack mods for Boreal Outrider Knight
    if "Winged Knight" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Winged Knight1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name])) * 0.854289940828402 * 1 # Mean reach and arc attack mods for Winged Knight
        bleedProc["Winged Knight2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name])) * 0.854289940828402 * 1.4921875 # Mean reach and arc attack mods for Winged Knight
        bleedProc["Winged Knight3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name])) * 0.854289940828402 * 2.30810546875 # Mean reach and arc attack mods for Winged Knight
        bleedProc["Winged Knight4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Winged Knight" in enemy.name])) * 0.854289940828402 * 3.44775390625 # Mean reach and arc attack mods for Winged Knight
    if "Black Knight" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Black Knight1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name])) * 0.831689677843523 * 1 # Mean reach and arc attack mods for Black Knight
        bleedProc["Black Knight2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name])) * 0.831689677843523 * 1.24305555555556 # Mean reach and arc attack mods for Black Knight
        bleedProc["Black Knight3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name])) * 0.831689677843523 * 1.63107638888889 # Mean reach and arc attack mods for Black Knight
        bleedProc["Black Knight4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Knight" in enemy.name])) * 0.831689677843523 * 2.1640625 # Mean reach and arc attack mods for Black Knight
    if "Heavy Knight" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Heavy Knight1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name])) * 0.715318869165023 * 1 # Mean reach and arc attack mods for Heavy Knight
        bleedProc["Heavy Knight2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name])) * 0.715318869165023 * 1.27777777777778 # Mean reach and arc attack mods for Heavy Knight
        bleedProc["Heavy Knight3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name])) * 0.715318869165023 * 1.72916666666667 # Mean reach and arc attack mods for Heavy Knight
        bleedProc["Heavy Knight4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Heavy Knight" in enemy.name])) * 0.715318869165023 * 2.35416666666667 # Mean reach and arc attack mods for Heavy Knight
    if "Titanite Demon" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Titanite Demon1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name])) * 0.664201183431952 * 1 # Mean reach and arc attack mods for Titanite Demon
        bleedProc["Titanite Demon2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name])) * 0.664201183431952 * 1.328125 # Mean reach and arc attack mods for Titanite Demon
        bleedProc["Titanite Demon3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name])) * 0.664201183431952 * 1.865234375 # Mean reach and arc attack mods for Titanite Demon
        bleedProc["Titanite Demon4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Titanite Demon" in enemy.name])) * 0.664201183431952 * 2.611328125 # Mean reach and arc attack mods for Titanite Demon
    if "Gargoyle" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Gargoyle1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name])) * 0.4982829670125 * 1 # Mean reach and arc attack mods for Gargoyle
        bleedProc["Gargoyle2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name])) * 0.4982829670125 * 1.34375 # Mean reach and arc attack mods for Gargoyle
        bleedProc["Gargoyle3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name])) * 0.4982829670125 * 1.8583984375 # Mean reach and arc attack mods for Gargoyle
        bleedProc["Gargoyle4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gargoyle" in enemy.name])) * 0.4982829670125 * 2.5439453125 # Mean reach and arc attack mods for Gargoyle
    if "Smelter Demon" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Smelter Demon1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name])) * 0.637292194967258 * 1 # Mean reach and arc attack mods for Smelter Demon
        bleedProc["Smelter Demon2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name])) * 0.637292194967258 * 1.33173076923077 # Mean reach and arc attack mods for Smelter Demon
        bleedProc["Smelter Demon3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name])) * 0.637292194967258 * 1.88792067307692 # Mean reach and arc attack mods for Smelter Demon
        bleedProc["Smelter Demon4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Smelter Demon" in enemy.name])) * 0.637292194967258 * 2.66856971153846 # Mean reach and arc attack mods for Smelter Demon
    if "The Pursuer" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["The Pursuer1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name])) * 0.577422577409091 * 1 # Mean reach and arc attack mods for The Pursuer
        bleedProc["The Pursuer2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name])) * 0.577422577409091 * 1.23863636363636 # Mean reach and arc attack mods for The Pursuer
        bleedProc["The Pursuer3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name])) * 0.577422577409091 * 1.60085227272727 # Mean reach and arc attack mods for The Pursuer
        bleedProc["The Pursuer4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Pursuer" in enemy.name])) * 0.577422577409091 * 2.08664772727273 # Mean reach and arc attack mods for The Pursuer
    if "Crossbreed Priscilla" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Crossbreed Priscilla1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.564137785276923 * 1 # Mean reach and arc attack mods for Crossbreed Priscilla
        bleedProc["Crossbreed Priscilla2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.564137785276923 * 1.52884615384615 # Mean reach and arc attack mods for Crossbreed Priscilla
        bleedProc["Crossbreed Priscilla3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.564137785276923 * 2.42427884615385 # Mean reach and arc attack mods for Crossbreed Priscilla
        bleedProc["Crossbreed Priscilla4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.564137785276923 * 3.68629807692308 # Mean reach and arc attack mods for Crossbreed Priscilla
    if "Gravelord Nito" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Gravelord Nito1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name])) * 0.584055367685799 * 1 # Mean reach and arc attack mods for Gravelord Nito
        bleedProc["Gravelord Nito2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name])) * 0.584055367685799 * 1.30288461538462 # Mean reach and arc attack mods for Gravelord Nito
        bleedProc["Gravelord Nito3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name])) * 0.584055367685799 * 1.81039663461538 # Mean reach and arc attack mods for Gravelord Nito
        bleedProc["Gravelord Nito4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gravelord Nito" in enemy.name])) * 0.584055367685799 * 2.52253605769231 # Mean reach and arc attack mods for Gravelord Nito
    if "Great Grey Wolf Sif" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Great Grey Wolf Sif1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name])) * 0.499542124515293 * 1 # Mean reach and arc attack mods for Great Grey Wolf Sif
        bleedProc["Great Grey Wolf Sif2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name])) * 0.499542124515293 * 1.42857142857143 # Mean reach and arc attack mods for Great Grey Wolf Sif
        bleedProc["Great Grey Wolf Sif3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name])) * 0.499542124515293 * 2.1015625 # Mean reach and arc attack mods for Great Grey Wolf Sif
        bleedProc["Great Grey Wolf Sif4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Great Grey Wolf Sif" in enemy.name])) * 0.499542124515293 * 3.01897321428571 # Mean reach and arc attack mods for Great Grey Wolf Sif
    if "Ornstein & Smough" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Ornstein & Smough1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name])) * 0.721657509146666 * 1 # Mean reach and arc attack mods for Ornstein & Smough
        bleedProc["Ornstein & Smough2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name])) * 0.721657509146666 * 1.1 # Mean reach and arc attack mods for Ornstein & Smough
        bleedProc["Ornstein & Smough3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name])) * 0.721657509146666 * 1.2625 # Mean reach and arc attack mods for Ornstein & Smough
        bleedProc["Ornstein & Smough4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Ornstein & Smough" in enemy.name])) * 0.721657509146666 * 1.4875 # Mean reach and arc attack mods for Ornstein & Smough
    if "Dancer of the Boreal Valley" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Dancer of the Boreal Valley1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name])) * 0.751391236958678 * 1 # Mean reach and arc attack mods for Dancer of the Boreal Valley
        bleedProc["Dancer of the Boreal Valley2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name])) * 0.751391236958678 * 1.27884615384615 # Mean reach and arc attack mods for Dancer of the Boreal Valley
        bleedProc["Dancer of the Boreal Valley3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name])) * 0.751391236958678 * 1.69951923076923 # Mean reach and arc attack mods for Dancer of the Boreal Valley
        bleedProc["Dancer of the Boreal Valley4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Dancer of the Boreal Valley" in enemy.name])) * 0.751391236958678 * 2.26201923076923 # Mean reach and arc attack mods for Dancer of the Boreal Valley
    if "Artorias" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Artorias1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name])) * 0.597421808945562 * 1 # Mean reach and arc attack mods for Artorias
        bleedProc["Artorias2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name])) * 0.597421808945562 * 1.32532051282051 # Mean reach and arc attack mods for Artorias
        bleedProc["Artorias3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name])) * 0.597421808945562 * 1.83804086538462 # Mean reach and arc attack mods for Artorias
        bleedProc["Artorias4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Artorias" in enemy.name])) * 0.597421808945562 * 2.53816105769231 # Mean reach and arc attack mods for Artorias
    if "Sir Alonne" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Sir Alonne1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name])) * 0.665962242867554 * 1 # Mean reach and arc attack mods for Sir Alonne
        bleedProc["Sir Alonne2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name])) * 0.665962242867554 * 1.23557692307692 # Mean reach and arc attack mods for Sir Alonne
        bleedProc["Sir Alonne3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name])) * 0.665962242867554 * 1.56159855769231 # Mean reach and arc attack mods for Sir Alonne
        bleedProc["Sir Alonne4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Sir Alonne" in enemy.name])) * 0.665962242867554 * 1.97806490384615 # Mean reach and arc attack mods for Sir Alonne
    if "Stray Demon" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Stray Demon1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name])) * 0.401025641025641 * 1 # Mean reach and arc attack mods for Stray Demon
        bleedProc["Stray Demon2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name])) * 0.401025641025641 * 1.26098901098901 # Mean reach and arc attack mods for Stray Demon
        bleedProc["Stray Demon3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name])) * 0.401025641025641 * 1.65296310832025 # Mean reach and arc attack mods for Stray Demon
        bleedProc["Stray Demon4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Stray Demon" in enemy.name])) * 0.401025641025641 * 2.17592229199372 # Mean reach and arc attack mods for Stray Demon
    if "Manus, Father of the Abyss" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Manus, Father of the Abyss1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name])) * 0.565866666666667 * 1 # Mean reach and arc attack mods for Manus, Father of the Abyss
        bleedProc["Manus, Father of the Abyss2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name])) * 0.565866666666667 * 1.27295918367347 # Mean reach and arc attack mods for Manus, Father of the Abyss
        bleedProc["Manus, Father of the Abyss3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name])) * 0.565866666666667 * 1.68923104956268 # Mean reach and arc attack mods for Manus, Father of the Abyss
        bleedProc["Manus, Father of the Abyss4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Manus, Father of the Abyss" in enemy.name])) * 0.565866666666667 * 2.24881559766764 # Mean reach and arc attack mods for Manus, Father of the Abyss
    if "The Four Kings" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["The Four Kings1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name])) * 0.66208 * 1 # Mean reach and arc attack mods for The Four Kings
        bleedProc["The Four Kings2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name])) * 0.66208 * 1.15 # Mean reach and arc attack mods for The Four Kings
        bleedProc["The Four Kings3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name])) * 0.66208 * 1.34630102040816 # Mean reach and arc attack mods for The Four Kings
        bleedProc["The Four Kings4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Four Kings" in enemy.name])) * 0.66208 * 1.58890306122449 # Mean reach and arc attack mods for The Four Kings
    if "The Last Giant" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["The Last Giant1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name])) * 0.468866666666667 * 1 # Mean reach and arc attack mods for The Last Giant
        bleedProc["The Last Giant2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name])) * 0.468866666666667 * 1.19866071428571 # Mean reach and arc attack mods for The Last Giant
        bleedProc["The Last Giant3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name])) * 0.468866666666667 * 1.47249681122449 # Mean reach and arc attack mods for The Last Giant
        bleedProc["The Last Giant4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "The Last Giant" in enemy.name])) * 0.468866666666667 * 1.82150829081633 # Mean reach and arc attack mods for The Last Giant
    if "Guardian Dragon" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Guardian Dragon1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name])) * 0.488581818181818 * 1 # Mean reach and arc attack mods for Guardian Dragon
        bleedProc["Guardian Dragon2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name])) * 0.488581818181818 * 1.19155844155844 # Mean reach and arc attack mods for Guardian Dragon
        bleedProc["Guardian Dragon3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name])) * 0.488581818181818 * 1.43378942486085 # Mean reach and arc attack mods for Guardian Dragon
        bleedProc["Guardian Dragon4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Guardian Dragon" in enemy.name])) * 0.488581818181818 * 1.72669294990723 # Mean reach and arc attack mods for Guardian Dragon
    if "Gaping Dragon" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Gaping Dragon1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name])) * 0.598047179487179 * 1 # Mean reach and arc attack mods for Gaping Dragon
        bleedProc["Gaping Dragon2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name])) * 0.598047179487179 * 1.21868131868131 # Mean reach and arc attack mods for Gaping Dragon
        bleedProc["Gaping Dragon3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name])) * 0.598047179487179 * 1.50392464678179 # Mean reach and arc attack mods for Gaping Dragon
        bleedProc["Gaping Dragon4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Gaping Dragon" in enemy.name])) * 0.598047179487179 * 1.85572998430141 # Mean reach and arc attack mods for Gaping Dragon
    if "Vordt of the Boreal Valley" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Vordt of the Boreal Valley1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name])) * 0.389319887955182 * 1 # Mean reach and arc attack mods for Vordt of the Boreal Valley
        bleedProc["Vordt of the Boreal Valley2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name])) * 0.389319887955182 * 1.1218487394958 # Mean reach and arc attack mods for Vordt of the Boreal Valley
        bleedProc["Vordt of the Boreal Valley3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name])) * 0.389319887955182 * 1.29591836734694 # Mean reach and arc attack mods for Vordt of the Boreal Valley
        bleedProc["Vordt of the Boreal Valley4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Vordt of the Boreal Valley" in enemy.name])) * 0.389319887955182 * 1.52220888355342 # Mean reach and arc attack mods for Vordt of the Boreal Valley
    if "Black Dragon Kalameet" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Black Dragon Kalameet1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name])) * 0.483323076923077 * 1 # Mean reach and arc attack mods for Black Dragon Kalameet
        bleedProc["Black Dragon Kalameet2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name])) * 0.483323076923077 * 1.26098901098901 # Mean reach and arc attack mods for Black Dragon Kalameet
        bleedProc["Black Dragon Kalameet3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name])) * 0.483323076923077 * 1.61680729984301 # Mean reach and arc attack mods for Black Dragon Kalameet
        bleedProc["Black Dragon Kalameet4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Black Dragon Kalameet" in enemy.name])) * 0.483323076923077 * 2.06745486656201 # Mean reach and arc attack mods for Black Dragon Kalameet
    if "Old Iron King" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Old Iron King1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name])) * 0.516959064327485 * 1 # Mean reach and arc attack mods for Old Iron King
        bleedProc["Old Iron King2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name])) * 0.516959064327485 * 1.24841269840793 # Mean reach and arc attack mods for Old Iron King
        bleedProc["Old Iron King3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name])) * 0.516959064327485 * 1.58441987905037 # Mean reach and arc attack mods for Old Iron King
        bleedProc["Old Iron King4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Old Iron King" in enemy.name])) * 0.516959064327485 * 2.00802154192732 # Mean reach and arc attack mods for Old Iron King
    if "Executioner's Chariot" in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        bleedProc["Executioner's Chariot1"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name])) * 0.508857346356197 * 1 # Mean reach and arc attack mods for Executioner's Chariot
        bleedProc["Executioner's Chariot2"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name])) * 0.508857346356197 * 1.27197802197802 # Mean reach and arc attack mods for Executioner's Chariot
        bleedProc["Executioner's Chariot3"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name])) * 0.508857346356197 * 1.68730376766091 # Mean reach and arc attack mods for Executioner's Chariot
        bleedProc["Executioner's Chariot4"] = (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if "Executioner's Chariot" in enemy.name])) * 0.508857346356197 * 2.24597723704866 # Mean reach and arc attack mods for Executioner's Chariot

    for enemy in enemies:
        while not path.isfile(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json"):
            sleep(60)
        with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json", "r") as eLoad:
            e = load(eLoad)
        enemyName = enemy.name[:enemy.name.index(" -")] if " -" in enemy.name else "regular"
        enemy.damageDone1[tier] += enemy.bleedDamage1[tier] * bleedProc[enemyName[:enemyName.index(" -") if " -" in enemyName else enemyName.index(" (") if " (" in enemyName else len(enemyName)] + ("1" if "boss" in enemy.enemyType else "")]
        enemy.damageDone2[tier] += enemy.bleedDamage2[tier] * bleedProc[enemyName[:enemyName.index(" -") if " -" in enemyName else enemyName.index(" (") if " (" in enemyName else len(enemyName)] + ("2" if "boss" in enemy.enemyType else "")]
        enemy.damageDone3[tier] += enemy.bleedDamage3[tier] * bleedProc[enemyName[:enemyName.index(" -") if " -" in enemyName else enemyName.index(" (") if " (" in enemyName else len(enemyName)] + ("3" if "boss" in enemy.enemyType else "")]
        enemy.damageDone4[tier] += enemy.bleedDamage4[tier] * bleedProc[enemyName[:enemyName.index(" -") if " -" in enemyName else enemyName.index(" (") if " (" in enemyName else len(enemyName)] + ("4" if "boss" in enemy.enemyType else "")]
        for t in range(1, 4):
            if t == tier:
                continue
            enemy.totalAttacks[t] = e["totalAttacks"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.damagingAttacks[t] = e["damagingAttacks"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.damageDone1[t] = e["damageDone"]["1"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.damageDone2[t] = e["damageDone"]["2"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.damageDone3[t] = e["damageDone"]["3"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.damageDone4[t] = e["damageDone"]["4"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.bleedDamage1[t] = e["bleedDamage"]["1"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.bleedDamage2[t] = e["bleedDamage"]["2"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.bleedDamage3[t] = e["bleedDamage"]["3"][str(t)] / (2 if enemy.enemyType == "regular" else 1)
            enemy.bleedDamage4[t] = e["bleedDamage"]["4"][str(t)] / (2 if enemy.enemyType == "regular" else 1)

        with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json", "w") as enemyFile:
                dump({"deaths": e["deaths"], "totalAttacks": enemy.totalAttacks, "damagingAttacks": enemy.damagingAttacks, "damageDone": {1: enemy.damageDone1, 2: enemy.damageDone2, 3: enemy.damageDone3, 4: enemy.damageDone4}, "bleedDamage": {1: enemy.bleedDamage1, 2: enemy.bleedDamage2, 3: enemy.bleedDamage3, 4: enemy.bleedDamage4}}, enemyFile)

except Exception as ex:
    input(ex)
    raise
