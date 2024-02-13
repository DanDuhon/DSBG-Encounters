from os import path
from json import load, dump
from itertools import combinations, islice, product, filterfalse
from random import shuffle
from collections import defaultdict
from glob import glob

from enemies import enemyIds, enemiesDict

baseFolder = path.dirname(__file__)
allEnemies = []
alonneBowKnight = enemiesDict["Alonne Bow Knight"].id
alonneSwordKnight = enemiesDict["Alonne Sword Knight"].id
blackHollowMage = enemiesDict["Black Hollow Mage"].id
bonewheelSkeleton = enemiesDict["Bonewheel Skeleton"].id
crossbowHollow = enemiesDict["Crossbow Hollow"].id
falchionSkeleton = enemiesDict["Falchion Skeleton"].id
firebombHollow = enemiesDict["Firebomb Hollow"].id
hollowSoldier = enemiesDict["Hollow Soldier"].id
mimic = enemiesDict["Mimic"].id
phalanx = enemiesDict["Phalanx"].id
phalanxHollow = enemiesDict["Phalanx Hollow"].id
sentinel = enemiesDict["Sentinel"].id
silverKnightSwordsman = enemiesDict["Silver Knight Swordsman"].id
silverKnightSpearman = enemiesDict["Silver Knight Spearman"].id
silverKnightGreatbowman = enemiesDict["Silver Knight Greatbowman"].id
skeletonArcher = enemiesDict["Skeleton Archer"].id
skeletonSoldier = enemiesDict["Skeleton Soldier"].id

skeletons = set([enemiesDict[e].id for e in enemiesDict if "Skeleton" in enemiesDict[e].name])
invaders = set()
invaders.add(enemiesDict["Armorer Dennis"].id)
invaders.add(enemiesDict["Fencer Sharron"].id)
invaders.add(enemiesDict["Invader Brylex"].id)
invaders.add(enemiesDict["Kirk, Knight of Thorns"].id)
invaders.add(enemiesDict["Longfinger Kirk"].id)
invaders.add(enemiesDict["Maldron the Assassin"].id)
invaders.add(enemiesDict["Maneater Mildred"].id)
invaders.add(enemiesDict["Marvelous Chester"].id)
invaders.add(enemiesDict["Melinda the Butcher"].id)
invaders.add(enemiesDict["Oliver the Collector"].id)
invaders.add(enemiesDict["Paladin Leeroy"].id)
invaders.add(enemiesDict["Xanthous King Jeremiah"].id)
invaders.add(enemiesDict["Hungry Mimic"].id)
invaders.add(enemiesDict["Voracious Mimic"].id)

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

gangEncounters = {
    "Undead Sanctum",
    "The Fountainhead",
    "Deathly Tolls",
    "Flooded Fortress",
    "Depths of the Cathedral",
    "Twilight Falls"
}

# For these encounters, it made more sense to sort the enemies
# by toughness rather than difficulty.
toughnessSortedEncounters = {
    "Deathly Freeze",
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


def check_if_valid(encounter, combo, difficulty, rangedCount):
    comboDifficulty = sum([enemyIds[enemy].difficulty[characterCount] * (1.5 if enemy in skeletons and blackHollowMage in combo else 1) for enemy in combo])
    comboRangedCount = sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3])
    comboHigherHealthCount = sum([1 for enemy in combo if enemyIds[enemy].health >= 5])

    return (difficulty * 0.9 <= comboDifficulty <= difficulty * 1.1
        and comboRangedCount == rangedCount
        and comboHigherHealthCount == higherHealthCount
        and sum([1 for enemy in combo if enemy in invaders]) == invaderCount
        # Can't have more enemies than available models and Phalanx is 3 Phalanx Hollows shoved together
        and ((3 if phalanx in combo else 0) + combo.count(phalanxHollow) < 6 or encounter == "Eye of the Storm")
        # Black Hollow Mages need to be with at least one "skeleton" enemy
        and (blackHollowMage not in combo or set(combo) & skeletons))

try:
    # skip = True
    for e in enc:
        # if e not in  {"Cold Snap", "Corrupted Hovel", "Deathly Freeze"}:
        #     continue
        #     skip = False
        # if skip:
        #     continue
        encounter = enc[e]

        for characterCount in range(1, 5):
            # Don't process an encounter already being processed.
            if glob(baseFolder + "\\combine\\" + e + str(characterCount) + ".json"):
                continue

            # Put a temporary file out there so we know it's being processed.
            with open(baseFolder + "\\combine\\" + e + str(characterCount) + ".json", "w") as ef:
                dump({}, ef)

            print(e + " " + str(characterCount))
            alternatives = dict()
            enemies = []
            for tile in encounter["tiles"]:
                enemies += encounter["tiles"][tile]["enemies"] + encounter["tiles"][tile]["spawns"]

            enemyCount = len(enemies)
            rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) == 4])
            invaderCount = sum([1 for enemy in enemies if enemy in invaders])
            higherHealthCount = sum([1 for enemy in enemies if enemyIds[enemy].health >= 5 and enemy not in invaders])
            difficulty = sum([enemyIds[enemy].difficulty[characterCount] * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])

            # All the gang encounters are very restrictive, so we do them custom a bit.
            # Otherwise they take far longer to process.
            if e in gangEncounters:
                gangMeleeCount =  enemies.count(hollowSoldier)
                gangRangedCount =  enemies.count(crossbowHollow)
                nonGangCount = len(enemies) - gangMeleeCount - gangRangedCount - higherHealthCount
                
                hollowMelee = combinations(([hollowSoldier] * gangMeleeCount) + ([phalanxHollow] * gangMeleeCount), gangMeleeCount)
                hollowRanged = combinations(([crossbowHollow] * gangRangedCount) + ([firebombHollow] * gangRangedCount), gangRangedCount)
                silverKnightMelee = combinations(([silverKnightSwordsman] * gangMeleeCount) + ([silverKnightSpearman] * gangMeleeCount), gangMeleeCount)
                silverKnightRanged = combinations(([silverKnightGreatbowman] * gangRangedCount), gangRangedCount)
                skeletonMelee = combinations(([skeletonSoldier] * gangMeleeCount) + ([falchionSkeleton] * gangMeleeCount) + ([bonewheelSkeleton] * gangMeleeCount), gangMeleeCount)
                skeletonRanged = combinations(([skeletonArcher] * gangRangedCount), gangRangedCount)
                silverKnightGangs = set([p[0] + p[1] for p in product(list(silverKnightMelee), list(silverKnightRanged))])
                skeletonGangs = set([p[0] + p[1] for p in product(list(skeletonMelee), list(skeletonRanged))])
                hollowGangs = set([p[0] + p[1] for p in product(list(hollowMelee), list(hollowRanged))])
                gangs = [a for a in hollowGangs] + [a for a in skeletonGangs] + [a for a in silverKnightGangs] + [([alonneSwordKnight] * gangMeleeCount) + ([alonneBowKnight] * gangRangedCount)]

                nonGangs = (
                    [enemiesDict["Demonic Foliage"].id] * 2
                    + [enemiesDict["Engorged Zombie"].id] * 2
                    + [enemiesDict["Plow Scarecrow"].id] * 3
                    + [enemiesDict["Shears Scarecrow"].id] * 3
                    + [enemiesDict["Snow Rat"].id] * 2
                    + [enemiesDict["Hollow Soldier"].id] * 3
                    + [enemiesDict["Phalanx Hollow"].id] * 3
                    + [enemiesDict["Bonewheel Skeleton"].id] * 3
                    + [enemiesDict["Falchion Skeleton"].id] * 3
                    + [enemiesDict["Skeleton Soldier"].id] * 3
                    + [enemiesDict["Silver Knight Swordsman"].id] * 3
                    + [enemiesDict["Silver Knight Spearman"].id] * 3
                    + [enemiesDict["Alonne Sword Knight"].id] * 3
                    + [enemiesDict["Alonne Bow Knight"].id] * 3
                    + [enemiesDict["Silver Knight Greatbowman"].id] * 3
                    + [enemiesDict["Skeleton Archer"].id] * 3
                    + [enemiesDict["Crossbow Hollow"].id] * 3
                    + [enemiesDict["Firebomb Hollow"].id] * 3
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
                    + [enemiesDict["Necromancer"].id] * 2
                    + [enemiesDict["Black Hollow Mage"].id] * 2
                )

                higherHealthCombos = set(combinations([enemyIds[en].id for en in higherHealthEnemies], higherHealthCount))
                nonGangCombos = set(combinations([enemyIds[en].id for en in nonGangs], nonGangCount))
                allCombos = [tuple(list(p[0]) + list(p[1]) + list(p[2])) for p in product(gangs, nonGangCombos, higherHealthCombos) if check_if_valid(e, list(p[0]) + list(p[1]) + list(p[2]), difficulty, rangedCount) and not set(p[0]) & set(p[1])]
                        
                combosDict = defaultdict(set)
                [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos]
            # For whatever reason, Corvian Host basically takes up all my memory. Not quite enough to cause the script to fail, but
            # I bet if more enemies are added it would.
            elif e == "Corvian Host":
                smallEnemies = [enemyIds[enemy].id for enemy in allEnemies if enemyIds[enemy].health == 1]
                smallEnemyCombos = combinations(smallEnemies, 4)
                bigEnemies = list(set([enemyIds[enemy].id for enemy in allEnemies if enemyIds[enemy].health >= 5 and enemyIds[enemy].numberOfModels > 1]))
                enemyCount = 8
                rangedCount = 4

                allCombos = [combo[0] + tuple([combo[1]] * 4) for combo in product(smallEnemyCombos, bigEnemies) if check_if_valid(e, combo[0] + tuple([combo[1]] * 4), difficulty, rangedCount)]

                combosDict = defaultdict(set)
                [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos]
            # Encounters that can break model limits because characters can't enter certain tiles until enemies are killed.
            # These have a flag that marks these encounters.
            # Enemies are generated at the tile level and saved that way.
            # Then DSBG-Shuffle will stitch them together when needed.
            elif e in modelLimitBreaks:
                combosDict = {}

                for tile in encounter["tiles"]:
                    enemies = encounter["tiles"][tile]["enemies"] + encounter["tiles"][tile]["spawns"]
                    enemyCount = len(enemies)
                    invaderCount = sum([1 for enemy in enemies if enemy in invaders])
                    rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1 and enemy not in invaders])
                    higherHealthCount = sum([1 for enemy in enemies if enemyIds[enemy].health >= 5 and enemy not in invaders])
                    difficulty = sum([enemyIds[enemy].difficulty[characterCount] * enemies.count(enemy) for enemy in enemyIds if enemy in enemies])
                    combosDict[tile] = defaultdict(set)

                    # Generate all combinations of enemies.
                    allCombos = list(set(filterfalse(lambda s: not check_if_valid(e, s, difficulty, rangedCount), combinations(allEnemies, enemyCount))))

                    # Create a dictionary of alternatives, put into keys that are the
                    # sets in which those enemies are found.
                    # Encounters with Crystal Lizards always require Iron Keep.
                    # Black Hollow Mage increases the difficulty of skeleton enemies since
                    # they resurrect defeated skeletons.
                    comboSet = [tuple(combo) for combo in allCombos]
            
                    tileCombosDict = defaultdict(set)

                    [tileCombosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in comboSet]
                    
                    combosDict[tile] = tileCombosDict
            elif enemyCount < 7:
                # Generate all combinations of enemies.
                allCombos = list(set(filterfalse(lambda s: not (
                        check_if_valid(e, s, difficulty, rangedCount)
                        # Enemies must be different
                        and (e not in set(["Abandoned and Forgotten", "The First Bastion"]) or len(s) == len(set(s)))
                        # No more than one of the two strongest enemies
                        and (e != "Trecherous Tower" or (s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 1))
                        # One of the toughest enemy
                        and (e != "Cold Snap" or s.count(sorted(s, key=lambda x: (-enemyIds[x].toughness, enemyIds[x].difficulty[characterCount]), reverse=True)[0]) == 1)
                        # Two of the toughest enemy
                        and (e != "Corrupted Hovel" or s.count(sorted(s, key=lambda x: (-enemyIds[x].toughness, enemyIds[x].difficulty[characterCount]), reverse=True)[0]) == 2)
                        # One of the weakest enemy and one of the strongest
                        and (e != "Gleaming Silver" or (s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 1))
                        # Two of the strongest enemy
                        and (e != "Skeletal Spokes" or s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2)
                        # Two of the weakest enemy
                        and (e != "The Shine of Gold" or s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 2)
                        # One of the strongest enemy and the rest can't cause poison
                        and (e != "Shattered Keep" or (
                            s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1
                            and sorted([enemy for enemy in s if all(["poison" not in enemyIds[enemy].attackEffect])], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1:]))
                       # No poison causing enemies
                        and (e != "Rain of Filth" or all(["poison" not in enemyIds[enemy].attackEffect for enemy in s]))
                        # One of the second strongest enemy and either 4 of the weakest enemy or 2 pairs of the two weakest enemies
                        and (e != "Eye of the Storm" or (
                            (s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 4
                                or (s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 2
                                    and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount])[2]) == 2))
                            and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 1))),
                    combinations([enemyIds[en].id for en in allEnemies if (
                    (en not in invaders or invaderCount > 0))], enemyCount))))

                # Create a dictionary of alternatives, put into keys that are the
                # sets in which those enemies are found.
                # Encounters with Crystal Lizards always require Iron Keep.
                # Black Hollow Mage increases the difficulty of skeleton enemies since
                # they resurrect defeated skeletons.
                combosDict = defaultdict(set)
                [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos]
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
                        # Generate all combinations of enemies.
                        allCombos = list(set(filterfalse(lambda s: not (
                                check_if_valid(e, s, difficulty, rangedCount)
                                # Two of the strongest enemy
                                and (e != "Frozen Revolutions" or s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2)
                                # Two of the toughest single target melee enemy and that enemy isn't in the blacklist
                                and (e != "Deathly Freeze" or (
                                    sum([1 for enemy in s if enemy not in deathlyFreezeEnemyBlacklist and (max(enemyIds[enemy].attackRange) < 2 or True not in set(enemyIds[enemy].nodeAttack)) and enemy == sorted(s, key=lambda x: (-enemyIds[x].toughness, enemyIds[x].difficulty[characterCount]), reverse=True)[0]]) == 2))
                                    # sum([1 for enemy in s if all([max([attack < 1 for attack in enemyIds[enemy].attackRange]), True not in enemyIds[enemy].nodeAttack]) and enemy not in deathlyFreezeEnemyBlacklist]) == 2
                                    # and sum([enemy for enemy in s if all([max([attack < 1 for attack in enemyIds[enemy].attackRange]), True not in enemyIds[enemy].nodeAttack]) and enemy not in deathlyFreezeEnemyBlacklist and (enemy, enemyIds[enemy].toughness, enemyIds[enemy].difficulty[characterCount]) == sorted([(enemy, enemyIds[enemy].toughness, enemyIds[enemy].difficulty[characterCount]) for enemy in s if all([max([attack < 1 for attack in enemyIds[enemy].attackRange]), True not in enemyIds[enemy].nodeAttack]) and enemy not in deathlyFreezeEnemyBlacklist], key=lambda x: (-enemyIds[x[0]].toughness, enemyIds[x[0]].difficulty[characterCount]), reverse=True)[0]]) == 2))
                                # One of the strongest enemy and either two of the second strongest or two that are the second and third strongest
                                and (e != "Trophy Room" or (
                                    (
                                        s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1
                                        and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 2)
                                    or (
                                        s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1
                                        and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 1
                                        and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[2]) == 1)
                                    ))),
                            combinations([enemyIds[en].id for en in expEnemies if en not in invaders or invaderCount > 0], enemyCount))))

                        # Create a dictionary of alternatives, put into keys that are the
                        # sets in which those enemies are found.
                        # Encounters with Crystal Lizards always require Iron Keep.
                        # Black Hollow Mage increases the difficulty of skeleton enemies since
                        # they resurrect defeated skeletons.
                        [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos]

                for expansionCombo in combosDict:
                    combosDict[expansionCombo] = list(combosDict[expansionCombo])
                    shuffle(combosDict[expansionCombo])
                    combosDict[expansionCombo] = set(combosDict[expansionCombo][:min([len(combosDict[expansionCombo]), 10000])])

                shuffledEnemies = allEnemies
                # In total, we're looking for up to 500,000 combinations but we'll trim that down later.
                while sum((len(combosDict[sets]) for sets in combosDict)) < 500000:
                    # Combinations go by the order of the iterable it's reading from,
                    # so shuffling the order of the enemies will give us different
                    # combinations.
                    # We're also going to keep the same distribution of 1 health and 5+ health enemies.
                    # Otherwise this just takes a lot longer.
                    shuffle(shuffledEnemies)
                    while sorted([enemyIds[enemy].health for enemy in shuffledEnemies[:enemyCount] if enemy not in invaders], key=lambda x: enemyIds[x].health, reverse=True) != sorted([enemyIds[enemy].health for enemy in enemies if enemy not in invaders], key=lambda x: enemyIds[x].health, reverse=True):
                        shuffle(shuffledEnemies)

                    # Grab the first 50,000 combinations.
                    allCombos = list(filterfalse(lambda s: not (
                                check_if_valid(e, s, difficulty, rangedCount)
                                # Two of the strongest enemy
                                and (e != "Frozen Revolutions" or s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2)
                                # Two of the toughest single target melee enemy and that enemy isn't in the blacklist
                                and (e != "Deathly Freeze" or (
                                    sum([1 for enemy in s if enemy not in deathlyFreezeEnemyBlacklist and (max(enemyIds[enemy].attackRange) < 2 or True not in set(enemyIds[enemy].nodeAttack)) and enemy == sorted(s, key=lambda x: (-enemyIds[x].toughness, enemyIds[x].difficulty[characterCount]), reverse=True)[0]]) == 2))
                                    # sum([1 for enemy in s if all([max([attack < 1 for attack in enemyIds[enemy].attackRange]), True not in enemyIds[enemy].nodeAttack]) and enemy not in deathlyFreezeEnemyBlacklist]) == 2
                                    # and sum([enemy for enemy in s if all([max([attack < 1 for attack in enemyIds[enemy].attackRange]), True not in enemyIds[enemy].nodeAttack]) and enemy not in deathlyFreezeEnemyBlacklist and (enemy, enemyIds[enemy].toughness, enemyIds[enemy].difficulty[characterCount]) == sorted([(enemy, enemyIds[enemy].toughness, enemyIds[enemy].difficulty[characterCount]) for enemy in s if all([max([attack < 1 for attack in enemyIds[enemy].attackRange]), True not in enemyIds[enemy].nodeAttack]) and enemy not in deathlyFreezeEnemyBlacklist], key=lambda x: (-enemyIds[x[0]].toughness, enemyIds[x[0]].difficulty[characterCount]), reverse=True)[0]]) == 2))
                                # One of the strongest enemy and either two of the second strongest or two that are the second and third strongest
                                and (e != "Trophy Room" or (
                                    (
                                        s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1
                                        and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 2)
                                    or (
                                        s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1
                                        and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 1
                                        and s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[2]) == 1)
                                    ))),
                            islice(combinations([en for en in shuffledEnemies if en not in invaders or invaderCount > 0], enemyCount), 50000)))

                    # Create the dictionary with the enemy sets as keys.
                    [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set())].add(combo) for combo in allCombos]

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
            with open(path.join(baseFolder + "\\encounters", e + str(characterCount) + ".json")) as ef:
                thisEnc = load(ef)
            alternatives["enemySlots"] = thisEnc.get("enemySlots")
                
            # For each key in the dictionary, shuffle the enemy combos,
            # then trim it down so we keep at most 50000 values per encounter.
            if e in modelLimitBreaks:
                # For these ones, we don't need to keep nearly as many since the tiles get combined.
                alternatives["alternatives"] = dict()

                for tile in combosDict:
                    for expansionCombo in combosDict[tile]:
                        combosDict[tile][expansionCombo] = list(combosDict[tile][expansionCombo])
                        shuffle(combosDict[tile][expansionCombo])
                        combosDict[tile][expansionCombo] = combosDict[tile][expansionCombo][:min([len(combosDict[tile][expansionCombo]), 200])]

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
                            altDifficulty = sorted(alt, key=lambda x: enemyIds[x].difficulty[characterCount])
                            for ord in enc[e]["difficultyOrder"][tile][str(characterCount)]:
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
                alts = min([50000, sum([len(combosDict[combo]) for combo in combosDict])])
                if alts == 50000:
                    keys = len(combosDict)
                    numToKeep = int(alts / keys)
                    for expansionCombo in combosDict:
                        combosDict[expansionCombo] = list(combosDict[expansionCombo])
                        shuffle(combosDict[expansionCombo])
                        combosDict[expansionCombo] = combosDict[expansionCombo][:min([len(combosDict[expansionCombo]), numToKeep])]

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
                        if e in toughnessSortedEncounters:
                            altDifficulty = sorted(alt, key=lambda x: (-enemyIds[x].toughness, enemyIds[x].difficulty[characterCount]))
                            for ord in enc[e]["difficultyOrder"][str(characterCount)]:
                                newAlt.append(altDifficulty[ord])
                        else:
                            altDifficulty = sorted(alt, key=lambda x: enemyIds[x].difficulty[characterCount])
                            for ord in enc[e]["difficultyOrder"][str(characterCount)]:
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
                        "expansionCombos": {1: [], 2: [], 3: [], 4: []}
                        }
                    
                encMain[e]["expansionCombos"][characterCount] = [str(k).split(",") for k in alternatives["alternatives"].keys()]
                    
            with open(baseFolder + "\\encounters\\" + e + str(characterCount) + ".json", "w") as encountersFile:
                dump(alternatives, encountersFile)

            with open(baseFolder + "\\combine\\" + e + str(characterCount) + ".json", "w") as ef:
                dump(encMain[e], ef)
except Exception as ex:
    input(ex)
    raise
