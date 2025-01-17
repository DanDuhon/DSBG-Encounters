from json import load, dump
from os import path
from enemies import enemies
from loadouts import expectedBlock, expectedResist, loadoutLookup
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


def arc_damage_mod(nodesAttacked, megaBoss, oldIronKing, chariot):
    nodes = 19 if oldIronKing else 27 if chariot else 28 if megaBoss else 16
    return {
        1: 1,
        2: 1 + (nodesAttacked / nodes),
        3: 1 + (((nodesAttacked / nodes) * 2) + ((nodesAttacked / nodes) * (nodesAttacked / nodes))),
        4: 1 + (((nodesAttacked / nodes) * 3) + (((nodesAttacked / nodes) * (nodesAttacked / nodes)) * 3))
        }


def add_to_bleed_proc_dict_reg(name):
    if name == "regular" and "regular" in set([enemy.enemyType for enemy in enemies]):
        print(name)
        if name not in bleedProc:
            bleedProc[name] = {}
        l = len(set([enemy.comboSet for enemy in enemies if enemy.enemyType == "regular"]))
        for x, c in enumerate(list(set([enemy.comboSet for enemy in enemies if enemy.enemyType == "regular"]))):
            print(str((x/l)*100)[:6] + "%", end="\r")
            if c not in bleedProc[name]:
                bleedProc[name][c] = 0
            if sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if enemy.comboSet == c]):
                bleedProc[name][c] += (sum([enemy.damagingAttacks[tier] * enemy.numberOfModels for enemy in enemies if enemy.comboSet == c]) / sum([enemy.totalAttacks[tier] * enemy.numberOfModels for enemy in enemies if enemy.comboSet == c])) * meanReachMod


def add_to_bleed_proc_dict_invader(name):
    if name in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        print(name)
        if name not in bleedProc:
            bleedProc[name] = {}
        l = len(set([enemy.comboSet for enemy in enemies if name in enemy.name]))
        for x, c in enumerate(list(set([enemy.comboSet for enemy in enemies if name in enemy.name]))):
            print(str((x/l)*100)[:6] + "%", end="\r")
            if c not in bleedProc[name]:
                bleedProc[name][c] = 0
            if sum([enemy.totalAttacks[tier] for enemy in enemies if enemy.comboSet == c]):
                bleedProc[name][c] += (sum([enemy.damagingAttacks[tier] for enemy in enemies if enemy.comboSet == c]) / sum([enemy.totalAttacks[tier] for enemy in enemies if enemy.comboSet == c])) * meanReachMod


def add_to_bleed_proc_dict_boss(name, reachMod, arcMod1, arcMod2, arcMod3, arcMod4):
    if name in set([enemy.name[:enemy.name.index(" -") if " -" in enemy.name else len(enemy.name)] for enemy in enemies]):
        print(name)
        if name + "1" not in bleedProc:
            bleedProc[name + "1"] = {}
            bleedProc[name + "2"] = {}
            bleedProc[name + "3"] = {}
            bleedProc[name + "4"] = {}
        for x, c in enumerate(list(set([enemy.comboSet for enemy in enemies]))):
            print(str((x/len(set([enemy.comboSet for enemy in enemies])))*100)[:6] + "%", end="\r")
            if c not in bleedProc[name + "1"]:
                bleedProc[name + "1"][c] = 0
                bleedProc[name + "2"][c] = 0
                bleedProc[name + "3"][c] = 0
                bleedProc[name + "4"][c] = 0
            if sum([enemy.totalAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c]):
                bleedProc[name + "1"][c] += (sum([enemy.damagingAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c]) / sum([enemy.totalAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c])) * reachMod * arcMod1
                bleedProc[name + "2"][c] += (sum([enemy.damagingAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c]) / sum([enemy.totalAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c])) * reachMod * arcMod2
                bleedProc[name + "3"][c] += (sum([enemy.damagingAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c]) / sum([enemy.totalAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c])) * reachMod * arcMod3
                bleedProc[name + "4"][c] += (sum([enemy.damagingAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c]) / sum([enemy.totalAttacks[tier] for enemy in enemies if name in enemy.name and enemy.comboSet == c])) * reachMod * arcMod4


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
    print(" ".join(list(set([enemy.name[:enemy.name.index(" - ") if " - " in enemy.name else enemy.name.index(" (") if " (" in enemy.name else len(enemy.name)] for enemy in enemies]))) + " offense tier " + str(tier))
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
            poisonAdded2 = False
            
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
                    dodge += 0.1528822055

                if dodge > 1:
                    dodge = 1

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
                        * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[2] if enemy.nodesAttacked[i] > 0 else 1))
                    poison3 = (((2 if enemy.id else 1) if enemy.attackEffect and "poison" in enemy.attackEffect[i] else 0)
                        * reach
                        * dodge
                        * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                        * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[3] if enemy.nodesAttacked[i] > 0 else 1))
                    poison4 = (((2 if enemy.id else 1) if enemy.attackEffect and "poison" in enemy.attackEffect[i] else 0)
                        * reach
                        * dodge
                        * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                        * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[4] if enemy.nodesAttacked[i] > 0 else 1))
                    
                    if poison1 > 0.0 or poison2 or poison3 > 0.0 or poison4 > 0.0:
                        poisonAdded = True

                bleedDamage1 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge)
                bleedDamage2 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[2] if enemy.nodesAttacked[i] > 0 else 1))
                bleedDamage3 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[3] if enemy.nodesAttacked[i] > 0 else 1))
                bleedDamage4 += multiplier * (((4 if enemy.id else 2) if enemy.attackEffect and "bleed" in enemy.attackEffect[i] else 0)
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[4] if enemy.nodesAttacked[i] > 0 else 1))
                
                expectedDamage1 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    ) + poison1) * multiplier
                expectedDamage2 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[2] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[2] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison2) * multiplier
                expectedDamage3 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[3] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[3] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison3) * multiplier
                expectedDamage4 = ((max([0, enemy.attacks[i] - (block if enemy.attackType[i] == "physical" else resist) + addedDamage])
                    * reach
                    * dodge
                    * (nodeAttackMod[4] if enemy.nodeAttack[i] and enemy.nodesAttacked[i] == 0 else 1)
                    * (arc_damage_mod(enemy.nodesAttacked[i], True if enemy.enemyType == "mega boss" else False, True if "Old Iron King" in enemy.name else False, True if "Executioner Chariot" in enemy.name else False)[4] if enemy.nodesAttacked[i] > 0 else 1)
                    ) + poison4) * multiplier
                
                # Attacks that aren't dodged and aren't fully blocked/resisted and don't include poison (or poison has already been accounted for).
                m = 1
                if enemy.attacks[i] > 0 and "Executioner's Chariot" not in enemy.name and (poisonAdded2 or (len(enemy.attackEffect) - 1 >= i and "poison" not in enemy.attackEffect[i])):
                    m = (expectedBlock if enemy.attackType[i] == "physical" else expectedResist)[int(max([0, enemy.attacks[i]]))][tier]
                damagingAttacks += (dodge * m) * multiplier
                
                if poison1 > 0.0 or poison2 or poison3 > 0.0 or poison4 > 0.0:
                    poisonAdded2 = True
                    
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
    add_to_bleed_proc_dict_reg("regular")
    add_to_bleed_proc_dict_invader("Armorer Dennis")
    add_to_bleed_proc_dict_invader("Fencer Sharron")
    add_to_bleed_proc_dict_invader("Invader Brylex")
    add_to_bleed_proc_dict_invader("Kirk, Knight of Thorns")
    add_to_bleed_proc_dict_invader("Longfinger Kirk")
    add_to_bleed_proc_dict_invader("Maldron the Assassin")
    add_to_bleed_proc_dict_invader("Maneater Mildred")
    add_to_bleed_proc_dict_invader("Marvelous Chester")
    add_to_bleed_proc_dict_invader("Melinda the Butcher")
    add_to_bleed_proc_dict_invader("Oliver the Collector")
    add_to_bleed_proc_dict_invader("Paladin Leeroy")
    add_to_bleed_proc_dict_invader("Xanthous King Jeremiah")
    add_to_bleed_proc_dict_invader("Hungry Mimic")
    add_to_bleed_proc_dict_invader("Voracious Mimic")
    add_to_bleed_proc_dict_boss("Old Dragonslayer", 0.845044378698225, 1, 1.296875, 1.794921875, 2.494140625)
    add_to_bleed_proc_dict_boss("Asylum Demon", 0.527284681130835, 1, 1.28472222222222, 1.75911458333333, 2.42317708333333)
    add_to_bleed_proc_dict_boss("Boreal Outrider Knight", 0.736316568047337, 1, 1.3515625, 1.88037109375, 2.58642578125)
    add_to_bleed_proc_dict_boss("Winged Knight", 0.854289940828402, 1, 1.4921875, 2.30810546875, 3.44775390625)
    add_to_bleed_proc_dict_boss("Black Knight", 0.831689677843523, 1, 1.24305555555556, 1.63107638888889, 2.1640625)
    add_to_bleed_proc_dict_boss("Heavy Knight", 0.715318869165023, 1, 1.27777777777778, 1.72916666666667, 2.35416666666667)
    add_to_bleed_proc_dict_boss("Titanite Demon", 0.664201183431952, 1, 1.328125, 1.865234375, 2.611328125)
    add_to_bleed_proc_dict_boss("Gargoyle", 0.7153188691650231, 1, 1.34375, 1.8583984375, 2.5439453125)
    add_to_bleed_proc_dict_boss("Smelter Demon", 0.637292194967258, 1, 1.33173076923077, 1.88792067307692, 2.66856971153846)
    add_to_bleed_proc_dict_boss("The Pursuer", 0.577422577409091, 1, 1.23863636363636, 1.60085227272727, 2.08664772727273)
    add_to_bleed_proc_dict_boss("Crossbreed Priscilla", 0.564137785276923, 1, 1.52884615384615, 2.42427884615385, 3.68629807692308)
    add_to_bleed_proc_dict_boss("Gravelord Nito", 0.584055367685799, 1, 1.30288461538462, 1.81039663461538, 2.52253605769231)
    add_to_bleed_proc_dict_boss("Great Grey Wolf Sif", 0.499542124515293, 1, 1.42857142857143, 2.1015625, 3.01897321428571)
    add_to_bleed_proc_dict_boss("Ornstein & Smough", 0.721657509146666, 1, 1.1, 1.2625, 1.4875)
    add_to_bleed_proc_dict_boss("Dancer of the Boreal Valley", 0.751391236958678, 1, 1.27884615384615, 1.69951923076923, 2.26201923076923)
    add_to_bleed_proc_dict_boss("Artorias", 0.597421808945562, 1, 1.32532051282051, 1.83804086538462, 2.53816105769231)
    add_to_bleed_proc_dict_boss("Sir Alonne", 0.665962242867554, 1, 1.23557692307692, 1.56159855769231, 1.97806490384615)
    add_to_bleed_proc_dict_boss("Stray Demon", 0.401025641025641, 1, 1.26098901098901, 1.65296310832025, 2.17592229199372)
    add_to_bleed_proc_dict_boss("Manus, Father of the Abyss", 0.565866666666667, 1, 1.27295918367347, 1.68923104956268, 2.24881559766764)
    add_to_bleed_proc_dict_boss("The Four Kings", 0.66208, 1, 1.15, 1.34630102040816, 1.58890306122449)
    add_to_bleed_proc_dict_boss("The Last Giant", 0.468866666666667, 1, 1.19866071428571, 1.47249681122449, 1.82150829081633)
    add_to_bleed_proc_dict_boss("Guardian Dragon", 0.488581818181818, 1, 1.19155844155844, 1.43378942486085, 1.72669294990723)
    add_to_bleed_proc_dict_boss("Gaping Dragon", 0.598047179487179, 1, 1.21868131868131, 1.50392464678179, 1.85572998430141)
    add_to_bleed_proc_dict_boss("Vordt of the Boreal Valley", 0.389319887955182, 1, 1.1218487394958, 1.29591836734694, 1.52220888355342)
    add_to_bleed_proc_dict_boss("Black Dragon Kalameet", 0.483323076923077, 1, 1.26098901098901, 1.61680729984301, 2.06745486656201)
    add_to_bleed_proc_dict_boss("Old Iron King", 0.516959064327485, 1, 1.24841269840793, 1.58441987905037, 2.00802154192732)
    add_to_bleed_proc_dict_boss("Executioner's Chariot", 0.508857346356197, 1, 1.27197802197802, 1.68730376766091, 2.24597723704866)

    l = len(enemies)
    print("Saving ")
    for i, enemy in enumerate(enemies):
        print(str((i/l)*100)[:6] + "%", end="\r")
        while not path.isfile(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json"):
            print((enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json")
            sleep(60)
        with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json", "r") as eLoad:
            e = load(eLoad)

        enemyName = enemy.name[:enemy.name.index(" -")] if " -" in enemy.name else "regular"
        bleedProcName = enemyName[:enemyName.index(" -") if " -" in enemyName else enemyName.index(" (") if " (" in enemyName else len(enemyName)]

        if "boss" in enemy.enemyType:
            enemy.damageDone1[tier] += enemy.bleedDamage1[tier] * bleedProc[bleedProcName + "1"][enemy.comboSet]
            enemy.damageDone2[tier] += enemy.bleedDamage2[tier] * bleedProc[bleedProcName + "2"][enemy.comboSet]
            enemy.damageDone3[tier] += enemy.bleedDamage3[tier] * bleedProc[bleedProcName + "3"][enemy.comboSet]
            enemy.damageDone4[tier] += enemy.bleedDamage4[tier] * bleedProc[bleedProcName + "4"][enemy.comboSet]
        elif "poison" in enemy.name:
            enemy.damageDone1[tier] += enemy.bleedDamage1[tier]
            enemy.damageDone2[tier] += enemy.bleedDamage2[tier]
            enemy.damageDone3[tier] += enemy.bleedDamage3[tier]
            enemy.damageDone4[tier] += enemy.bleedDamage4[tier]
        else:
            enemy.damageDone1[tier] += enemy.bleedDamage1[tier] * bleedProc[bleedProcName][enemy.comboSet]
            enemy.damageDone2[tier] += enemy.bleedDamage2[tier] * bleedProc[bleedProcName][enemy.comboSet]
            enemy.damageDone3[tier] += enemy.bleedDamage3[tier] * bleedProc[bleedProcName][enemy.comboSet]
            enemy.damageDone4[tier] += enemy.bleedDamage4[tier] * bleedProc[bleedProcName][enemy.comboSet]

        for t in range(1, 4):
            if t == tier:
                continue
            enemy.totalAttacks[t] = e["totalAttacks"][str(t)]
            enemy.damagingAttacks[t] = e["damagingAttacks"][str(t)]
            enemy.damageDone1[t] = e["damageDone"]["1"][str(t)]
            enemy.damageDone2[t] = e["damageDone"]["2"][str(t)]
            enemy.damageDone3[t] = e["damageDone"]["3"][str(t)]
            enemy.damageDone4[t] = e["damageDone"]["4"][str(t)]
            enemy.bleedDamage1[t] = e["bleedDamage"]["1"][str(t)]
            enemy.bleedDamage2[t] = e["bleedDamage"]["2"][str(t)]
            enemy.bleedDamage3[t] = e["bleedDamage"]["3"][str(t)]
            enemy.bleedDamage4[t] = e["bleedDamage"]["4"][str(t)]

        with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" (")] + "\\" if enemy.modified else "") + enemy.name + ".json", "w") as enemyFile:
            dump({"deaths": e["deaths"], "totalAttacks": enemy.totalAttacks, "damagingAttacks": enemy.damagingAttacks, "damageDone": {1: enemy.damageDone1, 2: enemy.damageDone2, 3: enemy.damageDone3, 4: enemy.damageDone4}, "bleedDamage": {1: enemy.bleedDamage1, 2: enemy.bleedDamage2, 3: enemy.bleedDamage3, 4: enemy.bleedDamage4}}, enemyFile)

except Exception as ex:
    print(enemy.attackEffect)
    print(i)
    input(ex)
    raise
