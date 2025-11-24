from os import path
from itertools import combinations, combinations_with_replacement, filterfalse
from math import ceil
from statistics import mean


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []

# Path attacks hit every node on the way to the target, as well as the source's and target's nodes.
# Calculate the average number of nodes attacked based on all configurations.
# Distances
# Same node: 13
# 1 node away: 64
# 2 nodes away: 64
# 3 nodes away: 24
# 4 nodes away: 4
# Nodes attacked
# Same node: 1.0
# 1 node away: 2.0
# 2 nodes away: 3.5
# 3 nodes away: 6.666666666666667
# 4 nodes away: 11.0
pathAttacks = ([1.0] * 13) + ([2.0] * 64) + ([3.5] * 64) + ([6.666666666666667] * 24) + ([11.0] * 4)
pathAttack = mean(pathAttacks)

newGamePlusMods = [
    "dodge1", "dodge2",
    "damage1", "damage2", "damage3", "damage4",
    "armor resist1", "armor resist2",
    #"armor1", "armor2",
    #"resist1", "resist2",
    "health1", "health2", "health3", "health4",
    "damage health1", "damage health2",
    #"repeat",
    #"magic", "physical",
    "effect1",# "effect2"
]

effectMods = [
    "bleed",
    "frostbite",
    "poison",
    "stagger"
]

effectCombos = list(combinations(effectMods, 2))

aoeMods = [
    "nodes1",
    "nodes2",
    "nodes3",
    "nodes4",
    "nodes5",
    "nodes6"
]

bdkAoeAverage = {
    0: mean([15, 15, 10, 11, 10, 11, 10, 10]),
    1: mean([16, 16, 11, 12, 11, 12, 11, 11]),
    2: mean([17, 17, 12, 13, 12, 13, 12, 12]),
    3: mean([18, 18, 13, 14, 13, 14, 13, 13]),
    4: mean([19, 19, 14, 15, 14, 15, 14, 14]),
    5: mean([20, 20, 15, 16, 15, 16, 15, 15]),
    6: mean([21, 21, 16, 17, 16, 17, 16, 16])
}

oikAoeAverage = {
    0: mean([8, 8, 8, 8, 9, 9]),
    1: mean([9, 9, 9, 9, 9, 10, 10]),
    2: mean([10, 10, 10, 10, 10, 10, 11, 11]),
    3: mean([11, 11, 11, 11, 11, 11, 12, 12]),
    4: mean([12, 12, 12, 12, 12, 12, 13, 13]),
    5: mean([13, 13, 13, 13, 13, 13, 14, 14]),
    6: mean([14, 14, 14, 14, 14, 14, 15, 15])
}

ecAoeAverage = {
    0: 5,
    1: 6,
    2: 7,
    3: 8,
    4: 9,
    5: 10,
    6: 11
}

gdAoeAverage = {
    0: 7,
    1: 8,
    2: 9,
    3: 10,
    4: 11,
    5: 12,
    6: 13
}

ngpc = []
for x in range(1, 5):
    ngpc += filterfalse(lambda c: (len(c) != len(set([a[:-1] for a in c])) or ("effect1" in c and "effect2" in c)), combinations(newGamePlusMods, x))

aoeNgpc = []
for x in range(1, 5):
    aoeNgpc += filterfalse(lambda c: len(c) != len(set([a[:-1] for a in c])) or ("effect1" in c and "effect2" in c) or len(set(c) & set(aoeMods)) > 1, combinations(newGamePlusMods + aoeMods, x))

class Enemy:
    def __init__(self, name, expansion, enemyType, numberOfModels, health, armor, resist, iconForEffects, attacks, attackType, dodge, move, attackRange, id=None, repeat=0, nodeAttack=[], nodesAttacked=[], attackEffect=[], weakArcs=None, windup=False, moveIndex=None, skipDefense=False, difficultyTiers={}, moveAttack=[], modified=False, comboSet=frozenset(), aoe=False, invisibility=False, ambush=False, frostbiteLeap=False) -> None:
        enemiesDict[name] = self
        enemies.append(self)

        if id:
            enemyIds[id] = self

        self.name = name
        self.id = id
        self.expansion = expansion
        self.enemyType = enemyType
        self.numberOfModels = numberOfModels
        self.health = health
        self.armor = armor
        self.resist = resist
        self.repeat = repeat
        self.skipDefense = skipDefense
        self.iconForEffects = iconForEffects
        self.invisibility = invisibility
        self.ambush = ambush
        self.frostbiteLeap = frostbiteLeap
        self.attacksTaken = {1: 0, 2: 0, 3: 0}

        if not nodeAttack:
            nodeAttack = [False for _ in attacks]

        if not nodesAttacked:
            nodesAttacked = [0 for _ in attacks]

        if not moveAttack:
            moveAttack = [False for _ in attacks]

        # Need to map the effects to their correct places in attackEffects
        if {"effect1", "effect2"} & comboSet:
            attackEffect = [attackEffect[i] if len(attackEffect) > i else set() for i in iconForEffects]
            
        # Add repeat.  However, don't add the initial push attack (for characters on the enemy's node)
        # Since they would have already been pushed out prior in the activation.
        self.attacks = attacks + ([a for i, a in enumerate(attacks) if not moveAttack[i] or move[i]] * repeat)
        self.iconForEffects = iconForEffects + ([e for i, e in enumerate(iconForEffects) if not moveAttack[i] or move[i]] * repeat)
        self.nodeAttack = nodeAttack + ([a for i, a in enumerate(nodeAttack) if not moveAttack[i] or move[i]] * repeat)
        self.nodesAttacked = nodesAttacked + ([a for i, a in enumerate(nodesAttacked) if not moveAttack[i] or move[i]] * repeat)
        self.attackType = attackType + ([a for i, a in enumerate(attackType) if not moveAttack[i] or move[i]] * repeat)
        self.attackRange = attackRange + ([a for i, a in enumerate(attackRange) if not moveAttack[i] or move[i]] * repeat)
        self.attackEffect = attackEffect + ([a for i, a in enumerate(attackEffect) if not moveAttack[i] or move[i]] * repeat)
        self.move = move + ([a for i, a in enumerate(move) if not moveAttack[i] or move[i]] * repeat)
        moveAttack = moveAttack + ([a for i, a in enumerate(moveAttack) if not moveAttack[i] or move[i]] * repeat)

        # This helps offset the penalty for enemies that move at the end of their turn.
        if enemyType == "regular":
            self.attacks = self.attacks * 2
            self.iconForEffects = self.iconForEffects * 2
            self.nodeAttack = self.nodeAttack * 2
            self.nodesAttacked = self.nodesAttacked * 2
            self.attackType = self.attackType * 2
            self.attackRange = self.attackRange * 2
            self.attackEffect = self.attackEffect * 2
            self.move = self.move * 2
            moveAttack = moveAttack * 2

        self.dodge = dodge
        self.weakArcs = weakArcs if weakArcs is not None else 1 if "boss" in enemyType else 0
        self.windup = windup
        self.difficultyTiers = difficultyTiers
        self.modified = modified
        self.comboSet = comboSet

        check = set()
        check.add(len(self.attacks))
        check.add(len(self.iconForEffects))
        check.add(len(self.attackRange))
        check.add(len(self.attackType))
        check.add(len(self.nodeAttack))
        check.add(len(self.nodesAttacked))
        check.add(len(moveAttack))
        if len(set(check)) > 1 or set(self.attackType) - {"physical", "magic"}:
            raise
        
        if "Hollow" in self.name and self.health == 1:
            self.gang = "Hollow"
        elif "Alonne" in self.name and self.health == 1:
            self.gang = "Alonne"
        elif "Skeleton" in self.name and self.health == 1:
            self.gang = "Skeleton"
        elif "Silver Knight" in self.name and self.health == 1:
            self.gang = "Silver Knight"
        else:
            self.gang = None

        self.deaths = {
            1: 0,
            2: 0,
            3: 0
        }
        self.damageDone1 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.damageDone2 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.damageDone3 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.damageDone4 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.bleedDamage1 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.bleedDamage2 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.bleedDamage3 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.bleedDamage4 = {
            1: 0,
            2: 0,
            3: 0
        }
        self.damagingAttacks = {
            1: 0,
            2: 0,
            3: 0
        }
        self.totalAttacks = {
            1: 0,
            2: 0,
            3: 0
        }
        self.loadoutDamage = {}

        for i, m in enumerate(self.move):
            reach.append(min([4, max([0, m + self.attackRange[i]])]))

        if not modified:
            for combo in aoeNgpc if aoe else ngpc:
                comboSet = frozenset(combo)
                if (
                    ("magic" in comboSet and "physical" not in attackType)
                    or ("physical" in comboSet and "magic" not in attackType)
                    or ("magic" in comboSet and not any([("physical", False) in set(zip(attackType, moveAttack))]))
                    or (attackEffect and all([len(ae) + (1 if "effect1" in comboSet else 2 if "effect2" in comboSet else 0) > 2 for i, ae in enumerate(attackEffect) if attacks[i]]))
                    or ({"damage health1", "damage health2", "armor resist1"} & comboSet and len(comboSet) < 4)
                    or ("armor resist1" in comboSet and {"armor1", "armor2", "resist1", "resist2"} & comboSet)
                    or ({"damage health1", "damage health2"} & comboSet and {"health1", "health2", "health3", "health4", "damage1", "damage2", "damage3", "damage4"} & comboSet)
                    or ("dodge1" in comboSet and dodge == 4)
                    or ("dodge2" in comboSet and dodge >= 3)
                    or (aoe and "repeat" in comboSet)
                    ):
                    continue

                healthBonus = (
                    1 if health == 1 and {"health1", "damage health1"} & comboSet
                    else 2 if health == 1 and {"health2", "damage health2"} & comboSet
                    else 3 if health == 1 and {"health3", "damage health3"} & comboSet
                    else 4 if health == 1 and {"health4", "damage health4"} & comboSet
                    else 2 if health == 5 and {"health1", "damage health1"} & comboSet
                    else 3 if health == 5 and {"health2", "damage health2"} & comboSet
                    else 5 if health == 5 and {"health3", "damage health3"} & comboSet
                    else 6 if health == 5 and {"health4", "damage health4"} & comboSet
                    else 2 if health == 10 and {"health1", "damage health1"} & comboSet
                    else 4 if health == 10 and {"health2", "damage health2"} & comboSet
                    else 6 if health == 10 and {"health3", "damage health3"} & comboSet
                    else 8 if health == 10 and {"health4", "damage health4"} & comboSet
                    else ceil(health * 0.1) if {"health1", "damage health1"} & comboSet
                    else ceil(health * 0.2) if {"health2", "damage health2"} & comboSet
                    else ceil(health * 0.3) if {"health3", "damage health3"} & comboSet
                    else ceil(health * 0.4) if {"health4", "damage health4"} & comboSet
                    else 0)
                
                if "Four Kings" in name:
                    healthBonus = ceil(healthBonus / 2)

                modAttackEffects = []
                if {"effect1", "effect2"} & comboSet:
                    if "effect2" in comboSet and any([ae for ae in attackEffect]):
                        continue

                    attacksForEffects = len(set(a for i, a in enumerate(iconForEffects) if attacks[i]))

                    for effectCombo in combinations_with_replacement(effectMods if "effect1" in comboSet else effectCombos, attacksForEffects):
                        if set(effectCombo) & set([item for row in attackEffect for item in row]):
                            continue
                        modAttackEffects.append(tuple((e,) for e in effectCombo) if "effect1" in comboSet else effectCombo)
                    
                if modAttackEffects:
                    for modAttackEffect in modAttackEffects:
                        Enemy(
                            name + " " + str(tuple([c for c in combo if "effect" not in c] + [[e for e in m] for m in modAttackEffect])),
                            expansion,
                            enemyType,
                            numberOfModels,
                            health=health + healthBonus,
                            armor=armor + (1 if "armor1" in combo or "armor resist1" in combo else 2 if "armor2" in combo else 0),
                            resist=resist + (1 if "resist1" in combo or "armor resist1" in combo else 2 if "resist2" in combo else 0),
                            iconForEffects=iconForEffects,
                            attacks=[attack + (0 if attack == 0 else 1 if {"damage1", "damage health1"} & comboSet else 2 if {"damage2", "damage health2"} & comboSet else 3 if "damage3" in combo else 4 if "damage4" in combo else 0) for attack in attacks],
                            attackType=["magic" if "magic" in combo and not moveAttack[i] else "physical" if "physical" in combo or moveAttack[i] else at for i, at in enumerate(attackType)],
                            dodge=dodge + (1 if "dodge1" in combo else 0) + (2 if "dodge2" in combo else 0),
                            move=move,
                            attackRange=attackRange,
                            repeat=repeat + (1 if "repeat" in combo else 0),
                            id=max([enemy.id for enemy in enemies]) + 1 if id else None,
                            attackEffect=modAttackEffect,
                            nodeAttack=nodeAttack,
                            nodesAttacked=nodesAttacked if not aoe else [(bdkAoeAverage if "Black Dragon Kalameet" in name else oikAoeAverage if "Old Iron King" in name else ecAoeAverage if "Executioner's Chariot" in name else gdAoeAverage if "Guardian Dragon" in name else {})[1 if "nodes1" in comboSet else 2 if "nodes2" in comboSet else 3 if "nodes3" in comboSet else 4 if "nodes4" in comboSet else 5 if "nodes5" in comboSet else 6 if "nodes6" in comboSet else 0]],
                            weakArcs=weakArcs,
                            windup=windup,
                            skipDefense=skipDefense,
                            modified=True,
                            comboSet=comboSet,
                            aoe=aoe)

                else:
                    Enemy(
                        name + " " + str(combo),
                        expansion,
                        enemyType,
                        numberOfModels,
                        health=health + healthBonus,
                        armor=armor + (1 if "armor1" in combo or "armor resist1" in combo else 2 if "armor2" in combo else 0),
                        resist=resist + (1 if "resist1" in combo or "armor resist1" in combo else 2 if "resist2" in combo else 0),
                        iconForEffects=iconForEffects,
                        attacks=[attack + (0 if attack == 0 else 1 if {"damage1", "damage health1"} & comboSet else 2 if {"damage2", "damage health2"} & comboSet else 3 if "damage3" in combo else 4 if "damage4" in combo else 0) for attack in attacks],
                        attackType=["magic" if "magic" in combo and not moveAttack[i] else "physical" if "physical" in combo or moveAttack[i] else at for i, at in enumerate(attackType)],
                        dodge=dodge + (1 if "dodge1" in combo else 0) + (2 if "dodge2" in combo else 0),
                        move=move,
                        attackRange=attackRange,
                        repeat=repeat + (1 if "repeat" in combo else 0),
                        id=max([enemy.id for enemy in enemies]) + 1 if id else None,
                        attackEffect=attackEffect,
                        nodeAttack=nodeAttack,
                        nodesAttacked=nodesAttacked if not aoe else [(bdkAoeAverage if "Black Dragon Kalameet" in name else oikAoeAverage if "Old Iron King" in name else ecAoeAverage if "Executioner's Chariot" in name else gdAoeAverage if "Guardian Dragon" in name else {})[1 if "nodes1" in comboSet else 2 if "nodes2" in comboSet else 3 if "nodes3" in comboSet else 4 if "nodes4" in comboSet else 5 if "nodes5" in comboSet else 6 if "nodes6" in comboSet else 0]],
                        weakArcs=weakArcs,
                        windup=windup,
                        skipDefense=skipDefense,
                        modified=True,
                        comboSet=comboSet,
                        aoe=aoe)


# Regular enemies
Enemy(id=1, name="Alonne Bow Knight", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 25.33, 2: 25.33, 3: 25.33, 4: 25.33}}, 2: {"toughness": 171980, "difficulty": {1: 1.19, 2: 1.19, 3: 1.19, 4: 1.19}}, 3: {"toughness": 349528, "difficulty": {1: 0.42, 2: 0.42, 3: 0.42, 4: 0.42}}})
Enemy(id=2, name="Alonne Knight Captain", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=5, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 15848, "difficulty": {1: 223.96, 2: 223.96, 3: 223.96, 4: 223.96}}, 2: {"toughness": 19688, "difficulty": {1: 9.35, 2: 9.35, 3: 9.35, 4: 9.35}}, 3: {"toughness": 67600, "difficulty": {1: 1.91, 2: 1.91, 3: 1.91, 4: 1.91}}})
Enemy(id=3, name="Alonne Sword Knight", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 71156, "difficulty": {1: 41.76, 2: 41.76, 3: 41.76, 4: 41.76}}, 2: {"toughness": 68704, "difficulty": {1: 2.13, 2: 2.13, 3: 2.13, 4: 2.13}}, 3: {"toughness": 225684, "difficulty": {1: 0.52, 2: 0.52, 3: 0.52, 4: 0.52}}})
Enemy(id=4, name="Black Hollow Mage", expansion="Executioner Chariot", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=3, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 9968, "difficulty": {1: 449.87, 2: 449.87, 3: 449.87, 4: 449.87}}, 2: {"toughness": 17116, "difficulty": {1: 15.89, 2: 15.89, 3: 15.89, 4: 15.89}}, 3: {"toughness": 59760, "difficulty": {1: 2.73, 2: 2.73, 3: 2.73, 4: 2.73}}})
Enemy(id=5, name="Bonewheel Skeleton", moveAttack=[True,True], expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, repeat=1, iconForEffects=[0, 0], attacks=[4,4], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 52.53, 2: 56.57, 3: 60.61, 4: 65.58}}, 2: {"toughness": 171980, "difficulty": {1: 2.47, 2: 2.66, 3: 2.85, 4: 3.09}}, 3: {"toughness": 349528, "difficulty": {1: 0.87, 2: 0.94, 3: 1, 4: 1.09}}})
Enemy(id=6, name="Crossbow Hollow", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=0, iconForEffects=[0], attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 162960, "difficulty": {1: 8.52, 2: 8.52, 3: 8.52, 4: 8.52}}, 2: {"toughness": 219936, "difficulty": {1: 0.33, 2: 0.33, 3: 0.33, 4: 0.33}}, 3: {"toughness": 354700, "difficulty": {1: 0.09, 2: 0.09, 3: 0.09, 4: 0.09}}})
Enemy(id=7, name="Crow Demon", moveAttack=[True,True], expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=2, iconForEffects=[0, 0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0], difficultyTiers={1: {"toughness": 23816, "difficulty": {1: 526.26, 2: 566.74, 3: 607.22, 4: 657.05}}, 2: {"toughness": 37404, "difficulty": {1: 19.12, 2: 20.59, 3: 22.07, 4: 23.88}}, 3: {"toughness": 121500, "difficulty": {1: 4.93, 2: 5.31, 3: 5.68, 4: 6.15}}})
Enemy(id=8, name="Demonic Foliage", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=1, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficultyTiers={1: {"toughness": 132996, "difficulty": {1: 22.34, 2: 22.34, 3: 22.34, 4: 22.34}}, 2: {"toughness": 128624, "difficulty": {1: 1.14, 2: 1.14, 3: 1.14, 4: 1.14}}, 3: {"toughness": 252748, "difficulty": {1: 0.46, 2: 0.46, 3: 0.46, 4: 0.46}}})
Enemy(id=9, name="Engorged Zombie", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 71156, "difficulty": {1: 18.78, 2: 18.78, 3: 18.78, 4: 18.78}}, 2: {"toughness": 68704, "difficulty": {1: 1.12, 2: 1.12, 3: 1.12, 4: 1.12}}, 3: {"toughness": 225684, "difficulty": {1: 0.13, 2: 0.13, 3: 0.13, 4: 0.13}}})
Enemy(id=10, name="Falchion Skeleton", expansion="Executioner Chariot", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[3], attackType=["physical"], attackEffect=[{"bleed",}], dodge=1, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 42.69, 2: 42.69, 3: 42.69, 4: 42.69}}, 2: {"toughness": 171980, "difficulty": {1: 2.09, 2: 2.09, 3: 2.09, 4: 2.09}}, 3: {"toughness": 349528, "difficulty": {1: 0.8, 2: 0.8, 3: 0.8, 4: 0.8}}})
Enemy(id=11, name="Firebomb Hollow", expansion="Explorers", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=1, move=[1], attackRange=[2], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 9.15, 2: 9.85, 3: 10.55, 4: 11.42}}, 2: {"toughness": 171980, "difficulty": {1: 0.41, 2: 0.44, 3: 0.48, 4: 0.51}}, 3: {"toughness": 349528, "difficulty": {1: 0.09, 2: 0.09, 3: 0.1, 4: 0.11}}})
Enemy(id=12, name="Giant Skeleton Archer", moveAttack=[True, True, False], expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=1, iconForEffects=[0,0,1], attacks=[2,2,5], attackType=["physical", "physical", "physical"], nodeAttack=[True, True, False], dodge=2, move=[0, 0, 0], attackRange=[0,0, 4], moveIndex=0, difficultyTiers={1: {"toughness": 41056, "difficulty": {1: 163.44, 2: 164.98, 3: 166.53, 4: 168.44}}, 2: {"toughness": 55572, "difficulty": {1: 6.7, 2: 6.76, 3: 6.83, 4: 6.91}}, 3: {"toughness": 133604, "difficulty": {1: 2.1, 2: 2.12, 3: 2.13, 4: 2.15}}})
Enemy(id=13, name="Giant Skeleton Soldier", moveAttack=[True, True, False], expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=1, iconForEffects=[0,0,1], attacks=[2,2,5], attackType=["physical", "physical", "physical"], nodeAttack=[True, True, False], dodge=1, move=[0, 1, 1], attackRange=[0,0, 1], difficultyTiers={1: {"toughness": 41056, "difficulty": {1: 89.23, 2: 90.06, 3: 90.88, 4: 91.9}}, 2: {"toughness": 55572, "difficulty": {1: 3.23, 2: 3.26, 3: 3.29, 4: 3.32}}, 3: {"toughness": 133604, "difficulty": {1: 1.02, 2: 1.03, 3: 1.03, 4: 1.04}}})
Enemy(id=14, name="Hollow Soldier", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 6.25, 2: 6.25, 3: 6.25, 4: 6.25}}, 2: {"toughness": 171980, "difficulty": {1: 0.29, 2: 0.29, 3: 0.29, 4: 0.29}}, 3: {"toughness": 349528, "difficulty": {1: 0.06, 2: 0.06, 3: 0.06, 4: 0.06}}})
Enemy(id=15, name="Ironclad Soldier", moveAttack=[True,True], expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=5, armor=3, resist=2, iconForEffects=[0,0], attacks=[5,5], attackType=["physical", "physical"], nodeAttack=[True, True], attackEffect=[{"stagger",},{"stagger",}], dodge=2, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 3852, "difficulty": {1: 1040.78, 2: 1120.84, 3: 1200.9, 4: 1299.44}}, 2: {"toughness": 6545, "difficulty": {1: 38.47, 2: 41.43, 3: 44.39, 4: 48.03}}, 3: {"toughness": 26442, "difficulty": {1: 4.84, 2: 5.21, 3: 5.58, 4: 6.04}}})
Enemy(id=16, name="Large Hollow Soldier", moveAttack=[True,True], expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=0, iconForEffects=[0,0], attacks=[5,5], attackType=["physical", "physical"], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 51620, "difficulty": {1: 42.64, 2: 45.92, 3: 49.2, 4: 53.24}}, 2: {"toughness": 75552, "difficulty": {1: 1.57, 2: 1.69, 3: 1.81, 4: 1.96}}, 3: {"toughness": 146676, "difficulty": {1: 0.43, 2: 0.47, 3: 0.5, 4: 0.54}}})
Enemy(id=34, name="Mimic", expansion="The Sunless City", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficultyTiers={1: {"toughness": 41056, "difficulty": {1: 196.08, 2: 196.08, 3: 196.08, 4: 196.08}}, 2: {"toughness": 55572, "difficulty": {1: 8.27, 2: 8.27, 3: 8.27, 4: 8.27}}, 3: {"toughness": 133604, "difficulty": {1: 2.88, 2: 2.88, 3: 2.88, 4: 2.88}}})
Enemy(id=17, name="Mushroom Child", expansion="Darkroot", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 23816, "difficulty": {1: 65.36, 2: 65.36, 3: 65.36, 4: 65.36}}, 2: {"toughness": 37404, "difficulty": {1: 2.24, 2: 2.24, 3: 2.24, 4: 2.24}}, 3: {"toughness": 121500, "difficulty": {1: 0.37, 2: 0.37, 3: 0.37, 4: 0.37}}})
Enemy(id=18, name="Mushroom Parent", moveAttack=[True,True], expansion="Darkroot", enemyType="regular", numberOfModels=1, health=10, armor=1, resist=2, iconForEffects=[0,0], attacks=[6,6], attackType=["physical", "physical"], nodeAttack=[True,True], attackEffect=[{"stagger",}, {"stagger",}], dodge=1, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 7138, "difficulty": {1: 447.92, 2: 482.38, 3: 516.84, 4: 559.24}}, 2: {"toughness": 14291, "difficulty": {1: 12.55, 2: 13.51, 3: 14.48, 4: 15.67}}, 3: {"toughness": 41741, "difficulty": {1: 2.44, 2: 2.62, 3: 2.81, 4: 3.04}}})
Enemy(id=19, name="Necromancer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=2, iconForEffects=[0], attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 23816, "difficulty": {1: 161.95, 2: 174.41, 3: 186.88, 4: 202.2}}, 2: {"toughness": 37404, "difficulty": {1: 8.7, 2: 9.35, 3: 10.04, 4: 10.85}}, 3: {"toughness": 121500, "difficulty": {1: 2.14, 2: 2.31, 3: 2.48, 4: 2.68}}})
Enemy(id=20, name="Phalanx", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=1, iconForEffects=[0,0], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=1, move=[0,1], attackRange=[1,0], difficultyTiers={1: {"toughness": 41056, "difficulty": {1: 63.53, 2: 66.8, 3: 70.07, 4: 74.09}}, 2: {"toughness": 55572, "difficulty": {1: 2.65, 2: 2.78, 3: 2.91, 4: 3.07}}, 3: {"toughness": 133604, "difficulty": {1: 0.59, 2: 0.62, 3: 0.65, 4: 0.68}}})
Enemy(id=21, name="Phalanx Hollow", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=5, health=1, armor=1, resist=1, iconForEffects=[0,0], attacks=[4,0], attackType=["physical", "physical"], dodge=1, move=[0,1], attackRange=[1,0], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 7.01, 2: 7.01, 3: 7.01, 4: 7.01}}, 2: {"toughness": 171980, "difficulty": {1: 0.32, 2: 0.32, 3: 0.32, 4: 0.32}}, 3: {"toughness": 349528, "difficulty": {1: 0.07, 2: 0.07, 3: 0.07, 4: 0.07}}})
Enemy(id=22, name="Plow Scarecrow", expansion="Darkroot", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 25.03, 2: 25.03, 3: 25.03, 4: 25.03}}, 2: {"toughness": 171980, "difficulty": {1: 1.18, 2: 1.18, 3: 1.18, 4: 1.18}}, 3: {"toughness": 349528, "difficulty": {1: 0.41, 2: 0.41, 3: 0.41, 4: 0.41}}})
Enemy(id=23, name="Sentinel", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=2, health=10, armor=2, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1], difficultyTiers={1: {"toughness": 16744, "difficulty": {1: 252.3, 2: 271.7, 3: 291.11, 4: 315}}, 2: {"toughness": 20220, "difficulty": {1: 10.73, 2: 11.55, 3: 12.38, 4: 13.4}}, 3: {"toughness": 44296, "difficulty": {1: 4.1, 2: 4.42, 3: 4.73, 4: 5.12}}})
Enemy(id=24, name="Shears Scarecrow", expansion="Darkroot", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0,0], attacks=[3,3], attackType=["physical", "physical"], nodeAttack=[True,True], dodge=2, move=[1, 1], attackRange=[0, 0], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 18.64, 2: 20.08, 3: 21.51, 4: 23.28}}, 2: {"toughness": 171980, "difficulty": {1: 0.93, 2: 1, 3: 1.08, 4: 1.16}}, 3: {"toughness": 349528, "difficulty": {1: 0.21, 2: 0.23, 3: 0.25, 4: 0.27}}})
Enemy(id=25, name="Silver Knight Greatbowman", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=0, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 146032, "difficulty": {1: 13.9, 2: 14.97, 3: 16.04, 4: 17.35}}, 2: {"toughness": 176580, "difficulty": {1: 0.55, 2: 0.59, 3: 0.63, 4: 0.69}}, 3: {"toughness": 257920, "difficulty": {1: 0.27, 2: 0.29, 3: 0.31, 4: 0.33}}})
Enemy(id=26, name="Silver Knight Spearman", expansion="Explorers", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, iconForEffects=[0,0], attacks=[6,0], attackType=["physical", "physical"], dodge=2, move=[0,1], attackRange=[1,0], difficultyTiers={1: {"toughness": 132996, "difficulty": {1: 33.64, 2: 33.64, 3: 33.64, 4: 33.64}}, 2: {"toughness": 128624, "difficulty": {1: 2.24, 2: 2.24, 3: 2.24, 4: 2.24}}, 3: {"toughness": 252748, "difficulty": {1: 0.63, 2: 0.63, 3: 0.63, 4: 0.63}}})
Enemy(id=27, name="Silver Knight Swordsman", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 132996, "difficulty": {1: 40.31, 2: 43.41, 3: 46.51, 4: 50.33}}, 2: {"toughness": 128624, "difficulty": {1: 2.31, 2: 2.48, 3: 2.66, 4: 2.88}}, 3: {"toughness": 252748, "difficulty": {1: 0.93, 2: 1.01, 3: 1.08, 4: 1.17}}})
Enemy(id=28, name="Skeleton Archer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 149924, "difficulty": {1: 13.54, 2: 13.54, 3: 13.54, 4: 13.54}}, 2: {"toughness": 171980, "difficulty": {1: 0.56, 2: 0.56, 3: 0.56, 4: 0.56}}, 3: {"toughness": 349528, "difficulty": {1: 0.2, 2: 0.2, 3: 0.2, 4: 0.2}}})
Enemy(id=29, name="Skeleton Beast", moveAttack=[True,True], expansion="Tomb of Giants", enemyType="regular", numberOfModels=1, health=5, armor=2, resist=2, repeat=1, iconForEffects=[0,0], attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True,True], dodge=2, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 15848, "difficulty": {1: 432.04, 2: 465.27, 3: 498.5, 4: 539.41}}, 2: {"toughness": 19688, "difficulty": {1: 19.99, 2: 21.53, 3: 23.06, 4: 24.96}}, 3: {"toughness": 67600, "difficulty": {1: 3.4, 2: 3.66, 3: 3.92, 4: 4.25}}})
Enemy(id=30, name="Skeleton Soldier", moveAttack=[True,True], expansion="Tomb of Giants", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, iconForEffects=[0,0], attacks=[2,2], attackType=["physical", "physical"], nodeAttack=[True,True], attackEffect=[{"bleed",},{"bleed",}], dodge=1, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 132996, "difficulty": {1: 34.56, 2: 37.22, 3: 39.88, 4: 43.15}}, 2: {"toughness": 128624, "difficulty": {1: 2.26, 2: 2.43, 3: 2.61, 4: 2.82}}, 3: {"toughness": 252748, "difficulty": {1: 0.63, 2: 0.68, 3: 0.73, 4: 0.79}}})
Enemy(id=31, name="Snow Rat", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=0, resist=1, iconForEffects=[0], attacks=[3], attackType=["physical"], attackEffect=[{"poison",}], dodge=1, move=[4], attackRange=[0], difficultyTiers={1: {"toughness": 154760, "difficulty": {1: 25.52, 2: 25.52, 3: 25.52, 4: 25.52}}, 2: {"toughness": 186956, "difficulty": {1: 1.23, 2: 1.23, 3: 1.23, 4: 1.23}}, 3: {"toughness": 363380, "difficulty": {1: 0.53, 2: 0.53, 3: 0.53, 4: 0.53}}})
Enemy(id=32, name="Stone Guardian", moveAttack=[True, True, False], expansion="Darkroot", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=3, iconForEffects=[0,0,1], attacks=[4,4,5], attackType=["physical", "physical", "physical"], nodeAttack=[True,True,True], dodge=1, move=[0,1, 0], attackRange=[0,0, 1], difficultyTiers={1: {"toughness": 9836, "difficulty": {1: 542.03, 2: 583.72, 3: 625.42, 4: 676.73}}, 2: {"toughness": 17116, "difficulty": {1: 15.14, 2: 16.3, 3: 17.47, 4: 18.9}}, 3: {"toughness": 59760, "difficulty": {1: 3.3, 2: 3.56, 3: 3.81, 4: 4.12}}})
Enemy(id=33, name="Stone Knight", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=5, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 12492, "difficulty": {1: 161.93, 2: 161.93, 3: 161.93, 4: 161.93}}, 2: {"toughness": 9844, "difficulty": {1: 11.79, 2: 11.79, 3: 11.79, 4: 11.79}}, 3: {"toughness": 38304, "difficulty": {1: 1.43, 2: 1.43, 3: 1.43, 4: 1.43}}})

# Enemy(id=49, name="Fire Witch", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=2, iconForEffects=[0,0], attacks=[0,4], attackType=["magic","magic"], dodge=1, move=[-1,0], attackRange=[0,3], nodesAttacked=[0,pathAttack], difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=50, name="Cathedral Evangelist", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=2, health=10, armor=0, resist=0, iconForEffects=[0, 0,0], attacks=[2, 5,0], attackType=["magic", "physical","physical"], dodge=1, move=[0,0,1], attackRange=[4,1,0], attackEffect=[{"bleed",},set(), set()], difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=51, name="Sewer Centipede", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[2], attackRange=[0], ambush=True, difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=52, name="Pontiff Knight", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=2, health=3, armor=1, resist=2, iconForEffects=[0,0], attacks=[4,5], attackType=["physical","magic"], dodge=2, move=[2,0], attackRange=[0,1], nodeAttack=[True,False], attackEffect=[{"frostbite",},set()], difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=53, name="Irithyllian Assassin Slave", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, iconForEffects=[0,0], attacks=[5,0], attackType=["physical", "physical"], dodge=2, move=[2,-2], attackRange=[0,0], attackEffect=[{"stagger",},set()], invisibility=True, difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=54, name="Irithyllian Sorcerer Slave", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=2, health=1, armor=0, resist=1, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=1, move=[0], attackRange=[4], invisibility=True, difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=55, name="Irithyllian Warrior Slave", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=4, health=2, armor=1, resist=0, iconForEffects=[0,0,0], attacks=[3,0,4], attackType=["magic","physical","physical"], nodeAttack=[True,False,False], dodge=1, move=[0,1,0], attackRange=[0,0,0], difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})
# Enemy(id=56, name="Irithyllian Beast-Hound", expansion="Irithyll of the Boreal Valley", enemyType="regular", numberOfModels=3, health=1, armor=0, resist=1, iconForEffects=[0], attacks=[3], attackType=["physical"], nodeAttack=[False], dodge=1, move=[4], attackRange=[0], frostbiteLeap=True, difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})


# Invaders
# Enemy(id=35, name="Armorer Dennis", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 6700.8, "difficulty": {1: 190.28, 2: 196.9, 3: 203.53, 4: 211.69}}, 2: {"toughness": 12129.2, "difficulty": {1: 5.55, 2: 5.74, 3: 5.92, 4: 6.15}}, 3: {"toughness": 35073.2, "difficulty": {1: 1.32, 2: 1.36, 3: 1.41, 4: 1.46}}})
# Enemy(id=36, name="Fencer Sharron", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 10097.29, "difficulty": {1: 479.64, 2: 492.23, 3: 504.82, 4: 520.31}}, 2: {"toughness": 14971, "difficulty": {1: 16.61, 2: 16.96, 3: 17.32, 4: 17.76}}, 3: {"toughness": 35240.57, "difficulty": {1: 5.38, 2: 5.49, 3: 5.6, 4: 5.73}}})
# Enemy(id=37, name="Invader Brylex", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 5420, "difficulty": {1: 1043.65, 2: 1086.46, 3: 1129.27, 4: 1181.96}}, 2: {"toughness": 7324, "difficulty": {1: 40.8, 2: 42.41, 3: 44.03, 4: 46.02}}, 3: {"toughness": 25180, "difficulty": {1: 9.22, 2: 9.6, 3: 9.98, 4: 10.45}}})
# Enemy(id=38, name="Kirk, Knight of Thorns", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 18312, "difficulty": {1: 184.41, 2: 190.97, 3: 197.53, 4: 205.61}}, 2: {"toughness": 26716, "difficulty": {1: 6.95, 2: 7.19, 3: 7.44, 4: 7.74}}, 3: {"toughness": 60520, "difficulty": {1: 2.4, 2: 2.48, 3: 2.57, 4: 2.67}}})
# Enemy(id=39, name="Longfinger Kirk", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 5800, "difficulty": {1: 1508.5, 2: 1542.38, 3: 1576.25, 4: 1617.94}}, 2: {"toughness": 7596, "difficulty": {1: 67.39, 2: 68.84, 3: 70.28, 4: 72.06}}, 3: {"toughness": 27076, "difficulty": {1: 15.72, 2: 16.05, 3: 16.38, 4: 16.78}}})
# Enemy(id=40, name="Maldron the Assassin", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 6700, "difficulty": {1: 798.72, 2: 818.4, 3: 838.08, 4: 862.3}}, 2: {"toughness": 8440, "difficulty": {1: 36.65, 2: 37.52, 3: 38.4, 4: 39.48}}, 3: {"toughness": 16820, "difficulty": {1: 13.94, 2: 14.28, 3: 14.63, 4: 15.05}}})
# Enemy(id=41, name="Maneater Mildred", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 9495.2, "difficulty": {1: 421.86, 2: 454.31, 3: 486.76, 4: 526.69}}, 2: {"toughness": 15845.8, "difficulty": {1: 11.71, 2: 12.62, 3: 13.52, 4: 14.63}}, 3: {"toughness": 36596.4, "difficulty": {1: 3.38, 2: 3.64, 3: 3.9, 4: 4.22}}})
# Enemy(id=42, name="Marvelous Chester", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 7436, "difficulty": {1: 1170.62, 2: 1176.68, 3: 1182.75, 4: 1190.21}}, 2: {"toughness": 12804, "difficulty": {1: 38.25, 2: 38.46, 3: 38.67, 4: 38.93}}, 3: {"toughness": 38280, "difficulty": {1: 10.2, 2: 10.26, 3: 10.32, 4: 10.39}}})
# Enemy(id=43, name="Melinda the Butcher", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 16497.8, "difficulty": {1: 169.36, 2: 177.74, 3: 186.12, 4: 196.43}}, 2: {"toughness": 24700.2, "difficulty": {1: 5.38, 2: 5.64, 3: 5.89, 4: 6.21}}, 3: {"toughness": 49450.2, "difficulty": {1: 1.74, 2: 1.82, 3: 1.91, 4: 2.01}}})
# Enemy(id=44, name="Oliver the Collector", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 16392.43, "difficulty": {1: 274.61, 2: 285.04, 3: 295.47, 4: 308.31}}, 2: {"toughness": 23513.57, "difficulty": {1: 8.31, 2: 8.6, 3: 8.89, 4: 9.24}}, 3: {"toughness": 47435, "difficulty": {1: 2.77, 2: 2.86, 3: 2.95, 4: 3.06}}})
# Enemy(id=45, name="Paladin Leeroy", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 4803.6, "difficulty": {1: 981.82, 2: 1050.67, 3: 1119.51, 4: 1204.25}}, 2: {"toughness": 6059.4, "difficulty": {1: 33.78, 2: 36.03, 3: 38.28, 4: 41.05}}, 3: {"toughness": 13589.4, "difficulty": {1: 10.91, 2: 11.61, 3: 12.3, 4: 13.16}}})
# Enemy(id=46, name="Xanthous King Jeremiah", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 19600, "difficulty": {1: 217.83, 2: 231.69, 3: 245.55, 4: 262.61}}, 2: {"toughness": 30800, "difficulty": {1: 8.06, 2: 8.56, 3: 9.07, 4: 9.7}}, 3: {"toughness": 71140, "difficulty": {1: 2.12, 2: 2.25, 3: 2.39, 4: 2.55}}})
# Enemy(id=47, name="Hungry Mimic", expansion="Explorers", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 12072, "difficulty": {1: 269.07, 2: 278.58, 3: 288.09, 4: 299.8}}, 2: {"toughness": 17920, "difficulty": {1: 9.84, 2: 10.18, 3: 10.52, 4: 10.94}}, 3: {"toughness": 41488, "difficulty": {1: 3.34, 2: 3.46, 3: 3.57, 4: 3.72}}})
# Enemy(id=48, name="Voracious Mimic", expansion="Explorers", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 4536, "difficulty": {1: 1018.51, 2: 1054.02, 3: 1089.53, 4: 1133.23}}, 2: {"toughness": 6244, "difficulty": {1: 41.34, 2: 42.75, 3: 44.17, 4: 45.91}}, 3: {"toughness": 21408, "difficulty": {1: 10.05, 2: 10.39, 3: 10.74, 4: 11.16}}})

# Enemy(name="Hungry Mimic - Raking Slash", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Hungry Mimic - Heavy Punch", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Hungry Mimic - Leaping Spin Kick", moveAttack=[True,True], expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0,0], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Hungry Mimic - Stomping Kick", expansion="Explorers", moveAttack=[True,True], enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0])
# Enemy(name="Hungry Mimic - Charging Chomp", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=3, move=[3], attackRange=[0])
# Enemy(name="Hungry Mimic - Vicious Chomp", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[0])
# Enemy(name="Hungry Mimic - Aggressive Grab", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0])
# Enemy(name="Voracious Mimic - Raking Slash", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Voracious Mimic - Heavy Punch", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Voracious Mimic - Leaping Spin Kick", moveAttack=[True,True], expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Voracious Mimic - Stomping Kick", moveAttack=[True,True], expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0,0], attacks=[7,7], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0])
# Enemy(name="Voracious Mimic - Charging Chomp", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=3, move=[3], attackRange=[0])
# Enemy(name="Voracious Mimic - Vicious Chomp", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], dodge=2, move=[0], attackRange=[0])
# Enemy(name="Voracious Mimic - Aggressive Grab", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=1, move=[2], attackRange=[0])

# Enemy(name="Armorer Dennis - Soul Spear Launch", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4])
# Enemy(name="Armorer Dennis - Soul Greatsword", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, iconForEffects=[0], attacks=[6], attackType=["magic"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Armorer Dennis - Soul Vortex", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, repeat=1, iconForEffects=[0], attacks=[4], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4])
# Enemy(name="Armorer Dennis - Soul Flash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=2, move=[2], attackRange=[0])
# Enemy(name="Armorer Dennis - Upward Slash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"stagger",}], dodge=1, move=[1], attackRange=[0])
# Enemy(name="Fencer Sharron - Puzzling Stone Sword Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0])
# Enemy(name="Fencer Sharron - Puzzling Stone Sword Whip", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0,0], attacks=[6,0], attackType=["physical", "physical"], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Fencer Sharron - Spider Fang Sword Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0])
# Enemy(name="Fencer Sharron - Spider Fang Sword Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0])
# Enemy(name="Fencer Sharron - Spider Fang Web Blast", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Fencer Sharron - Dual Sword Assault", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0])
# Enemy(name="Fencer Sharron - Dual Sword Slash", moveAttack=[True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], attackEffect=[{"stagger",},{"stagger",}], nodeAttack=[True,True], dodge=2, move=[0,1], attackRange=[0,0])
# Enemy(name="Invader Brylex - Leaping Strike", moveAttack=[True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, iconForEffects=[0,0], attacks=[7,7], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,4], attackRange=[0,0])
# Enemy(name="Invader Brylex - Trampling Charge", moveAttack=[True,True,True, True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, iconForEffects=[0,0,0,0], attacks=[4,4,4,4], attackType=["physical","physical", "physical", "physical"], nodeAttack=[True,True,True, True], dodge=1, move=[0,1,1,1], attackRange=[0,0,0,0])
# Enemy(name="Invader Brylex - Blade Dervish", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[4], attackRange=[0])
# Enemy(name="Invader Brylex - Fire Surge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Invader Brylex - Fire Whip", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=1, move=[2], attackRange=[0])
# Enemy(name="Kirk, Knight of Thorns - Forward Roll", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, iconForEffects=[0,0,0], attacks=[3,3,3], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], attackEffect=[{"bleed",},{"bleed",},{"bleed",}], dodge=1, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Kirk, Knight of Thorns - Shield Bash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"bleed",}], dodge=2, move=[1], attackRange=[0])
# Enemy(name="Kirk, Knight of Thorns - Shield Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], attackEffect=[{"bleed",}], dodge=1, move=[1], attackRange=[0])
# Enemy(name="Kirk, Knight of Thorns - Overhead Chop", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"bleed",}], dodge=1, move=[1], attackRange=[0])
# Enemy(name="Kirk, Knight of Thorns - Barbed Sword Thrust", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Longfinger Kirk - Rolling Barbs", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, iconForEffects=[0,0,0], attacks=[4,4,4], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], attackEffect=[{"bleed",}, {"bleed",}, {"bleed",}], dodge=1, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Longfinger Kirk - Lunging Stab", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], dodge=3, move=[1], attackRange=[0])
# Enemy(name="Longfinger Kirk - Cleave", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], attackEffect=[{"bleed",}], dodge=2, move=[1], attackRange=[0])
# Enemy(name="Longfinger Kirk - Crushing Blow", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], dodge=3, move=[4], attackRange=[0])
# Enemy(name="Longfinger Kirk - Barbed Sword Strikes", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Maldron the Assassin - Greatlance Lunge", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, iconForEffects=[0,0,1], attacks=[4,4,0], attackType=["physical","physical","physical"], nodeAttack=[True,True,False], dodge=3, move=[0,1,-1], attackRange=[0,0,1])
# Enemy(name="Maldron the Assassin - Double Lance Lunge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Maldron the Assassin - Leaping Lance Strike", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, iconForEffects=[0,0,1], attacks=[5,5,0], attackType=["physical","physical","physical"], nodeAttack=[True,True,False], dodge=2, move=[0,4,-2], attackRange=[0,0,2])
# Enemy(name="Maldron the Assassin - Jousting Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=3, move=[2], attackRange=[1])
# Enemy(name="Maldron the Assassin - Corrosive Urn Toss", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, iconForEffects=[0], attacks=[3], attackType=["magic"], attackEffect=[{"poison",}], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Maneater Mildred - Death Blow", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Maneater Mildred - Executioner Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[0])
# Enemy(name="Maneater Mildred - Guillotine", moveAttack=[True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, iconForEffects=[0,0], attacks=[5,5], attackType=["physical","physical"], attackEffect=[{"stagger",},{"stagger",}], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0])
# Enemy(name="Maneater Mildred - Butcher Chop", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Maneater Mildred - Butchery", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=2, move=[2], attackRange=[0])
# Enemy(name="Marvelous Chester - Crossbow Volley", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[0], attackRange=[4])
# Enemy(name="Marvelous Chester - Crossbow Snipe", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=4, move=[0], attackRange=[4])
# Enemy(name="Marvelous Chester - Throwing Knife Volley", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, repeat=1, iconForEffects=[0,0], attacks=[4,0], attackType=["physical", "physical"], attackEffect=[{"bleed",}, {"bleed",}], dodge=2, move=[0,-1], attackRange=[2,2])
# Enemy(name="Marvelous Chester - Throwing Knife Flurry", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, repeat=2, iconForEffects=[0,0], attacks=[3,0], attackType=["physical", "physical"], attackEffect=[{"bleed",}, {"bleed",}], dodge=1, move=[0,-1], attackRange=[2,2])
# Enemy(name="Marvelous Chester - Spinning Low Kick", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=3, move=[1,-1], attackRange=[0,1])
# Enemy(name="Melinda the Butcher - Double Smash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, repeat=1, iconForEffects=[0], attacks=[3], attackType=["physical"], dodge=2, move=[1], attackRange=[0])
# Enemy(name="Melinda the Butcher - Cleaving Strikes", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, repeat=1, iconForEffects=[0,0], attacks=[4,0], attackType=["physical", "physical"], dodge=1, move=[0,1], attackRange=[0,0])
# Enemy(name="Melinda the Butcher - Jumping Cleave", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, repeat=2, iconForEffects=[0,0], attacks=[3,0], attackType=["physical", "physical"], dodge=1, move=[0,4], attackRange=[0,0])
# Enemy(name="Melinda the Butcher - Greataxe Sweep", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=2, move=[1], attackRange=[0])
# Enemy(name="Melinda the Butcher - Sweeping Advance", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[0])
# Enemy(name="Oliver the Collector - Bone Fist Punches", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=2, move=[1], attackRange=[0])
# Enemy(name="Oliver the Collector - Minotaur Helm Charge", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, iconForEffects=[0,0,0], attacks=[5,5,5], attackType=["physical","physical","physical"], attackEffect=[{"stagger",},{"stagger",},{"stagger",}], nodeAttack=[True,True,True], dodge=1, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Oliver the Collector - Puzzling Stone Sword Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=3, move=[1], attackRange=[0])
# Enemy(name="Oliver the Collector - Majestic Greatsword Slash", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, iconForEffects=[0,0,1], attacks=[4,4,0], attackType=["physical","physical","physical"], dodge=2, move=[0,1,-1], attackRange=[0,0,1])
# Enemy(name="Oliver the Collector - Santier's Spear Lunge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"stagger",}], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Oliver the Collector - Smelter Hammer Whirlwind", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, repeat=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Oliver the Collector - Ricard's Rapier Thrust", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, iconForEffects=[0,0], attacks=[4,0], attackType=["physical", "physical"], dodge=2, move=[0,-1], attackRange=[1,1])
# Enemy(name="Paladin Leeroy - Advancing Grant Slam", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Paladin Leeroy - Grant Slam Withdrawal", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, iconForEffects=[0,0], attacks=[6,0], attackType=["physical", "physical"], attackEffect=[{"stagger",},{"stagger",}], nodeAttack=[True, False], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Paladin Leeroy - Sanctus Shield Slam", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[0])
# Enemy(name="Paladin Leeroy - Sanctus Shield Dash", moveAttack=[True,True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, iconForEffects=[0,0,0], attacks=[4,4,4], attackType=["physical","physical","physical"], nodeAttack=[True,True,True], dodge=2, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Paladin Leeroy - Wrath of the Gods", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Xanthous King Jeremiah - Great Chaos Fireball", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, iconForEffects=[0], attacks=[5], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4])
# Enemy(name="Xanthous King Jeremiah - Chaos Fire Whip", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Xanthous King Jeremiah - Chaos Storm", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, repeat=1, iconForEffects=[0], attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Xanthous King Jeremiah - Fiery Retreat", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, iconForEffects=[0], attacks=[4], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Xanthous King Jeremiah - Whiplash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"bleed",}], nodeAttack=[True], dodge=1, move=[2], attackRange=[0])

# # Mini Bosses
# Enemy(name="Old Dragonslayer - Darkness Bolt", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=3, move=[0], attackRange=[3])
# Enemy(name="Old Dragonslayer - Spear Lunge", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[2])
# Enemy(name="Old Dragonslayer - Leaping Darkness", weakArcs=0, expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[12], dodge=1, move=[4], attackRange=[1])
# Enemy(name="Old Dragonslayer - Skewering Charge", iconForEffects=[0,0,0], moveAttack=[True,True,True], expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[4,4,4], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], dodge=1, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Old Dragonslayer - Spear Sweep", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0,1], attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[6,0], dodge=2, move=[0,1], attackRange=[2,0])
# Enemy(name="Old Dragonslayer - Darkness Falls", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[6], dodge=1, move=[4], attackRange=[2])
# Enemy(name="Old Dragonslayer - Massive Sweep", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[14,0], dodge=2, move=[0,1], attackRange=[2,0])
# Enemy(name="Old Dragonslayer - Lunging Combo", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, iconForEffects=[0,1], attacks=[5,5], attackType=["physical", "physical"], dodge=2, move=[0,1], attackRange=[1,1])
# Enemy(name="Asylum Demon - Mighty Hammer Smash", iconForEffects=[0], moveAttack=[True], windup=True, expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[4], attackRange=[0])
# Enemy(name="Asylum Demon - Leaping Hammer Smash", iconForEffects=[0,0], expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, moveAttack=[True,True], attacks=[4,4], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,4], attackRange=[0,0])
# Enemy(name="Asylum Demon - Ground Pound", weakArcs=0, iconForEffects=[0], windup=True, expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[12], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Asylum Demon - Delayed Hammer Drive", iconForEffects=[0,0], moveAttack=[True,True], windup=True, expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5,5], attackType=["physical", "physical"], attackEffect=[{"stagger",}, {"stagger",}], nodeAttack=[True,True], dodge=1, move=[1,1], attackRange=[0,0])
# Enemy(name="Asylum Demon - Hammer Drive", iconForEffects=[0,0,0], moveAttack=[True,True,True], expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,4,4], attackType=["physical","physical", "physical"], attackEffect=[{"stagger",}, {"stagger",}, {"stagger",}], nodeAttack=[True,True,True], dodge=2, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Asylum Demon - Retreating Sweep", iconForEffects=[0,1], expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Asylum Demon - Lumbering Swings", iconForEffects=[0], windup=True, expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, repeat=1, attacks=[4], attackType=["physical"], nodesAttacked=[12], dodge=1, move=[2], attackRange=[1])
# Enemy(name="Asylum Demon - Sweeping Strikes", iconForEffects=[0,1], expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], nodesAttacked=[7,7], dodge=2, move=[1,0], attackRange=[1,1])
# Enemy(name="Asylum Demon - Crushing Leaps", iconForEffects=[0,0,1], moveAttack=[True,True,True], weakArcs=0, expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5,5,5], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], dodge=1, move=[0,4,4], attackRange=[0,0,0])
# Enemy(name="Boreal Outrider Knight - Backhand Slashes", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"frostbite",}], nodesAttacked=[7], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Boreal Outrider Knight - Overhand Slash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Boreal Outrider Knight - Sweeping Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Boreal Outrider Knight - Chilling Thrust", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, iconForEffects=[0], attacks=[4], attackType=["magic"], attackEffect=[{"frostbite",}], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Boreal Outrider Knight - Leaping Frost", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, repeat=1, iconForEffects=[0,1], attacks=[4,0], attackType=["physical", "physical"], attackEffect=[{"frostbite",}, set()], nodesAttacked=[7,0], dodge=1, move=[0,4], attackRange=[1,1])
# Enemy(name="Boreal Outrider Knight - Lunging Triple Slash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, repeat=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Boreal Outrider Knight - Uppercut Slam", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"frostbite",}], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Boreal Outrider Knight - Frost Breath", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[10], attackEffect=[{"frostbite",}], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Winged Knight - Backhand Shaft Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Winged Knight - Overhand Smash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Winged Knight - Double Slash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[10], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Winged Knight - Whirlwind", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, repeat=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[12], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Winged Knight - Pillars of Light", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[16], dodge=1, move=[0], attackRange=[4])
# Enemy(name="Winged Knight - Sweeping Blade Swing", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Winged Knight - Diagonal Uppercut", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=1, move=[0,-1], attackRange=[1,0])
# Enemy(name="Winged Knight - Charging Assault", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Black Knight - Overhead Swing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[6,0], dodge=2, move=[0,2], attackRange=[2,0])
# Enemy(name="Black Knight - Heavy Slash", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], attackEffect=[{"stagger",}, set()], nodeAttack=[True, False], dodge=1, move=[0,1], attackRange=[2,0])
# Enemy(name="Black Knight - Backswing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], attackEffect=[{"stagger",}, set()], nodeAttack=[True, False], dodge=1, move=[0,-2], attackRange=[2,2])
# Enemy(name="Black Knight - Vicious Hack", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=1, move=[0,2], attackRange=[2,2])
# Enemy(name="Black Knight - Defensive Strike", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0,1], attackRange=[2,2])
# Enemy(name="Black Knight - Wide Swing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[4,0], attackType=["physical", "physical"], attackEffect=[{"stagger",}, set()], nodesAttacked=[7,0], dodge=2, move=[0,1], attackRange=[2,2])
# Enemy(name="Black Knight - Massive Swing", weakArcs=0, expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[14], dodge=2, move=[0], attackRange=[2])
# Enemy(name="Black Knight - Hacking Slash", moveAttack=[False,True,True], weakArcs=0, expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1,1], attacks=[5,4,4], attackType=["physical", "physical", "physical"], nodesAttacked=[4,0,0], attackEffect=[{"stagger",}, set(), set()], nodeAttack=[False, True,True], dodge=2, move=[0,0,1], attackRange=[2,0,0])
# Enemy(name="Black Knight - Charge", weakArcs=0, expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodeAttack=[True, False], attackEffect=[{"stagger",},set()], dodge=2, move=[0,3], attackRange=[2,0])
# Enemy(name="Heavy Knight - Defensive Swipe", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0,1], attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=3, move=[0,-2], attackRange=[1,2])
# Enemy(name="Heavy Knight - Charging Chop", weakArcs=2, expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Heavy Knight - Defensive Chop", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0,-2], attackRange=[1,2])
# Enemy(name="Heavy Knight - Overhead Chop", weakArcs=2, expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Heavy Knight - Shield Swipe", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[10], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Heavy Knight - Double Slash", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[10], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Heavy Knight - Slashing Blade", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Heavy Knight - Double Chop", weakArcs=2, expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Heavy Knight - Shield Smash", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], dodge=3, move=[1], attackRange=[1])
# Enemy(name="Titanite Demon - Double Swing", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Titanite Demon - Tail Whip", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[10], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Titanite Demon - Grab & Smash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Titanite Demon - Lightning Bolt", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Titanite Demon - Vicious Swing", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Titanite Demon - Sweeping Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[14], dodge=1, move=[-2], attackRange=[2])
# Enemy(name="Titanite Demon - Vaulting Slam", moveAttack=[True], weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[4], attackRange=[0])
# Enemy(name="Titanite Demon - Double Pole Crush", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, repeat=1, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[4,0], dodge=1, move=[0,-1], attackRange=[2,2])
# Enemy(name="Gargoyle - Sweeping Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Gargoyle - Halberd Thrust", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Gargoyle - Tail Sweep", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Gargoyle - Tail Whip", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0,1], attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=2, move=[0,-1], attackRange=[1,1])
# Enemy(name="Gargoyle - Electric Breath", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[4], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Gargoyle - Flying Tail Whip", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Gargoyle - Swooping Cleave", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Gargoyle - Aerial Electric Breath", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[6], dodge=2, move=[0], attackRange=[2])

# # Main bosses
# Enemy(name="Smelter Demon - Double Sweep", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, repeat=1, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Smelter Demon - Overhead Chop", weakArcs=2, expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], attackEffect=[{"stagger",}], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Smelter Demon - Fiery Blast", weakArcs=0, expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[12], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Smelter Demon - Leaping Impalement Strike", moveAttack=[True,True,False], weakArcs=2, expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0,0,1], attacks=[4,4,4], attackType=["physical","physical", "physical"], nodeAttack=[True,True, False], dodge=2, move=[0,4,0], attackRange=[0,0,1])
# Enemy(name="Smelter Demon - Sweeping Slash", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Smelter Demon - Lunging Strike", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0,1,2], attacks=[0,0,7], attackType=["physical", "physical", "physical"], dodge=1, move=[-1,2,0], attackRange=[1,1,1])
# Enemy(name="Smelter Demon - Flaming Impalement Strike", moveAttack=[True,True,False], weakArcs=2, expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0,0,1], attacks=[4,4,4], attackType=["physical","physical", "magic"], nodeAttack=[True,True,True], dodge=2, move=[0,4,0], attackRange=[0,0,1])
# Enemy(name="Smelter Demon - Fiery Explosion", weakArcs=0, expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[12], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Smelter Demon - Flaming Double Sweep", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, repeat=1, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], nodesAttacked=[7,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Smelter Demon - Flaming Sweeping Slash", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[15], dodge=1, move=[1], attackRange=[2])
# Enemy(name="Smelter Demon - Flaming Overhead Chop", weakArcs=2, expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodeAttack=[True], attackEffect=[{"stagger",}], dodge=2, move=[1], attackRange=[2])
# Enemy(name="Smelter Demon - Flame Wave", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[6], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Smelter Demon - Flaming Lunging Strike", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=22, armor=4, resist=3, iconForEffects=[0,1,2], attacks=[0,0,7], attackType=["magic", "magic", "magic"], dodge=1, move=[-1,2,0], attackRange=[2,2,2])
# Enemy(name="The Pursuer - Wide Blade Swing 1", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Wide Blade Swing 2", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Wide Blade Swing 3", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Stabbing Strike 1", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Stabbing Strike 2", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Rising Blade Swing", weakArcs=2, expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[0], attackRange=[1])
# Enemy(name="The Pursuer - Overhead Cleave", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[2], attackRange=[1])
# Enemy(name="The Pursuer - Cursed Impale", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Dark Magic", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[4], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[4])
# Enemy(name="The Pursuer - Shield Bash", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="The Pursuer - Shield Smash", expansion="Explorers", enemyType="main boss", numberOfModels=1, health=28, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Icy Blast", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0,1], attackRange=[2,2])
# Enemy(name="Crossbreed Priscilla - Flanking Slash", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[10], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Scything Withdrawal", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], attackEffect=[{"bleed",}, set()], nodesAttacked=[10,0], dodge=2, move=[0,-1], attackRange=[1,1])
# Enemy(name="Crossbreed Priscilla - Blizzard", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[14,0], dodge=1, move=[0,1], attackRange=[2,2])
# Enemy(name="Crossbreed Priscilla - Scythe Strike", weakArcs=2, expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Scythe Slash", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Snowstorm", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0,1], attacks=[4,0], attackType=["magic", "magic"], nodesAttacked=[14,0], dodge=2, move=[0,1], attackRange=[2,2])
# Enemy(name="Crossbreed Priscilla - Backslash", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[10], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Mournful Gaze", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0,1], attacks=[0,3], attackEffect=[set(), {"frostbite",}], attackType=["magic", "magic"], nodesAttacked=[0,14], dodge=3, move=[-2,0], attackRange=[4,4])
# Enemy(name="Crossbreed Priscilla - Scything Lunge", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[10], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Double Lunge", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Double Strike", weakArcs=2, expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"bleed",}], nodeAttack=[True], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Crossbreed Priscilla - Double Slash", expansion="Painted World of Ariamis", enemyType="main boss", numberOfModels=1, health=40, armor=2, resist=1, iconForEffects=[0], attacks=[5], repeat=1, attackType=["physical"], attackEffect=[{"bleed",}], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Gravelord Nito - Gravelord Greatsword", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0,1], attacks=[0,4], attackType=["magic", "magic"], nodeAttack=[False, True], dodge=1, move=[-1,0], attackRange=[4,4])
# Enemy(name="Gravelord Nito - Death Wave", weakArcs=0, expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[12], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Gravelord Nito - Miasma", weakArcs=0, expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[3], attackType=["magic"], nodesAttacked=[16], dodge=2, move=[0], attackRange=[3])
# Enemy(name="Gravelord Nito - Sword Slam", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Gravelord Nito - Sword Sweep", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Gravelord Nito - Deathly Thrust", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], attackEffect=[{"poison",}], dodge=1, move=[1], attackRange=[2])
# Enemy(name="Gravelord Nito - Death Grip", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], dodge=2, move=[0,1], attackRange=[1,1])
# Enemy(name="Gravelord Nito - Deathly Strike", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=1, move=[0,2], attackRange=[1,1])
# Enemy(name="Gravelord Nito - Toxicity", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[10], attackEffect=[{"poison",}], dodge=1, move=[1], attackRange=[2])
# Enemy(name="Gravelord Nito - Entropy", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], attackEffect=[{"poison",}], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Gravelord Nito - Creeping Death", moveAttack=[True,True], expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, repeat=2, iconForEffects=[0,0], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], attackEffect=[{"poison",},{"poison",}], dodge=1, move=[0,1], attackRange=[0,0])
# Enemy(name="Gravelord Nito - Death's Embrace", weakArcs=0, expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"poison",}], nodeAttack=[True], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Gravelord Nito - Lunging Cleave", expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], attackEffect=[{"poison",}], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Dashing Slice", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Spinning Slash", weakArcs=0, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[12], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Sword Slam", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Evasive Strike", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Great Grey Wolf Sif - Upward Slash", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[7], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Pouncing Assault", moveAttack=[True,True], expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], attackEffect=[{"stagger",},{"stagger",}], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Great Grey Wolf Sif - Slashing Assault", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0,1], attacks=[5,5], attackType=["physical", "physical"], nodesAttacked=[7,7], dodge=1, move=[1,0], attackRange=[1,1])
# Enemy(name="Great Grey Wolf Sif - Sidestep Cleave", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Sidestep Slash", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Slashing Retreat", weakArcs=0, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[12,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Great Grey Wolf Sif - Feral Onslaught", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[10], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Great Grey Wolf Sif - Cyclone Strikes", weakArcs=0, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, repeat=1, iconForEffects=[0,1], attacks=[7,0], attackType=["physical", "physical"], attackEffect=[{"stagger",}, set()], nodesAttacked=[12,0], dodge=2, move=[0,1], attackRange=[1,1])
# Enemy(name="Great Grey Wolf Sif - Savage Retreat", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, repeat=2, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], attackEffect=[{"stagger",}, set()], nodesAttacked=[10,0], dodge=2, move=[0,-1], attackRange=[1,1])
# Enemy(name="Great Grey Wolf Sif - Limping Strike", weakArcs=3, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=36, armor=2, resist=3, iconForEffects=[0], attacks=[2], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Gliding Stab", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Hammer Smash", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Ornstein & Smough - Evasive Sweep", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[4], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[-1], attackRange=[2])
# Enemy(name="Ornstein & Smough - Trampling Charge", iconForEffects=[0,0,0], moveAttack=[True,True,True], expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, repeat=1, attacks=[5,5,5], attackType=["physical","physical","physical"], nodeAttack=[True,True,True], dodge=1, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Ornstein & Smough - Spear Slam", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[4], attackRange=[1])
# Enemy(name="Ornstein & Smough - Hammer Sweep", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=1, move=[0,-1], attackRange=[1,1])
# Enemy(name="Ornstein & Smough - Swiping Combo", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Bonzai Drop", moveAttack=[True,True], weakArcs=0, expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0,0], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Ornstein & Smough - Lightning Bolt", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4])
# Enemy(name="Ornstein & Smough - Jumping Slam", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Charged Swiping Combo", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, repeat=2, iconForEffects=[0], attacks=[5], attackType=["magic"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Charged Bolt", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], dodge=3, move=[0], attackRange=[4])
# Enemy(name="Ornstein & Smough - Electric Clash", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[12], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Ornstein & Smough - Lightning Stab", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[7], attackType=["magic"], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - High Voltage", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=30, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], dodge=1, move=[4], attackRange=[1])
# Enemy(name="Ornstein & Smough - Electric Hammer Smash", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Lightning Sweep", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Jumping Volt Slam", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[10], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Ornstein & Smough - Electric Bonzai Drop", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[7], attackType=["magic"], nodesAttacked=[12], dodge=1, move=[4], attackRange=[1])
# Enemy(name="Ornstein & Smough - Charged Charge", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=45, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["magic"], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Uppercut", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[3], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Blade Dance", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[2], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Plunging Assault", moveAttack=[True,True], weakArcs=0, expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, repeat=2, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,4], attackRange=[0,0])
# Enemy(name="Dancer of the Boreal Valley - Whirling Blades", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, repeat=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Double Slash", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Plunging Attack", moveAttack=[True,True], weakArcs=0, expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Dancer of the Boreal Valley - Triple Slash", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, repeat=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Lunging Thrust", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[3], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Backhand Blade Swipe", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Flashing Blade", weakArcs=0, expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[12], dodge=1, move=[2], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Deadly Grasp", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Sweeping Blade Swipe", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Dancer of the Boreal Valley - Ash Cloud", expansion="Dark Souls The Board Game", enemyType="main boss", numberOfModels=1, health=34, armor=2, resist=2, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], nodesAttacked=[4,0], dodge=1, move=[0,4], attackRange=[4,0])
# Enemy(name="Artorias - Steadfast Leap", weakArcs=0, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[12], dodge=2, move=[4], attackRange=[1])
# Enemy(name="Artorias - Somersault Slam", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Artorias - Overhead Cleave", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Artorias - Charging Slash", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[2], attackRange=[1])
# Enemy(name="Artorias - Heavy Thrust", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[1])
# Enemy(name="Artorias - Spinning Slash", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=2, move=[0,-1], attackRange=[1,1])
# Enemy(name="Artorias - Abyss Sludge", expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], attackEffect=[{"stagger",}, set()], nodesAttacked=[10, 0], dodge=1, move=[1,4], attackRange=[1,0])
# Enemy(name="Artorias - Wrath of the Abyss", weakArcs=0, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[12], dodge=1, move=[0], attackRange=[2])
# Enemy(name="Artorias - Somersault Strike", moveAttack=[True,True], expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0,0], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Artorias - Retreating Strike", weakArcs=0, expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], attackEffect=[{"stagger",}, set()], nodesAttacked=[4,0], dodge=2, move=[0,-2], attackRange=[1,2])
# Enemy(name="Artorias - Abyss Assault", moveAttack=[True,True,False], expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0,0,1], attacks=[5,5,5], attackType=["physical","physical", "magic"], nodesAttacked=[0,0,10], nodeAttack=[True,True, False], dodge=2, move=[0,4,0], attackRange=[0,0,1])
# Enemy(name="Artorias - Leaping Fury", moveAttack=[True,True,True], expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=3, iconForEffects=[0,0,1], attacks=[5,5,6], attackType=["physical","physical","physical"], nodeAttack=[True,True,True], dodge=2, move=[0,4,4], attackRange=[0,0,0])
# Enemy(name="Artorias - Lunging Cleave", moveAttack=[True,True,False], expansion="Darkroot", enemyType="main boss", numberOfModels=1, health=25, armor=3, resist=2, iconForEffects=[0,0,1], attacks=[5,5,6], attackType=["physical","physical", "physical"], nodesAttacked=[0,0,4], nodeAttack=[True,True, False], dodge=2, move=[0,4,0], attackRange=[0,0,1])
# Enemy(name="Sir Alonne - Lunging Slash Combo", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Sir Alonne - Triple Slash Combo", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, repeat=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Sir Alonne - Stabbing Slash Combo", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Sir Alonne - Fast Katana Lunge", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0,1], attacks=[0,5], attackType=["physical", "physical"], nodesAttacked=[0,4], dodge=2, move=[-1,2], attackRange=[1,1])
# Enemy(name="Sir Alonne - Charging Katana Slash", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0,1], attacks=[0,6], attackType=["physical", "physical"], nodesAttacked=[0,7], dodge=1, move=[-1,2], attackRange=[1,1])
# Enemy(name="Sir Alonne - Charging Katana Lunge", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0,1], attacks=[0,6], attackType=["physical", "physical"], dodge=2, move=[-1,2], attackRange=[1,1])
# Enemy(name="Sir Alonne - Dark Wave", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[4])
# Enemy(name="Sir Alonne - Life Drain", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0], attacks=[7], attackType=["magic"], dodge=1, move=[0], attackRange=[0])
# Enemy(name="Sir Alonne - Double Slash Combo", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, repeat=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Sir Alonne - Left Sidestep Slash", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Sir Alonne - Stab & Slash Combo", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0,1], attacks=[5,5], attackType=["physical", "physical"], nodesAttacked=[0,4], dodge=1, move=[1,0], attackRange=[1,1])
# Enemy(name="Sir Alonne - Right Sidestep Slash", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Sir Alonne - Katana Plunge", expansion="Iron Keep", enemyType="main boss", numberOfModels=1, health=26, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[4], attackRange=[1])

# # Mega bosses
# Enemy(name="Stray Demon - Mighty Hammer Smash", windup=True, expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0], attacks=[8], attackType=["physical"], nodeAttack=[True], dodge=1, move=[4], attackRange=[0])
# Enemy(name="Stray Demon - Leaping Hammer Smash", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0,0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Stray Demon - Ground Pound", windup=True, expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0], attacks=[9], attackType=["physical"], attackEffect=[{"stagger",}], nodesAttacked=[12], dodge=1, move=[0], attackRange=[1])
# Enemy(name="Stray Demon - Delayed Hammer Drive", windup=True, expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0,0], attacks=[8,8], attackType=["physical", "physical"], attackEffect=[{"stagger",}, {"stagger",}], nodeAttack=[True,True], dodge=1, move=[1,1], attackRange=[0,0])
# Enemy(name="Stray Demon - Hammer Drive", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0,0,0], attacks=[6,6,6], attackType=["physical","physical", "physical"], attackEffect=[{"stagger",},{"stagger",}, {"stagger",}], nodeAttack=[True,True,True], dodge=3, move=[0,1,1], attackRange=[0,0,0])
# Enemy(name="Stray Demon - Retreating Sweep", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=2, move=[0,-1], attackRange=[1,1])
# Enemy(name="Stray Demon - Lumbering Swings", windup=True, expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, repeat=1, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[12], dodge=1, move=[2], attackRange=[1])
# Enemy(name="Stray Demon - Sweeping Strikes", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0,1], attacks=[7,7], attackType=["physical", "physical"], nodesAttacked=[7,7], dodge=2, move=[1,0], attackRange=[1,1])
# Enemy(name="Stray Demon - Crushing Leaps", weakArcs=0, expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0,0,1], attacks=[7,7,7], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], dodge=2, move=[0,4,4], attackRange=[0,0,0])
# Enemy(name="Stray Demon - Sidestep Right Sweep", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Stray Demon - Sidestep Left Sweep", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], dodge=2, move=[0], attackRange=[1])
# Enemy(name="Stray Demon - Hammer Blast", expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[20], dodge=3, move=[0], attackRange=[2])
# Enemy(name="Stray Demon - Shockwave", windup=True, expansion="Asylum Demon", enemyType="mega boss", numberOfModels=1, health=34, armor=4, resist=3, iconForEffects=[0], attacks=[8], attackType=["magic"], nodesAttacked=[20], dodge=1, move=[0], attackRange=[2])
# Enemy(name="Manus, Father of the Abyss - Ground Slam", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=3, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[3,0], move=[0,1], attackRange=[1,1])
# Enemy(name="Manus, Father of the Abyss - Diving Slam", moveAttack=[True,True], expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=1, weakArcs=0, iconForEffects=[0,0], attacks=[7,7], attackType=["physical","physical"], nodeAttack=[True,True], move=[0,4], attackRange=[0,0])
# Enemy(name="Manus, Father of the Abyss - Sweeping Strike", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[7,0], move=[0,1], attackRange=[1,0])
# Enemy(name="Manus, Father of the Abyss - Extended Sweep", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[12], move=[0], attackRange=[2])
# Enemy(name="Manus, Father of the Abyss - Back Swipe", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=3, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[5,0], move=[0,1], attackRange=[1,0])
# Enemy(name="Manus, Father of the Abyss - Frenzied Attacks", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, repeat=2, dodge=1, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[4,0], move=[0,1], attackRange=[1,0])
# Enemy(name="Manus, Father of the Abyss - Crushing Palm", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodeAttack=[True], move=[1], attackRange=[1])
# Enemy(name="Manus, Father of the Abyss - Catalyst Strike", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[4], move=[1], attackRange=[1])
# Enemy(name="Manus, Father of the Abyss - Catalyst Smash", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[6], attackType=["magic"], nodeAttack=[True], move=[1], attackRange=[1])
# Enemy(name="Manus, Father of the Abyss - Dark Orb Barrage", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=3, iconForEffects=[0,1], attacks=[5,0], attackType=["magic", "magic"], nodesAttacked=[3,0], move=[0,1], attackRange=[3,0])
# Enemy(name="Manus, Father of the Abyss - Descending Darkness", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], nodesAttacked=[12,0], move=[0,1], attackRange=[2,0])
# Enemy(name="Manus, Father of the Abyss - Abyss Rain", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=3, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[24], move=[0], attackRange=[3], weakArcs=0)
# Enemy(name="Manus, Father of the Abyss - Abyss Cage", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=2, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], nodesAttacked=[12,0], move=[0,1], attackRange=[2,0])
# Enemy(name="Manus, Father of the Abyss - Ring of Darkfire", expansion="Manus, Father of the Abyss", enemyType="mega boss", numberOfModels=1, health=48, armor=3, resist=3, dodge=1, iconForEffects=[0,1], attacks=[7,0], attackType=["magic", "magic"], nodesAttacked=[21,0], move=[0,1], attackRange=[3,0])
# Enemy(name="The Four Kings - Horizontal Slash", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], move=[1], attackRange=[1])
# Enemy(name="The Four Kings - Upward Slash", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",}], attackType=["physical"], nodesAttacked=[7], move=[0], attackRange=[1])
# Enemy(name="The Four Kings - Downward Slash", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",}], attackType=["physical"], nodesAttacked=[7], move=[0], attackRange=[1])
# Enemy(name="The Four Kings - Forward Thrust", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[6], attackType=["physical"], move=[1], attackRange=[2])
# Enemy(name="The Four Kings - Wrath of the Kings", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, weakArcs=0, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[12], move=[0], attackRange=[1])
# Enemy(name="The Four Kings - Homing Arrow Mass", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[4], move=[0], attackRange=[4])
# Enemy(name="The Four Kings - Homing Abyss Arrow", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[0], move=[0], attackRange=[4])
# Enemy(name="The Four Kings - Lifedrain Grab", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",1}], attackType=["magic"], move=[1], attackRange=[1])
# Enemy(name="The Four Kings - Evasive Slash", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[10,0], move=[1,-1], attackRange=[1,0])
# Enemy(name="The Four Kings - Thrust & Retreat", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=2, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], move=[1,-1], attackRange=[2,0])
# Enemy(name="The Four Kings - Cautious Arrow Mass", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, iconForEffects=[0,1], attacks=[5,0], attackType=["magic", "magic"], nodesAttacked=[4,0], move=[0,-1], attackRange=[4,0])
# Enemy(name="The Four Kings - Evasive Abyss Arrow", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=2, iconForEffects=[0,1], attacks=[5,0], attackType=["magic", "magic"], move=[0,-1], attackRange=[4,0])
# Enemy(name="The Four Kings - Precision Slash", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=3, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], move=[1], attackRange=[1])
# Enemy(name="The Four Kings - Unerring Thrust", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=3, iconForEffects=[0], attacks=[6], attackType=["physical"], move=[1], attackRange=[2])
# Enemy(name="The Four Kings - Blazing Wrath", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=3, weakArcs=0, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[12], move=[0], attackRange=[1])
# Enemy(name="The Four Kings - Pinpoint Homing Arrows", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=3, iconForEffects=[0], attacks=[4], attackType=["magic"], nodesAttacked=[4], move=[0], attackRange=[4])
# Enemy(name="The Four Kings - Executioner's Slash", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=2, weakArcs=0, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",}], attackType=["physical"], nodesAttacked=[4], move=[1], attackRange=[1])
# Enemy(name="The Four Kings - Shockwave", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=1, weakArcs=0, iconForEffects=[0], attacks=[5], attackType=["magic"], attackEffect=[{"stagger",}], nodesAttacked=[12], move=[0], attackRange=[1])
# Enemy(name="The Four Kings - Into the Abyss", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=2, weakArcs=0, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",}], attackType=["magic"], move=[0], attackRange=[4])
# Enemy(name="The Four Kings - Lifedrain Death Grasp", expansion="The Four Kings", enemyType="mega boss", numberOfModels=1, health=25, armor=2, resist=2, dodge=2, weakArcs=0, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",}], attackType=["physical"], move=[1], attackRange=[1])
# Enemy(name="The Last Giant - Left Foot Stomp", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[1])
# Enemy(name="The Last Giant - Right Foot Stomp", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[1])
# Enemy(name="The Last Giant - Stomp Rush", moveAttack=[True,True], expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, repeat=2, dodge=1, iconForEffects=[0,0], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], move=[0,1], attackRange=[0,0])
# Enemy(name="The Last Giant - Backstep Stomp", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[10,0], move=[0,-1], attackRange=[1,0])
# Enemy(name="The Last Giant - Triple Stomp", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=1, iconForEffects=[0,1,2], attacks=[5,5,5], attackType=["physical", "physical", "physical"], nodesAttacked=[7,7,7], move=[0,0,0], attackRange=[1,1,1])
# Enemy(name="The Last Giant - Sweeping Strike", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[1], windup=True)
# Enemy(name="The Last Giant - Backhand Strike", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[1], windup=True)
# Enemy(name="The Last Giant - Clubbing Blow", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodeAttack=[True], move=[2], attackRange=[1], windup=True)
# Enemy(name="The Last Giant - Heavy Swings", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, repeat=1, dodge=1, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[10,0], move=[0,1], attackRange=[1,1], windup=True)
# Enemy(name="The Last Giant - Overhead Smash", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=3, iconForEffects=[0], attacks=[6], attackEffect=[{"stagger",}], attackType=["physical"], nodeAttack=[True], move=[0], attackRange=[1], windup=True)
# Enemy(name="The Last Giant - Arm Club Sweep", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[2], windup=True)
# Enemy(name="The Last Giant - Arm Club Backhand", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[2], windup=True)
# Enemy(name="The Last Giant - Beat You With It", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[], move=[2], attackRange=[2], windup=True)
# Enemy(name="The Last Giant - Armed Swings", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, repeat=1, dodge=1, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[20,0], move=[0,1], attackRange=[2,2])
# Enemy(name="The Last Giant - Arm Smash", expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=3, iconForEffects=[0], attacks=[6], attackType=["physical"], attackEffect=[{"stagger",}], nodeAttack=[True], move=[0], attackRange=[2], windup=True)
# Enemy(name="The Last Giant - Falling Slam", moveAttack=[True,True], expansion="The Last Giant", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, dodge=1, weakArcs=4, iconForEffects=[0,0], attacks=[9,9], attackType=["physical","physical"], nodeAttack=[True,True], move=[0,4], attackRange=[0,0])
# Enemy(name="Guardian Dragon - Fireball", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodeAttack=[True], move=[0], attackRange=[3], dodge=3)
# Enemy(name="Guardian Dragon - Fire Breath", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, repeat=1, iconForEffects=[0,1], attacks=[5,0], attackType=["magic", "magic"], nodesAttacked=[4,0], move=[0,-1], attackRange=[2,2], dodge=1)
# Enemy(name="Guardian Dragon - Leaping Breath", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, repeat=1, iconForEffects=[0,1], attacks=[4,0], attackType=["magic", "magic"], nodesAttacked=[12,0], move=[0,4], attackRange=[0,1], dodge=1, weakArcs=0)
# Enemy(name="Guardian Dragon - Fire Sweep", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0,1,2], attacks=[4,4,0], attackType=["magic", "magic", "magic"], nodesAttacked=[7,7,0], move=[0,0,1], attackRange=[1,1,1], dodge=2)
# Enemy(name="Guardian Dragon - Charging Flame", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, repeat=1, iconForEffects=[0,1], attacks=[5,0], attackType=["magic", "magic"], nodesAttacked=[4,0], move=[0,1], attackRange=[1,1], dodge=2)
# Enemy(name="Guardian Dragon - Tail Sweep", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackEffect=[{"stagger",}], attackType=["physical"], nodesAttacked=[4], move=[1], attackRange=[2], dodge=2)
# Enemy(name="Guardian Dragon - Bite", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[8], attackEffect=[{"stagger",}], attackType=["physical"], nodeAttack=[True], move=[0], attackRange=[1], dodge=2)
# Enemy(name="Guardian Dragon - Left Stomp", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackEffect=[{"stagger",}], attackType=["magic"], nodesAttacked=[7], move=[0], attackRange=[1], dodge=1)
# Enemy(name="Guardian Dragon - Right Stomp", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackEffect=[{"stagger",}], attackType=["magic"], nodesAttacked=[7], move=[0], attackRange=[1], dodge=1)
# Enemy(name="Guardian Dragon - Cage Grasp Inferno", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[gdAoeAverage[0]], move=[0], attackRange=[0], dodge=1, weakArcs=0, skipDefense=True, aoe=True)
# Enemy(name="Gaping Dragon - Crawling Charge", moveAttack=[True,True,True], expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0,0,0], attacks=[5,5,5], attackType=["physical", "physical", "physical"], nodesAttacked=[0,0,0], nodeAttack=[True,True, True], move=[1,1,1], attackRange=[0,0,0], dodge=2)
# Enemy(name="Gaping Dragon - Stomach Slam", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[4], nodeAttack=[False], move=[0], attackRange=[2], dodge=2)
# Enemy(name="Gaping Dragon - Right Hook", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackEffect=[{"stagger",}], attackType=["physical"], nodesAttacked=[7], move=[1], attackRange=[1], dodge=2)
# Enemy(name="Gaping Dragon - Triple Stomp", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, repeat=2, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[4], move=[0], attackRange=[1], dodge=2)
# Enemy(name="Gaping Dragon - Claw Swipe", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[10], move=[1], attackRange=[1], dodge=1)
# Enemy(name="Gaping Dragon - Tail Whip", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[10], move=[0], attackRange=[1], attackEffect=[{"stagger",}], dodge=2)
# Enemy(name="Gaping Dragon - Flying Smash", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, weakArcs=0, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[12], move=[4], attackRange=[1], dodge=1)
# Enemy(name="Gaping Dragon - Gorge", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, repeat=2, iconForEffects=[0], attacks=[5], attackEffect=[{"stagger",}], attackType=["physical"], move=[0], attackRange=[1], dodge=3)
# Enemy(name="Gaping Dragon - Stomp Slam", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0,1], attacks=[6,6], attackType=["physical", "physical"], nodesAttacked=[7,7], move=[0,0], attackRange=[1,1], dodge=2)
# Enemy(name="Gaping Dragon - Corrosive Ooze (Front Right Left)", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], attackEffect=[{"corrosion",}], nodesAttacked=[10], move=[0], attackRange=[2], dodge=2)
# Enemy(name="Gaping Dragon - Corrosive Ooze (Front Left)", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackType=["magic"], attackEffect=[{"corrosion",}], nodesAttacked=[7], move=[0], attackRange=[2], dodge=2)
# Enemy(name="Gaping Dragon - Corrosive Ooze (Front Right)", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[6], attackType=["magic"], attackEffect=[{"corrosion",}], nodesAttacked=[7], move=[0], attackRange=[2], dodge=2)
# Enemy(name="Gaping Dragon - Corrosive Ooze (Front)", expansion="Gaping Dragon", enemyType="mega boss", numberOfModels=1, health=46, armor=3, resist=2, iconForEffects=[0], attacks=[7], attackType=["magic"], attackEffect=[{"corrosion",}], nodesAttacked=[4], move=[0], attackRange=[2], dodge=2)
# Enemy(name="Vordt of the Boreal Valley - Frostbreath", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackEffect=[{"frostbite",}], attackType=["magic"], nodesAttacked=[20], move=[0], attackRange=[2], dodge=2)
# Enemy(name="Vordt of the Boreal Valley - Tracking Charge", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,1,1,1], attacks=[0,5,5,5], attackType=["physical","physical","physical","physical"], nodeAttack=[False,True,True,True], move=[-1,1,1,1], attackRange=[0,0,0,0], dodge=1, skipDefense=True, moveAttack=[True,True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Shove Right", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,0,1], attacks=[5,5,0], attackType=["physical","physical", "physical"], nodeAttack=[True,True, False], move=[0,1,2], attackRange=[0,0,0], dodge=1, skipDefense=True, moveAttack=[True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Shove Left", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,1,1], attacks=[0,5,5], attackType=["physical","physical","physical"], nodeAttack=[False,True,True], move=[2,1,1], attackRange=[0,0,0], dodge=1, moveIndex=1, skipDefense=True, moveAttack=[True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Crushing Charge", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,0,1], attacks=[5,5,0], attackType=["physical","physical", "physical"], nodeAttack=[True,True, False], move=[0,1,2], attackRange=[0,0,0], dodge=1, skipDefense=True, moveAttack=[True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Jump Rush", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,0,1], attacks=[5,5,0], attackType=["physical","physical", "physical"], nodeAttack=[True,True, False], move=[0,-1,2], attackRange=[0,0,0], dodge=1, skipDefense=True, moveAttack=[True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Trampling Charge", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,0,0,1], attacks=[5,5,5,0], attackType=["physical","physical", "physical", "physical"], nodeAttack=[True,True,True, False], move=[0,1,1,2], attackRange=[0,0,0,0], dodge=1, skipDefense=True, moveAttack=[True,True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Berserk Rush", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, repeat=2, iconForEffects=[0,0,0], attacks=[6,6,6], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], move=[0,1,1], attackRange=[0,0,0], dodge=2, skipDefense=True, moveAttack=[True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Berserk Trample", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, repeat=1, iconForEffects=[0,0,0,0], attacks=[6,6,6,6], attackType=["physical","physical", "physical", "physical"], nodeAttack=[True,True,True,True], move=[0,1,1,1], attackRange=[0,0,0,0], dodge=2, skipDefense=True, moveAttack=[True,True,True,True])
# Enemy(name="Vordt of the Boreal Valley - Double Swipe", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,0], attacks=[5,5], attackType=["magic", "magic"], nodesAttacked=[7,7], move=[0,0], attackRange=[1,1], dodge=1)
# Enemy(name="Vordt of the Boreal Valley - Mace Thrust", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], move=[0], attackRange=[2], dodge=3)
# Enemy(name="Vordt of the Boreal Valley - Backhand Swipe", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[10], move=[0], attackRange=[1], dodge=1)
# Enemy(name="Vordt of the Boreal Valley - Retreating Sweep", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], move=[0,-1], attackRange=[1,1], dodge=2)
# Enemy(name="Vordt of the Boreal Valley - Hammerfist", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], move=[0], attackRange=[1], dodge=2)
# Enemy(name="Vordt of the Boreal Valley - Handle Slam", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], move=[0], attackRange=[1], dodge=2)
# Enemy(name="Vordt of the Boreal Valley - Wild Swings", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, repeat=2, iconForEffects=[0], attacks=[6], attackType=["magic"], move=[0], attackRange=[1], dodge=1)
# Enemy(name="Vordt of the Boreal Valley - Hammerfist Combo", expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, repeat=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], move=[0], attackRange=[1], dodge=1)
# Enemy(name="Black Dragon Kalameet - Mark of Calamity", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[4], attackEffect=[{"calamity",}], attackType=["magic"], nodesAttacked=[4], move=[0], attackRange=[1], dodge=2)
# Enemy(name="Black Dragon Kalameet - Hellfire Blast", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, weakArcs=0, iconForEffects=[0], attacks=[5], attackType=["magic"], attackRange=[0], nodesAttacked=[bdkAoeAverage[0]], move=[0], dodge=2, aoe=True)
# Enemy(name="Black Dragon Kalameet - Sweeping Flame", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[10], move=[0], attackRange=[2], dodge=1)
# Enemy(name="Black Dragon Kalameet - Consuming Blaze", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], nodeAttack=[True, False], move=[0,-1], attackRange=[4,4], dodge=1)
# Enemy(name="Black Dragon Kalameet - Conflagration", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0,1], attacks=[6,0], attackType=["magic", "magic"], nodesAttacked=[10,0], move=[0,-1], attackRange=[1,1], dodge=2)
# Enemy(name="Black Dragon Kalameet - Rising Inferno", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[7], attackType=["magic"], nodesAttacked=[12], move=[0], attackRange=[1], weakArcs=0, dodge=1)
# Enemy(name="Black Dragon Kalameet - Flame Feint", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[7], move=[2], attackRange=[2], dodge=1)
# Enemy(name="Black Dragon Kalameet - Head Strike", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], move=[1], attackEffect=[{"stagger",}], attackRange=[1], dodge=2)
# Enemy(name="Black Dragon Kalameet - Tail Sweep", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[10,0], move=[0,1], attackRange=[1,1], dodge=1)
# Enemy(name="Black Dragon Kalameet - Rush Strike", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[7], move=[2], attackRange=[1], attackEffect=[{"stagger",}], dodge=3)
# Enemy(name="Black Dragon Kalameet - Evasive Tail Whip", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0,1], attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[12, 0], weakArcs=0, move=[0,-1], attackRange=[1,1], dodge=2)
# Enemy(name="Black Dragon Kalameet - Swooping Charge", moveAttack=[True,True,True,True], expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0,0,0,0], attacks=[5,5,5,5], attackType=["physical","physical", "physical", "physical"], nodeAttack=[True,True, True,True], attackEffect=[{"stagger",}, {"stagger",}, {"stagger",}, {"stagger",}], move=[0,1,1,1], attackRange=[0,0,0,0], dodge=2)
# Enemy(name="Black Dragon Kalameet - Hellfire Barrage", expansion="Black Dragon Kalameet", enemyType="mega boss", numberOfModels=1, health=38, armor=4, resist=3, iconForEffects=[0], attacks=[6], attackRange=[0], weakArcs=0, attackType=["magic"], nodesAttacked=[bdkAoeAverage[0]], move=[0], dodge=2, aoe=True)
# Enemy(name="Old Iron King - Fist Pound", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[4], move=[0], attackRange=[1], attackEffect=[{"stagger",}], dodge=2)
# Enemy(name="Old Iron King - Double Fist Pound", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[6], move=[0], attackEffect=[{"stagger",}], attackRange=[1], dodge=2)
# Enemy(name="Old Iron King - Swipe", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[8], move=[0], attackRange=[1], weakArcs=0, dodge=1)
# Enemy(name="Old Iron King - Shockwave", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[16], move=[0], attackRange=[2], dodge=1)
# Enemy(name="Old Iron King - Bash", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], move=[0], attackEffect=[{"stagger",}], attackRange=[2], dodge=3)
# Enemy(name="Old Iron King - Searing Blast", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodeAttack=[True], move=[0], attackRange=[4], dodge=1)
# Enemy(name="Old Iron King - Double Swipe", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0,1], attacks=[6,6], attackType=["physical", "physical"], nodesAttacked=[6,6], move=[0,0], attackRange=[1,1], dodge=2, weakArcs=0)
# Enemy(name="Old Iron King - Firestorm", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[14.33333333333333], move=[0], attackRange=[4], dodge=2)
# Enemy(name="Old Iron King - Magma Blast", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodeAttack=[True], move=[0], attackRange=[4], dodge=3)
# Enemy(name="Old Iron King - Fire Beam (Left)", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[oikAoeAverage[0]], move=[0], attackRange=[1], dodge=1, aoe=True)
# Enemy(name="Old Iron King - Fire Beam (Right)", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[oikAoeAverage[0]], move=[0], attackRange=[1], dodge=1, aoe=True)
# Enemy(name="Old Iron King - Fire Beam (Front)", expansion="Old Iron King", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[oikAoeAverage[0]], move=[0], attackRange=[1], dodge=1, aoe=True)
# Enemy(name="Executioner's Chariot - Death Race 1", expansion="Executioner Chariot", enemyType="mega boss", aoe=True, numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[5], move=[0], attackRange=[1], dodge=1, skipDefense=True)
# Enemy(name="Executioner's Chariot - Death Race 2", expansion="Executioner Chariot", enemyType="mega boss", aoe=True, numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[5], move=[0], attackRange=[1], dodge=1, skipDefense=True)
# Enemy(name="Executioner's Chariot - Death Race 3", expansion="Executioner Chariot", enemyType="mega boss", aoe=True, numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[5], move=[0], attackRange=[1], dodge=1, skipDefense=True)
# Enemy(name="Executioner's Chariot - Death Race 4", expansion="Executioner Chariot", enemyType="mega boss", aoe=True, numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[7], attackType=["physical"], nodesAttacked=[5], move=[0], attackRange=[1], dodge=1, skipDefense=True)
# Enemy(name="Executioner's Chariot - Charging Ram", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[20], move=[2], attackRange=[1], dodge=2)
# Enemy(name="Executioner's Chariot - Roiling Darkness", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[14], move=[0], attackRange=[2], dodge=1)
# Enemy(name="Executioner's Chariot - Stomp Rush", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, repeat=1, iconForEffects=[0,1], attacks=[7,0], weakArcs=2, attackType=["physical", "physical"], nodeAttack=[True, False], move=[0,1], attackRange=[1,1], dodge=2)
# Enemy(name="Executioner's Chariot - Trampling Charge", moveAttack=[True,True,True], expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0,0,0], attacks=[6,6,6], weakArcs=2, attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], move=[0,1,1], attackRange=[0,0,0], dodge=2)
# Enemy(name="Executioner's Chariot - Engulfing Darkness", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[14], move=[0], attackRange=[2], dodge=1)
# Enemy(name="Executioner's Chariot - Advancing Back Kick", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["physical"], nodesAttacked=[4], attackEffect=[{"stagger",}], move=[1], attackRange=[1], dodge=3)
# Enemy(name="Executioner's Chariot - Charging Breath", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[20], move=[2], attackRange=[2], dodge=1)
# Enemy(name="Executioner's Chariot - Headbutt", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["physical"], nodesAttacked=[4], move=[1], attackRange=[1], attackEffect=[{"stagger",}], dodge=3)
# Enemy(name="Executioner's Chariot - Deadly Breath", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0], attacks=[6], attackType=["magic"], nodesAttacked=[14], move=[0], attackRange=[2], dodge=3)
# Enemy(name="Executioner's Chariot - Rearing Charge", moveAttack=[True,True,True,True], expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0,0,1,1], attacks=[4,4,5,5], attackType=["physical","physical","physical","physical"], nodeAttack=[True,True,True,True], move=[0,-1,1,1], attackRange=[0,0,0,0], weakArcs=2, dodge=2)
# Enemy(name="Executioner's Chariot - Back Kick", expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0,1], attacks=[6,0], attackType=["physical", "physical"], nodesAttacked=[4,0], attackEffect=[{"stagger",}, set()], move=[0,1], attackRange=[1,1], dodge=3)
# Enemy(name="Executioner's Chariot - Merciless Charge", moveAttack=[True,True,True,True,True,True], expansion="Executioner Chariot", enemyType="mega boss", numberOfModels=1, health=24, armor=3, resist=3, iconForEffects=[0,0,0,1,1,1], attacks=[6,6,6,6,6,6], attackType=["physical","physical","physical","physical","physical","physical"], nodeAttack=[True,True,True,True,True,True], move=[1,1,1,1,1,1], attackRange=[0,0,0,0,0,0], dodge=1)
