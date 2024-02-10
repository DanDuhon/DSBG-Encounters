from json import load, dump
from os import path
from enemies import enemies
from attacks import attacks, bleedTrigger, blackKnight
from loadouts import dodgeMod, expectedBlock3Plus
from math import ceil


baseFolder = path.dirname(__file__)

maxAttacksTaken = 0
maxStaminaSpent = 0

try:
    # Calculate enemy defense.
    # First pass to get how many times to apply each attack.
    for enemy in enemies:
        if enemy.skip:
            continue
        for attack in attacks:
            damage = attack.expectedDamage[enemy.resist if attack.magic else enemy.armor]

            if attack.bleed:
                damage += bleedTrigger[enemy.resist if attack.magic else enemy.armor]

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

            attack.totalDamage[enemy] = damage

            if damage > 0 and enemy.expansion != "Phantoms" and enemy.health / damage > maxAttacksTaken:
                maxAttacksTaken = ceil(enemy.health / damage)

            if damage > 0 and enemy.expansion != "Phantoms" and (enemy.health / damage) * attack.staminaCost > maxStaminaSpent:
                maxStaminaSpent = ceil((enemy.health / damage) * attack.staminaCost)

    # Second pass to get the number of deaths the attacks cause.
    print("Defense")
    for i, enemy in enumerate(enemies):
        if i % 50 == 0 and i > 0:
            print("\t" + str((i/len(enemies)*100))[:5] + "%")
        if enemy.skip:
            continue
        for attack in attacks:
            damage = attack.totalDamage[enemy]
            currentHealth = enemy.health

            if attack.staminaCost > 0:
                staminaSpent = 0
                while staminaSpent < maxStaminaSpent:
                    if enemy.name == "Titanite Demon":
                        if damage >= 3:
                            damage -= 1

                    currentHealth -= damage

                    if currentHealth <= 0:
                        enemy.deaths += 1
                        currentHealth = enemy.health
                    elif enemy.name == "Heavy Knight" and currentHealth <= 15:
                        currentHealth += 3 * (1/5)

                    staminaSpent += attack.staminaCost

                    if any([{"stagger", "frostbite"} & e for e in enemy.attackEffect]):
                        staminaSpent += dodgeMod[enemy.dodge[0] if type(enemy.dodge) == list and len(enemy.dodge) == 1 else enemy.dodge]

                    if enemy.name == "Winged Knight":
                        staminaSpent += expectedBlock3Plus
                    elif enemy.name == "Black Knight":
                        staminaSpent += blackKnight
                    elif enemy.name == "Heavy Knight":
                        staminaSpent += dodgeMod[enemy.dodge] * (0.8 if currentHealth <= 15 else 1)
                    elif enemy.name == "Gargoyle" and currentHealth <= 12 and not attack.noRange0:
                        staminaSpent += 1/(attack.range + 1) 
            else:
                for _ in range(maxAttacksTaken):
                    currentHealth -= damage
                    if currentHealth <= 0:
                        enemy.deaths += 1
                        currentHealth = enemy.health
                    elif enemy.name == "Heavy Knight" and currentHealth <= 15:
                        currentHealth += 3 * (1/5)

    for enemy in enemies:
        with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "r") as eLoad:
            e = load(eLoad)
        with open(baseFolder + "\\enemies\\" + enemy.name + ".json", "w") as eDump:
            dump({"deaths": enemy.deaths, "totalAttacks": e["totalAttacks"], "damagingAttacks": e["damagingAttacks"], "damageDone": e["damageDone"], "bleedDamage": e["bleedDamage"]}, eDump)
except Exception as ex:
    input(ex)
    raise
