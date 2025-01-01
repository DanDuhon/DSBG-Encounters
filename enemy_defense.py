from json import load, dump
from os import path
from enemies import enemies
from attacks import attackTiers, bleedTrigger, blackKnight
from loadouts import loadoutLookup, dodgeMod, expectedBlock
from math import ceil
from statistics import mean
from pathlib import Path


baseFolder = path.dirname(__file__)

maxAttacksTaken = 100
maxStaminaSpent = 500

reachMod = {
    0: 0.07692307692307693,
    1: 0.44970414201183434,
    2: 0.8224852071005917,
    3: 0.9763313609467456,
    4: 1
}

try:
    # Calculate enemy defense.
    for tier in range(1, 4):
        for enemy in enemies:
            if tier < 3 and enemy.modified:
                continue
            
            for attack in attackTiers[tier]:
                damage = attack.expectedDamage[enemy.resist if attack.magic else enemy.armor]

                if attack.bleed:
                    damage += 2 * bleedTrigger[tier][enemy.resist if attack.magic else enemy.armor]

                if attack.poison:
                    damage += 1

                if set(enemy.name.lower().split(" ")) & attack.damageBonus:
                    damage += 1

                # Account for boss weak arcs.
                if "boss" in enemy.enemyType:
                    damage += 1.5 * (enemy.weakArcs / 4)
                        
                if "Crossbreed Priscilla" in enemy.name:
                    # Odds of Priscilla being invisible: once at the start, once at heatup, once per empty deck.
                    damage -= ((2/40) + ((1/5) * (15/40)) + ((1/6) * (25/40))) * (enemy.weakArcs / 4)

                if "Titanite Demon" in enemy.name:
                    if damage >= 3:
                        damage -= 1

                attack.totalDamage[enemy] = damage

        # Second pass to get the number of deaths the attacks cause.
        print("Defense")
        for i, enemy in enumerate(enemies):
            if tier < 3 and enemy.modified:
                continue
            
            print("\t" + str((i/len(enemies)*100))[:5] + "%", end="\r")

            if "Maldron" in enemy.name:
                enemy.health += 5
            elif "Leeroy" in enemy.name:
                enemy.health += 2

            extraStaminaSpent = 0
            if any([{"stagger", "frostbite"} & e for e in enemy.attackEffect]):
                if enemy.attackEffect == [{"stagger", "frostbite"}]:
                    pass
                # Guess at how often this enemy will land with an attack.
                # Used to modify Stagger and Frostbite.
                nums = []
                den = 1000
                for i, a in enumerate(enemy.attacks[:int(len(enemy.attacks) / (2 if enemy.id else 1))]):
                    if a == 0 or not {"stagger", "frostbite"} & enemy.attackEffect[i]:
                        continue
                    nums.append(round(reachMod[max([0, min([4, enemy.move[i] + enemy.attackRange[i]])])] * den, 0))

                stage = 1
                for n in nums:
                    stage = stage * (den - n)
                chance = 1 - (stage / (den ** len(nums)))

                # Double the stamina spent if both Frostbite and Stagger are applied.
                extraStaminaSpent = chance * dodgeMod[tier][enemy.dodge] * (2 if any([{"stagger",} & e for e in enemy.attackEffect]) and any([{"frostbite",} & e for e in enemy.attackEffect]) else 1)

            # Maneater Mildred gains health if she does damage.
            # Abstract it out based on the tier.
            extraHealthGained = 0.0
            if "Maneater Mildred" in enemy.name:
                expandedBlock = [[l[0]] * loadoutLookup[tier][l] for l in loadoutLookup[tier]]
                # Flatten it to a single list then find the mean.
                block = mean([a for b in expandedBlock for a in b])

                for i, a in enumerate(enemy.attacks[:int(len(enemy.attacks) / (2 if enemy.id else 1))]):
                    if a == 0:
                        continue
                    if enemy.attacks[i] > block:
                        extraHealthGained += (reachMod[max([0, min([4, enemy.move[i] + enemy.attackRange[i]])])]
                            * dodgeMod[tier][enemy.dodge])
                    

            for attack in attackTiers[tier]:
                damage = attack.totalDamage[enemy]
                currentHealth = enemy.health

                if attack.bleed:
                    damage += 2 * bleedTrigger[tier][enemy.resist if attack.magic else enemy.armor]

                if "Titanite Demon" in enemy.name:
                    if damage >= 3:
                        damage -= 1

                if attack.staminaCost > 0:
                    staminaSpent = 0
                    while staminaSpent < maxStaminaSpent:
                        currentHealth -= damage

                        if currentHealth <= 0:
                            enemy.deaths[tier] += 1
                            currentHealth = enemy.health
                        elif "Heavy Knight" in enemy.name and currentHealth <= 15:
                            currentHealth += 3 * (1/5)
                        elif "Maneater Mildred" in enemy.name and currentHealth < enemy.health:
                            currentHealth += extraHealthGained
                            if currentHealth > enemy.health:
                                currentHealth = enemy.health

                        staminaSpent += attack.staminaCost + extraStaminaSpent

                        if "Winged Knight" in enemy.name:
                            staminaSpent += expectedBlock[3][tier]
                        elif "Black Knight" in enemy.name:
                            staminaSpent += blackKnight[tier]
                        elif "Heavy Knight" in enemy.name:
                            staminaSpent += dodgeMod[tier][enemy.dodge] * (0.8 if currentHealth <= 15 else 1)
                        elif "Gargoyle" in enemy.name and currentHealth <= 12 and not attack.noRange0:
                            staminaSpent += 1/(attack.attackRange + 1) 
                else:
                    for _ in range(maxAttacksTaken):
                        currentHealth -= damage
                        if currentHealth <= 0:
                            enemy.deaths[tier] += 1
                            currentHealth = enemy.health
                        elif "Heavy Knight" in enemy.name and currentHealth <= 15:
                            currentHealth += 3 * (1/5)
                        elif "Maneater Mildred" in enemy.name and currentHealth < enemy.health:
                            currentHealth += extraHealthGained
                            if currentHealth > enemy.health:
                                currentHealth = enemy.health

    for enemy in enemies:
        Path(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" [")] + "\\" if enemy.modified else "")).mkdir(exist_ok=True)
        # with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "r") as eLoad:
        #     e = load(eLoad)
        # with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as eDump:
        #     dump({"deaths": enemy.deaths, "totalAttacks": e["totalAttacks"], "damagingAttacks": e["damagingAttacks"], "damageDone": e["damageDone"], "bleedDamage": e["bleedDamage"]}, eDump)
        with open(baseFolder + "\\enemies\\" + (enemy.name[:enemy.name.rfind(" [")] + "\\" if enemy.modified else "") + enemy.name + ".json", "w") as eDump:
            dump({"health": enemy.health, "deaths": enemy.deaths, "totalAttacks": {1: 0, 2: 0, 3: 0}, "damagingAttacks": {1: 0, 2: 0, 3: 0}, "damageDone": {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}, 4: {1: 0, 2: 0, 3: 0}}, "bleedDamage": {1: {1: 0, 2: 0, 3: 0}, 2: {1: 0, 2: 0, 3: 0}, 3: {1: 0, 2: 0, 3: 0}, 4: {1: 0, 2: 0, 3: 0}}}, eDump)
except Exception as ex:
    input(ex)
    raise
