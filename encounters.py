import datetime
from os import path
from json import load, dump
from itertools import combinations, product, filterfalse
from random import shuffle, sample
from collections import defaultdict
from glob import glob
from copy import deepcopy

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
largeHollowSoldier = enemiesDict["Large Hollow Soldier"].id
mimic = enemiesDict["Mimic"].id
phalanx = enemiesDict["Phalanx"].id
phalanxHollow = enemiesDict["Phalanx Hollow"].id
sentinel = enemiesDict["Sentinel"].id
silverKnightSwordsman = enemiesDict["Silver Knight Swordsman"].id
silverKnightSpearman = enemiesDict["Silver Knight Spearman"].id
silverKnightGreatbowman = enemiesDict["Silver Knight Greatbowman"].id
skeletonArcher = enemiesDict["Skeleton Archer"].id
skeletonSoldier = enemiesDict["Skeleton Soldier"].id
kirks = {enemiesDict["Kirk, Knight of Thorns"].id, enemiesDict["Longfinger Kirk"].id}
mimics = {enemiesDict["Mimic"].id, enemiesDict["Hungry Mimic"].id, enemiesDict["Voracious Mimic"].id}

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

fangBoarEncounters = {
    "Broken Passageway (TSC)",
    "Parish Gates",
    "Flooded Fortress",
    "Archive Entrance",
    "Depths of the Cathedral"
}

envoyBannerEncounters = {
    "Kingdom's Messengers",
    "Deathly Tolls",
    "Grim Reunion"
}

gangEncounters = {
    "Undead Sanctum",
    "The Fountainhead",
    "Deathly Tolls",
    "Flooded Fortress",
    "Depths of the Cathedral",
    "Twilight Falls"
}

respawnEncounters = {
    "Altar of Bones",
    "Bridge Too Far",
    "Broken Passageway (TSC)",
    "Central Plaza (TSC)",
    "Deathly Tolls",
    "Last Rites",
    "The Mass Grave"
}

# For these encounters, it made more sense to sort the enemies
# by toughness rather than difficulty.
toughnessSortedEncounters = {
    "Cold Snap",
    "Dark Alleyway",
    "Deathly Freeze",
    "No Safe Haven",
    "The First Bastion",
    "Corrupted Hovel",
    "Skeleton Overlord",
    "The Shine of Gold"
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
    enemiesDict["Mushroom Parent"].id,
    enemiesDict["Skeleton Beast"].id,
    enemiesDict["Skeleton Soldier"].id,
    }

# Trophy Room makes certain enemy attacks magic. That would be confusing
# with move attacks because those are always physical and there's no
# clear way to indicate that it should do magic damage instead.
# So exclude move-attack only enemies.
# Also exclude enemies that already do magic damage.
trophyRoomEnemyBlacklist = {
    enemiesDict["Alonne Knight Captain"].id,
    enemiesDict["Black Hollow Mage"].id,
    enemiesDict["Bonewheel Skeleton"].id,
    enemiesDict["Crossbow Hollow"].id,
    enemiesDict["Crow Demon"].id,
    enemiesDict["Engorged Zombie"].id,
    enemiesDict["Firebomb Hollow"].id,
    enemiesDict["Ironclad Soldier"].id,
    enemiesDict["Large Hollow Soldier"].id,
    enemiesDict["Mushroom Parent"].id,
    enemiesDict["Necromancer"].id,
    enemiesDict["Skeleton Beast"].id,
    enemiesDict["Skeleton Soldier"].id,
    enemiesDict["Stone Knight"].id
}

for enemy in enemyIds:
    for _ in range(enemyIds[enemy].numberOfModels):
        allEnemies.append(enemy)

with open(path.join(baseFolder + "\\encounters", "all_encounters.json")) as aef:
    enc = load(aef)

with open(path.join(baseFolder, "dsbg_shuffle_encounters.json")) as ef:
    encMain = load(ef)

with open(path.join(baseFolder, "enemy_stats.json")) as vf:
    vectors = load(vf)


def get_stk(enemyId, level):
    name = enemyIds[enemyId].name
    return vectors[name][str(level)]["stk"]


def get_dps(enemyId, level):
    name = enemyIds[enemyId].name
    return vectors[name][str(level)]["dps"]


def get_volume(enemyId, level, hasBhm=False):
    vol = get_stk(enemyId, level) * get_dps(enemyId, level)
    # Apply Black Hollow Mage synergy internally for sorting logic
    if hasBhm and "Skeleton" in enemyIds[enemyId].name:
        # Effect of multiplying both stats by 1.5
        vol *= 2.25
    return vol


def check_if_valid(encounter, level, combo, targetStk, targetDps, rangedCount, toughnessSorted):
    # Make sure we're not putting both Kirk enemies in the same encounter
    if len(set(combo) & kirks) >= 2:
        return False
    # Make sure we only have one Mimic model
    if len(set(combo) & mimics) >= 2:
        return False
    # Black Hollow Mages need to be with at least one "skeleton" enemy
    if blackHollowMage in combo and not (set(combo) & skeletons):
        return False
    # Can't have more enemies than available models and Phalanx is 3 Phalanx Hollows shoved together
    if (3 if phalanx in combo else 0) + combo.count(phalanxHollow) >= 6 and encounter != "Eye of the Storm":
        return False
    
    comboRangedCount = sum([rangedCache[enemy] for enemy in combo])
    if enc[encounter]["expansion"] == "Painted World of Ariamis":
        if comboRangedCount > rangedCount:
            return False
    elif comboRangedCount != rangedCount:
        return False
    
    comboStk = 0.0
    comboDps = 0.0
    comboRangedCount = 0
    comboHigherHealthCount = 0
    
    for enemy in combo:
        stk = stkCache[level][enemy]
        dps = dpsCache[level][enemy]
        if blackHollowMage in combo and enemy in skeletons:
            stk *= 1.5
            dps *= 1.5
        comboStk += stk
        comboDps += dps
        comboRangedCount += 1 if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3 or enemyIds[enemy].enemyType == "invader" else 0
        comboHigherHealthCount += 1 if enemyIds[enemy].health >= 5 else 0
        
    # 10% tolerance on both stats
    stkValid = (targetStk * 0.9 <= comboStk <= targetStk * 1.1)
    dpsValid = (targetDps * 0.9 <= comboDps <= targetDps * 1.1)

    if not (stkValid and dpsValid):
        return False
    if toughnessSorted and not sum([1 for enemy in combo if enemyIds[enemy].armor + enemyIds[enemy].resist > 2]):
        return False
    
    return True


stkCache = {}
dpsCache = {}
rangedCache = {}

for level in [1, 2, 3]:
    stkCache[level] = {}
    dpsCache[level] = {}
    
    for enemy in allEnemies:
        stkCache[level][enemy] = get_stk(enemy, level)
        dpsCache[level][enemy] = get_dps(enemy, level)
        rangedCache[enemy] = 1 if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 3 or enemyIds[enemy].enemyType == "invader" else 0


try:
    # skip = True
    for ei, e in enumerate(enc):
        # if e not in {"Cold Snap",}:
        #     continue
        #     skip = False
        # if skip:
        #     continue
        # if enc[e]["level"] == 4:
        #     continue
        encounter = enc[e]

        # Don't process an encounter already being processed.
        if glob(baseFolder + "\\combine\\" + e + ".json"):
            continue

        # Put a temporary file out there so we know it's being processed.
        with open(baseFolder + "\\combine\\" + e + ".json", "w") as ef:
            dump({}, ef)

        print(e + " " + str(datetime.datetime.now()))
        level = enc[e]["level"] if enc[e]["level"] < 4 else 3
        alternatives = dict()
        enemies = []
        for tile in encounter["tiles"]:
            enemies += encounter["tiles"][tile]["enemies"] + encounter["tiles"][tile]["spawns"]

        # If the encounter breaks the model limit, we should too.
        allEnemiesMod = deepcopy(allEnemies)


        def get_max_overage(conditionFunc):
            overages = [enemies.count(e) - enemyIds[e].numberOfModels for e in enemyIds if conditionFunc(e)]
            return max([0] + overages)
            
        
        # 1 Health Melee Overage
        is1hpMelee = lambda e: enemyIds[e].health < 5 and max(enemyIds[e].attackRange) <= 1 and max(enemyIds[e].move) < 4
        for _ in range(get_max_overage(is1hpMelee)):
            allEnemiesMod.extend([e for e in enemyIds if is1hpMelee(e)])

        # 1 Health Ranged/Leap Overage
        is1hpRanged = lambda e: enemyIds[e].health < 5 and (max(enemyIds[e].attackRange) > 1 or max(enemyIds[e].move) >= 4)
        for _ in range(get_max_overage(is1hpRanged)):
            allEnemiesMod.extend([e for e in enemyIds if is1hpRanged(e)])

        # 5+ Health Melee Overage
        is5hpMelee = lambda e: 5 <= enemyIds[e].health <= 10 and max(enemyIds[e].attackRange) <= 1 and max(enemyIds[e].move) < 4
        for _ in range(get_max_overage(is5hpMelee)):
            allEnemiesMod.extend([e for e in enemyIds if is5hpMelee(e)])

        # 5+ Health Ranged/Leap Overage
        is5hpRanged = lambda e: 5 <= enemyIds[e].health <= 10 and (max(enemyIds[e].attackRange) > 1 or max(enemyIds[e].move) >= 4)
        for _ in range(get_max_overage(is5hpRanged)):
            allEnemiesMod.extend([e for e in enemyIds if is5hpRanged(e)])

        enemyCount = len(enemies)
        rangedCount = sum([1 for enemy in enemies if max(enemyIds[enemy].attackRange) > 1 or max(enemyIds[enemy].move) > 4])
        invaderCount = sum([1 for enemy in enemies if enemy in invaders])
        higherHealthCount = sum([1 for enemy in enemies if enemyIds[enemy].health >= 5])
        targetStk = 0.0
        targetDps = 0.0
        
        for enemy in enemies:
            stk = get_stk(enemy, level)
            dps = get_dps(enemy, level)
            if blackHollowMage in enemies and enemy in skeletons:
                stk *= 1.5
                dps *= 1.5
            targetStk += stk
            targetDps += dps

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

            if e not in respawnEncounters:
                higherHealthEnemies += (
                    [enemiesDict["Armorer Dennis"].id]
                    + [enemiesDict["Fencer Sharron"].id]
                    + [enemiesDict["Invader Brylex"].id]
                    + [enemiesDict["Kirk, Knight of Thorns"].id]
                    + [enemiesDict["Longfinger Kirk"].id]
                    + [enemiesDict["Maldron the Assassin"].id]
                    + [enemiesDict["Maneater Mildred"].id]
                    + [enemiesDict["Marvelous Chester"].id]
                    + [enemiesDict["Melinda the Butcher"].id]
                    + [enemiesDict["Oliver the Collector"].id]
                    + [enemiesDict["Paladin Leeroy"].id]
                    + [enemiesDict["Xanthous King Jeremiah"].id]
                    + [enemiesDict["Hungry Mimic"].id]
                    + [enemiesDict["Voracious Mimic"].id]
                )

            higherHealthCombos = set(combinations([enemyIds[en].id for en in higherHealthEnemies], higherHealthCount))
            nonGangCombos = set(combinations([enemyIds[en].id for en in nonGangs], nonGangCount))
            allCombos = [tuple(list(p[0]) + list(p[1]) + list(p[2])) for p in product(gangs, nonGangCombos, higherHealthCombos) if check_if_valid(e, level, list(p[0]) + list(p[1]) + list(p[2]), targetStk, targetDps, rangedCount, e in toughnessSortedEncounters) and not set(p[0]) & set(p[1])]
                    
            combosDict = defaultdict(set)
            [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set()).union({"The Sunless City"} if e in fangBoarEncounters | envoyBannerEncounters else set())].add(combo) for combo in allCombos]
        # Corvian Host is kinda like a model limit break encounter, except that the 5 health enemies all have to be the same.
        # Easier to have some custom code for it.
        elif e == "Corvian Host":
            smallEnemies = [enemyIds[enemy].id for enemy in allEnemies if enemyIds[enemy].health == 1]
            smallEnemyCombos = combinations(smallEnemies, 4)
            bigEnemies = list(set([enemyIds[enemy].id for enemy in allEnemies if enemyIds[enemy].health >= 5 and enemyIds[enemy].numberOfModels > 1]))
            enemyCount = 8
            rangedCount = 4

            allCombos = [combo[0] + tuple([combo[1]] * 4) for combo in product(smallEnemyCombos, bigEnemies) if check_if_valid(e, level, combo[0] + tuple([combo[1]] * 4), targetStk, targetDps, rangedCount, e in toughnessSortedEncounters)]

            combosDict = defaultdict(set)
            [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set()).union({"The Sunless City"} if e in fangBoarEncounters | envoyBannerEncounters else set())].add(combo) for combo in allCombos]
        elif enemyCount < 7:
            highHpPool = [en for en in allEnemiesMod if enemyIds[en].health >= 5]
            lowHpPool = [en for en in allEnemiesMod if enemyIds[en].health < 5]

            potentiallyValidCombos = (
                tuple(list(h) + list(l)) 
                for h in combinations(highHpPool, higherHealthCount) 
                for l in combinations(lowHpPool, enemyCount - higherHealthCount)
            )

            # Generate all combinations of enemies.
            allCombos = list(set(filterfalse(lambda s: not (
                    check_if_valid(e, level, s, targetStk, targetDps, rangedCount, e in toughnessSortedEncounters)
                    # Don't put invaders in encounters that respawn enemies
                    and (e not in respawnEncounters or sum(1 for x in s if enemyIds[x].enemyType == "invader") == 0)
                    # Has to be an enemy with dodge difficulty 2+, no invader (because of the dodge difficulty reduction)
                    and ((e not in {"Cloak and Feathers",} or enemyIds[s[0]].dodge >= 2) and enemyIds[s[0]].enemyType != "invader")
                    # No more than one of the two toughest enemies
                    and (e not in {"The First Bastion",} or (s.count(sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[1]) == 1))
                    # No more than one of the two strongest enemies
                    and (e not in {"Trecherous Tower", "Abandoned and Forgotten"} or (s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1]) == 1))
                    # No duplicate enemies
                    and (e != "The Last Bastion" or len(set(s)) > 1)
                    # One of the toughest enemy
                    and (e != "Cold Snap" or s.count(sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[0]) == 1)
                    # Two of the toughest enemy
                    and (e != "Corrupted Hovel" or s.count(sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[0]) == 2)
                    # One of the weakest enemy and one of the strongest
                    and (e != "Gleaming Silver" or (s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s))[0]) == 1))
                    # Two of the weakest enemy and the weakest enemy must be ranged (no leap)
                    and (e != "The Hellkite Bridge" or (
                        s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s))[0]) == 2
                        and max(enemyIds[sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s))[0]].attackRange) > 1))
                    # One of the toughest enemy
                    and (e != "No Safe Haven" or s.count(sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[0]) == 1)
                    # Two of the strongest enemy
                    and (e != "Skeletal Spokes" or s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 2)
                    # The strongest enemy must have more than 1 health
                    and (e != "Skeleton Overlord" or enemyIds[sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]].health > 1)
                    # One of the strongest enemy and the rest can't cause poison
                    and (e != "Shattered Keep" or (
                        s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1
                        and sorted([enemy for enemy in s if all(["poison" not in attackEffect for attackEffect in enemyIds[enemy].attackEffect])], key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1:]))
                    # No poison causing enemies
                    and (e != "Rain of Filth" or all([all(["poison" not in attackEffect for attackEffect in enemyIds[enemy].attackEffect]) for enemy in s]))
                    # No move attacks (it conflicts with the special rules)
                    and (e != "The Iron Golem" or all(not any(getattr(enemyIds[x], "moveAttack", [])) for x in s))
                    # One of the strongest enemy and 4 of the weakest enemy
                    and (e != "Eye of the Storm" or (
                        s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s))[0]) == 4
                        and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1))),
                potentiallyValidCombos)))

            # Create a dictionary of alternatives, put into keys that are the
            # sets in which those enemies are found.
            # Encounters with Crystal Lizards always require Iron Keep.
            # Black Hollow Mage increases the difficulty of skeleton enemies since
            # they resurrect defeated skeletons.
            combosDict = defaultdict(set)
            [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set()).union({"The Sunless City"} if e in fangBoarEncounters | envoyBannerEncounters else set())].add(combo) for combo in allCombos]
        # 6 enemies seems to be the limit for generating all combinations of enemies
        # in a reasonable amount of time.  For encounters with more than that, we're
        # going to take a sample instead.
        else:
            highHpPool = [en for en in allEnemiesMod if enemyIds[en].health >= 5]
            lowHpPool = [en for en in allEnemiesMod if enemyIds[en].health < 5]

            combosDict = defaultdict(set)
            comboCount = []

            expansions = list(set([enemyIds[enemy].expansion for enemy in allEnemiesMod]))
            for x in range(1, 3):
                for expCombo in combinations(expansions, x):
                    # Isolate enemies only for this specific expansion combo
                    expEnemies = [enemy for enemy in allEnemiesMod if enemyIds[enemy].expansion in expCombo]
                    expHighHp = [en for en in expEnemies if enemyIds[en].health >= 5]
                    expLowHp = [en for en in expEnemies if enemyIds[en].health < 5]
                    
                    # Skip if this expansion combo doesn't have enough models
                    if len(expHighHp) < higherHealthCount or len(expLowHp) < (enemyCount - higherHealthCount):
                        continue

                    expValidCombos = (
                        tuple(list(h) + list(l)) 
                        for h in combinations(expHighHp, higherHealthCount) 
                        for l in combinations(expLowHp, enemyCount - higherHealthCount)
                    )

                    allCombos = list(set(filterfalse(lambda s: not (
                            check_if_valid(e, level, s, targetStk, targetDps, rangedCount, e in toughnessSortedEncounters)
                            # Don't put invaders in encounters that respawn enemies
                            and (e not in respawnEncounters or sum(1 for x in s if enemyIds[x].enemyType == "invader") == 0)
                            # Two of the strongest enemy
                            and (e != "Frozen Revolutions" or s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 2)
                            # Two of the toughest single target melee enemy and that enemy isn't in the blacklist
                            and (e != "Deathly Freeze" or (
                                sum([1 for enemy in s if enemy not in deathlyFreezeEnemyBlacklist and (max(enemyIds[enemy].attackRange) < 2 or True not in set(enemyIds[enemy].nodeAttack)) and enemy == sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[0]]) == 2))
                            # One of the strongest enemy and either two of the second strongest or two that are the second and third strongest
                            and (e != "Trophy Room" or (
                                not trophyRoomEnemyBlacklist & set(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1:3])
                                and ((s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1]) == 2)
                                    or (s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[2]) == 1))
                                    ))),
                        expValidCombos)))

                    # Create a dictionary of alternatives, put into keys that are the
                    # sets in which those enemies are found.
                    # Encounters with Crystal Lizards always require Iron Keep.
                    # Black Hollow Mage increases the difficulty of skeleton enemies since
                    # they resurrect defeated skeletons.
                    [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set()).union({"The Sunless City"} if e in fangBoarEncounters | envoyBannerEncounters else set())].add(combo) for combo in allCombos]

            for expansionCombo in combosDict:
                combosDict[expansionCombo] = list(combosDict[expansionCombo])
                shuffle(combosDict[expansionCombo])
                combosDict[expansionCombo] = set(combosDict[expansionCombo][:min([len(combosDict[expansionCombo]), 10000])])

            # In total, we're looking for up to 500,000 combinations but we'll trim that down later.
            while sum((len(combosDict[sets]) for sets in combosDict)) < 500000:
                batchCombos = []
                for _ in range(50000):
                    highHpSample = sample(highHpPool, higherHealthCount)
                    lowHpSample = sample(lowHpPool, enemyCount - higherHealthCount)
                    if len(set([enemyIds[x].expansion for x in highHpSample + lowHpSample])) < 3:
                        continue
                    batchCombos.append(tuple(highHpSample + lowHpSample))

                allCombos = list(filterfalse(lambda s: not (
                        check_if_valid(e, level, s, targetStk, targetDps, rangedCount, e in toughnessSortedEncounters)
                        and (e not in respawnEncounters or sum(1 for x in s if enemyIds[x].enemyType == "invader") == 0)
                        # Two of the strongest enemy
                        and (e != "Frozen Revolutions" or s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 2)
                        # Two of the toughest single target melee enemy and that enemy isn't in the blacklist
                        and (e != "Deathly Freeze" or (
                            sum([1 for enemy in s if enemy not in deathlyFreezeEnemyBlacklist and (max(enemyIds[enemy].attackRange) < 2 or True not in set(enemyIds[enemy].nodeAttack)) and enemy == sorted(s, key=lambda x: (-get_stk(x, level), get_volume(x, level, blackHollowMage in s)), reverse=True)[0]]) == 2))
                        # One of the strongest enemy and either two of the second strongest or two that are the second and third strongest
                        and (e != "Trophy Room" or (
                            not trophyRoomEnemyBlacklist & set(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1:3])
                            and ((s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1]) == 2)
                                or (s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[0]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[1]) == 1 and s.count(sorted(s, key=lambda x: get_volume(x, level, blackHollowMage in s), reverse=True)[2]) == 1))
                                ))),
                    batchCombos))

                # Create the dictionary with the enemy sets as keys.
                [combosDict[frozenset([enemyIds[enemyId].expansion for enemyId in combo]).union({"Iron Keep"} if e in crystalLizardEncounters else set()).union({"The Sunless City"} if e in fangBoarEncounters | envoyBannerEncounters else set())].add(combo) for combo in allCombos]

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
        # [Tile 1 Row 1, Tile 1 Row 2, Tile 1 Row 3 (level 4 only), Tile 1 Row 4 (level 4 only), Tile 1 spawns,
        # Tile 2 Row 1, Tile 2 Row 2, Tile 2 spawns, Tile 3 Row 1, Tile 3 Row 2, Tile 3 spawns]
        with open(path.join(baseFolder + "\\encounters", e + ".json")) as ef:
            thisEnc = load(ef)
        alternatives["enemySlots"] = thisEnc.get("enemySlots")
            
        # For each key in the dictionary, shuffle the enemy combos,
        # then trim it down so we keep at most 50000 values per encounter.
        # Keep all combos that only consist of 1 or 2 sets.
        # If this is an encounter that requires a particular encounter, expand how many we keep by 1.
        keepLimit = 3 if e in (crystalLizardEncounters | fangBoarEncounters | envoyBannerEncounters) else 2
        
        # Convert sets to lists once
        for k in combosDict:
            combosDict[k] = list(combosDict[k])

        # Split keys by number of expansions
        smallKeys = [k for k in combosDict if len(k) <= keepLimit]
        bigKeys   = [k for k in combosDict if len(k) > keepLimit]

        # How many "always keep" combos do we have?
        smallTotal = sum(len(combosDict[k]) for k in smallKeys)

        # How many slots remain for big combos?
        remaining = 50000 - smallTotal

        if remaining <= 0:
            # Budget is used up by 1–keepLimit-set combos.
            # Drop all >keepLimit-set combos.
            combosDict = {k: combosDict[k] for k in smallKeys}
        else:
            # Flatten all big combos with their expansion key
            flat = []
            for k in bigKeys:
                for combo in combosDict[k]:
                    flat.append((k, combo))

            # If we have more than we can keep, sample
            if len(flat) > remaining:
                shuffle(flat)
                flat = flat[:remaining]

            # Rebuild big part, only keys that actually got at least one combo survive
            newBig = defaultdict(list)
            for k, combo in flat:
                newBig[k].append(combo)

            # Merge small + trimmed big
            combosDict = {k: combosDict[k] for k in smallKeys}
            combosDict.update(newBig)

        # Put the alternative enemies in the same difficulty order as the
        # original enemies. This way I can just iterate through the list
        # when we load the encounter and take the enemies in order.
        alternatives["alternatives"] = {",".join(k): v for k, v in combosDict.items() if v}
        for expansionCombo in alternatives["alternatives"]:
            newAlts = []
            for alt in alternatives["alternatives"][expansionCombo]:
                newAlt = []
                has_bhm = blackHollowMage in alt
                if e in toughnessSortedEncounters:
                    altDifficulty = sorted(alt, key=lambda x: (-get_stk(x, level), get_volume(x, level, has_bhm)))
                else:
                    altDifficulty = sorted(alt, key=lambda x: get_volume(x, level, has_bhm))
                    
                for ord in enc[e]["difficultyOrder"]:
                    newAlt.append(altDifficulty[ord])
                if newAlt not in newAlts:
                    newAlts.append(newAlt)
            alternatives["alternatives"][expansionCombo] = newAlts

        # Account for duplicate enemies in the newer core sets that are essentially redoing the older stuff.
        # The Sunless City
        for combo in [c for c in alternatives["alternatives"] if "Dark Souls The Board Game" in c]:
            toAdd = []
            for alt in alternatives["alternatives"][combo]:
                if e in {"The Grand Hall", "Depths of the Cathedral", "Twilight Falls"} or (alt.count(crossbowHollow) <= 3
                    and alt.count(hollowSoldier) <= 3
                    and alt.count(silverKnightGreatbowman) <= 2
                    and alt.count(silverKnightSwordsman) <= 2
                    and alt.count(sentinel) <= 1
                    and alt.count(largeHollowSoldier) == 0):
                    toAdd.append(alt)
                
            if toAdd:
                if "The Sunless City" not in combo:
                    altKey = combo.replace("Dark Souls The Board Game", "The Sunless City")
                else:
                    altKey = combo.replace("Dark Souls The Board Game,", "").replace(",Dark Souls The Board Game", "")
                alternatives["alternatives"][altKey] = toAdd

        if e not in encMain:
            encMain[e] = {
                "name": enc[e]["name"],
                "expansion": enc[e]["expansion"],
                "level": enc[e]["level"],
                "expansionCombos": []
                }
            
        encMain[e]["expansionCombos"] = [str(k).split(",") for k in alternatives["alternatives"].keys()]
                
        with open(baseFolder + "\\encounters\\" + e + ".json", "w") as encountersFile:
            dump(alternatives, encountersFile)

        with open(baseFolder + "\\combine\\" + e + ".json", "w") as ef:
            dump(encMain[e], ef)
except Exception as ex:
    input(ex)
    raise
