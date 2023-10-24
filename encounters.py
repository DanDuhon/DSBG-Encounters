from os import path
from json import load, dump
from itertools import combinations, islice
from random import shuffle
from collections import defaultdict

from enemies import enemyIds, enemiesDict

baseFolder = path.dirname(__file__)
allEnemies = []
stdInvader = enemiesDict["Standard Invader/Hungry Mimic"].id
advInvader = enemiesDict["Advanced Invader/Voracious Mimic"].id
phalanx = enemiesDict["Phalanx"].id
phalanxHollow = enemiesDict["Phalanx Hollow"].id
crowDemon = enemiesDict["Crow Demon"].id
giantSkeletonArcher = enemiesDict["Giant Skeleton Archer"].id
giantSkeletonSoldier = enemiesDict["Giant Skeleton Soldier"].id
blackHollowMage = enemiesDict["Black Hollow Mage"].id
crossbowHollow = enemiesDict["Crossbow Hollow"].id
hollowSoldier = enemiesDict["Hollow Soldier"].id
sentinel = enemiesDict["Sentinel"].id
silverKnightSwordsman = enemiesDict["Silver Knight Swordsman"].id
silverKnightGreatbowman = enemiesDict["Silver Knight Greatbowman"].id
crossbowHollowTsc = enemiesDict["Crossbow Hollow (TSC)"].id
hollowSoldierTsc = enemiesDict["Hollow Soldier (TSC)"].id
sentinelTsc = enemiesDict["Sentinel (TSC)"].id
silverKnightSwordsmanTsc = enemiesDict["Silver Knight Swordsman (TSC)"].id
silverKnightGreatbowmanTsc = enemiesDict["Silver Knight Greatbowman (TSC)"].id
skeletons = set([enemiesDict[e].id for e in enemiesDict if "Skeleton" in enemiesDict[e].name])
invaders = {stdInvader, advInvader}

# Some encounters have enemies (via initial placement or with spawns)
# that violate the limits of the number of models available.
# This will make sure that the app can actually produce the original
# encounter, as unlikely as that may be.
extraEnemies = {
    "Depths of the Cathedral": [hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc],
    "The Grand Hall": [sentinelTsc],
    "Corvian Host": [crowDemon, crowDemon],
    "Giant's Coffin": [giantSkeletonArcher, giantSkeletonSoldier]
}

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

onslaughtEncounters = {
    "Undead Sanctum",
    "Deathly Tolls",
    "Hanging Rafters"
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

with open(path.join(baseFolder + "\\encounters", "all_encounters.json")) as aef:
    enc = load(aef)

with open(path.join(baseFolder, "encounters.json")) as ef:
    encMain = load(ef)

encountersWithTrial = set([
    "Corvian Host",
    "Distant Tower"
])

# skip = True
for e in enc:
#     if e == "Depths of the Cathedral":
# #     #     continue
#         skip = False
#     if skip:
#         continue
    encounter = enc[e]
    print(e)

    alternatives = dict()
    combosDict = dict()
    enemies = []
    diffMod = 0.1

    trialEnemies = set()

    for tile in encounter["tiles"]:
        for enemy in encounter["tiles"][str(tile)]:
            enemies.append(enemy)
    for enemy in encounter.get("spawns", []):
        enemies.append(enemy)
        
    enemyCount = sum([1 for enemy in enemies if enemy not in invaders])
    rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1])
    difficulty = sum([enemyIds[enemy].difficulty * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])

    # 6 enemies seems to be the limit for generating all combinations of enemies
    # in a reasonable amount of time.  For encounters with more than that, we're
    # going to take a sample instead.
    if sum([1 for en in enemies if en not in invaders]) < 7:
        # Generate all combinations of enemies, excluding invaders and old style mimics.
        # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
        # The Sunless City actually breaks the model limit for that set at the encounter
        # (but not tile) level. For TSC encounters, add as many TSC enemies as required
        # to be able to generate the original encounter.
        allCombos = set(combinations([enemyIds[en].id for en in allEnemies + extraEnemies.get(e, []) if (
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
        # Black Hollow Mage increases the difficulty of skeleton enemies since
        # they resurrect defeated skeletons.
        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].set for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
            difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
            and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
            and ((3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6 or e == "Eye of the Storm")
            # Account for duplicate models from the new core sets.
            # I assume anyone who had the original core set wouldn't buy The Sunless City
            # (especially not if they're using this app), so limit the total number of
            # those models.
            and ((enc[e]["set"] == "The Sunless City" and e not in onslaughtEncounters)
                or (enemies.count(crossbowHollow) + enemies.count(crossbowHollowTsc) <= 3
                    and enemies.count(hollowSoldier) + enemies.count(hollowSoldierTsc) <= 3
                    and enemies.count(sentinel) + enemies.count(sentinelTsc) <= 2
                    and enemies.count(silverKnightGreatbowman) + enemies.count(silverKnightGreatbowmanTsc) <= 3
                    and enemies.count(silverKnightSwordsman) + enemies.count(silverKnightSwordsmanTsc) <= 3))
            # Black Hollow Mages need to be with at least one "skeleton" enemy
            and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
            # One of the strongest enemy
            and (e != "Cold Snap" or combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1)
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
        shuffledEnemies = allEnemies + extraEnemies.get(e, [])

        # These are the encounters that would take too long to generate all the combinations because we need
        # too many enemies (more than 6).
        # In total, we're looking for up to 1 million combinations but we'll trim that down later.
        while sum((len(combosDict[sets]) for sets in combosDict)) < 1000000:
            # Combinations go by the order of the iterable it's reading from,
            # so shuffling the order of the enemies will give us different
            # combinations.
            shuffle(shuffledEnemies)
            # Grab the first 100,000 combinations.
            allCombos = list(islice(combinations([en for en in shuffledEnemies if en not in invaders], enemyCount), 100000))

            # Create the dictionary with the enemy sets as keys.
            [combosDict[frozenset([enemyIds[enemyId].set for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
                difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty* (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
                and sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount
                and ((3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6 or e == "Eye of the Storm")
                # Account for duplicate models from the new core sets.
                # I assume anyone who had the original core set wouldn't buy The Sunless City
                # (especially not if they're using this app), so limit the total number of
                # those models.
                and ((enc[e]["set"] == "The Sunless City" and e not in onslaughtEncounters)
                    or (enemies.count(crossbowHollow) + enemies.count(crossbowHollowTsc) <= 3
                        and enemies.count(hollowSoldier) + enemies.count(hollowSoldierTsc) <= 3
                        and enemies.count(sentinel) + enemies.count(sentinelTsc) <= 2
                        and enemies.count(silverKnightGreatbowman) + enemies.count(silverKnightGreatbowmanTsc) <= 3
                        and enemies.count(silverKnightSwordsman) + enemies.count(silverKnightSwordsmanTsc) <= 3))
                # Black Hollow Mages need to be with at least one "skeleton" enemy
                and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
                # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                and (e != "Deathly Freeze" or (
                    combo.count(sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2
                    and sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0] not in deathlyFreezeEnemyBlacklist))
            )]

            # Keep track of the number of combinations we have.
            comboCount.append(sum((len(combosDict[sets]) for sets in combosDict)))

            # If we didn't find any new combos in the last 100 loops, be done.
            # This prevents an infinite loop if there will never be 1 million alternatives.
            # Deathly Freeze is an example of this.
            if len(comboCount) >= 100 and len(set(comboCount[-100:])) == 1:
                break

    if e in encountersWithTrial:
        for combo in combosDict:
            for alternative in combosDict[combo]:
                if e == "Corvian Host":
                    trialEnemies.add(sorted([enemy for enemy in list(alternative) if enemyIds[enemy].health >= 5], key=lambda x: enemyIds[x].difficulty, reverse=True)[0])
                if e == "Distant Tower":
                    trialEnemies.add(sorted(list(alternative), key=lambda x: enemyIds[x].difficulty, reverse=True)[0])

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
    enemyOrder = enc[e]["tiles"].get("1", []) + enc[e]["tiles"].get("2", []) + enc[e]["tiles"].get("3", []) + enc[e].get("spawns", [])
    enemyDifficulty = sorted([enemy for enemy in enemyOrder], key=lambda x: enemyIds[x].difficulty)
    originalDifficultyOrder = []
    for i, a in enumerate(enemyOrder):
        idx = enemyDifficulty.index(a)
        while idx in originalDifficultyOrder:
            idx += 1
        originalDifficultyOrder.append(idx)

    # Alternative enemy order by difficulty matching original enemy order.
    alternatives["alternatives"] = {",".join([k for k in key]): list(value) for key, value in combosDict.items()}
    for setCombo in alternatives["alternatives"]:
        newAlts = []
        for alt in alternatives["alternatives"][setCombo]:
            newAlt = []
            altDifficulty = sorted(alt, key=lambda x: enemyIds[x].difficulty)
            for ord in originalDifficultyOrder:
                newAlt.append(altDifficulty[ord])
            if newAlt not in newAlts:
                newAlts.append(newAlt)
        alternatives["alternatives"][setCombo] = newAlts

    # This is manually set for each encounter in the JSON file.
    # It is the number of enemies in each row following this pattern:
    # [Tile 1 Row 1, Tile 1 Row 2, Tile 1 Row 3 (level 3 only), Tile 1 Row 4 (level 3 only), Tile 2 Row 1, Tile 2 Row 2, Tile 3 Row 3]
    with open(path.join(baseFolder + "\\encounters", e + ".json")) as ef:
        thisEnc = load(ef)
    alternatives["enemySlots"] = thisEnc.get("enemySlots")

    # Remove alternatives that break model limits on a tile level.
    # Only applies to The Sunless City encounters without Onslaught.
    alternativesToRemove = {}
    if e in extraEnemies and e not in onslaughtEncounters:
        slots = alternatives["enemySlots"]
        tile1Num = sum([s for s in slots[:5]])
        tile2Num = sum([s for s in slots[5:7]])
        for setCombo in alternatives["alternatives"]:
            for alt in alternatives["alternatives"][setCombo]:
                for enemy in alt:
                    if any([
                        [en for en in alt[:tile1Num + 1]].count(enemy) > enemyIds[enemy].numberOfModels,
                        [en for en in alt[tile1Num + 1:tile2Num + 1]].count(enemy) > enemyIds[enemy].numberOfModels,
                        [en for en in alt[tile2Num + 1:]].count(enemy) > enemyIds[enemy].numberOfModels
                        ]):
                        if setCombo not in alternativesToRemove:
                            alternativesToRemove[setCombo] = set()
                        alternativesToRemove[setCombo].add(tuple(alt))

        for setCombo in alternativesToRemove:
            for alt in list(alternativesToRemove[setCombo]):
                alternatives["alternatives"][setCombo].remove(list(alt))
    elif e in extraEnemies and e in onslaughtEncounters:
        for setCombo in alternatives["alternatives"]:
            for alt in alternatives["alternatives"][setCombo]:
                for enemy in alt:
                    if alt.count(enemy) > enemyIds[enemy].numberOfModels:
                        if setCombo not in alternativesToRemove:
                            alternativesToRemove[setCombo] = set()
                        alternativesToRemove[setCombo].add(tuple(alt))

    keysToDelete = []

    for setCombo in alternatives["alternatives"]:
        if not alternatives["alternatives"][setCombo]:
            keysToDelete.append(setCombo)

    for key in keysToDelete:
        del alternatives["alternatives"][key]

    # For each key in the dictionary, shuffle the enemy combos,
    # then trim it down so we keep at most 1000 values per key.
    for setCombo in alternatives["alternatives"]:
        alternatives["alternatives"][setCombo] = list(alternatives["alternatives"][setCombo])
        shuffle(alternatives["alternatives"][setCombo])
        alternatives["alternatives"][setCombo] = alternatives["alternatives"][setCombo][:min([len(alternatives["alternatives"][setCombo]), 1000])]

    if e not in encMain:
        encMain[e] = {
            "name": enc[e]["name"],
            "expansion": enc[e]["set"],
            "level": enc[e]["level"],
            "setCombos": [k.split(",") for k in alternatives["alternatives"].keys()]
            }
    else:
        encMain[e]["setCombos"] = [k.split(",") for k in alternatives["alternatives"].keys()]
            
    with open(baseFolder + "\\encounters\\" + e + ".json", "w") as encountersFile:
        dump(alternatives, encountersFile)

    with open(baseFolder + "\\encounters.json", "w") as ef:
        dump(encMain, ef)

    if trialEnemies:
        with open(baseFolder + "\\encounters\\" + e + " Trial Enemies.json", "w") as trial:
            dump(list(trialEnemies), trial)
