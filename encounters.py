from os import path
from json import load, dump
from itertools import combinations, islice
from random import shuffle
from collections import defaultdict, Counter

from enemies import enemyIds, enemiesDict

baseFolder = path.dirname(__file__)
allEnemies = []
alonneBowKnight = enemiesDict["Alonne Bow Knight"].id
alonneKnightCaptain = enemiesDict["Alonne Knight Captain"].id
alonneSwordKnight = enemiesDict["Alonne Sword Knight"].id
blackHollowMage = enemiesDict["Black Hollow Mage"].id
crossbowHollow = enemiesDict["Crossbow Hollow"].id
crossbowHollowTsc = enemiesDict["Crossbow Hollow (TSC)"].id
crowDemon = enemiesDict["Crow Demon"].id
falchionSkeleton = enemiesDict["Falchion Skeleton"].id
firebombHollow = enemiesDict["Firebomb Hollow"].id
giantSkeletonArcher = enemiesDict["Giant Skeleton Archer"].id
giantSkeletonSoldier = enemiesDict["Giant Skeleton Soldier"].id
hollowSoldier = enemiesDict["Hollow Soldier"].id
hollowSoldierTsc = enemiesDict["Hollow Soldier (TSC)"].id
phalanx = enemiesDict["Phalanx"].id
phalanxHollow = enemiesDict["Phalanx Hollow"].id
plowScarecrow = enemiesDict["Plow Scarecrow"].id
sentinel = enemiesDict["Sentinel"].id
sentinelTsc = enemiesDict["Sentinel (TSC)"].id
silverKnightSwordsman = enemiesDict["Silver Knight Swordsman"].id
silverKnightSwordsmanTsc = enemiesDict["Silver Knight Swordsman (TSC)"].id
silverKnightGreatbowman = enemiesDict["Silver Knight Greatbowman"].id
silverKnightGreatbowmanTsc = enemiesDict["Silver Knight Greatbowman (TSC)"].id
skeletonArcher = enemiesDict["Skeleton Archer"].id
skeletonSoldier = enemiesDict["Skeleton Soldier"].id
shearsScarecrow = enemiesDict["Shears Scarecrow"].id
stoneGuardian = enemiesDict["Stone Guardian"].id
stoneKnight = enemiesDict["Stone Knight"].id

skeletons = set([enemiesDict[e].id for e in enemiesDict if "Skeleton" in enemiesDict[e].name])
stdInvader = enemiesDict["Standard Invader/Hungry Mimic"].id
advInvader = enemiesDict["Advanced Invader/Voracious Mimic"].id
invaders = {stdInvader, advInvader}

# Some encounters have enemies (via initial placement or with spawns)
# that violate the limits of the number of models available.
# This will make sure that the app can actually produce the original
# encounter, as unlikely as that may be.
# For Depths of the Cathedral specifically, provide enough gang
# enemies so that the gang can be made up of enemies from other sets.
extraEnemies = {
    "The Grand Hall": [sentinelTsc],
    "Corvian Host": [
        crowDemon,
        sentinel,
        stoneGuardian,
        stoneKnight],
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
    enemiesDict["Sentinel (TSC)"].id,
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

# skip = True
for e in enc:
    if e not in ["Undead Sanctum"]:
        continue
#         skip = False
#     if skip:
#         continue
    encounter = enc[e]
    print(e)

    alternatives = dict()
    combosDict = dict()
    enemies = []
    diffMod = 0.1

    for tile in encounter["tiles"]:
        for enemy in encounter["tiles"][str(tile)]:
            enemies.append(enemy)
    for enemy in encounter.get("spawns", []):
        enemies.append(enemy)
        
    enemyCount = sum([1 for enemy in enemies if enemy not in invaders])
    rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1])
    difficulty = sum([enemyIds[enemy].difficulty * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])

    if e == "Undead Sanctum":
        allCombos = set(combinations([enemyIds[en].id for en in allEnemies + extraEnemies.get(e, []) if (
            en not in invaders
            and enemyIds[en].health in {
                    enemyIds[enemies[0]].health,
                    5 if enemyIds[enemies[0]].health == 10 else enemyIds[enemies[0]].health
                } if enemyCount == 1 else enemyIds[en].health
            )], enemyCount))
        
        goodCombos = []
        
        for combo in allCombos:
            # Undead Sanctum - I don't know why this works here and not below, but whatever. I'll leave this for now.
            if (
                difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
                and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                    or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                and ((3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6 or e == "Eye of the Storm")
                # Account for duplicate models from the new core sets.
                # I assume anyone who had the original core set wouldn't buy The Sunless City
                # (especially not if they're using this app), so limit the total number of
                # those models.
                and ((enc[e]["expansion"] == "The Sunless City" and e not in onslaughtEncounters)
                    or (enemies.count(crossbowHollow) + enemies.count(crossbowHollowTsc) <= 3
                        and enemies.count(hollowSoldier) + enemies.count(hollowSoldierTsc) <= 3
                        and enemies.count(sentinel) + enemies.count(sentinelTsc) <= 2
                        and enemies.count(silverKnightGreatbowman) + enemies.count(silverKnightGreatbowmanTsc) <= 3
                        and enemies.count(silverKnightSwordsman) + enemies.count(silverKnightSwordsmanTsc) <= 3))
                # Black Hollow Mages need to be with at least one "skeleton" enemy
                and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
                and sum([1 for enemy in combo if enemyIds[enemy].gang]) == 5
                and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 5):
                goodCombos.append(combo)

        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in goodCombos]
    # 6 enemies seems to be the limit for generating all combinations of enemies
    # in a reasonable amount of time.  For encounters with more than that, we're
    # going to take a sample instead.
    elif sum([1 for en in enemies if en not in invaders]) < 7:
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
        # Black Hollow Mage increases the difficulty of skeleton enemies since
        # they resurrect defeated skeletons.
        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
            difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
            and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
            and ((3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6 or e == "Eye of the Storm")
            # Account for duplicate models from the new core sets.
            # I assume anyone who had the original core set wouldn't buy The Sunless City
            # (especially not if they're using this app), so limit the total number of
            # those models.
            and ((enc[e]["expansion"] == "The Sunless City" and e not in onslaughtEncounters)
                or (enemies.count(crossbowHollow) + enemies.count(crossbowHollowTsc) <= 3
                    and enemies.count(hollowSoldier) + enemies.count(hollowSoldierTsc) <= 3
                    and enemies.count(sentinel) + enemies.count(sentinelTsc) <= 2
                    and enemies.count(silverKnightGreatbowman) + enemies.count(silverKnightGreatbowmanTsc) <= 3
                    and enemies.count(silverKnightSwordsman) + enemies.count(silverKnightSwordsmanTsc) <= 3))
            # Black Hollow Mages need to be with at least one "skeleton" enemy
            and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
            # Enemies must be different
            and (e not in set(["Abandoned and Forgotten", "The First Bastion"]) or len(combo) == len(set(combo)))
            # No more than one of the two strongest enemies
            and (e != "Trecherous Tower" or (combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1 and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[1]) == 1))
            # One of the strongest enemy
            and (e != "Cold Snap" or combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1)
            # A pair of enemies
            and (e != "Corrupted Hovel" or any([combo.count(enemy) == 2 for enemy in combo]))
            # Two pairs of enemies and one of the strongest enemy
            and (e != "Eye of the Storm" or (
                (len(set([enemy for enemy in combo if combo.count(enemy) == 2])) == 2
                    or [enemy for enemy in combo if combo.count(enemy) == 4])
                and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1))
            # Two pairs of enemies and the pairs can't contain the strongest enemy
            and (e != "Gleaming Silver" or (len(set([enemy for enemy in combo if combo.count(enemy) == 2])) == 2 and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1))
            # Two of the weakest 1 health enemy
            and (e not in set(["Skeletal Spokes", "The Shine of Gold"]) or ([enemy for enemy in combo if enemyIds[enemy].health == 1] and combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty)[0]) == 2))
            # Three of the weakest 1 health enemy, also no poison causing enemies
            and (e != "Shattered Keep" or (
                combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty)[0]) == 3
                and all(["poison" not in enemyIds[enemy].attackEffect for enemy in combo])))
            # Four of the same gang
            and (e != "Flooded Fortress" or (Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1) and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 4))
            # Five of the same gang
            and (e not in set(["Undead Sanctum", "The Fountainhead"]) or (sum([1 for enemy in combo if enemyIds[enemy].gang]) == 5 and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 5))
            # No poison causing enemies
            and (e != "Rain of Filth" or all(["poison" not in enemyIds[enemy].attackEffect for enemy in combo]))
        )]
    # Depths of the Cathedral is a beast to generate because of the 9 gang members,
    # so I spun it off into a more controlled setting.
    # Here we define the gang up front, and then fill in the rest.
    elif e == "Depths of the Cathedral":
        gangs = [
            [alonneSwordKnight, alonneSwordKnight, alonneSwordKnight, alonneSwordKnight, alonneSwordKnight, alonneSwordKnight, alonneBowKnight, alonneBowKnight, alonneBowKnight],
            [hollowSoldier, hollowSoldier, hollowSoldier, hollowSoldier, hollowSoldier, hollowSoldier, crossbowHollow, crossbowHollow, crossbowHollow],
            [hollowSoldier, hollowSoldier, hollowSoldier, hollowSoldier, hollowSoldier, hollowSoldier, firebombHollow, firebombHollow, firebombHollow],
            [hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, crossbowHollowTsc, crossbowHollowTsc, crossbowHollowTsc],
            [hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, hollowSoldierTsc, firebombHollow, firebombHollow, firebombHollow],
            [phalanxHollow, phalanxHollow, phalanxHollow, phalanxHollow, phalanxHollow, phalanxHollow, crossbowHollow, crossbowHollow, crossbowHollow],
            [phalanxHollow, phalanxHollow, phalanxHollow, phalanxHollow, phalanxHollow, phalanxHollow, firebombHollow, firebombHollow, firebombHollow],
            [skeletonSoldier, skeletonSoldier, skeletonSoldier, skeletonSoldier, skeletonSoldier, skeletonSoldier, skeletonArcher, skeletonArcher, skeletonArcher]
        ]

        nonGangs = [
            enemiesDict["Demonic Foliage"].id,
            enemiesDict["Demonic Foliage"].id,
            enemiesDict["Engorged Zombie"].id,
            enemiesDict["Engorged Zombie"].id,
            enemiesDict["Plow Scarecrow"].id,
            enemiesDict["Plow Scarecrow"].id,
            enemiesDict["Plow Scarecrow"].id,
            enemiesDict["Shears Scarecrow"].id,
            enemiesDict["Shears Scarecrow"].id,
            enemiesDict["Shears Scarecrow"].id,
            enemiesDict["Silver Knight Greatbowman"].id,
            enemiesDict["Silver Knight Greatbowman"].id,
            enemiesDict["Silver Knight Greatbowman"].id,
            enemiesDict["Silver Knight Greatbowman (TSC)"].id,
            enemiesDict["Silver Knight Greatbowman (TSC)"].id,
            enemiesDict["Silver Knight Spearman"].id,
            enemiesDict["Silver Knight Spearman"].id,
            enemiesDict["Silver Knight Spearman"].id,
            enemiesDict["Silver Knight Swordsman"].id,
            enemiesDict["Silver Knight Swordsman"].id,
            enemiesDict["Silver Knight Swordsman"].id,
            enemiesDict["Silver Knight Swordsman (TSC)"].id,
            enemiesDict["Silver Knight Swordsman (TSC)"].id,
            enemiesDict["Snow Rat"].id,
            enemiesDict["Snow Rat"].id
        ]

        higherHealthEnemies = [
            enemiesDict["Alonne Knight Captain"].id,
            enemiesDict["Crow Demon"].id,
            enemiesDict["Giant Skeleton Archer"].id,
            enemiesDict["Giant Skeleton Soldier"].id,
            enemiesDict["Ironclad Soldier"].id,
            enemiesDict["Large Hollow Soldier"].id,
            enemiesDict["Mimic"].id,
            enemiesDict["Mushroom Child"].id,
            enemiesDict["Mushroom Parent"].id,
            enemiesDict["Phalanx"].id,
            enemiesDict["Sentinel"].id,
            enemiesDict["Sentinel (TSC)"].id,
            enemiesDict["Stone Guardian"].id,
            enemiesDict["Stone Knight"].id
        ]

        allCombos = []
        for gang in gangs:
            for hh in higherHealthEnemies:
                nonGangCombos = set(combinations([enemyIds[en].id for en in nonGangs], 3))
                for combo in nonGangCombos:
                    allCombos.append(tuple(gang) + (hh,) + tuple(combo) + (enemiesDict["Mimic"].id,))
                
        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo])].add(combo) for combo in allCombos if (
            difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty for enemy in combo]) <= difficulty * (1 + diffMod)
            and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
            and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6)]
    else:
        combosDict = defaultdict(set)
        comboCount = []
        # Including 5 health enemies in Frozen Revolutions really seems to throw it off,
        # such that it doesn't generate any alternatives.
        if e == "Frozen Revolutions":
            shuffledEnemies = [enemy for enemy in allEnemies + extraEnemies.get(e, []) if enemyIds[enemy].health == 1]
        else:
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
            [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
                difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty* (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
                and sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount
                and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                # Account for duplicate models from the new core sets.
                # I assume anyone who had the original core set wouldn't buy The Sunless City
                # (especially not if they're using this app), so limit the total number of
                # those models.
                and ((enc[e]["expansion"] == "The Sunless City" and e not in onslaughtEncounters)
                    or (enemies.count(crossbowHollow) + enemies.count(crossbowHollowTsc) <= 3
                        and enemies.count(hollowSoldier) + enemies.count(hollowSoldierTsc) <= 3
                        and enemies.count(sentinel) + enemies.count(sentinelTsc) <= 2
                        and enemies.count(silverKnightGreatbowman) + enemies.count(silverKnightGreatbowmanTsc) <= 3
                        and enemies.count(silverKnightSwordsman) + enemies.count(silverKnightSwordsmanTsc) <= 3))
                # Black Hollow Mages need to be with at least one "skeleton" enemy
                and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
                # Three of the strongest 5 health enemy
                and (e != "Corvian Host" or ([enemy for enemy in combo if enemyIds[enemy].health >= 5] and combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health >= 5], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 3))
                # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                and (e != "Deathly Freeze" or (
                    combo.count(sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2
                    and sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0] not in deathlyFreezeEnemyBlacklist
                    # This will make sure that there isn't a situation in which a duplicate
                    # enemy from another set screws things up.
                    and Counter([enemyIds[enemy].difficulty for enemy in combo])[sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0]] == 2))
                # Two of the strongest 1 health enemy
                and (e != "Frozen Revolutions" or combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2)
                # Two of the second strongest enemy (second strongest cannot also be the first strongest)
                and (e != "Trophy Room" or (combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[1]) == 2
                                            and sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[1] == sorted(list(set([enemy for enemy in combo])), key=lambda x: enemyIds[x].difficulty, reverse=True)[1]))
                # Three of the same gang
                and (e != "Deathly Tolls" or (Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1) and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 3))
                # Five of the same gang
                and (e != "Twilight Falls" or (Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1) and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 5))
            )]

            # Keep track of the number of combinations we have.
            comboCount.append(sum((len(combosDict[sets]) for sets in combosDict)))

            # If we didn't find any new combos in the last 100 loops, be done.
            # This prevents an infinite loop if there will never be 1 million alternatives.
            # Corvian Host is an example of this.
            if len(comboCount) >= 100 and len(set(comboCount[-100:])) == 1:
                break

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

    # Alternative enemy order by difficulty matching original enemy order.
    alternatives["alternatives"] = {",".join([k for k in key]): list(value) for key, value in combosDict.items()}
    for expansionCombo in alternatives["alternatives"]:
        newAlts = []
        for alt in alternatives["alternatives"][expansionCombo]:
            newAlt = []
            altDifficulty = sorted(alt, key=lambda x: enemyIds[x].difficulty)
            for ord in enc[e]["difficultyOrder"]:
                newAlt.append(altDifficulty[ord])
            if newAlt not in newAlts:
                newAlts.append(newAlt)
        alternatives["alternatives"][expansionCombo] = newAlts

    # This is manually set for each encounter in the JSON file.
    # enemySlots is the number of enemies in each row following this pattern:
    # [Tile 1 Row 1, Tile 1 Row 2, Tile 1 Row 3 (level 3 only), Tile 1 Row 4 (level 3 only), Tile 2 Row 1, Tile 2 Row 2, Tile 3 Row 3]
    with open(path.join(baseFolder + "\\encounters", e + ".json")) as ef:
        thisEnc = load(ef)
    alternatives["enemySlots"] = thisEnc.get("enemySlots")

    # Remove alternatives that break model limits on a tile level.
    # Only applies to certain encounters.
    alternativesToRemove = {}
    if e in extraEnemies and e not in onslaughtEncounters:
        slots = alternatives["enemySlots"]
        tile1Num = sum([s for s in slots[:5]])
        tile2Num = sum([s for s in slots[5:7]])
        for expansionCombo in alternatives["alternatives"]:
            for alt in alternatives["alternatives"][expansionCombo]:
                for enemy in alt:
                    if any([
                        [en for en in alt[:tile1Num + 1]].count(enemy) > enemyIds[enemy].numberOfModels,
                        [en for en in alt[tile1Num + 1:tile2Num + 1]].count(enemy) > enemyIds[enemy].numberOfModels,
                        [en for en in alt[tile2Num + 1:]].count(enemy) > enemyIds[enemy].numberOfModels
                        ]):
                        if expansionCombo not in alternativesToRemove:
                            alternativesToRemove[expansionCombo] = set()
                        alternativesToRemove[expansionCombo].add(tuple(alt))

        for expansionCombo in alternativesToRemove:
            for alt in list(alternativesToRemove[expansionCombo]):
                alternatives["alternatives"][expansionCombo].remove(list(alt))
    elif e in extraEnemies and e in onslaughtEncounters:
        for expansionCombo in alternatives["alternatives"]:
            for alt in alternatives["alternatives"][expansionCombo]:
                for enemy in alt:
                    if alt.count(enemy) > enemyIds[enemy].numberOfModels:
                        if expansionCombo not in alternativesToRemove:
                            alternativesToRemove[expansionCombo] = set()
                        alternativesToRemove[expansionCombo].add(tuple(alt))

    keysToDelete = []

    for expansionCombo in alternatives["alternatives"]:
        if not alternatives["alternatives"][expansionCombo]:
            keysToDelete.append(expansionCombo)

    for key in keysToDelete:
        del alternatives["alternatives"][key]

    # For each key in the dictionary, shuffle the enemy combos,
    # then trim it down so we keep at most 1000 values per key.
    for expansionCombo in alternatives["alternatives"]:
        alternatives["alternatives"][expansionCombo] = list(alternatives["alternatives"][expansionCombo])
        shuffle(alternatives["alternatives"][expansionCombo])
        alternatives["alternatives"][expansionCombo] = alternatives["alternatives"][expansionCombo][:min([len(alternatives["alternatives"][expansionCombo]), 1000])]

    if e not in encMain:
        encMain[e] = {
            "name": enc[e]["name"],
            "expansion": enc[e]["expansion"],
            "level": enc[e]["level"],
            "expansionCombos": [k.split(",") for k in alternatives["alternatives"].keys()]
            }
    else:
        encMain[e]["expansionCombos"] = [k.split(",") for k in alternatives["alternatives"].keys()]
            
    with open(baseFolder + "\\encounters\\" + e + ".json", "w") as encountersFile:
        dump(alternatives, encountersFile)

    with open(baseFolder + "\\encounters.json", "w") as ef:
        dump(encMain, ef)
