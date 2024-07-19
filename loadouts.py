from itertools import product, chain, combinations
from statistics import mean

from armor import armorDict, armorUpgradesDict
from hand_items import handItemsDict, handItemUpgradesDict
from treasure_item_tiers import a


b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)
means = {
    b: mean(b),
    u: mean(u),
    o: mean(o),
    d: mean(d)
}

dodgeList = []

loadouts = {
    "Assassin": {
        1: [],
        2: [],
        3: []
    },
    "Cleric": {
        1: [],
        2: [],
        3: []
    },
    "Deprived": {
        1: [],
        2: [],
        3: []
    },
    "Herald": {
        1: [],
        2: [],
        3: []
    },
    "Knight": {
        1: [],
        2: [],
        3: []
    },
    "Mercenary": {
        1: [],
        2: [],
        3: []
    },
    "Pyromancer": {
        1: [],
        2: [],
        3: []
    },
    "Sorcerer": {
        1: [],
        2: [],
        3: []
    },
    "Thief": {
        1: [],
        2: [],
        3: []
    },
    "Warrior": {
        1: [],
        2: [],
        3: []
    }
}

dodgeMod = {
    1: {},
    2: {},
    3: {}
}


class Loadout:
    def __init__(self, character, tier, armor, handItem1, handItem2, armorUpgrade1, armorUpgrade2, handItem1Upgrade1, handItem1Upgrade2, handItem2Upgrade1, handItem2Upgrade2) -> None:
        loadouts[character][tier].append(self)
        self.character = character
        self.tier = tier
        self.armor = armor
        self.handItem1 = handItem1
        self.handItem2 = handItem2
        self.armorUpgrade1 = armorUpgrade1
        self.armorUpgrade2 = armorUpgrade2
        self.handItem1Upgrade1 = handItem1Upgrade1
        self.handItem1Upgrade2 = handItem1Upgrade2
        self.handItem2Upgrade1 = handItem2Upgrade1
        self.handItem2Upgrade2 = handItem2Upgrade2
        
        self.block = sum([means[die] for die in armor.block + handItem1.block + handItem2.block]) + sum([armor.blockMod, handItem1.blockMod, handItem2.blockMod]),
        self.resist = sum([means[die] for die in armor.resist + handItem1.resist + handItem2.resist]) + sum([armor.resistMod, handItem1.resistMod, handItem2.resistMod]),
        self.dodge = 0 if not all([armor.canDodge, handItem1.canDodge, handItem2.canDodge]) else (armor.dodge + handItem1.dodge + handItem2.dodge + (armorUpgrade1.dodge if armorUpgrade1 else []) + (armorUpgrade2.dodge if armorUpgrade2 else [])),
        self.dodgeBonus = armor.dodgeBonus,
        self.immunities = armor.immunities | handItem1.immunities | handItem2.immunities

        self.damage3StaminaBonus = (
            (armorUpgrade1 and armorUpgrade1.damage3StaminaBonus)
            or (armorUpgrade2 and armorUpgrade2.damage3StaminaBonus)
            or (armorUpgrade1 and armorUpgrade1.damage3StaminaBonus)
            or (armorUpgrade2 and armorUpgrade2.damage3StaminaBonus)
            )
        
        self.staminaFromDamage = (
            (armorUpgrade1 and armorUpgrade1.staminaFromDamage)
            or (armorUpgrade2 and armorUpgrade2.staminaFromDamage)
            or (armorUpgrade1 and armorUpgrade1.staminaFromDamage)
            or (armorUpgrade2 and armorUpgrade2.staminaFromDamage)
            )

        self.staminaRegen = (
            3
            + (armorUpgrade1.staminaRegenBonus if armorUpgrade1 else 0)
            + (armorUpgrade2.staminaRegenBonus if armorUpgrade2 else 0)
            + (armorUpgrade1.twoAttackStaminaBonus if armorUpgrade1
                and (
                    any(a.bleed for a in handItem1.attacks)
                    or any(a.poison for a in handItem1.attacks)
                    or any(d.damage[0] for d in handItem1.attacks))
                and (
                    any(a.bleed for a in handItem2.attacks)
                    or any(a.poison for a in handItem2.attacks)
                    or any(d.damage[0] for d in handItem2.attacks)) else 0
                )
            + (armorUpgrade2 and armorUpgrade2.twoAttackStaminaBonus if armorUpgrade2
                and (
                    any(a.bleed for a in handItem1.attacks)
                    or any(a.poison for a in handItem1.attacks)
                    or any(d.damage[0] for d in handItem1.attacks))
                and (
                    any(a.bleed for a in handItem2.attacks)
                    or any(a.poison for a in handItem2.attacks)
                    or any(d.damage[0] for d in handItem2.attacks)) else 0
                )
            )
        
        self.healthRegen = (
            0
            )

        dodgeList.append(len(self.dodge[0]) if self.dodge != (0,) else 0)

        # These are item effects that affect all attacks.
        turnMagic = any([a.attacksAreMagic for a in handItem1.attacks + handItem2.attacks])
        magicDamageMod = sum([a.attacksMagicDamageBonus for a in handItem1.attacks + handItem2.attacks])
        magicDamageBonus = handItem1.magicDamageBonus + handItem2.magicDamageBonus
        magicStaminaCostMod = handItem1.magicStaminaCost + handItem2.magicStaminaCost

        for attack in handItem1.attacks:
            attack.magic = True if turnMagic else attack.magic
            attack.staminaCost += magicStaminaCostMod if attack.magic else 0
            for damage in attack.damage:
                damage += magicDamageBonus if attack.magic else []
            attack.damageMod += magicDamageMod if attack.magic else 0

        for attack in handItem2.attacks:
            attack.magic = True if turnMagic else attack.magic
            attack.staminaCost += magicStaminaCostMod if attack.magic else 0
            for damage in attack.damage:
                damage += magicDamageBonus if attack.magic else []
            attack.damageMod += magicDamageMod if attack.magic else 0

        maxStamina1 = max(a.staminaCost for a in handItem1.attacks) if handItem1 and handItem1.attacks else None
        maxStamina2 = max(a.staminaCost for a in handItem2.attacks) if handItem2 and handItem2.attacks else None

        for upgrade in [handItem1Upgrade1, handItem1Upgrade2]:
            if not upgrade:
                continue
            for attack in handItem1.attacks:
                attack.magic = True if upgrade.magic else attack.magic
                attack.bleed = True if upgrade.bleed else attack.bleed
                attack.poison = True if upgrade.poison else attack.poison
                attack.attackRange = 1 if attack.attackRange == 0 and upgrade.range0GetRange1 else attack.attackRange
                attack.staminaCost += upgrade.staminaCostMod
                attack.staminaCost += upgrade.highestStaminaMod if attack.staminaCost == maxStamina1 else 0
                attack.staminaCost += upgrade.highestStaminaModIfBoss if attack.staminaCost == maxStamina1 and handItem1.boss else 0
                for damage in attack.damage:
                    damage += upgrade.damage
                attack.damageMod += upgrade.damageMod

        for upgrade in [handItem2Upgrade1, handItem2Upgrade2]:
            if not upgrade:
                continue
            for attack in handItem2.attacks:
                attack.magic = True if upgrade.magic else attack.magic
                attack.bleed = True if upgrade.bleed else attack.bleed
                attack.poison = True if upgrade.poison else attack.poison
                attack.attackRange = 1 if attack.attackRange == 0 and upgrade.range0GetRange1 else attack.attackRange
                attack.staminaCost += upgrade.staminaCostMod
                attack.staminaCost += upgrade.highestStaminaMod if attack.staminaCost == maxStamina2 else 0
                attack.staminaCost += upgrade.highestStaminaModIfBoss if attack.staminaCost == maxStamina2 and handItem2.boss else 0
                for damage in attack.damage:
                    damage += upgrade.damage
                attack.damageMod += upgrade.damageMod


        self.attacks = [a for a in handItem1.attacks + handItem2.attacks if (a.bleed and not a.damage[0])]
        self.attacks += [a for a in handItem1.attacks + handItem2.attacks if a not in set(self.attacks)]


loadoutLookup = {1: {}, 2: {}, 3: {}}

for character in ["Assassin", "Cleric", "Deprived", "Herald", "Knight", "Mercenary", "Pyromancer", "Sorcerer", "Thief", "Warrior"]:
    for tier in range(1, 4):
        loadoutsCombos = chain(
            product([armorDict[armor] for armor in armorDict if armorDict[armor].tier[character] == tier],
                    combinations([armorUpgradesDict[u] for u in set(a[character]["upgradeArmor"])], 2 if tier == 3 else 1 if tier == 2 else 0),
                    product([handItemsDict[h] for h in handItemsDict if handItemsDict[h].twoHanded and handItemsDict[h].tier[character] == tier],
                            (
                                [handItemsDict[h] for h in handItemsDict if handItemsDict[h].canUseWithTwoHanded and handItemsDict[h].tier[character] == tier] if [handItemsDict[h] for h in handItemsDict if handItemsDict[h].canUseWithTwoHanded and handItemsDict[h].tier[character] == tier]
                                else [handItemsDict[h] for h in handItemsDict if handItemsDict[h].canUseWithTwoHanded and handItemsDict[h].tier[character] == tier - 1] if [handItemsDict[h] for h in handItemsDict if handItemsDict[h].canUseWithTwoHanded and handItemsDict[h].tier[character] == tier - 1]
                                else [handItemsDict[h] for h in handItemsDict if handItemsDict[h].canUseWithTwoHanded and handItemsDict[h].tier[character] == tier - 2]
                            )),
                    combinations([handItemUpgradesDict[u] for u in set(a[character]["upgradeWeapon"])], 2 if tier == 3 else 1 if tier == 2 else 0)),
            product([armorDict[armor] for armor in armorDict if tier == armorDict[armor].tier[character]],
                    combinations([armorUpgradesDict[u] for u in set(a[character]["upgradeArmor"])], 2 if tier == 3 else 1 if tier == 2 else 0),
                    combinations([handItemsDict[h] for h in handItemsDict if handItemsDict[h].name not in {"None1", "None2"} and not handItemsDict[h].twoHanded and handItemsDict[h].tier[character] == tier], 2),
                    combinations([handItemUpgradesDict[u] for u in set(a[character]["upgradeWeapon"])], 4 if tier == 3 else 2 if tier == 2 else 0)))

        for i, l in enumerate(loadoutsCombos):
            armor = l[0]
            armorUpgrades = l[1]
            armorUpgrade1 = None if tier == 1 or armor.upgradeSlots == 0 else armorUpgrades[0]
            armorUpgrade2 = None if tier <= 2 or armor.upgradeSlots <= 1 else armorUpgrades[1]
            handItems = l[2]
            handItem1 = handItems[0]
            handItem2 = handItems[1] if len(handItems) > 1 else None
            # Skip this loadout if it can't deal damage.
            if all(not a.damage[0] and not a.poison for a in handItem1.attacks + handItem2.attacks):
                continue
            handItemUpgrades = l[3]
            handItem1Upgrade1 = None if tier == 1 or handItem1.upgradeSlots == 0 else handItemUpgrades[0]
            handItem1Upgrade2 = None if tier <= 2 or handItem1.upgradeSlots <= 1 else handItemUpgrades[1]
            handItem2Upgrade1 = (
                handItemUpgrades[1] if tier == 2 and handItem2.upgradeSlots > 0
                else None if tier == 1 or len(handItems) <= 1 or handItem2.upgradeSlots == 0
                else handItemUpgrades[2])
            handItem2Upgrade2 = None if tier <= 2 or len(handItems) <= 1 or handItem2.upgradeSlots <= 1 else handItemUpgrades[3]
            Loadout(
                character=character,
                tier=tier,
                armor=armor,
                handItem1=handItem1,
                handItem2=handItem2,
                armorUpgrade1=armorUpgrade1,
                armorUpgrade2=armorUpgrade2,
                handItem1Upgrade1=handItem1Upgrade1,
                handItem1Upgrade2=handItem1Upgrade2,
                handItem2Upgrade1=handItem2Upgrade1,
                handItem2Upgrade2=handItem2Upgrade2)
            # This is to speed things up for testing.
            # if i > 100:
            #     break
#             loadouts[tier].append({
#                 "block": sum([means[die] for die in l[0].block + l[1][0].block + l[1][1].block]) + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod]),
#                 "blockRoll": [[v + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod]) for v in b] for b in l[0].block + l[1][0].block + l[1][1].block],
#                 "resist": sum([means[die] for die in l[0].resist + l[1][0].resist + l[1][1].resist]) + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod]),
#                 "resistRoll": [[v + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod]) for v in b] for b in l[0].resist + l[1][0].resist + l[1][1].resist],
#                 "dodge": 0 if not all([l[0].canDodge, l[1][0].canDodge, l[1][1].canDodge]) else (l[0].dodge + l[1][0].dodge + l[1][1].dodge),
#                 "dodgeBonus": l[0].dodgeBonus,
#                 "immunities": l[0].immunities | l[1][0].immunities | l[1][1].immunities
#             })

#             block = sum([means[die] for die in l[0].block + l[1][0].block + l[1][1].block]) + sum([l[0].blockMod, l[1][0].blockMod, l[1][1].blockMod])
#             resist = sum([means[die] for die in l[0].resist + l[1][0].resist + l[1][1].resist]) + sum([l[0].resistMod, l[1][0].resistMod, l[1][1].resistMod])
#             dodge = (0,) if not all([l[0].canDodge, l[1][0].canDodge, l[1][1].canDodge]) else tuple(l[0].dodge + l[1][0].dodge + l[1][1].dodge)

#             if tuple([block, resist, dodge]) in loadoutLookup[tier]:
#                 loadoutLookup[tier][tuple([block, resist, dodge])] += 1
#             else:
#                 loadoutLookup[tier][tuple([block, resist, dodge])] = 1
#                 x += 1

#         # Overall dodge modifier for the following dodge difficulties.
#         # Used for enemies that inflict Stagger or Frostbite.
#         dodgeMod[tier] = {
#             0: 1,
#             1: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 1]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
#             2: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 2]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
#             3: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 3]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
#             4: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 4]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
#             5: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 5]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]]),
#             6: mean([1 if l["dodge"] == 0 else (1 - (sum([1 for do in product(*l["dodge"]) if sum(do) >= 6]) / len(list(product(*l["dodge"]))))) for l in loadouts[tier]])
#         }

# # Winged Knight gets a bonus against blocks of 3 or higher.
# expectedBlock = {}
# expectedResist = {}
# for x in range(2, 14):
#     expectedBlock[x] = {
#         1: 1 - (sum([1 for l in loadouts[1] if l["block"] >= x]) / len(loadouts[1])),
#         2: 1 - (sum([1 for l in loadouts[2] if l["block"] >= x]) / len(loadouts[2])),
#         3: 1 - (sum([1 for l in loadouts[3] if l["block"] >= x]) / len(loadouts[3]))
#         }
#     expectedResist[x] = {
#         1: 1 - (sum([1 for l in loadouts[1] if l["resist"] >= x]) / len(loadouts[1])),
#         2: 1 - (sum([1 for l in loadouts[2] if l["resist"] >= x]) / len(loadouts[2])),
#         3: 1 - (sum([1 for l in loadouts[3] if l["resist"] >= x]) / len(loadouts[3]))
#         }
print(mean(dodgeList))
pass