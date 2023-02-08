from os import path
from json import load, dump
from itertools import combinations, islice
from random import shuffle
from collections import defaultdict

from enemies import enemyIds, enemiesDict


baseFolder = path.dirname(__file__)
coreSets = {"Dark Souls The Board Game", "The Painted World of Ariamis", "The Tomb of Giants"}
allEnemies = []
stdInvader = enemiesDict["Standard Invader/Hungry Mimic"].id
advInvader = enemiesDict["Advanced Invader/Voracious Mimic"].id
phalanx = enemiesDict["Phalanx"].id
phalanxHollow = enemiesDict["Phalanx Hollow"].id
invaders = {stdInvader, advInvader}
crystalLizardEncounters = {
    "Base of Cardinal Tower",
    "Blazing Furnace",
    "Brume Tower",
    "Cells of the Dead",
    "Flaming Passageway",
    "Iron Depths",
    "Manor Foregarden",
    "Melting Gallery",
    "New Londo Ruins",
    "Pyre of Souls",
    "Royal Woods Passage",
    "Ruined Walkway",
    "Smoking Gallery",
    "The Castle Grounds",
    "Threshold Bridge"
}

deathlyFreezeEnemyBlacklist = {
    enemiesDict["Bonewheel Skeleton"].id,
    enemiesDict["Crow Demon"].id,
    enemiesDict["Ironclad Soldier"].id,
    enemiesDict["Large Hollow Soldier"].id,
    enemiesDict["Mushroom Child"].id,
    enemiesDict["Mushroom Parent"].id,
    enemiesDict["Phalanx"].id,
    enemiesDict["Sentinel"].id,
    enemiesDict["Skeleton Beast"].id,
    enemiesDict["Skeleton Soldier"].id,
    enemiesDict["Stone Guardian"].id
    }

for enemy in enemyIds:
    for _ in range(enemyIds[enemy].numberOfModels):
        allEnemies.append(enemy)

with open(path.join(baseFolder + "\\encounters", "all_encounters.json")) as ef:
    enc = load(ef)

with open(path.join(baseFolder, "encounters.json")) as ef:
    encMain = load(ef)

#skip = True
for e in enc:
    # if e == "Eye of the Storm":
    #     skip = False
    # if skip:
    #     continue
    encounter = enc[e]
    print(e)

    alternatives = dict()
    combosDict = dict()
    enemies = []
    diffMod = 0.1

    for tile in encounter["tiles"]:
        for enemy in encounter["tiles"][str(tile)]:
            enemies.append(enemy)
        
    enemyCount = sum([1 for enemy in enemies if enemy not in invaders])
    rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1])
    difficulty = sum([enemyIds[enemy].difficulty * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])

    # 6 enemies seems to be the limit for generating all combinations of enemies
    # in a reasonable amount of time.  For encounters with more than that, we're
    # going to take a sample instead.
    if sum([1 for en in enemies if en not in invaders]) < 7:
        # Generate all combinations of enemies, excluding invaders and mimics.
        # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
        allCombos = set(combinations([enemyIds[en].id for en in allEnemies if (
            en not in invaders
            and enemyIds[en].health in {
                    enemyIds[enemies[0]].health,
                    5 if enemyIds[enemies[0]].health == 10 else enemyIds[enemies[0]].health
                } if enemyCount == 1 else enemyIds[en].health
            )], enemyCount))

        # Create a dictionary of alternatives, put into keys that are the
        # sets in which those enemies are found.
        # Encounters with Crystal Lizards always require Iron Keep.
        # Encounters with the Eerie rule always require The Painted World of Ariamis
        # (since the enemies for that are calculated on the fly, I can't guarantee
        # the mix of enabled sets will work).
        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set()).union({"The Painted World of Ariamis"} if e in {"Abandoned and Forgotten", "Trecherous Tower"} else set())].add(combo) for combo in allCombos if (
            difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty for enemy in combo]) <= difficulty * (1 + diffMod)
            and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
            and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
            # A pair of enemies
            and (e != "Corrupted Hovel" or any([combo.count(enemy) == 2 for enemy in combo]))
            # Two of the strongest 5 health enemy
            and (e != "Corvian Host" or ([enemy for enemy in combo if enemyIds[enemy].health >= 5] and combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health >= 5], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2))
            # Two pairs of enemies
            and (e != "Eye of the Storm" or len(set([enemy for enemy in combo if combo.count(enemy) == 2])) == 2 or [enemy for enemy in combo if combo.count(enemy) == 4])
            # Two of the strongest 1 health enemy
            and (e != "Frozen Revolutions" or combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2)
            # Two of the weakest 1 health enemy
            and (e != "Skeletal Spokes" or combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty)[0]) == 2)
        )]
    else:
        combosDict = defaultdict(set)
        comboCount = []

        # These are the encounters that would take too long to generate all the combinations because we need
        # too many enemies (more than 6).
        # In total, we're looking for up to 1 million combinations but we'll trim that down later.
        while sum((len(combosDict[expansions]) for expansions in combosDict)) < 1000000:
            # Combinations go by the order of the iterable it's reading from,
            # so shuffling the order of the enemies will give us different
            # combinations.
            shuffle(allEnemies)
            # Grab the first 100,000 combinations.
            allCombos = list(islice(combinations([en for en in allEnemies if en not in invaders], enemyCount), 100000))

            # Create the dictionary with the enemy sets as keys.
            [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
                difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty for enemy in combo]) <= difficulty * (1 + diffMod)
                and sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount
                and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                and (e != "Deathly Freeze" or (
                    combo.count(sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2
                    and sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0] not in deathlyFreezeEnemyBlacklist))
            )]

            # Keep track of the number of combinations we have.
            comboCount.append(sum((len(combosDict[expansions]) for expansions in combosDict)))

            # If we didn't find any new combos in the last 100 loops, be done.
            # This prevents an infinite loop if there will never be 1 million alternatives.
            # Deathly Freeze is an example of this.
            if len(comboCount) >= 100 and len(set(comboCount[-100:])) == 1:
                break

    # For each key in the dictionary, shuffle the enemy combos,
    # then trim it down so we keep at most 1000 values per key.
    for combo in combosDict:
        combosDict[combo] = list(combosDict[combo])
        shuffle(combosDict[combo])
        combosDict[combo] = combosDict[combo][:min([len(combosDict[combo]), 1000])]

    # If there's a standard invader or Hungry Mimic, add that to each combo.
    if stdInvader in enemies:
        for combos in combosDict:
            newCombos = []
            for combo in combosDict[combos]:
                newCombos.append(tuple([stdInvader] + list(combo)))
            combosDict[combos] = newCombos
                
    # If there's an advanced invader or Voracious Mimic, add that to each combo.
    if advInvader in enemies:
        for combos in combosDict:
            newCombos = []
            for combo in combosDict[combos]:
                newCombos.append(tuple([advInvader] + list(combo)))
            combosDict[combos] = newCombos

    # Put the alternative enemies in the same difficulty order as the
    # original enemies. This way I can just iterate through the list
    # when we load the encounter and take the enemies in order.

    # Original enemy order by difficulty
    enemyOrder = enc[e]["tiles"].get("1", []) + enc[e]["tiles"].get("2", []) + enc[e]["tiles"].get("3", [])
    enemyDifficulty = sorted([enemy for enemy in enemyOrder], key=lambda x: enemyIds[x].difficulty)
    originalDifficultyOrder = []
    for i, a in enumerate(enemyOrder):
        idx = enemyDifficulty.index(a)
        while idx in originalDifficultyOrder:
            idx += 1
        originalDifficultyOrder.append(idx)

    # Alternative enemy order by difficulty matching original enemy order.
    alternatives["alternatives"] = {",".join([k for k in key]): list(value) for key, value in combosDict.items()}
    for expCombo in alternatives["alternatives"]:
        newAlts = []
        for alt in alternatives["alternatives"][expCombo]:
            newAlt = []
            altDifficulty = sorted(alt, key=lambda x: enemyIds[x].difficulty)
            for ord in originalDifficultyOrder:
                newAlt.append(altDifficulty[ord])
            newAlts.append(newAlt)
        alternatives["alternatives"][expCombo] = newAlts

    with open(path.join(baseFolder + "\\encounters", e + ".json")) as ef:
        thisEnc = load(ef)
    alternatives["enemySlots"] = thisEnc["enemySlots"]

    encMain[e]["setCombos"] = [k.split(",") for k in alternatives["alternatives"].keys()]
            
    with open(baseFolder + "\\encounters\\" + e + ".json", "w") as encountersFile:
        dump(alternatives, encountersFile)

    with open(baseFolder + "\\encounters.json", "w") as ef:
        dump(encMain, ef)