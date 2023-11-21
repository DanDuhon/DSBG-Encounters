from os import path
from json import load, dump
from itertools import combinations, islice, product
from random import shuffle
from collections import defaultdict, Counter

from enemies import enemyIds, enemiesDict

baseFolder = path.dirname(__file__)
allEnemies = []
alonneBowKnight = enemiesDict["Alonne Bow Knight"].id
alonneSwordKnight = enemiesDict["Alonne Sword Knight"].id
blackHollowMage = enemiesDict["Black Hollow Mage"].id
crossbowHollow = enemiesDict["Crossbow Hollow"].id
falchionSkeleton = enemiesDict["Falchion Skeleton"].id
firebombHollow = enemiesDict["Firebomb Hollow"].id
hollowSoldier = enemiesDict["Hollow Soldier"].id
mimic = enemiesDict["Mimic"].id
phalanx = enemiesDict["Phalanx"].id
phalanxHollow = enemiesDict["Phalanx Hollow"].id
sentinel = enemiesDict["Sentinel"].id
silverKnightSwordsman = enemiesDict["Silver Knight Swordsman"].id
silverKnightGreatbowman = enemiesDict["Silver Knight Greatbowman"].id
skeletonArcher = enemiesDict["Skeleton Archer"].id
skeletonSoldier = enemiesDict["Skeleton Soldier"].id

skeletons = set([enemiesDict[e].id for e in enemiesDict if "Skeleton" in enemiesDict[e].name])
stdInvader = enemiesDict["Standard Invader"].id
advInvader = enemiesDict["Advanced Invader"].id
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

# Encounters in which you have to kill all enemies on a tile in order
# to leave that tile, therefore normal encounter model limits do not apply.
# These encounters will be generated one tile at a time, and the app
# will mix and match them.
# Some of these have funky settings in all_encounters.json to increase
# variety.
# Eye of the Storm is not included here because it only has 6 enemies
# to begin with and it works better when not generated at the tile level.
modelLimitBreaks = {
    "Central Plaza",
    "Death's Precipice",
    "Lost Chapel",
    "The Grand Hall"
}

# These are enemies that shouldn't be the target for the special rules
# in Deathly Freeze (increases range to 1 and adds node attack) because
# these enemies attack as part of their movement and the rule interaction
# would just be confusing.
deathlyFreezeEnemyBlacklist = {
    enemiesDict["Bonewheel Skeleton"].id,
    enemiesDict["Crow Demon"].id,
    enemiesDict["Ironclad Soldier"].id,
    enemiesDict["Large Hollow Soldier"].id,
    enemiesDict["Skeleton Beast"].id,
    enemiesDict["Skeleton Soldier"].id,
    enemiesDict["Snow Rat"].id
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
    if e != "Puppet Master":
        continue
        skip = False
    # if skip:
    #     continue
    encounter = enc[e]
    print(e)

    alternatives = dict()
    combosDict = dict()
    diffMod = 0.1
    enemyCount = 0
    rangedCount = 0
    difficulty = 0
    enemies = []
    for tile in encounter["tiles"]:
        enemies += encounter["tiles"][tile]["enemies"] + encounter["tiles"][tile]["spawns"]

    enemyCount = sum([1 for enemy in enemies if enemy not in invaders])
    rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1])
    difficulty = sum([enemyIds[enemy].difficulty * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])
    separated = False

    # Depths of the Cathedral is such a beast I'm cheating the way I do it.
    # It basically never finishes running otherwise.
    if e == "Depths of the Cathedral":
        # The gang consists of 6 melee and 3 ranged.
        hollowMelee = combinations(([hollowSoldier] * 6) + ([phalanxHollow] * 6), 6)
        hollowRanged = combinations(([crossbowHollow] * 3) + ([firebombHollow] * 3), 3)
        skeletonMelee = combinations(([skeletonSoldier] * 6) + ([falchionSkeleton] * 6), 6)
        skeletonRanged = combinations(([skeletonArcher] * 3), 3)
        skeletonGangs = set([p[0] + p[1] for p in product(list(skeletonMelee), list(skeletonRanged))])
        hollowGangs = set([p[0] + p[1] for p in product(list(hollowMelee), list(hollowRanged))])
        gangs = [a for a in hollowGangs] + [a for a in skeletonGangs] + [([alonneSwordKnight] * 6) + ([alonneBowKnight] * 3)]

        nonGangs = (
            [enemiesDict["Demonic Foliage"].id] * 2
            + [enemiesDict["Engorged Zombie"].id] * 2
            + [enemiesDict["Plow Scarecrow"].id] * 3
            + [enemiesDict["Shears Scarecrow"].id] * 3
            + [enemiesDict["Silver Knight Greatbowman"].id] * 3
            + [enemiesDict["Silver Knight Spearman"].id] * 3
            + [enemiesDict["Silver Knight Swordsman"].id] * 3
            + [enemiesDict["Snow Rat"].id] * 2
        )

        higherHealthEnemies = (
            [enemiesDict["Alonne Knight Captain"].id] * 3
            + [enemiesDict["Crow Demon"].id] * 2
            + [enemiesDict["Giant Skeleton Archer"].id] * 2
            + [enemiesDict["Giant Skeleton Soldier"].id] * 2
            + [enemiesDict["Ironclad Soldier"].id] * 3
            + [enemiesDict["Large Hollow Soldier"].id] * 2
            + [enemiesDict["Mimic"].id]
            + [enemiesDict["Mushroom Child"].id]
            + [enemiesDict["Mushroom Parent"].id]
            + [enemiesDict["Phalanx"].id]
            + [enemiesDict["Sentinel"].id] * 2
            + [enemiesDict["Stone Guardian"].id] * 2
            + [enemiesDict["Stone Knight"].id] * 2
        )

        allCombos = []
        for gang in gangs:
            higherHealthCombos = set(combinations([enemyIds[en].id for en in higherHealthEnemies], 2))
            for hh in higherHealthCombos:
                nonGangCombos = set(combinations([enemyIds[en].id for en in nonGangs], 3))
                for combo in nonGangCombos:
                    allCombos.append(tuple(gang) + tuple(hh) + tuple(combo))
                
        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo])].add(combo) for combo in allCombos if (
            difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty for enemy in combo]) <= difficulty * (1 + diffMod)
            and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount))]
    # For whatever reason, Corvian Host basically takes up all my memory. Not quite enough to cause the script to fail, but
    # I bet if more enemies are added it would.
    elif e == "Corvian Host":
        smallEnemies = [enemyIds[enemy].id for enemy in allEnemies if enemyIds[enemy].health == 1]
        smallEnemyCombos = combinations(smallEnemies, 4)
        bigEnemies = list(set([enemyIds[enemy].id for enemy in allEnemies if enemyIds[enemy].health >= 5 and enemyIds[enemy].numberOfModels > 1]))
        enemyCount = 8
        rangedCount = 4

        allCombos = [combo[0] + tuple([combo[1]] * 4) for combo in product(smallEnemyCombos, bigEnemies)]

        combosDict = defaultdict(set)
        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo])].add(combo) for combo in allCombos if (
            difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty for enemy in combo]) <= difficulty * (1 + diffMod)
            and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
            and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6)]
    # Encounters that can break model limits because characters can't enter certain tiles until enemies are killed.
    # These have a flag that marks these encounters.
    # Enemies are generated at the tile level and saved that way.
    # Then DSBG-Shuffle will stitch them together when needed.
    elif e in modelLimitBreaks:
        separated = True
        combosDict = {}

        for tile in encounter["tiles"]:
            enemies = encounter["tiles"][tile]["enemies"] + encounter["tiles"][tile]["spawns"]
            enemyCount = sum([1 for enemy in enemies if enemy not in invaders])
            rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1])
            difficulty = sum([enemyIds[enemy].difficulty * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])
            combosDict[tile] = defaultdict(set)

            # Generate all combinations of enemies, excluding invaders.
            # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
            allCombos = list(set(combinations([enemyIds[en].id for en in allEnemies if (
                en not in invaders
                and (enemyIds[en].health in {
                        enemyIds[enemies[0]].health,
                        5 if enemyIds[enemies[0]].health == 10 else enemyIds[enemies[0]].health
                    } if enemyCount == 1 else enemyIds[en].health)
                )], enemyCount)))

            # Create a dictionary of alternatives, put into keys that are the
            # sets in which those enemies are found.
            # Encounters with Crystal Lizards always require Iron Keep.
            # Black Hollow Mage increases the difficulty of skeleton enemies since
            # they resurrect defeated skeletons.
            comboSet = [tuple(combo) for combo in allCombos if (
                        difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
                        and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                            or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                        and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                        # Black Hollow Mages need to be with at least one "skeleton" enemy
                        and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0))]
    
            tileCombosDict = defaultdict(set)

            [tileCombosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in comboSet]
            
            combosDict[tile] = tileCombosDict
    elif enemyCount < 7:
        # Generate all combinations of enemies, excluding invaders and old style mimics.
        # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
        allCombos = list(set(combinations([enemyIds[en].id for en in allEnemies if (
            en not in invaders
            and (enemyIds[en].health in {
                    enemyIds[enemies[0]].health,
                    5 if enemyIds[enemies[0]].health == 10 else enemyIds[enemies[0]].health
                } if enemyCount == 1 else enemyIds[en].health)
            )], enemyCount)))

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
            # Black Hollow Mages need to be with at least one "skeleton" enemy
            and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
            # Enemies must be different
            and (e not in set(["Abandoned and Forgotten", "The First Bastion"]) or len(combo) == len(set(combo)))
            # Two enemies with 5 health
            and (e != "Puppet Master" or [enemyIds[enemy].health >= 5 for enemy in combo].count(True) == 2)
            # No more than one of the two strongest enemies
            and (e != "Trecherous Tower" or (combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1 and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[1]) == 1))
            # One of the strongest enemy
            and (e != "Cold Snap" or combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1)
            # A pair of enemies
            and (e != "Corrupted Hovel" or any([combo.count(enemy) == 2 for enemy in combo]))
            # Two pairs of enemies and the pairs can't contain the strongest enemy
            and (e != "Gleaming Silver" or (len(set([enemy for enemy in combo if combo.count(enemy) == 2])) == 2 and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1))
            # Two of the weakest 1 health enemy
            and (e not in set(["Skeletal Spokes", "The Shine of Gold"]) or ([enemy for enemy in combo if enemyIds[enemy].health == 1] and combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty)[0]) == 2))
            # Three of the weakest 1 health enemy, also no poison causing enemies
            and (e != "Shattered Keep" or (
                combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty)[0]) == 3
                and all(["poison" not in enemyIds[enemy].attackEffect for enemy in combo])))
            # Four of the same gang
            and (e != "Flooded Fortress" or (sum([1 for enemy in combo if enemyIds[enemy].gang]) == 4 and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 4))
            # Five of the same gang
            and (e not in set(["Undead Sanctum", "The Fountainhead"]) or (sum([1 for enemy in combo if enemyIds[enemy].gang]) == 5 and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 5))
            # No poison causing enemies
            and (e != "Rain of Filth" or all(["poison" not in enemyIds[enemy].attackEffect for enemy in combo]))
            # One of the strongest enemy and either 4 of the weakest enemy or 2 pairs of the two weakest enemies
            and (e != "Eye of the Storm" or (
                (combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty)[0]) == 4
                    or (combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty)[0]) == 2
                        and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty)[2]) == 2))
                and combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 1))
        )]
    # 6 enemies seems to be the limit for generating all combinations of enemies
    # in a reasonable amount of time.  For encounters with more than that, we're
    # going to take a sample instead.
    else:
        combosDict = defaultdict(set)
        comboCount = []
        shuffledEnemies = allEnemies

        # Go through expansions and pairs of expansions and generate all combos.
        expansions = list(set([enemyIds[enemy].expansion for enemy in allEnemies]))
        for x in range(1, 3):
            for expCombo in combinations(expansions, x):
                expEnemies = [enemy for enemy in allEnemies if enemyIds[enemy].expansion in expCombo]
                # Generate all combinations of enemies, excluding invaders and old style mimics.
                # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
                allCombos = list(set(combinations([enemyIds[en].id for en in expEnemies if (
                    en not in invaders
                    and (enemyIds[en].health in {
                            enemyIds[enemies[0]].health,
                            5 if enemyIds[enemies[0]].health == 10 else enemyIds[enemies[0]].health
                        } if enemyCount == 1 else enemyIds[en].health)
                    )], enemyCount)))

                # Create a dictionary of alternatives, put into keys that are the
                # sets in which those enemies are found.
                # Encounters with Crystal Lizards always require Iron Keep.
                # Black Hollow Mage increases the difficulty of skeleton enemies since
                # they resurrect defeated skeletons.
                [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
                    difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
                    and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                        or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                    and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                    # Black Hollow Mages need to be with at least one "skeleton" enemy
                    and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
                    # Two of the strongest 1 health enemy
                    and (e != "Frozen Revolutions" or combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2)
                    # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                    and (e != "Deathly Freeze" or (
                        combo.count(sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2
                        and sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0] not in deathlyFreezeEnemyBlacklist))
                    # Two of the second strongest enemy (second strongest cannot also be the first strongest)
                    and (e != "Trophy Room" or (combo.count(sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[1]) == 2
                                                and sorted([enemy for enemy in combo], key=lambda x: enemyIds[x].difficulty, reverse=True)[1] == sorted(list(set([enemy for enemy in combo])), key=lambda x: enemyIds[x].difficulty, reverse=True)[1]))
                    # Three of the same gang
                    and (e != "Deathly Tolls" or (Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1) and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 3))
                    # Five of the same gang
                    and (e != "Twilight Falls" or (Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1) and Counter([enemyIds[enemy].gang for enemy in combo if enemyIds[enemy].gang]).most_common(1)[0][1] == 5))
                )]

        shuffledEnemies = allEnemies
        # In total, we're looking for up to 500,000 combinations but we'll trim that down later.
        while sum((len(combosDict[sets]) for sets in combosDict)) < 500000:
            # Combinations go by the order of the iterable it's reading from,
            # so shuffling the order of the enemies will give us different
            # combinations.
            # We're also going to keep the same distribution of 1 health and 5+ health enemies.
            # Otherwise this just takes a lot longer.
            shuffle(shuffledEnemies)
            while sorted([enemyIds[enemy].health for enemy in shuffledEnemies[:enemyCount]], key=lambda x: enemyIds[x].health, reverse=True) != sorted([enemyIds[enemy].health for enemy in enemies if enemyIds[enemy].health > 0], key=lambda x: enemyIds[x].health, reverse=True):
                shuffle(shuffledEnemies)

            # Grab the first 50,000 combinations.
            allCombos = list(islice(combinations([en for en in shuffledEnemies if en not in invaders], enemyCount), 50000))

            # Create the dictionary with the enemy sets as keys.
            [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos if (
                difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in combo]) <= difficulty * (1 + diffMod)
                and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                    or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                # Black Hollow Mages need to be with at least one "skeleton" enemy
                and (blackHollowMage not in combo or [enemy in skeletons for enemy in combo].count(True) > 0)
                # Two of the strongest 1 health enemy
                and (e != "Frozen Revolutions" or combo.count(sorted([enemy for enemy in combo if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2)
                # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                and (e != "Deathly Freeze" or (
                    combo.count(sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0]) == 2
                    and sorted(combo, key=lambda x: enemyIds[x].difficulty, reverse=True)[0] not in deathlyFreezeEnemyBlacklist))
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
            # Deathly Freeze is an example of this.
            if len(comboCount) >= 100 and len(set(comboCount[-100:])) == 1:
                print("\tBreaking")
                break

        if max([len(k) for k in combosDict]) < 3:
            print(len(comboCount))
            print(len(set(comboCount[-100:])))
            input("SOMETHING'S WRONG!")

    if len(combosDict) == 0:
        input("SOMETHING'S WRONG!")

    # This is manually set for each encounter in the JSON file.
    # enemySlots is the number of enemies in each row following this pattern:
    # [Tile 1 Row 1, Tile 1 Row 2, Tile 1 Row 3 (level 3 only), Tile 1 Row 4 (level 3 only), Tile 2 Row 1, Tile 2 Row 2, Tile 3 Row 3]
    with open(path.join(baseFolder + "\\encounters", e + ".json")) as ef:
        thisEnc = load(ef)
    alternatives["enemySlots"] = thisEnc.get("enemySlots")
        
    # For each key in the dictionary, shuffle the enemy combos,
    # then trim it down so we keep at most 1000 values per key.
    if e in modelLimitBreaks:
        alternatives["alternatives"] = dict()

        for tile in combosDict:
            for expansionCombo in combosDict[tile]:
                combosDict[tile][expansionCombo] = list(combosDict[tile][expansionCombo])
                shuffle(combosDict[tile][expansionCombo])
                combosDict[tile][expansionCombo] = combosDict[tile][expansionCombo][:min([len(combosDict[tile][expansionCombo]), 1000])]

            # If there's a standard invader, add that to each combo.
            if stdInvader in enemies:
                for combos in combosDict[tile]:
                    newCombos = []
                    for combo in combosDict[tile][combos]:
                        newCombos.append(tuple([stdInvader] + list(combo)))
                    combosDict[tile][combos] = newCombos
                        
            # If there's an advanced invader, add that to each combo.
            if advInvader in enemies:
                for combos in combosDict[tile]:
                    newCombos = []
                    for combo in combosDict[tile][combos]:
                        newCombos.append(tuple([advInvader] + list(combo)))
                    combosDict[tile][combos] = newCombos

            # Put the alternative enemies in the same difficulty order as the
            # original enemies. This way I can just iterate through the list
            # when we load the encounter and take the enemies in order.
            alternatives["alternatives"][tile] = {",".join([k for k in key]): list(value) for key, value in combosDict[tile].items()}

            # Alternative enemy order by difficulty matching original enemy order.
            alternatives["alternatives"][tile] = {",".join([k for k in key]): list(value) for key, value in combosDict[tile].items()}
            for expansionCombo in alternatives["alternatives"][tile]:
                newAlts = []
                for alt in alternatives["alternatives"][tile][expansionCombo]:
                    newAlt = []
                    altDifficulty = sorted(alt, key=lambda x: enemyIds[x].difficulty)
                    for ord in enc[e]["difficultyOrder"][tile]:
                        newAlt.append(altDifficulty[ord])
                    if newAlt not in newAlts:
                        newAlts.append(newAlt)
                alternatives["alternatives"][tile][expansionCombo] = newAlts

            # Account for duplicate enemies in the newer core sets that are essentially redoing the older stuff.
            # The Sunless City
            for combo in [c for c in alternatives["alternatives"][tile] if "Dark Souls The Board Game" in c and not "The Sunless City" in c]:
                toAdd = []
                for alt in alternatives["alternatives"][tile][combo]:
                    if (alt.count(crossbowHollow) <= 3
                        and alt.count(hollowSoldier) <= 3
                        and alt.count(silverKnightGreatbowman) <= 2
                        and alt.count(silverKnightSwordsman) <= 2
                        and alt.count(phalanx) <= 1):
                        toAdd.append(alt)
                    
                if toAdd:
                    alternatives["alternatives"][tile][combo.replace("Dark Souls The Board Game", "The Sunless City")] = toAdd

            if e not in encMain:
                encMain[e] = {
                    "name": enc[e]["name"],
                    "expansion": enc[e]["expansion"],
                    "level": enc[e]["level"],
                    "expansionCombos": {tile: [str(k).split(",") for k in alternatives["alternatives"][tile].keys()]}
                    }
            else:
                encMain[e]["expansionCombos"][tile] = [str(k).split(",") for k in alternatives["alternatives"][tile].keys()] if [str(k).split(",") for k in alternatives["alternatives"][tile].keys()] else []
    else:
        for expansionCombo in combosDict:
            combosDict[expansionCombo] = list(combosDict[expansionCombo])
            shuffle(combosDict[expansionCombo])
            combosDict[expansionCombo] = combosDict[expansionCombo][:min([len(combosDict[expansionCombo]), 1000])]

        # If there's a standard invader, add that to each combo.
        if stdInvader in enemies:
            for combos in combosDict:
                newCombos = []
                for combo in combosDict[combos]:
                    newCombos.append(tuple([stdInvader] + list(combo)))
                combosDict[combos] = newCombos
                    
        # If there's an advanced invader, add that to each combo.
        if advInvader in enemies:
            for combos in combosDict:
                newCombos = []
                for combo in combosDict[combos]:
                    newCombos.append(tuple([advInvader] + list(combo)))
                combosDict[combos] = newCombos

        # Put the alternative enemies in the same difficulty order as the
        # original enemies. This way I can just iterate through the list
        # when we load the encounter and take the enemies in order.

        alternatives["alternatives"] = {",".join([k for k in key]): list(value) for key, value in combosDict.items()}

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

        # Account for duplicate enemies in the newer core sets that are essentially redoing the older stuff.
        # The Sunless City
        for combo in [c for c in alternatives["alternatives"] if "Dark Souls The Board Game" in c and not "The Sunless City" in c]:
            toAdd = []
            for alt in alternatives["alternatives"][combo]:
                if (alt.count(crossbowHollow) <= 3
                    and alt.count(hollowSoldier) <= 3
                    and alt.count(silverKnightGreatbowman) <= 2
                    and alt.count(silverKnightSwordsman) <= 2
                    and alt.count(phalanx) <= 1):
                    toAdd.append(alt)
                
            if toAdd:
                alternatives["alternatives"][combo.replace("Dark Souls The Board Game", "The Sunless City")] = toAdd

        if e not in encMain:
            encMain[e] = {
                "name": enc[e]["name"],
                "expansion": enc[e]["expansion"],
                "level": enc[e]["level"],
                "expansionCombos": [str(k).split(",") for k in alternatives["alternatives"].keys()]
                }
        else:
            encMain[e]["expansionCombos"] = [str(k).split(",") for k in alternatives["alternatives"].keys()]
            
    with open(baseFolder + "\\encounters\\" + e + ".json", "w") as encountersFile:
        dump(alternatives, encountersFile)

    with open(baseFolder + "\\encounters.json", "w") as ef:
        dump(encMain, ef)
