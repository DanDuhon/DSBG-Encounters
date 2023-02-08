from itertools import product
from json import load, dump
from os import path, listdir
from random import shuffle

from attacks import attacks
from enemies import enemies


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
    0: 0.07692307692307693,
    1: 0.44970414201183434,
    2: 0.8224852071005917,
    3: 0.9763313609467456,
    4: 1
}

# This will be used to help calculate expected bleed damage from
# potential bleed damage.  Since any enemy can proc bleed once it
# has been applied, one piece of the puzzle we need is how often
# we can expect any enemy to be able to make an attack.
reachSum = 0
reachDiv = 0
for enemy in enemies:
    for _ in range(enemy.numberOfModels):
        for i in range(len(enemy.attacks)):
            reachSum += reachMod[enemy.move[i] + enemy.attackRange[i]]
            reachDiv += 1
meanReachMod = reachSum / reachDiv

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

# Calculate enemy deaths.
for enemy in enemies:
    enemy.reset()
    currentHealth = enemy.health

    for attack in allAttacks:
        damage = attack[0]
        
        # Bonus damage against hollows.
        if "Hollow" in enemy.name and attack[1] == "hollow":
            damage += 1

        if not attack[2] and not attack[3]:
            damage = max([0, damage - enemy.armor])
        elif attack[2]:
            damage = max([0, damage - enemy.resist])

        # Poison
        if attack[4]:
            damage += 1

        # If the enemy was bleeding and they took damage,
        # add two damage and remove bleed.
        if enemy.bleeding and damage > 0:
            damage += 2
            enemy.bleeding = False

        if attack[5]:
            enemy.bleeding = True

        currentHealth -= damage
        # If the enemy was reduced to 0 or fewer health,
        # add a death, reset their health, and remove bleed
        # if they had it.
        if currentHealth <= 0:
            enemy.deaths += 1
            currentHealth = enemy.health
            enemy.bleeding = False

    with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as enemyFile:
        dump({"deaths": enemy.deaths, "totalAttacks": enemy.totalAttacks, "damagingAttacks": enemy.damagingAttacks, "damageDone": enemy.damageDone, "bleedDamage": enemy.bleedDamage, "loadoutDamage": enemy.loadoutDamage}, enemyFile)

# Calculate enemy damage.
for loadoutFile in listdir(baseFolder + "\\loadouts"):
    print(loadoutFile)
    
    with open(path.join(baseFolder + "\\loadouts", loadoutFile)) as lf:
        loadouts = load(lf)
    
    loadoutsLen = len(loadouts)

    for enemy in enemies:
        totalAttacks = enemy.totalAttacks
        damagingAttacks = enemy.damagingAttacks
        bleedDamage = enemy.bleedDamage
        for l, loadoutKey in enumerate(loadouts, 1):
            block = loadouts[loadoutKey]["expected damage block"]
            resist = loadouts[loadoutKey]["expected damage resist"]
            dodge = loadouts[loadoutKey]["dodge mod"]
            immunities = loadouts[loadoutKey]["immunities"]

            damageDone = []
            # If we've already seen a loadout that has the same defensive
            # stats as this one, go get the results from that loadout
            # rather than calculating it over again.
            if str([block, resist, dodge, immunities]) in enemy.loadoutDamage:
                totalAttacks = enemy.loadoutDamage[str([block, resist, dodge, immunities])][0]
                damagingAttacks = enemy.loadoutDamage[str([block, resist, dodge, immunities])][1]
                damageDone = [d for d in enemy.loadoutDamage[str([block, resist, dodge, immunities])][2]]
                bleedDamage = enemy.loadoutDamage[str([block, resist, dodge, immunities])][3]
            else:
                # For each enemy attack, calculate the expected
                # damage the enemy would do to this loadout.
                # Everything gets multiplied by two decimals.
                # One represents the reach concept - how likely
                # the enemy is to be in range to attack at all.
                # The second represents character dodge - how
                # likely the attack is to be dodged.
                for i in range(len(enemy.attacks)):
                    totalAttacks += 1

                    poison = (1 if enemy.attackEffect and "poison" in enemy.attackEffect[i] and "poison" not in loadouts[loadoutKey]["immunities"] else 0
                        * reachMod[enemy.move[i] + enemy.attackRange[i]]
                        * dodge[str(enemy.dodge)])

                    bleedDamage += (2 if enemy.attackEffect and "bleed" in enemy.attackEffect[i] and "bleed" not in loadouts[loadoutKey]["immunities"] else 0
                        * reachMod[enemy.move[i] + enemy.attackRange[i]]
                        * dodge[str(enemy.dodge)])
                    
                    expectedDamage = (reachMod[enemy.move[i] + enemy.attackRange[i]]
                        * block[str(enemy.dodge)][str(enemy.attacks[i])] if enemy.attackType[i] == "physical" else resist[str(enemy.dodge)][str(enemy.attacks[i])]) + poison

                    damagingAttacks += dodge[str(enemy.dodge)]
                        
                    damageDone.append(expectedDamage)

                # Add this loadouts results to the dictionary
                # so if we come across another loadout with the
                # same defensive stats we can just look it up
                # rather than calculate it over again.
                enemy.loadoutDamage[str([block, resist, dodge, immunities])] = (totalAttacks, damagingAttacks, damageDone, bleedDamage)

            enemy.totalAttacks += totalAttacks
            enemy.damagingAttacks += damagingAttacks
            enemy.damageDone += sum([d for d in damageDone])
            enemy.bleedDamage += bleedDamage

        with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as enemyFile:
            dump({"deaths": enemy.deaths, "totalAttacks": enemy.totalAttacks, "damagingAttacks": enemy.damagingAttacks, "damageDone": enemy.damageDone, "bleedDamage": enemy.bleedDamage, "loadoutDamage": enemy.loadoutDamage}, enemyFile)
            
    # (Damaging attacks / total attacks) * average enemy reach
    # This is the % that bleed will be procced.  The attack has
    # to be made (reach), and then do damage.
    bleedProc = (sum([enemy.damagingAttacks * enemy.numberOfModels for enemy in enemies]) / sum([enemy.totalAttacks * enemy.numberOfModels for enemy in enemies])) * meanReachMod

    for enemy in enemies:
        enemy.damageDone += enemy.bleedDamage * bleedProc
        with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as enemyFile:
            dump({"deaths": enemy.deaths, "totalAttacks": enemy.totalAttacks, "damagingAttacks": enemy.damagingAttacks, "damageDone": enemy.damageDone, "bleedDamage": enemy.bleedDamage, "loadoutDamage": enemy.loadoutDamage}, enemyFile)

for enemy in enemies:
    print(enemy.name + "_" + str(enemy.deaths) + "_" + str(enemy.damageDone))
