import numpy as np
import math
import json
import itertools

from enemies import enemies
from attacks import attacks as all_attacks
from armor import armorByName
from hand_items import handItemsByName
from builds import builds as classBuilds

b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)

BLACK_PMF = np.array([1/6, 3/6, 2/6])
BLUE_PMF = np.array([0, 2/6, 3/6, 1/6])
ORANGE_PMF = np.array([0, 1/6, 2/6, 2/6, 1/6])

REACH_MOD = {
    0: 0.0769,
    1: 0.4497,
    2: 0.8224,
    3: 0.9763,
    4: 1.0
}

STAM_COST = 0.33  # Stamina cost of Stagger/Frostbite/Push

ENEMY_FREQUENCY = {
    1: { # Level 1 Encounters
        "Alonne Bow Knight": 0.09,
        "Alonne Sword Knight": 0.05,
        "Bonewheel Skeleton": 0.03,
        "Crossbow Hollow": 0.55,
        "Crow Demon": 0.02,
        "Demonic Foliage": 0.05,
        "Engorged Zombie": 0.05,
        "Falchion Skeleton": 0.03,
        "Firebomb Hollow": 0.1,
        "Giant Skeleton Soldier": 0.03,
        "Hollow Soldier": 0.66,
        "Large Hollow Soldier": 0.03,
        "Mimic": 0.02,
        "Mushroom Child": 0.03,
        "Necromancer": 0.07,
        "Phalanx Hollow": 0.09,
        "Plow Scarecrow": 0.12,
        "Sentinel": 0.02,
        "Shears Scarecrow": 0.09,
        "Silver Knight Greatbowman": 0.12,
        "Silver Knight Spearman": 0.03,
        "Silver Knight Swordsman": 0.14,
        "Skeleton Archer": 0.09,
        "Skeleton Beast": 0.02,
        "Skeleton Soldier": 0.19,
        "Snow Rat": 0.21
    },
    2: {
        "Alonne Bow Knight": 0.1,
        "Alonne Knight Captain": 0.05,
        "Alonne Sword Knight": 0.03,
        "Bonewheel Skeleton": 0.09,
        "Crossbow Hollow": 0.38,
        "Crow Demon": 0.09,
        "Demonic Foliage": 0.05,
        "Engorged Zombie": 0.12,
        "Falchion Skeleton": 0.03,
        "Firebomb Hollow": 0.07,
        "Giant Skeleton Archer": 0.05,
        "Giant Skeleton Soldier": 0.09,
        "Hollow Soldier": 0.5,
        "Ironclad Soldier": 0.05,
        "Large Hollow Soldier": 0.16,
        "Mimic": 0.09,
        "Mushroom Child": 0.05,
        "Mushroom Parent": 0.03,
        "Necromancer": 0.12,
        "Phalanx": 0.02,
        "Phalanx Hollow": 0.17,
        "Plow Scarecrow": 0.05,
        "Sentinel": 0.03,
        "Shears Scarecrow": 0.03,
        "Silver Knight Greatbowman": 0.29,
        "Silver Knight Spearman": 0.1,
        "Silver Knight Swordsman": 0.36,
        "Skeleton Archer": 0.17,
        "Skeleton Beast": 0.03,
        "Skeleton Soldier": 0.41,
        "Snow Rat": 0.14,
        "Stone Guardian": 0.03,
        "Stone Knight": 0.02
    },
    3: {
        "Alonne Bow Knight": 0.14,
        "Alonne Knight Captain": 0.14,
        "Alonne Sword Knight": 0.1,
        "Black Hollow Mage": 0.03,
        "Bonewheel Skeleton": 0.1,
        "Crossbow Hollow": 0.41,
        "Crow Demon": 0.16,
        "Demonic Foliage": 0.1,
        "Engorged Zombie": 0.16,
        "Falchion Skeleton": 0.05,
        "Firebomb Hollow": 0.1,
        "Giant Skeleton Archer": 0.19,
        "Giant Skeleton Soldier": 0.17,
        "Hollow Soldier": 0.43,
        "Ironclad Soldier": 0.05,
        "Large Hollow Soldier": 0.29,
        "Mimic": 0.1,
        "Mushroom Child": 0.03,
        "Mushroom Parent": 0.03,
        "Necromancer": 0.09,
        "Phalanx": 0.03,
        "Phalanx Hollow": 0.36,
        "Plow Scarecrow": 0.09,
        "Sentinel": 0.29,
        "Silver Knight Greatbowman": 0.53,
        "Silver Knight Spearman": 0.14,
        "Silver Knight Swordsman": 0.57,
        "Skeleton Archer": 0.19,
        "Skeleton Beast": 0.09,
        "Skeleton Soldier": 0.28,
        "Snow Rat": 0.14,
        "Stone Guardian": 0.05,
        "Stone Knight": 0.1
    }
}


def convert_to_pmf(diceList):
    """Converts a list of tuples like [(0,1,1,1,2,2), (1,1,2,2,2,3)] into a NumPy PMF."""
    flatList = [item for sublist in diceList for item in (sublist if isinstance(sublist, list) else [sublist])]
    
    blackCount = flatList.count(b)
    blueCount = flatList.count(u)
    orangeCount = flatList.count(o)
    
    pool = np.array([1.0])
    for _ in range(blackCount): pool = np.convolve(pool, BLACK_PMF)
    for _ in range(blueCount):  pool = np.convolve(pool, BLUE_PMF)
    for _ in range(orangeCount): pool = np.convolve(pool, ORANGE_PMF)
    
    return pool


def count_dodge_dice(dodgeList):
    return dodgeList.count(d)


def calculate_ev_against_defense(pmf, defenseVal):
    """EV of an attack against block/resist."""
    ev = 0.0
    for roll, prob in enumerate(pmf):
        ev += max(0, roll - defenseVal) * prob
    return ev


def calculate_expected_damage_taken(enemyDamage, defensePmf):
    """EV of damage that gets past defense."""
    evTaken = 0.0
    for blockVal, prob in enumerate(defensePmf):
        evTaken += max(0, enemyDamage - blockVal) * prob
    return evTaken


def calculate_dodge_chance(dodgeTarget, dodgeDice):
    if dodgeTarget == 0: return 1.0
    if dodgeDice == 0: return 0.0
    
    success = 0.5
    chance = sum(
        math.comb(dodgeDice, k) * (success**k) * ((1-success)**(dodgeDice-k))
        for k in range(dodgeTarget, dodgeDice + 1)
    )
    return chance


def get_weapon_attacks(name):
    return [a for a in all_attacks if a.name == name]


def enemy_strength(enemy, charDefense, charKiteRange, sharron3Plus=0.0, bleedSynergy=1.75):
    totalStrength = 0.0
    
    if "Melinda" in enemy.name and charDefense["dodgeDice"] > 0:
        charKiteRange = max(0, charKiteRange - 1)
        
    # Leap Overrides Kiting Completely
    if hasattr(enemy, "frostbiteLeap") and enemy.frostbiteLeap:
        charKiteRange = 0
    elif hasattr(enemy, "leap") and enemy.leap:
        charKiteRange = 0
        
    # Invisibility Caps Kiting at Range 1
    if hasattr(enemy, "invisibility") and enemy.invisibility:
        charKiteRange = min(charKiteRange, 1)

    cumulativeMove = 0
    
    for i in range(len(enemy.attacks)):
        cumulativeMove += enemy.move[i]
        
        # Shaft
        stopDistance = max(0, charKiteRange - cumulativeMove)
        if hasattr(enemy, "shaft") and enemy.shaft[i] is not None:
            if stopDistance <= enemy.shaft[i]:
                continue
        
        damage = enemy.attacks[i]
        if damage == 0:
            continue
            
        reach = min(4, max(0, cumulativeMove + enemy.attackRange[i]))
        reachMod = 1.0
        if charKiteRange > reach:
            reachMod = REACH_MOD.get(reach, 1.0)
            
        poison = 1.0 if any(e == "poison" for e in enemy.attackEffect[i]) else 0.0
        bleedDamage = bleedSynergy if any(e == "bleed" for e in enemy.attackEffect[i]) else 0.0 
        
        defensePmf = charDefense["resistPmf"] if enemy.attackType[i] == "magic" else charDefense["blockPmf"]
        expectedDamageTaken = calculate_expected_damage_taken(damage, defensePmf)
        
        if "Armorer Dennis" in enemy.name:
            dodgeNormalPhase = calculate_dodge_chance(enemy.dodge, charDefense["dodgeDice"])
            dodgeHeatupPhase = calculate_dodge_chance(enemy.dodge + 1, charDefense["dodgeDice"])
            avgDodgeFail = 1.0 - ((dodgeNormalPhase * 0.375) + (dodgeHeatupPhase * 0.625))
            dodgeFailRate = avgDodgeFail
        else:
            dodgeFailRate = 1.0 - calculate_dodge_chance(enemy.dodge, charDefense["dodgeDice"])
        
        stepStrength = (expectedDamageTaken + poison + bleedDamage) * dodgeFailRate * reachMod
        
        if hasattr(enemy, "nodesAttacked") and enemy.nodesAttacked[i] > 1.0:
            stepStrength *= 1.2
        elif enemy.nodeAttack[i]:
            stepStrength *= 1.1
            
        totalStrength += stepStrength
        
    if "Fencer Sharron" in enemy.name:
        totalStrength *= (1.0 + sharron3Plus)
        
    return totalStrength

def enemy_toughness(enemy, playerDefense, attacks, tierBleedSynergy):
    bestStam = float("inf")
    bestProb3Plus = 0.0
    
    enemyHitChance = 1.0 - calculate_dodge_chance(enemy.dodge, playerDefense["dodgeDice"])
    
    # Pre-calculate Mildred's expected healing per activation sequence
    expectedHealingPerTurn = 0.0
    if "Maneater Mildred" in enemy.name:
        for i in range(len(enemy.attacks)):
            damage = enemy.attacks[i]
            if damage == 0:
                continue
            defensePmf = playerDefense["resistPmf"] if enemy.attackType[i] == "magic" else playerDefense["blockPmf"]
            # Probability that the damage exceeds defense
            pierceProb = sum(prob for val, prob in enumerate(defensePmf) if damage - val > 0)
            expectedHealingPerTurn += enemyHitChance * pierceProb

    for attack in attacks:
        targetDefense = enemy.resist if attack.magic else enemy.armor
        attackPmf = convert_to_pmf(attack.damage[0] if attack.damage else [])
        
        evDamage = calculate_ev_against_defense(attackPmf, targetDefense)
        
        if "Maneater Mildred" in enemy.name:
            netEv = evDamage - expectedHealingPerTurn
        else:
            netEv = evDamage
            
        if netEv <= 0:
            continue
            
        if "Paladin Leeroy" in enemy.name:
            expectedAttacks = math.ceil(14 / netEv) + math.ceil(2 / netEv)
        elif "Maldron" in enemy.name:
            expectedAttacks = math.ceil(3 / netEv) + math.ceil(8 / netEv)
        elif "Armorer Dennis" in enemy.name:
            expectedAttacks = math.ceil(6 / netEv) + math.ceil(10 / netEv)
        else:
            expectedAttacks = enemy.health / netEv 
        
        staminaCost = expectedAttacks * attack.staminaCost
        
        dodgableStam = 0.0
        undodgableStam = 0.0
        
        cumulativeMove = 0
        
        kitingRange = attack.attackRange
        if hasattr(enemy, "invisibility") and enemy.invisibility:
            kitingRange = min(kitingRange, 1)
        
        for i in range(len(enemy.attacks)):
            cumulativeMove += enemy.move[i]
            
            # Shaft
            stopDistance = max(0, kitingRange - cumulativeMove)
            shaftMiss = False
            if hasattr(enemy, "shaft") and enemy.shaft[i] is not None:
                if stopDistance <= enemy.shaft[i]:
                    shaftMiss = True
            
            # Dodgable
            reach = min(4, max(0, cumulativeMove + enemy.attackRange[i]))
            reachMod = 1.0
            
            if kitingRange > reach:
                reachMod = REACH_MOD.get(reach, 1.0)
                
            stepDodgable = 0.0
            
            if not shaftMiss:
                if any(e == "push" for e in enemy.attackEffect[i]) and attack.attackRange == 0: stepDodgable += 1
                if any(e == "stagger" for e in enemy.attackEffect[i]): stepDodgable += 1
                if any(e == "frostbite" for e in enemy.attackEffect[i]): stepDodgable += 1
            
            multiTargetMod = 1.0
            if hasattr(enemy, "nodesAttacked") and enemy.nodesAttacked[i] > 1.0:
                multiTargetMod = enemy.nodesAttacked[i]
                
            dodgableStam += (stepDodgable * reachMod * multiTargetMod)

            # Undodgable FSA
            if hasattr(enemy, "movePush") and enemy.movePush[i] and attack.attackRange == 0:
                moveReach = cumulativeMove
                moveReachMod = 1.0
                
                if kitingRange > moveReach:
                    moveReachMod = REACH_MOD.get(moveReach, 1.0)
                    
                undodgableStam += (1.0 * moveReachMod * multiTargetMod)

        # Frostbite Leap
        if hasattr(enemy, "frostbiteLeap") and enemy.frostbiteLeap:
            undodgableStam += 1.0

        stamPenalty = expectedAttacks * STAM_COST * ((dodgableStam * enemyHitChance) + undodgableStam)
        # STK = stamina to kill
        totalStk = staminaCost + stamPenalty
        
        # Chester retreats when hit
        if "Marvelous Chester" in enemy.name and attack.attackRange <= 2:
            totalStk += expectedAttacks * 1.0
        # Attacks at 0 range against Kirk cause bleed
        elif "Longfinger Kirk" in enemy.name and attack.attackRange == 0:
            totalStk += expectedAttacks * tierBleedSynergy
            
        if totalStk < bestStam:
            bestStam = totalStk
            # Sharron's double attack trigger probability
            bestProb3Plus = sum(prob for val, prob in enumerate(attackPmf) if max(0, val - targetDefense) >= 3)
            
    return bestStam, bestProb3Plus


def get_item_obj(name):
    if name in armorByName: return armorByName[name]
    if name in handItemsByName: return handItemsByName[name]
    return None

def generate_loadouts(names):
    """Generates all valid combinations of gear from a tier's item pool."""
    armors = []
    hand_items = []
    
    for name in names:
        item = get_item_obj(name)
        if not item: continue
        
        if name in armorByName:
            armors.append(item)
        else:
            hand_items.append(item)
            
    twoHanders = [h for h in hand_items if h.twoHanded]
    oneHanders = [h for h in hand_items if not h.twoHanded]
    
    loadouts = []
    
    for a in armors:
        for h in twoHanders:
            loadouts.append([a, h])
            
        for h1, h2 in itertools.combinations(oneHanders, 2):
            loadouts.append([a, h1, h2])
            
        for h in oneHanders:
            loadouts.append([a, h])
            
    return loadouts

def main():
    print("Loadouts")
    
    tierProfiles = {1: [], 2: [], 3: []}
    
    for _, partyDict in classBuilds.items():
        for _, tierDict in partyDict.items():
            for tier, item_names in tierDict.items():
                
                loadouts = generate_loadouts(item_names)
                
                for loadout in loadouts:
                    totalBlock = []
                    totalResist = []
                    totalDodge = []
                    totalBlockArmor = []
                    totalResistArmor = []
                    totalDodgeArmor = []
                    weapons = []
                    for item in loadout:
                        totalBlock.extend(item.block)
                        totalResist.extend(item.resist)
                        totalDodge.extend(item.dodge)
                        if item.name in armorByName:
                            totalBlockArmor.extend(item.block)
                            totalResistArmor.extend(item.resist)
                            totalDodgeArmor.extend(item.dodge)
                        if item.name in handItemsByName:
                            weapons.append(item)
                            
                    allAttacks = []
                    for w in weapons:
                        allAttacks.extend(get_weapon_attacks(w.name))
                        
                    if not allAttacks:
                        continue
                        
                    maxRange = max([a.attackRange for a in allAttacks] + [0])
                    
                    tierProfiles[tier].append({
                        "defense": {
                            "blockPmf": convert_to_pmf(totalBlock),
                            "resistPmf": convert_to_pmf(totalResist),
                            "dodgeDice": count_dodge_dice(totalDodge)
                        },
                        "armorDefense": {
                            "blockPmf": convert_to_pmf(totalBlockArmor),
                            "resistPmf": convert_to_pmf(totalResistArmor),
                            "dodgeDice": count_dodge_dice(totalDodgeArmor)
                        },
                        "attacks": allAttacks,
                        "maxRange": maxRange
                    })

    print("Average Damage Output by Loadout per Tier")
    for tier in [1, 2, 3]:
        physTotals = []
        magicTotals = []
        for profile in tierProfiles[tier]:
            physTotal = 0.0
            magicTotal = 0.0
            for a in profile["attacks"]:
                ev = a.expectedDamage[0]
                if a.magic:
                    magicTotal += ev
                else:
                    physTotal += ev
            physTotals.append(physTotal)
            magicTotals.append(magicTotal)
        avgPhys = sum(physTotals) / len(physTotals) if physTotals else 0.0
        avgMagic = sum(magicTotals) / len(magicTotals) if magicTotals else 0.0
        print(f"  Tier {tier}: Avg Physical = {avgPhys:.3f}, Avg Magic = {avgMagic:.3f}")

    print("Average Defense by Loadout per Tier")
    for tier in [1, 2, 3]:
        dodgeTotals = []
        blockTotals = []
        resistTotals = []
        for profile in tierProfiles[tier]:
            dodgeTotals.append(profile["defense"]["dodgeDice"])
            blockEv = sum(i * p for i, p in enumerate(profile["defense"]["blockPmf"]))
            resistEv = sum(i * p for i, p in enumerate(profile["defense"]["resistPmf"]))
            blockTotals.append(blockEv)
            resistTotals.append(resistEv)
        avgDodge = sum(dodgeTotals) / len(dodgeTotals) if dodgeTotals else 0.0
        avgBlock = sum(blockTotals) / len(blockTotals) if blockTotals else 0.0
        avgResist = sum(resistTotals) / len(resistTotals) if resistTotals else 0.0
        print(f"  Tier {tier}: Avg Dodge = {avgDodge:.3f}, Avg Block = {avgBlock:.3f}, Avg Resist = {avgResist:.3f}")

    print("Average Armor Defense by Tier")
    for tier in [1, 2, 3]:
        armorDodgeTotals = []
        armorBlockTotals = []
        armorResistTotals = []
        for profile in tierProfiles[tier]:
            armorDodgeTotals.append(profile["armorDefense"]["dodgeDice"])
            armorBlockEv = sum(i * p for i, p in enumerate(profile["armorDefense"]["blockPmf"]))
            armorResistEv = sum(i * p for i, p in enumerate(profile["armorDefense"]["resistPmf"]))
            armorBlockTotals.append(armorBlockEv)
            armorResistTotals.append(armorResistEv)
        avgArmorDodge = sum(armorDodgeTotals) / len(armorDodgeTotals) if armorDodgeTotals else 0.0
        avgArmorBlock = sum(armorBlockTotals) / len(armorBlockTotals) if armorBlockTotals else 0.0
        avgArmorResist = sum(armorResistTotals) / len(armorResistTotals) if armorResistTotals else 0.0
        print(f"  Tier {tier}: Avg Armor Dodge = {avgArmorDodge:.3f}, Avg Armor Block = {avgArmorBlock:.3f}, Avg Armor Resist = {avgArmorResist:.3f}")

    print("Bleed Synergy")
    
    bleedSynergy = {1: 0.0, 2: 0.0, 3: 0.0}
    
    for tier in [1, 2, 3]:
        weightedPierceRateSum = 0.0
        enemyFrequencyWeight = sum(ENEMY_FREQUENCY[tier].values())
            
        for enemy in enemies:
            weight = ENEMY_FREQUENCY[tier].get(enemy.name, 0.0)
            if weight == 0.0:
                continue
                
            enemyPierceProbability = 0.0
            
            # Test this enemy against all player profiles in this tier
            for profile in tierProfiles[tier]:
                dodgeFailRate = 1.0 - calculate_dodge_chance(enemy.dodge, profile["defense"]["dodgeDice"])
                
                for i in range(len(enemy.attacks)):
                    damage = enemy.attacks[i]
                    if damage == 0:
                        continue
                    
                    defensePmf = profile["defense"]["resistPmf"] if enemy.attackType[i] == "magic" else profile["defense"]["blockPmf"]
                    
                    # Probability the attack pierces the block
                    pierceProb = sum(prob for val, prob in enumerate(defensePmf) if damage - val > 0)
                    
                    # Accumulate average pierce chance across all attacks and profiles
                    enemyPierceProbability += (dodgeFailRate * pierceProb)
            
            # Average the enemy's pierce rate across the profiles and multiply by its frequency
            avgEnemyPierce = enemyPierceProbability / (len(tierProfiles[tier]) * len(enemy.attacks))
            weightedPierceRateSum += (avgEnemyPierce * weight)
            
        # The true probability of an attack piercing in this specific tier's frequency
        globalPierceRate = weightedPierceRateSum / enemyFrequencyWeight
        
        encounterTriggerChance = 1.0 - math.pow((1.0 - globalPierceRate), 4)
        
        bleedSynergy[tier] = 2.0 * encounterTriggerChance
        print(f"  Tier {tier} Bleed Synergy: +{bleedSynergy[tier]:.3f} Expected Damage")

    print("Enemy Strength and Toughness")
    
    data = {}
    
    for enemy in enemies:
        tierResults = {1: {"stk": [], "dps": []}, 2: {"stk": [], "dps": []}, 3: {"stk": [], "dps": []}}
        
        for tier in [1, 2, 3]:
            for profile in tierProfiles[tier]:
                stk, sharron_prob = enemy_toughness(enemy, profile["defense"], profile["attacks"], bleedSynergy[tier])
                dps = enemy_strength(enemy, profile["defense"], profile["maxRange"], sharron_prob, bleedSynergy[tier])
                
                tierResults[tier]["dps"].append(dps)
                if stk != float("inf"):
                    tierResults[tier]["stk"].append(stk)
                    
        data[enemy.name] = {
            "hpTier": enemy.health,
            "isRanged": any(r > 1 for r in enemy.attackRange),
            "isLeap": enemy.leap
        }
        
        for tier in [1, 2, 3]:
            stkList = tierResults[tier]["stk"]
            dpsList = tierResults[tier]["dps"]
            avg_stk = sum(stkList) / len(stkList) if stkList else float("inf")
            avg_dps = sum(dpsList) / len(dpsList) if dpsList else 0.0
            
            data[enemy.name][tier] = {
                "stk": round(avg_stk, 3) if avg_stk != float("inf") else 9999.0,
                "dps": round(avg_dps, 3)
            }
            
    SUMMONS = {
        "Necromancer": ("Skeleton Soldier", 3)
    }

    DEATH_SPAWNS = {
        "Phalanx": ("Phalanx Hollow", 3)
    }
    
    for summonerName, (summonedName, maxCap) in SUMMONS.items():
        if summonerName not in data or summonedName not in data:
            continue
            
        for tier in [1, 2, 3]:
            baseStk = data[summonerName][tier]["stk"]
            baseDps = data[summonerName][tier]["dps"]
            
            summonDps = data[summonedName][tier]["dps"]
            
            if baseStk == 9999.0:
                expectedSummons = maxCap
            else:
                estimated_player_attacks = baseStk / 2.0 
                # Only count half the expected summons given that summoners are usually high priority
                expectedSummons = min(maxCap, estimated_player_attacks) * 0.5
                
            trueDps = baseDps + (expectedSummons * summonDps)
            
            data[summonerName][tier]["stk"] = round(baseStk, 3)
            data[summonerName][tier]["dps"] = round(trueDps, 3)

    for spawnerName, (spawnedName, count) in DEATH_SPAWNS.items():
        if spawnerName not in data or spawnedName not in data:
            continue
            
        for tier in [1, 2, 3]:
            baseStk = data[spawnerName][tier]["stk"]
            baseDps = data[spawnerName][tier]["dps"]
            
            spawnStk = data[spawnedName][tier]["stk"]
            spawnDps = data[spawnedName][tier]["dps"]
            
            if baseStk == 9999.0:
                trueStk = 9999.0 
            else:
                trueStk = baseStk + (count * spawnStk)
                
            trueDps = baseDps + (count * spawnDps)
            
            data[spawnerName][tier]["stk"] = round(trueStk, 3)
            data[spawnerName][tier]["dps"] = round(trueDps, 3)

    invaders = {}
    
    for enemyName, tiers in list(data.items()):
        if " - " in enemyName:
            baseName = enemyName.split(" - ")[0]
            
            if baseName not in invaders:
                invaders[baseName] = {
                    "count": 0,
                    "hpTier": tiers["hpTier"],
                    "isRanged": tiers["isRanged"],
                    "isLeap": tiers["isLeap"],
                    1: {"stk": 0.0, "dps": 0.0},
                    2: {"stk": 0.0, "dps": 0.0},
                    3: {"stk": 0.0, "dps": 0.0}
                }
            
            agg = invaders[baseName]
            agg["count"] += 1
            
            agg["isRanged"] = agg["isRanged"] or tiers["isRanged"]
            agg["isLeap"] = agg["isLeap"] or tiers["isLeap"]
            
            for t in [1, 2, 3]:
                stk_val = tiers[t]["stk"]
                agg[t]["stk"] += 50.0 if stk_val == 9999.0 else stk_val
                agg[t]["dps"] += tiers[t]["dps"]

    # Average for invaders
    for baseName, agg in invaders.items():
        count = agg["count"]
        data[baseName] = {
            "hpTier": agg["hpTier"],
            "isRanged": agg["isRanged"],
            "isLeap": agg["isLeap"],
            1: {
                "stk": round(agg[1]["stk"] / count, 3),
                "dps": round(agg[1]["dps"] / count, 3)
            },
            2: {
                "stk": round(agg[2]["stk"] / count, 3),
                "dps": round(agg[2]["dps"] / count, 3)
            },
            3: {
                "stk": round(agg[3]["stk"] / count, 3),
                "dps": round(agg[3]["dps"] / count, 3)
            }
        }

    # Cut invidividual invader behaviors, keep the aggregates
    data = {k: v for k, v in data.items() if " - " not in k}

    with open("enemy_stats.json", "w") as f:
        json.dump(data, f)
        

if __name__ == "__main__":
    main()