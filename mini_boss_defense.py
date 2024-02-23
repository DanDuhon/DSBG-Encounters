from json import load, dump
from os import path
from enemies import enemies
from attacks import attackTiers, bleedTrigger, blackKnight
from loadouts import dodgeMod, expectedBlock3Plus
from math import ceil


baseFolder = path.dirname(__file__)

maxAttacksTaken = 0
maxStaminaSpent = 0

reachMod = {
    0: 0.07692307692307693,
    1: 0.44970414201183434,
    2: 0.8224852071005917,
    3: 0.9763313609467456,
    4: 1
}

try:
    # Calculate enemy defense.
    # First pass to get how many times to apply each attack.
    for enemy in enemies:
        if enemy.skip:
            continue
        for attack in attackTiers[2]:
            damage = attack.expectedDamage[enemy.resist if attack.magic else enemy.armor]

            if attack.bleed:
                damage += bleedTrigger[2][enemy.resist if attack.magic else enemy.armor]

            if attack.poison:
                damage += 1

            if set(enemy.name.lower().split(" ")) & attack.damageBonus:
                damage += 1

            # Account for boss weak arcs.
            damage += 1.5 * (enemy.weakArcs / 4)

            attack.totalDamage[enemy] = damage

            if damage > 0 and enemy.health / damage > maxAttacksTaken:
                maxAttacksTaken = ceil(enemy.health / damage)

            if damage > 0 and (enemy.health / damage) * attack.staminaCost > maxStaminaSpent:
                maxStaminaSpent = ceil((enemy.health / damage) * attack.staminaCost)

    # Second pass to get the number of deaths the attacks cause.
    print("Defense")
    for i, enemy in enumerate(enemies):
        if i % 50 == 0 and i > 0:
            print("\t" + str((i/len(enemies)*100))[:5] + "%")
        if enemy.skip:
            continue

        extraStaminaSpent = 0
        if any([{"stagger", "frostbite"} & e for e in enemy.attackEffect]):
            # Guess at how often this enemy will land with an attack.
            # Used to modify Stagger and Frostbite.
            nums = []
            den = 1000
            for i, a in enumerate(enemy.attacks[:int(len(enemy.attacks) / (2 if enemy.id else 1))]):
                if a == 0 or not {"stagger", "frostbite"} & enemy.attackEffect[i]:
                    continue
                nums.append(round(reachMod[enemy.move[i] + enemy.attackRange[i]] * den, 0))

            stage = 1
            for n in nums:
                stage = stage * (den - n)
            chance = 1 - (stage / (den ** len(nums)))

            extraStaminaSpent = chance * dodgeMod[2][enemy.dodge[0] if type(enemy.dodge) == list and len(enemy.dodge) == 1 else enemy.dodge]
                

        for attack in attackTiers[2]:
            damage = attack.totalDamage[enemy]
            currentHealth = enemy.health

            if attack.staminaCost > 0:
                staminaSpent = 0
                while staminaSpent < maxStaminaSpent:
                    if "Titanite Demon" in enemy.name:
                        if damage >= 3:
                            damage -= 1

                    currentHealth -= damage

                    if currentHealth <= 0:
                        enemy.deaths[2] += 1
                        currentHealth = enemy.health
                    elif "Heavy Knight" in enemy.name and currentHealth <= 15:
                        currentHealth += 3 * (1/5)

                    staminaSpent += attack.staminaCost + extraStaminaSpent

                    if "Winged Knight" in enemy.name:
                        staminaSpent += expectedBlock3Plus[2]
                    elif "Black Knight" in enemy.name:
                        staminaSpent += blackKnight[2]
                    elif "Heavy Knight" in enemy.name:
                        staminaSpent += dodgeMod[2][enemy.dodge] * (0.8 if currentHealth <= 15 else 1)
                    elif "Gargoyle" in enemy.name and currentHealth <= 12 and not attack.noRange0:
                        staminaSpent += 1/(attack.attackRange + 1) 
            else:
                for _ in range(maxAttacksTaken):
                    currentHealth -= damage
                    if currentHealth <= 0:
                        enemy.deaths[2] += 1
                        currentHealth = enemy.health
                    elif "Heavy Knight" in enemy.name and currentHealth <= 15:
                        currentHealth += 3 * (1/5)

    for enemy in enemies:
        # with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "r") as eLoad:
        #     e = load(eLoad)
        # with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as eDump:
        #     dump({"deaths": enemy.deaths, "totalAttacks": e["totalAttacks"], "damagingAttacks": e["damagingAttacks"], "damageDone": e["damageDone"], "bleedDamage": e["bleedDamage"]}, eDump)
        with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as eDump:
            dump({"deaths": enemy.deaths, "totalAttacks": {1: 0, 2: 0, 3: 0}, "damagingAttacks": {1: 0, 2: 0, 3: 0}, "damageDone": {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}, 4: {1: 0, 2: 0, 3: 0}}, "bleedDamage": {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}, 4: {1: 0, 2: 0, 3: 0}}}, eDump)
except Exception as ex:
    input(ex)
    raise
