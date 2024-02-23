from json import load, dump
from os import path
from enemies import enemies
from attacks import attackTiers, bleedTrigger
from loadouts import dodgeMod
from math import ceil


baseFolder = path.dirname(__file__)

maxAttacksTaken = 0
maxStaminaSpent = 0

reachMod = {
    0: 0.0384615384615385,
    1: 0.2582417582,
    2: 0.5412087912,
    3: 0.7637362637,
    4: 1
}

try:
    # Calculate enemy defense.
    # First pass to get how many times to apply each attack.
    for tier in range(1, 4):
        for enemy in enemies:
            if enemy.skip:
                continue
            for attack in attackTiers[tier]:
                damage = attack.expectedDamage[enemy.resist if attack.magic else enemy.armor]

                if attack.bleed:
                    damage += bleedTrigger[tier][enemy.resist if attack.magic else enemy.armor]

                if attack.poison:
                    damage += 1

                if set(enemy.name.lower().split(" ")) & attack.damageBonus:
                    damage += 1

                # Account for boss weak arcs.
                damage += 1.5 * (enemy.weakArcs / 4)
                        
                if "Crossbreed Priscilla" in enemy.name:
                    # Odds of Priscilla being invisible: once at the start, once at heatup, once per empty deck.
                    damage -= ((2/40) + ((1/5) * (15/40)) + ((1/6) * (25/40))) * (enemy.weakArcs / 4)

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

                extraStaminaSpent = chance * dodgeMod[tier][enemy.dodge[0] if type(enemy.dodge) == list and len(enemy.dodge) == 1 else enemy.dodge]

            for attack in attackTiers[tier]:
                damage = attack.totalDamage[enemy]
                currentHealth = enemy.health

                if attack.staminaCost > 0:
                    staminaSpent = 0
                    while staminaSpent < maxStaminaSpent:
                        currentHealth -= damage

                        if currentHealth <= 0:
                            enemy.deaths[tier] += 1
                            currentHealth = enemy.health

                        staminaSpent += attack.staminaCost + extraStaminaSpent
                else:
                    for _ in range(maxAttacksTaken):
                        currentHealth -= damage
                        if currentHealth <= 0:
                            enemy.deaths[tier] += 1
                            currentHealth = enemy.health

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
