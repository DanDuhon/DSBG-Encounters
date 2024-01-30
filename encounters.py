from os import path
from json import load, dump
from itertools import combinations, islice, product, filterfalse
from random import shuffle
from collections import defaultdict, Counter

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

try:
    skip = True
    for e in enc:
        if e in {"Brume Tower"}:
            # continue
            skip = False
        if skip:
            continue
        encounter = enc[e]

        for characterCount in range(1, 5):
            print(e + " " + str(characterCount))
            alternatives = dict()
            combosDict = dict()
            diffMod = 0.1
            enemies = []
            for tile in encounter["tiles"]:
                enemies += encounter["tiles"][tile]["enemies"] + encounter["tiles"][tile]["spawns"]

            enemyCount = len(enemies)
            rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1])
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

                allCombos = []
                for gang in gangs:
                    higherHealthCombos = set(combinations([enemyIds[en].id for en in higherHealthEnemies], higherHealthCount))
                    for hh in higherHealthCombos:
                        nonGangCombos = set(combinations([enemyIds[en].id for en in nonGangs], nonGangCount))
                        for combo in nonGangCombos:
                            if (not set(combo) & set(gang)
                                and difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty[characterCount] for enemy in combo]) <= difficulty * (1 + diffMod)
                                and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                                    or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)):
                                continue
                            allCombos.append(tuple(gang) + tuple(hh) + tuple(combo))
                        
                combosDict = defaultdict(set)
                [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo])].add(combo) for combo in allCombos]
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
                    difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty[characterCount] for enemy in combo]) <= difficulty * (1 + diffMod)
                    and (sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                        or sum([1 for enemy in combo if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                    and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6)]
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
                    # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
                    allCombos = list(set(filterfalse(lambda s: not (
                        sum([1 for enemy in s if enemyIds[enemy].health >= 5]) == higherHealthCount
                        and difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty[characterCount] * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in s]) <= difficulty * (1 + diffMod)
                        and sum([1 for enemy in s if enemy in invaders]) == invaderCount
                        and (sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                            or sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                        and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                        # Black Hollow Mages need to be with at least one "skeleton" enemy
                        and (blackHollowMage not in s or [enemy in skeletons for enemy in s].count(True) > 0)),
                        combinations(allEnemies, enemyCount))))

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
                        sum([1 for enemy in s if enemyIds[enemy].health >= 5]) == higherHealthCount
                        and difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty[characterCount] * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in s]) <= difficulty * (1 + diffMod)
                        and sum([1 for enemy in s if enemy in invaders]) == invaderCount
                        and (sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                            or sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                        and ((3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6 or e == "Eye of the Storm")
                        # Black Hollow Mages need to be with at least one "skeleton" enemy
                        and (blackHollowMage not in s or [enemy in skeletons for enemy in s].count(True) > 0)
                        # Enemies must be different
                        and (e not in set(["Abandoned and Forgotten", "The First Bastion"]) or len(s) == len(set(s)))
                        # Two enemies with 5 health
                        and (e != "Puppet Master" or [enemyIds[enemy].health >= 5 for enemy in s].count(True) == 2)
                        # No more than one of the two strongest enemies
                        and (e != "Trecherous Tower" or (s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1 and s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 1))
                        # One of the strongest enemy
                        and (e != "Cold Snap" or s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1)
                        # A pair of enemies
                        and (e != "Corrupted Hovel" or any([s.count(enemy) == 2 for enemy in s]))
                        # Two pairs of enemies and the pairs can't contain the strongest enemy
                        and (e != "Gleaming Silver" or (len(set([enemy for enemy in s if s.count(enemy) == 2])) == 2 and s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1))
                        # Two of the weakest 1 health enemy
                        and (e not in set(["Skeletal Spokes", "The Shine of Gold"]) or ([enemy for enemy in s if enemyIds[enemy].health == 1] and s.count(sorted([enemy for enemy in s if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 2))
                        # Three of the weakest 1 health enemy, also no poison causing enemies
                        and (e != "Shattered Keep" or (
                            s.count(sorted([enemy for enemy in s if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 3
                            and all(["poison" not in enemyIds[enemy].attackEffect for enemy in s])))
                       # No poison causing enemies
                        and (e != "Rain of Filth" or all(["poison" not in enemyIds[enemy].attackEffect for enemy in s]))
                        # One of the strongest enemy and either 4 of the weakest enemy or 2 pairs of the two weakest enemies
                        and (e != "Eye of the Storm" or (
                            (s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 4
                                or (s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount])[0]) == 2
                                    and s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount])[2]) == 2))
                            and s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 1))),
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
                        # Generate all combinations of enemies, excluding invaders and old style mimics.
                        # Also make sure we don't replace a single 5 health enemy with a 1 health enemy.
                        allCombos = list(set(filterfalse(lambda s: (
                                sum([1 for enemy in s if enemyIds[enemy].health >= 5]) == higherHealthCount
                                and difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty[characterCount] * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in s]) <= difficulty * (1 + diffMod)
                                and sum([1 for enemy in s if enemy in invaders]) == invaderCount
                                and (sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                                    or sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                                and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                                # Black Hollow Mages need to be with at least one "skeleton" enemy
                                and (blackHollowMage not in s or [enemy in skeletons for enemy in s].count(True) > 0)
                                # Two of the strongest 1 health enemy
                                and (e != "Frozen Revolutions" or s.count(sorted([enemy for enemy in s if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2)
                                # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                                and (e != "Deathly Freeze" or (
                                    s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2
                                    and sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0] not in deathlyFreezeEnemyBlacklist))
                                # Two of the second strongest enemy (second strongest cannot also be the first strongest)
                                and (e != "Trophy Room" or (s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 2
                                                            and sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1] == sorted(list(set([enemy for enemy in s])), key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]))),
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
                    allCombos = list(filterfalse(lambda s: (
                                sum([1 for enemy in s if enemyIds[enemy].health >= 5]) == higherHealthCount
                                and difficulty * (1 - diffMod) <= sum([enemyIds[enemy].difficulty[characterCount] * (1.5 if enemy in skeletons and blackHollowMage in enemies else 1) for enemy in s]) <= difficulty * (1 + diffMod)
                                and sum([1 for enemy in s if enemy in invaders]) == invaderCount
                                and (sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1]) == rangedCount
                                    or sum([1 for enemy in s if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3]) == rangedCount)
                                and (3 if phalanx in enemies else 0) + enemies.count(phalanxHollow) < 6
                                # Black Hollow Mages need to be with at least one "skeleton" enemy
                                and (blackHollowMage not in s or [enemy in skeletons for enemy in s].count(True) > 0)
                                # Two of the strongest 1 health enemy
                                and (e != "Frozen Revolutions" or s.count(sorted([enemy for enemy in s if enemyIds[enemy].health == 1], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2)
                                # If there are 2 of the strongest enemy and that enemy isn't in the blacklist
                                and (e != "Deathly Freeze" or (
                                    s.count(sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0]) == 2
                                    and sorted(s, key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[0] not in deathlyFreezeEnemyBlacklist))
                                # Two of the second strongest enemy (second strongest cannot also be the first strongest)
                                and (e != "Trophy Room" or (s.count(sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]) == 2
                                                            and sorted([enemy for enemy in s], key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1] == sorted(list(set([enemy for enemy in s])), key=lambda x: enemyIds[x].difficulty[characterCount], reverse=True)[1]))),
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
            with open(path.join(baseFolder + "\\encounters", e + ".json")) as ef:
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
                        "expansionCombos": [str(k).split(",") for k in alternatives["alternatives"].keys()]
                        }
                else:
                    encMain[e]["expansionCombos"] = [str(k).split(",") for k in alternatives["alternatives"].keys()]
                    
            with open(baseFolder + "\\encounters\\" + e + str(characterCount) + ".json", "w") as encountersFile:
                dump(alternatives, encountersFile)

            with open(baseFolder + "\\encounters.json", "w") as ef:
                dump(encMain, ef)
except Exception as ex:
    input(ex)
    raise
