from json import load, dump
from os import path
from enemies import enemies
from loadouts import loadouts
from itertools import product


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
reachSum = 0
reachDiv = 0
for enemy in enemies:
    if enemy.enemyType == "regular":
        for _ in range(enemy.numberOfModels):
            for i in range(len(enemy.attacks)):
                reachSum += reachMod[enemy.enemyType][max([0, min([4, sum(enemy.move[:i+1]) + sum(enemy.attackRange[:i+1]) - (1 if enemy.windup else 0)])])]
                reachDiv += 1
meanReachMod = reachSum / reachDiv

# Cheating way of doing this faster, just doing it in simultaneous batches.
# Need to update a and b then run the script.
# Stitch it together afterwards.
# Current loadout count: 1031778
a=900000
b=1100000
try:
    # Calculate enemy offense.
    print("Enemy offense")
    for x, loadout in enumerate(loadouts):
        if x < a or x > b:
            continue
        if x % 10000 == 0 and x > a:
            print("\t" + str(((x-a)/(b-a))*100)[:6] + "%")
        for enemy in enemies:
            if enemy.skip:
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
            
            # For each enemy attack, calculate the expected
            # damage the enemy would do to this loadout.
            # Everything gets multiplied by two decimals.
            # One represents the reach concept - how likely
            # the enemy is to be in range to attack at all.
            # The second represents character dodge - how
            # likely the attack is to be dodged.
            for i in range(len(enemy.attacks)):
                totalAttacks += 1
                reach = reachMod["Executioner's Chariot" if "Executioner's Chariot" in enemy.name else "Old Iron King" if "Old Iron King" in enemy.name else enemy.enemyType][max([0, min([4, sum(enemy.move[:i+1]) + sum(enemy.attackRange[:i+1]) - (1 if enemy.windup else 0)])])]
                if type(enemy.dodge) == int:
                    dodge = 1 if loadout["dodge"] == 0 else (1 - (sum([1 for do in product(*loadout["dodge"]) if sum(do) >= enemy.dodge]) / len(list(product(*loadout["dodge"])))))
                else:
                    dodge = 1 if loadout["dodge"] == 0 else (1 - (sum([1 for do in product(*loadout["dodge"]) if sum(do) >= enemy.dodge[i]]) / len(list(product(*loadout["dodge"])))))

                # This is the effect of Calamity, see below for more details.
                if "Black Dragon Kalameet" in enemy.name:
                    dodge -= 0.1528822055
                    
                damagingAttacks += dodge

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
                elif "Executioner's Chariot" in enemy.name and len(list(product(*loadout["blockRoll" if enemy.attackType[i] == "physical" else "resistRoll"]))) > 0:
                    addedDamage = (sum([1 for do in product(*loadout["blockRoll" if enemy.attackType[i] == "physical" else "resistRoll"]) if sum(do) >= enemy.attacks[i]]) / len(list(product(*loadout["blockRoll" if enemy.attackType[i] == "physical" else "resistRoll"]))))
                else:
                    addedDamage = 0
                    

                poison1 = ((1 if enemy.attackEffect and "poison" in enemy.attackEffect[i] and "poison" not in loadout["immunities"] else 0)
                    * reach
                    * dodge)
                poison2 = ((1 if enemy.attackEffect and "poison" in enemy.attackEffect[i] and "poison" not in loadout["immunities"] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[2] if enemy.nodesAttacked[i] > 0 else 1))
                poison3 = ((1 if enemy.attackEffect and "poison" in enemy.attackEffect[i] and "poison" not in loadout["immunities"] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[3] if enemy.nodesAttacked[i] > 0 else 1))
                poison4 = ((1 if enemy.attackEffect and "poison" in enemy.attackEffect[i] and "poison" not in loadout["immunities"] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[4] if enemy.nodesAttacked[i] > 0 else 1))

                bleedDamage1 += ((2 if enemy.attackEffect and "bleed" in enemy.attackEffect[i] and "bleed" not in loadout["immunities"] else 0)
                    * reach
                    * dodge)
                bleedDamage2 += ((2 if enemy.attackEffect and "bleed" in enemy.attackEffect[i] and "bleed" not in loadout["immunities"] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[2] if enemy.nodesAttacked[i] > 0 else 1))
                bleedDamage3 += ((2 if enemy.attackEffect and "bleed" in enemy.attackEffect[i] and "bleed" not in loadout["immunities"] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[3] if enemy.nodesAttacked[i] > 0 else 1))
                bleedDamage4 += ((2 if enemy.attackEffect and "bleed" in enemy.attackEffect[i] and "bleed" not in loadout["immunities"] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[4] if enemy.nodesAttacked[i] > 0 else 1))
                
                expectedDamage1 = (max([0, enemy.attacks[i] - (loadout["block"] if enemy.attackType[i] == "physical" else loadout["resist"]) + addedDamage])
                    * reach
                    * dodge
                    ) + poison1
                expectedDamage2 = (max([0, enemy.attacks[i] - (loadout["block"] if enemy.attackType[i] == "physical" else loadout["resist"]) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[2] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison2
                expectedDamage3 = (max([0, enemy.attacks[i] - (loadout["block"] if enemy.attackType[i] == "physical" else loadout["resist"]) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[3] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison3
                expectedDamage4 = (max([0, enemy.attacks[i] - (loadout["block"] if enemy.attackType[i] == "physical" else loadout["resist"]) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False)[4] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison4

                damagingAttacks += dodge
                    
                damageDone1.append(expectedDamage1)
                damageDone2.append(expectedDamage2)
                damageDone3.append(expectedDamage3)
                damageDone4.append(expectedDamage4)

            enemy.totalAttacks += totalAttacks
            enemy.damagingAttacks += damagingAttacks
            enemy.damageDone1 += sum([d for d in damageDone1])
            enemy.damageDone2 += sum([d for d in damageDone2])
            enemy.damageDone3 += sum([d for d in damageDone3])
            enemy.damageDone4 += sum([d for d in damageDone4])
            enemy.bleedDamage1 += bleedDamage1
            enemy.bleedDamage2 += bleedDamage2
            enemy.bleedDamage3 += bleedDamage3
            enemy.bleedDamage4 += bleedDamage4
                
    # (Damaging attacks / total attacks) * average enemy reach
    # This is the % that bleed will be procced.  The attack has
    # to be made (reach), and then do damage.
    # Only regular enemies count for this.
    bleedProc = {
        "regular": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if enemy.enemyType == "regular"]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if enemy.enemyType == "regular"])) * meanReachMod,
        "Kirk, Knight of Thorns": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Kirk, Knight of Thorns" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Kirk, Knight of Thorns" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod,
        "Longfinger Kirk": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Longfinger Kirk" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Longfinger Kirk" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod,
        "Marvelous Chester": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Marvelous Chester" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Marvelous Chester" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod,
        "Xanthous King Jeremiah": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Xanthous King Jeremiah" in enemy.name or enemy.enemyType == "regular"]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Xanthous King Jeremiah" in enemy.name or enemy.enemyType == "regular"])) * meanReachMod,
        "Crossbreed Priscilla1": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.5408653846 * 1, # Mean reach and arc attack mods for Priscilla only
        "Crossbreed Priscilla2": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.5408653846 * 1.596153846, # Mean reach and arc attack mods for Priscilla only
        "Crossbreed Priscilla3": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.5408653846 * 2.59375, # Mean reach and arc attack mods for Priscilla only
        "Crossbreed Priscilla4": (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies if "Crossbreed Priscilla" in enemy.name])) * 0.5408653846 * 3.992788462 # Mean reach and arc attack mods for Priscilla only
        }

    for enemy in enemies:
        with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "r") as eLoad:
            e = load(eLoad)
        enemy.damageDone1 += enemy.bleedDamage1 * bleedProc["Kirk, Knight of Thorns" if "Kirk, Knight of Thorns" in enemy.name else "Longfinger Kirk" if "Longfinger Kirk" in enemy.name else "Marvelous Chester" if "Marvelous Chester" in enemy.name else "Xanthous King Jeremiah" if "Xanthous King Jeremiah" in enemy.name else "Crossbreed Priscilla1" if "Crossbreed Priscilla" in enemy.name else "regular"]
        enemy.damageDone2 += enemy.bleedDamage2 * bleedProc["Kirk, Knight of Thorns" if "Kirk, Knight of Thorns" in enemy.name else "Longfinger Kirk" if "Longfinger Kirk" in enemy.name else "Marvelous Chester" if "Marvelous Chester" in enemy.name else "Xanthous King Jeremiah" if "Xanthous King Jeremiah" in enemy.name else "Crossbreed Priscilla2" if "Crossbreed Priscilla" in enemy.name else "regular"]
        enemy.damageDone3 += enemy.bleedDamage3 * bleedProc["Kirk, Knight of Thorns" if "Kirk, Knight of Thorns" in enemy.name else "Longfinger Kirk" if "Longfinger Kirk" in enemy.name else "Marvelous Chester" if "Marvelous Chester" in enemy.name else "Xanthous King Jeremiah" if "Xanthous King Jeremiah" in enemy.name else "Crossbreed Priscilla3" if "Crossbreed Priscilla" in enemy.name else "regular"]
        enemy.damageDone4 += enemy.bleedDamage4 * bleedProc["Kirk, Knight of Thorns" if "Kirk, Knight of Thorns" in enemy.name else "Longfinger Kirk" if "Longfinger Kirk" in enemy.name else "Marvelous Chester" if "Marvelous Chester" in enemy.name else "Xanthous King Jeremiah" if "Xanthous King Jeremiah" in enemy.name else "Crossbreed Priscilla4" if "Crossbreed Priscilla" in enemy.name else "regular"]
        with open(baseFolder + "\\enemies\\" + enemy.name + str(a)+".json", "w") as enemyFile:
            dump({"deaths": e["deaths"], "totalAttacks": enemy.totalAttacks, "damagingAttacks": enemy.damagingAttacks, "damageDone": {1: enemy.damageDone1, 2: enemy.damageDone2, 3: enemy.damageDone3, 4: enemy.damageDone4}, "bleedDamage": {1: enemy.bleedDamage1, 2: enemy.bleedDamage2, 3: enemy.bleedDamage3, 4: enemy.bleedDamage4}}, enemyFile)

except Exception as ex:
    input(ex)
    raise
