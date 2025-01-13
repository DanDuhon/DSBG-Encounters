from os import path
from itertools import combinations, combinations_with_replacement, filterfalse
from math import ceil
from statistics import mean


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []

newGamePlusMods = [
    # "dodge1", "dodge2",
    # "damage1", "damage2", "damage3", "damage4",
    # "armor resist1",
    # "armor1", "armor2",
    # "resist1", "resist2",
    # "health1", "health2", "health3", "health4",
    # "damage health1", "damage health2",
    # "repeat",
    # "magic", "physical",
    "effect1", "effect2"
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
    4: 9
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
    def __init__(self, name, expansion, enemyType, numberOfModels, health, armor, resist, iconForEffects, attacks, attackType, dodge, move, attackRange, id=None, repeat=0, nodeAttack=[], nodesAttacked=[], attackEffect=[], weakArcs=None, windup=False, moveIndex=None, skipDefense=False, difficultyTiers=0, moveAttack=[], modified=False, comboSet=frozenset(), aoe=False) -> None:
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
        self.iconForEffects = iconForEffects + ([a for i, a in enumerate(attacks) if not moveAttack[i] or move[i]] * repeat)
        self.nodeAttack = nodeAttack + ([a for i, a in enumerate(nodeAttack) if not moveAttack[i] or move[i]] * repeat)
        self.nodesAttacked = nodesAttacked + ([a for i, a in enumerate(nodesAttacked) if not moveAttack[i] or move[i]] * repeat)
        self.attackType = attackType + ([a for i, a in enumerate(attackType) if not moveAttack[i] or move[i]] * repeat)
        self.attackRange = attackRange + ([a for i, a in enumerate(attackRange) if not moveAttack[i] or move[i]] * repeat)
        self.attackEffect = attackEffect + ([a for i, a in enumerate(attackEffect) if not moveAttack[i] or move[i]] * repeat)
        self.move = move + ([a for i, a in enumerate(move) if not moveAttack[i] or move[i]] * repeat)
        moveAttack = moveAttack + ([a for i, a in enumerate(moveAttack) if not moveAttack[i] or move[i]] * repeat)

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
                    or (aoe and "Executioner's Chariot - Death Race" in name and ("nodes5" in comboSet or "nodes6" in comboSet))
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
                    attacksForEffects = len(set(a for i, a in enumerate(iconForEffects) if attacks[i]))

                    for effectCombo in combinations_with_replacement(effectMods if "effect1" in comboSet else effectCombos, attacksForEffects):
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
Enemy(id=1, name="Alonne Bow Knight", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 75.66, 2: 75.66, 3: 75.66, 4: 75.66}}, 2: {"toughness": 42968, "difficulty": {1: 14.04, 2: 14.04, 3: 14.04, 4: 14.04}}, 3: {"toughness": 88396, "difficulty": {1: 40.82, 2: 40.82, 3: 40.82, 4: 40.82}}})
Enemy(id=2, name="Alonne Knight Captain", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=5, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 3975, "difficulty": {1: 669.97, 2: 669.97, 3: 669.97, 4: 669.97}}, 2: {"toughness": 4949, "difficulty": {1: 177.52, 2: 177.52, 3: 177.52, 4: 177.52}}, 3: {"toughness": 17101, "difficulty": {1: 208.48, 2: 208.48, 3: 208.48, 4: 208.48}}})
Enemy(id=3, name="Alonne Sword Knight", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 17854, "difficulty": {1: 146.64, 2: 146.64, 3: 146.64, 4: 146.64}}, 2: {"toughness": 17195, "difficulty": {1: 37.05, 2: 37.05, 3: 37.05, 4: 37.05}}, 3: {"toughness": 57021, "difficulty": {1: 55.69, 2: 55.69, 3: 55.69, 4: 55.69}}})
Enemy(id=4, name="Black Hollow Mage", expansion="Executioner Chariot", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=3, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 2505, "difficulty": {1: 1188.15, 2: 1188.15, 3: 1188.15, 4: 1188.15}}, 2: {"toughness": 4306, "difficulty": {1: 206.95, 2: 206.95, 3: 206.95, 4: 206.95}}, 3: {"toughness": 15121, "difficulty": {1: 260.16, 2: 260.16, 3: 260.16, 4: 260.16}}})
Enemy(id=5, name="Bonewheel Skeleton", moveAttack=[True,True], expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, repeat=1, iconForEffects=[0, 0], attacks=[4,4], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 156.91, 2: 168.98, 3: 181.05, 4: 195.91}}, 2: {"toughness": 42968, "difficulty": {1: 29.12, 2: 31.36, 3: 33.6, 4: 36.36}}, 3: {"toughness": 88396, "difficulty": {1: 84.67, 2: 91.18, 3: 97.69, 4: 105.71}}})
Enemy(id=6, name="Crossbow Hollow", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=0, iconForEffects=[0], attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 40923, "difficulty": {1: 23.51, 2: 23.51, 3: 23.51, 4: 23.51}}, 2: {"toughness": 54957, "difficulty": {1: 5.08, 2: 5.08, 3: 5.08, 4: 5.08}}, 3: {"toughness": 89972, "difficulty": {1: 8.58, 2: 8.58, 3: 8.58, 4: 8.58}}})
Enemy(id=7, name="Crow Demon", moveAttack=[True,True], expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=2, iconForEffects=[0, 0], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0], difficultyTiers={1: {"toughness": 6001, "difficulty": {1: 1579.49, 2: 1700.99, 3: 1822.48, 4: 1972.02}}, 2: {"toughness": 9397, "difficulty": {1: 275.69, 2: 296.89, 3: 318.1, 4: 344.2}}, 3: {"toughness": 30671, "difficulty": {1: 553.28, 2: 595.84, 3: 638.4, 4: 690.78}}})
Enemy(id=8, name="Demonic Foliage", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=1, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 78.59, 2: 78.59, 3: 78.59, 4: 78.59}}, 2: {"toughness": 32175, "difficulty": {1: 19.8, 2: 19.8, 3: 19.8, 4: 19.8}}, 3: {"toughness": 64201, "difficulty": {1: 49.46, 2: 49.46, 3: 49.46, 4: 49.46}}})
Enemy(id=9, name="Engorged Zombie", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=2, resist=2, iconForEffects=[0], attacks=[4], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 17854, "difficulty": {1: 67.06, 2: 67.06, 3: 67.06, 4: 67.06}}, 2: {"toughness": 17195, "difficulty": {1: 21.78, 2: 21.78, 3: 21.78, 4: 21.78}}, 3: {"toughness": 57021, "difficulty": {1: 22.23, 2: 22.23, 3: 22.23, 4: 22.23}}})
Enemy(id=10, name="Falchion Skeleton", expansion="Executioner Chariot", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[3], attackType=["physical"], attackEffect=[{"bleed",}], dodge=1, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 77.56, 2: 77.56, 3: 77.56, 4: 77.56}}, 2: {"toughness": 42968, "difficulty": {1: 19.91, 2: 19.91, 3: 19.91, 4: 19.91}}, 3: {"toughness": 88396, "difficulty": {1: 43.16, 2: 43.16, 3: 43.16, 4: 43.16}}})
Enemy(id=11, name="Firebomb Hollow", expansion="Explorers", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=1, move=[1], attackRange=[2], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 25.24, 2: 27.19, 3: 29.13, 4: 31.52}}, 2: {"toughness": 42968, "difficulty": {1: 6.42, 2: 6.92, 3: 7.41, 4: 8.02}}, 3: {"toughness": 88396, "difficulty": {1: 8.63, 2: 9.29, 3: 9.95, 4: 10.77}}})
Enemy(id=12, name="Giant Skeleton Archer", moveAttack=[True, True, False], expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=1, iconForEffects=[0,0,1], attacks=[2,2,5], attackType=["physical", "physical", "physical"], nodeAttack=[True, True, False], dodge=2, move=[0, 0, 0], attackRange=[0,0, 4], moveIndex=0, difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 475.19, 2: 478.3, 3: 481.41, 4: 485.24}}, 2: {"toughness": 13939, "difficulty": {1: 84.46, 2: 84.91, 3: 85.36, 4: 85.91}}, 3: {"toughness": 33839, "difficulty": {1: 217.19, 2: 218.3, 3: 219.42, 4: 220.79}}})
Enemy(id=13, name="Giant Skeleton Soldier", moveAttack=[True, True, False], expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=1, iconForEffects=[0,0,1], attacks=[2,2,5], attackType=["physical", "physical", "physical"], nodeAttack=[True, True, False], dodge=1, move=[0, 1, 1], attackRange=[0,0, 1], difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 301.88, 2: 303.92, 3: 305.96, 4: 308.47}}, 2: {"toughness": 13939, "difficulty": {1: 52.23, 2: 52.43, 3: 52.64, 4: 52.89}}, 3: {"toughness": 33839, "difficulty": {1: 107.59, 2: 108.04, 3: 108.49, 4: 109.04}}})
Enemy(id=14, name="Hollow Soldier", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 30.58, 2: 30.58, 3: 30.58, 4: 30.58}}, 2: {"toughness": 42968, "difficulty": {1: 5.36, 2: 5.36, 3: 5.36, 4: 5.36}}, 3: {"toughness": 88396, "difficulty": {1: 12.19, 2: 12.19, 3: 12.19, 4: 12.19}}})
Enemy(id=15, name="Ironclad Soldier", moveAttack=[True,True], expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=5, armor=3, resist=2, iconForEffects=[0,1], attacks=[5,5], attackType=["physical", "physical"], nodeAttack=[True, True], attackEffect=[{"stagger",},{"stagger",}], dodge=2, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 945, "difficulty": {1: 4266.44, 2: 4594.63, 3: 4922.82, 4: 5326.74}}, 2: {"toughness": 1614, "difficulty": {1: 610.8, 2: 657.78, 3: 704.77, 4: 762.59}}, 3: {"toughness": 6644, "difficulty": {1: 928.55, 2: 999.98, 3: 1071.4, 4: 1159.31}}})
Enemy(id=16, name="Large Hollow Soldier", moveAttack=[True,True], expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=0, iconForEffects=[0,1], attacks=[5,5], attackType=["physical", "physical"], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 12952, "difficulty": {1: 199.52, 2: 214.87, 3: 230.22, 4: 249.1}}, 2: {"toughness": 18934, "difficulty": {1: 33.21, 2: 35.76, 3: 38.32, 4: 41.46}}, 3: {"toughness": 37265, "difficulty": {1: 84.1, 2: 90.57, 3: 97.04, 4: 105}}})
Enemy(id=34, name="Mimic", expansion="The Sunless City", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 590.45, 2: 590.45, 3: 590.45, 4: 590.45}}, 2: {"toughness": 13939, "difficulty": {1: 119.38, 2: 119.38, 3: 119.38, 4: 119.38}}, 3: {"toughness": 33839, "difficulty": {1: 322.1, 2: 322.1, 3: 322.1, 4: 322.1}}})
Enemy(id=17, name="Mushroom Child", expansion="Darkroot", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 6001, "difficulty": {1: 304.55, 2: 304.55, 3: 304.55, 4: 304.55}}, 2: {"toughness": 9397, "difficulty": {1: 47.32, 2: 47.32, 3: 47.32, 4: 47.32}}, 3: {"toughness": 30671, "difficulty": {1: 72.27, 2: 72.27, 3: 72.27, 4: 72.27}}})
Enemy(id=18, name="Mushroom Parent", moveAttack=[True,True], expansion="Darkroot", enemyType="regular", numberOfModels=1, health=10, armor=1, resist=2, iconForEffects=[0,1], attacks=[6,6], attackType=["physical", "physical"], nodeAttack=[True,True], attackEffect=[{"stagger",}, {"stagger",}], dodge=1, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 1756, "difficulty": {1: 2030.85, 2: 2187.07, 3: 2343.29, 4: 2535.56}}, 2: {"toughness": 3363, "difficulty": {1: 296.95, 2: 319.79, 3: 342.64, 4: 370.75}}, 3: {"toughness": 10340, "difficulty": {1: 512.43, 2: 551.84, 3: 591.26, 4: 639.78}}})
Enemy(id=19, name="Necromancer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=2, iconForEffects=[0], attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 6001, "difficulty": {1: 368.21, 2: 396.54, 3: 424.86, 4: 459.72}}, 2: {"toughness": 9397, "difficulty": {1: 99.48, 2: 107.13, 3: 114.79, 4: 124.2}}, 3: {"toughness": 30671, "difficulty": {1: 137.66, 2: 148.27, 3: 158.84, 4: 171.87}}})
Enemy(id=20, name="Phalanx", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=1, iconForEffects=[0,0], attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=1, move=[0,1], attackRange=[1,0], difficultyTiers={1: {"toughness": 10311, "difficulty": {1: 301.53, 2: 316.81, 3: 332.09, 4: 350.9}}, 2: {"toughness": 13939, "difficulty": {1: 53.79, 2: 56.54, 3: 59.29, 4: 62.68}}, 3: {"toughness": 33839, "difficulty": {1: 114.4, 2: 120.05, 3: 125.7, 4: 132.65}}})
Enemy(id=21, name="Phalanx Hollow", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=5, health=1, armor=1, resist=1, iconForEffects=[0,0], attacks=[4,0], attackType=["physical", "physical"], dodge=1, move=[0,1], attackRange=[1,0], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 34.28, 2: 34.28, 3: 34.28, 4: 34.28}}, 2: {"toughness": 42968, "difficulty": {1: 6.01, 2: 6.01, 3: 6.01, 4: 6.01}}, 3: {"toughness": 88396, "difficulty": {1: 13.66, 2: 13.66, 3: 13.66, 4: 13.66}}})
Enemy(id=22, name="Plow Scarecrow", expansion="Darkroot", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 74.76, 2: 74.76, 3: 74.76, 4: 74.76}}, 2: {"toughness": 42968, "difficulty": {1: 13.87, 2: 13.87, 3: 13.87, 4: 13.87}}, 3: {"toughness": 88396, "difficulty": {1: 40.34, 2: 40.34, 3: 40.34, 4: 40.34}}})
Enemy(id=23, name="Sentinel", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=2, health=10, armor=2, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1], difficultyTiers={1: {"toughness": 4192, "difficulty": {1: 861.9, 2: 928.2, 3: 994.5, 4: 1076.1}}, 2: {"toughness": 5068, "difficulty": {1: 199.64, 2: 215, 3: 230.36, 4: 249.26}}, 3: {"toughness": 11264, "difficulty": {1: 476.58, 2: 513.24, 3: 549.9, 4: 595.02}}})
Enemy(id=24, name="Shears Scarecrow", expansion="Darkroot", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0,1], attacks=[3,3], attackType=["physical", "physical"], nodeAttack=[True,True], dodge=2, move=[1, 1], attackRange=[0, 0], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 59.36, 2: 63.92, 3: 68.49, 4: 74.11}}, 2: {"toughness": 42968, "difficulty": {1: 9.73, 2: 10.48, 3: 11.23, 4: 12.15}}, 3: {"toughness": 88396, "difficulty": {1: 26.61, 2: 28.66, 3: 30.7, 4: 33.22}}})
Enemy(id=25, name="Silver Knight Greatbowman", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=0, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 36573, "difficulty": {1: 49.51, 2: 53.32, 3: 57.13, 4: 61.82}}, 2: {"toughness": 44164, "difficulty": {1: 8.2, 2: 8.83, 3: 9.46, 4: 10.24}}, 3: {"toughness": 65777, "difficulty": {1: 25.75, 2: 27.73, 3: 29.71, 4: 32.15}}})
Enemy(id=26, name="Silver Knight Spearman", expansion="Explorers", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, iconForEffects=[0,0], attacks=[6,0], attackType=["physical", "physical"], dodge=2, move=[0,1], attackRange=[1,0], difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 131.86, 2: 131.86, 3: 131.86, 4: 131.86}}, 2: {"toughness": 32175, "difficulty": {1: 37.32, 2: 37.32, 3: 37.32, 4: 37.32}}, 3: {"toughness": 64201, "difficulty": {1: 122.5, 2: 122.5, 3: 122.5, 4: 122.5}}})
Enemy(id=27, name="Silver Knight Swordsman", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[0], difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 122.62, 2: 132.05, 3: 141.48, 4: 153.09}}, 2: {"toughness": 32175, "difficulty": {1: 31.04, 2: 33.43, 3: 35.82, 4: 38.76}}, 3: {"toughness": 64201, "difficulty": {1: 97.36, 2: 104.85, 3: 112.34, 4: 121.55}}})
Enemy(id=28, name="Skeleton Archer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficultyTiers={1: {"toughness": 37664, "difficulty": {1: 48.08, 2: 48.08, 3: 48.08, 4: 48.08}}, 2: {"toughness": 42968, "difficulty": {1: 8.43, 2: 8.43, 3: 8.43, 4: 8.43}}, 3: {"toughness": 88396, "difficulty": {1: 19.16, 2: 19.16, 3: 19.16, 4: 19.16}}})
Enemy(id=29, name="Skeleton Beast", moveAttack=[True,True], expansion="Tomb of Giants", enemyType="regular", numberOfModels=1, health=5, armor=2, resist=2, repeat=1, iconForEffects=[0,1], attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True,True], dodge=2, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 3975, "difficulty": {1: 1486.79, 2: 1601.16, 3: 1715.53, 4: 1856.29}}, 2: {"toughness": 4949, "difficulty": {1: 252.83, 2: 272.28, 3: 291.73, 4: 315.66}}, 3: {"toughness": 17101, "difficulty": {1: 437.64, 2: 471.31, 3: 504.97, 4: 546.41}}})
Enemy(id=30, name="Skeleton Soldier", moveAttack=[True,True], expansion="Tomb of Giants", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, iconForEffects=[0,1], attacks=[2,2], attackType=["physical", "physical"], nodeAttack=[True,True], attackEffect=[{"bleed",},{"bleed",}], dodge=1, move=[0,1], attackRange=[0,0], difficultyTiers={1: {"toughness": 33314, "difficulty": {1: 69.29, 2: 74.62, 3: 79.95, 4: 86.51}}, 2: {"toughness": 32175, "difficulty": {1: 23.25, 2: 25.04, 3: 26.83, 4: 29.03}}, 3: {"toughness": 64201, "difficulty": {1: 37.5, 2: 40.39, 3: 43.27, 4: 46.82}}})
Enemy(id=31, name="Snow Rat", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=0, resist=1, iconForEffects=[0], attacks=[3], attackType=["physical"], attackEffect=[{"poison",}], dodge=1, move=[4], attackRange=[0], difficultyTiers={1: {"toughness": 38873, "difficulty": {1: 78.39, 2: 78.39, 3: 78.39, 4: 78.39}}, 2: {"toughness": 46157, "difficulty": {1: 22.85, 2: 22.85, 3: 22.85, 4: 22.85}}, 3: {"toughness": 91859, "difficulty": {1: 73.77, 2: 73.77, 3: 73.77, 4: 73.77}}})
Enemy(id=32, name="Stone Guardian", moveAttack=[True, True, False], expansion="Darkroot", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=3, iconForEffects=[0,0,1], attacks=[4,4,5], attackType=["physical", "physical", "physical"], nodeAttack=[True,True,True], dodge=1, move=[0,1, 0], attackRange=[0,0, 1], difficultyTiers={1: {"toughness": 2472, "difficulty": {1: 1910.86, 2: 2057.85, 3: 2204.84, 4: 2385.75}}, 2: {"toughness": 4306, "difficulty": {1: 245.77, 2: 264.67, 3: 283.58, 4: 306.84}}, 3: {"toughness": 15121, "difficulty": {1: 340.23, 2: 366.41, 3: 392.58, 4: 424.79}}})
Enemy(id=33, name="Stone Knight", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=5, armor=3, resist=2, iconForEffects=[0], attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficultyTiers={1: {"toughness": 3123, "difficulty": {1: 595.26, 2: 595.26, 3: 595.26, 4: 595.26}}, 2: {"toughness": 2471, "difficulty": {1: 248.18, 2: 248.18, 3: 248.18, 4: 248.18}}, 3: {"toughness": 9691, "difficulty": {1: 256.81, 2: 256.81, 3: 256.81, 4: 256.81}}})

# Invaders
# Enemy(id=35, name="Armorer Dennis", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 1677, "difficulty": {1: 572.22, 2: 592, 3: 611.78, 4: 636.12}}, 2: {"toughness": 2987.6, "difficulty": {1: 99.41, 2: 102.96, 3: 106.51, 4: 110.88}}, 3: {"toughness": 8811.4, "difficulty": {1: 143.95, 2: 148.69, 3: 153.44, 4: 159.29}}})
# Enemy(id=36, name="Fencer Sharron", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 2534, "difficulty": {1: 1475.48, 2: 1513.74, 3: 1552, 4: 1599.08}}, 2: {"toughness": 3749.14, "difficulty": {1: 248.86, 2: 254.15, 3: 259.44, 4: 265.95}}, 3: {"toughness": 8927.57, "difficulty": {1: 580.44, 2: 592.43, 3: 604.42, 4: 619.17}}})
# Enemy(id=37, name="Invader Brylex", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 1360, "difficulty": {1: 3419.26, 2: 3565.43, 3: 3711.59, 4: 3891.49}}, 2: {"toughness": 1839, "difficulty": {1: 681.69, 2: 710.42, 3: 739.15, 4: 774.51}}, 3: {"toughness": 6374, "difficulty": {1: 1016.7, 2: 1060.45, 3: 1104.21, 4: 1158.06}}})
# Enemy(id=38, name="Kirk, Knight of Thorns", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 4599, "difficulty": {1: 410.45, 2: 424.28, 3: 438.12, 4: 455.15}}, 2: {"toughness": 6715, "difficulty": {1: 73.92, 2: 76.44, 3: 78.95, 4: 82.04}}, 3: {"toughness": 15341, "difficulty": {1: 128.24, 2: 132.07, 3: 135.9, 4: 140.61}}})
# Enemy(id=39, name="Longfinger Kirk", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 1455, "difficulty": {1: 3466.83, 2: 3547.92, 3: 3629.01, 4: 3728.81}}, 2: {"toughness": 1919, "difficulty": {1: 716.29, 2: 732.89, 3: 749.48, 4: 769.91}}, 3: {"toughness": 6851, "difficulty": {1: 1358.46, 2: 1387.29, 3: 1416.11, 4: 1451.59}}})
# Enemy(id=40, name="Maldron the Assassin", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 3032, "difficulty": {1: 1274.67, 2: 1307.03, 3: 1339.38, 4: 1379.2}}, 2: {"toughness": 3551, "difficulty": {1: 276.66, 2: 283.34, 3: 290.01, 4: 298.23}}, 3: {"toughness": 6733, "difficulty": {1: 927.83, 2: 950.11, 3: 972.38, 4: 999.81}}})
# Enemy(id=41, name="Maneater Mildred", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 2315.6, "difficulty": {1: 1352.88, 2: 1456.94, 3: 1561.01, 4: 1689.09}}, 2: {"toughness": 3787, "difficulty": {1: 158.18, 2: 170.35, 3: 182.52, 4: 197.49}}, 3: {"toughness": 9182, "difficulty": {1: 339.16, 2: 365.25, 3: 391.34, 4: 423.45}}})
# Enemy(id=42, name="Marvelous Chester", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 1874, "difficulty": {1: 2865.34, 2: 2882.45, 3: 2899.55, 4: 2920.6}}, 2: {"toughness": 3216, "difficulty": {1: 429.31, 2: 431.93, 3: 434.54, 4: 437.76}}, 3: {"toughness": 9666, "difficulty": {1: 804.78, 2: 810.73, 3: 816.67, 4: 823.99}}})
# Enemy(id=43, name="Melinda the Butcher", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 4139.6, "difficulty": {1: 535.55, 2: 562.29, 3: 589.02, 4: 621.93}}, 2: {"toughness": 6151, "difficulty": {1: 70.07, 2: 73.69, 3: 77.31, 4: 81.76}}, 3: {"toughness": 12534.8, "difficulty": {1: 169.97, 2: 178.61, 3: 187.25, 4: 197.89}}})
# Enemy(id=44, name="Oliver the Collector", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 4095.71, "difficulty": {1: 947.49, 2: 985.25, 3: 1023.01, 4: 1069.49}}, 2: {"toughness": 5825.71, "difficulty": {1: 131.73, 2: 136.83, 3: 141.93, 4: 148.21}}, 3: {"toughness": 12000, "difficulty": {1: 283.54, 2: 293.1, 3: 302.66, 4: 314.42}}})
# Enemy(id=45, name="Paladin Leeroy", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 1686, "difficulty": {1: 2308.82, 2: 2472.96, 3: 2637.1, 4: 2839.11}}, 2: {"toughness": 2047.4, "difficulty": {1: 404.6, 2: 432.54, 3: 460.48, 4: 494.86}}, 3: {"toughness": 4575.8, "difficulty": {1: 888.4, 2: 945.88, 3: 1003.36, 4: 1074.1}}})
# Enemy(id=46, name="Xanthous King Jeremiah", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 6038.5, "difficulty": {1: 510.81, 2: 543.2, 3: 575.59, 4: 615.46}}, 2: {"toughness": 11494.5, "difficulty": {1: 82.37, 2: 87.57, 3: 92.76, 4: 99.16}}, 3: {"toughness": 19651, "difficulty": {1: 108.53, 2: 115.31, 3: 122.09, 4: 130.44}}})
# Enemy(id=47, name="Hungry Mimic", expansion="Explorers", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 3032, "difficulty": {1: 838.69, 2: 869.16, 3: 899.62, 4: 937.11}}, 2: {"toughness": 4505, "difficulty": {1: 137.56, 2: 142.59, 3: 147.62, 4: 153.81}}, 3: {"toughness": 10513, "difficulty": {1: 348.15, 2: 360.57, 3: 372.99, 4: 388.28}}})
# Enemy(id=48, name="Voracious Mimic", expansion="Explorers", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[0], attackType=["magic"], iconForEffects=[0], dodge=0, move=[0], attackRange=[0], difficultyTiers={1: {"toughness": 1139, "difficulty": {1: 3150.4, 2: 3262.92, 3: 3375.44, 4: 3513.93}}, 2: {"toughness": 1569, "difficulty": {1: 625.8, 2: 648.28, 3: 670.76, 4: 698.42}}, 3: {"toughness": 5421, "difficulty": {1: 1121.31, 2: 1160.46, 3: 1199.62, 4: 1247.8}}})

# Enemy(name="Hungry Mimic - Raking Slash", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Hungry Mimic - Heavy Punch", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Hungry Mimic - Leaping Spin Kick", moveAttack=[True,True], expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0,1], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Hungry Mimic - Stomping Kick", expansion="Explorers", moveAttack=[True,True], enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0,1], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0])
# Enemy(name="Hungry Mimic - Charging Chomp", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[4], attackType=["physical"], dodge=3, move=[3], attackRange=[0])
# Enemy(name="Hungry Mimic - Vicious Chomp", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[0])
# Enemy(name="Hungry Mimic - Aggressive Grab", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=1, resist=1, iconForEffects=[0], attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0])
# Enemy(name="Voracious Mimic - Raking Slash", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
# Enemy(name="Voracious Mimic - Heavy Punch", expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0], attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[1])
# Enemy(name="Voracious Mimic - Leaping Spin Kick", moveAttack=[True,True], expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0,1], attacks=[6,6], attackType=["physical","physical"], nodeAttack=[True,True], dodge=2, move=[0,4], attackRange=[0,0])
# Enemy(name="Voracious Mimic - Stomping Kick", moveAttack=[True,True], expansion="Explorers", enemyType="invader", numberOfModels=1, health=18, armor=2, resist=2, iconForEffects=[0,1], attacks=[7,7], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0])
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
# Enemy(name="Fencer Sharron - Dual Sword Slash", moveAttack=[True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, iconForEffects=[0,1], attacks=[6,6], attackType=["physical","physical"], attackEffect=[{"stagger",},{"stagger",}], nodeAttack=[True,True], dodge=2, move=[0,1], attackRange=[0,0])
# Enemy(name="Invader Brylex - Leaping Strike", moveAttack=[True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, iconForEffects=[0,1], attacks=[7,7], attackType=["physical","physical"], nodeAttack=[True,True], dodge=1, move=[0,4], attackRange=[0,0])
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
# Enemy(name="Maneater Mildred - Guillotine", moveAttack=[True,True], expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, iconForEffects=[0,1], attacks=[5,5], attackType=["physical","physical"], attackEffect=[{"stagger",},{"stagger",}], nodeAttack=[True,True], dodge=1, move=[0,1], attackRange=[0,0])
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

# Mini Bosses
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
# Enemy(name="Black Knight - Hacking Slash", moveAttack=[False,True,True], weakArcs=0, expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, iconForEffects=[0,1,1], attacks=[5,4,4], attackType=["physical", "physical", "physical"], nodesAttacked=[4,0,0], attackEffect=[{"stagger",}, set(), set()], nodeAttack=[False, True,True], dodge=2, move=[0,1,1], attackRange=[2,0,0])
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

# Main bosses
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
# Enemy(name="Gravelord Nito - Creeping Death", moveAttack=[True,True], expansion="Tomb of Giants", enemyType="main boss", numberOfModels=1, health=30, armor=2, resist=2, repeat=2, iconForEffects=[0,1], attacks=[5,5], attackType=["physical","physical"], nodeAttack=[True,True], attackEffect=[{"poison",},{"poison",}], dodge=1, move=[0,1], attackRange=[0,0])
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

# Mega bosses
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
# Enemy(name="Guardian Dragon - Fiery Breath 1", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[gdAoeAverage[0]], move=[0], attackRange=[0], dodge=1, weakArcs=0, skipDefense=True, aoe=True)
# Enemy(name="Guardian Dragon - Fiery Breath 2", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[gdAoeAverage[0]], move=[0], attackRange=[0], dodge=1, weakArcs=0, skipDefense=True, aoe=True)
# Enemy(name="Guardian Dragon - Fiery Breath 3", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[gdAoeAverage[0]], move=[0], attackRange=[0], dodge=1, weakArcs=0, skipDefense=True, aoe=True)
# Enemy(name="Guardian Dragon - Fiery Breath 4", expansion="Guardian Dragon", enemyType="mega boss", numberOfModels=1, health=44, armor=3, resist=3, iconForEffects=[0], attacks=[5], attackType=["magic"], nodesAttacked=[gdAoeAverage[0]], move=[0], attackRange=[0], dodge=1, weakArcs=0, skipDefense=True, aoe=True)
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
# Enemy(name="Vordt of the Boreal Valley - Berserk Rush", weakArcs=0, expansion="Vordt of the Boreal Valley", enemyType="mega boss", numberOfModels=1, health=42, armor=3, resist=3, repeat=2, iconForEffects=[0,0,], attacks=[6,6,6], attackType=["physical","physical", "physical"], nodeAttack=[True,True,True], move=[0,1,1], attackRange=[0,0,0], dodge=2, skipDefense=True, moveAttack=[True,True,True])
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
