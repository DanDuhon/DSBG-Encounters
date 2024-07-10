from statistics import mean
from itertools import product


b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)
means = {
    b: mean(b),
    u: mean(u),
    o: mean(o)
}

reachMod = {
    1: 0.44970414201183434,
    2: 0.8224852071005917,
    3: 0.9763313609467456,
    4: 1
}

bleedTrigger = {
    1: {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: []
    },
    2: {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: []
    },
    3: {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: []
    }
}

gear = {
    "Assassin": {
        "armor": [],
        "hand": [],
        "upgradesArmor": [],
        "upgradesHand": []
    }
}


class Armor:
    def __init__(self, name, character, tier, block=[], resist=[], dodge=[], blockMod=0, resistMod=0, canDodge=True, dodgeBonus=None, immunities=set(), upgradeSlots=0, turnHeal=0, turnStamina=0, dodgeMoveBonus=0) -> None:
        self.name = name
        self.character = character
        self.tier = tier
        self.block = block
        self.resist = resist
        self.dodge = dodge
        self.blockMod = blockMod
        self.resistMod = resistMod
        self.canDodge = canDodge
        self.dodgeBonus = dodgeBonus
        self.immunities = immunities
        self.upgradeSlots = upgradeSlots
        self.turnHeal = turnHeal
        self.turnStamina = turnStamina
        self.dodgeMoveBonus = dodgeMoveBonus


class HandItem:
    def __init__(self, name, character, tier, attacks=[], block=[], resist=[], dodge=[], blockMod=0, resistMod=0, twoHanded=False, canUseWithTwoHanded=False, turnHeal=0, turnStamina=0, canDodge=True, dodgeMoveBonus=0, immunities=set(), upgradeSlots=0, pushOnAttacked=0, pushType=None) -> None:
        self.name = name
        self.character = character
        self.tier = tier
        self.attacks = attacks
        self.block = block
        self.resist = resist
        self.dodge = dodge
        self.blockMod = blockMod
        self.resistMod = resistMod
        self.twoHanded = twoHanded
        self.canUseWithTwoHanded = canUseWithTwoHanded
        self.canDodge = canDodge
        self.immunities = immunities
        self.upgradeSlots = upgradeSlots
        self.turnHeal = turnHeal
        self.turnStamina = turnStamina
        self.dodgeMoveBonus = dodgeMoveBonus
        self.pushOnAttacked = pushOnAttacked
        self.pushType = pushType


class Upgrade:
    def __init__(self, name, character, tier, type, block=[], resist=[], dodge=[], damage=[[]], rerollDefense=False, staminaGainFromDamage=99, dodgeMod=0, dodgeModRange=0, damageMod=0, attackRangeMod=0, attackRangeLimit=set(), magic=False, turnHeal=0, turnStamina=0, dodgeMoveBonus=0, multiAttackStamina=0) -> None:
        self.name = name
        self.character = character
        self.tier = tier
        self.type = type
        self.block = block
        self.resist = resist
        self.dodge = dodge
        self.damage = damage
        self.damageMod = damageMod
        self.attackRangeMod = attackRangeMod
        self.magic = magic
        self.turnHeal = turnHeal
        self.turnStamina = turnStamina
        self.dodgeMoveBonus = dodgeMoveBonus
        self.multiAttackStamina = multiAttackStamina
        self.dodgeMod = dodgeMod
        self.dodgeModRange = dodgeModRange
        self.staminaGainFromDamage = staminaGainFromDamage
        self.rerollDefense = rerollDefense


class Attack:
    def __init__(self, name, attackNumber, staminaCost, damage=[[]], damageMod=0, attackRange=0, magic=False, bleed=False, poison=False, ignoreDefense=False, damageBonus=set(), noRange0=False) -> None:
        self.name = name
        self.attackNumber = attackNumber
        # Uses reachMod to calculate the stamina cost to get into range (1 stamina, 2 stamina, 3 stamina).
        self.staminaCost = staminaCost + (1 - reachMod[min([4, attackRange + 1])]) + (1 - reachMod[min([4, attackRange + 2])]) + (1 - reachMod[min([4, attackRange + 3])])
        self.attackRange = attackRange
        self.damage = damage
        self.damageMod = damageMod
        self.magic = magic
        self.bleed = bleed
        self.poison = poison
        self.ignoreDefense = ignoreDefense
        self.damageBonus = damageBonus
        self.noRange0 = noRange0
        self.totalDamage = {}

        self.expectedDamage = {
            -1: 0,
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0
        }
        for x in range(7): # defense
            for attack in self.damage:
                for die in attack:
                    self.expectedDamage[x] += means[die]
                self.expectedDamage[x] = self.expectedDamage[x] + self.damageMod - (x if not self.ignoreDefense else 0)
            self.expectedDamage[x] = max([0, self.expectedDamage[x] + (1 if poison else 0)])

        for x in range(7): # defense
            for attack in self.damage:
                combos = list(product(*attack))
                bleedTrigger[self.tier][x].append((sum([1 for c in combos if sum(c) > x]) / len([c for c in combos]) if len([c for c in combos]) > 0 else 0))


class Loadout:
    def __init__(self, armor, handItem1, handItem2, armorUpgrade, handItem1Upgrade1, handItem1Upgrade2, handItem2Upgrade1, handItem2Upgrade2):
        self.armor = armor
        self.handItem1 = handItem1
        self.handItem2 = handItem2
        self.armorUpgrade = armorUpgrade
        self.handItem1Upgrade1 = handItem1Upgrade1
        self.handItem1Upgrade2 = handItem1Upgrade2
        self.handItem2Upgrade1 = handItem2Upgrade1
        self.handItem2Upgrade2 = handItem2Upgrade2




Armor(name="Assassin Armour", character="Assassin", tier=1, block=[b], resist=[b], dodge=[d])
Armor(name="Shadow Armour", character="Assassin", tier=2, dodge=[d, d], upgradeSlots=2, dodgeMoveBonus=True)
Armor(name="Alva Armour", character="Assassin", tier=3, block=[u], resist=[u], dodge=[d, d], upgradeSlots=1)
Upgrade(name="Hornet Ring", character="Assassin", tier=2, type="armor", damage=[o,o], damageMod=-2)
HandItem(name="Estoc", character="Assassin", tier=1)
HandItem(name="Target Shield", character="Assassin", tier=1, dodge=[d])
HandItem(name="Spotted Whip", character="Assassin", tier=2, dodge=[d])
HandItem(name="Rotten Ghru Dagger", character="Assassin", tier=2)
HandItem(name="Composite Bow", character="Assassin", tier=2, twoHanded=True, dodge=[d])
HandItem(name="Umbral Dagger", character="Assassin", tier=3, dodge=[d])
HandItem(name="Lucerne", character="Assassin", tier=3, twoHanded=True, block=[b], resist=[b], dodge=[d])
HandItem(name="Elkhorn Round Shield", character="Assassin", tier=3, canUseWithTwoHanded=True, block=[b], resist=[b, b], dodge=[d])
HandItem(name="Carthus Curved Sword", character="Assassin", tier=3, dodge=[d])

Armor(name="Cleric Robes", character="Cleric", tier=1, block=[b], resist=[u])
Armor(name="Archdeacon Robe", character="Cleric", tier=3, block=[o], resist=[b, o], upgradeSlots=2)
Upgrade(name="Magic Stoneplate Ring", character="Cleric", tier=3, type="armor", resist=[b])
HandItem(name="Mace", resist=[b], character="Cleric", tier=1)
HandItem(name="Sacred Chime", character="Cleric", tier=1)
HandItem(name="Blue Wooden Shield", block=[b], character="Cleric", tier=1)
HandItem(name="Sunset Shield", character="Cleric", tier=2, block=[b], resist=[u], pushType="Hollow", pushOnAttacked=1)
HandItem(name="Sacred Oath", character="Cleric", tier=2, block=[u])
HandItem(name="Med Heal", character="Cleric", tier=2)
HandItem(name="Magic Barrier", character="Cleric", tier=2, resist=[u])
HandItem(name="Cleric's Candlestick", character="Cleric", tier=2, upgradeSlots=1)
HandItem(name="Morne's Great Hammer", character="Cleric", tier=3, twoHanded=True, block=[b, b], resist=[b, b], upgradeSlots=1)
HandItem(name="Great Heal", character="Cleric", tier=3)
HandItem(name="Atonement", character="Cleric", tier=3)

Armor(name="Loincloth", character="Deprived", tier=1, resist=[b])
Armor(name="Brass Armour", character="Deprived", tier=2, block=[b, b], resist=[b, b], upgradeSlots=1)
Armor(name="Mirrah Armour", character="Deprived", tier=3, block=[u], resist=[o], dodge=[d], upgradeSlots=1)
Upgrade(name="Carthus Milkring", character="Deprived", tier=3, type="armor", dodge=[d])
HandItem(name="Club", character="Deprived", tier=1)
HandItem(name="Plank Shield", character="Deprived", tier=1, block=[b])
HandItem(name="Dung Pie", character="Deprived", tier=2)
HandItem(name="Buckler", character="Deprived", tier=2, canUseWithTwoHanded=True, block=[b], dodge=[d])
HandItem(name="Broken Straight Sword", character="Deprived", tier=2, upgradeSlots=2)
HandItem(name="Black Knight Shield (Deprived)", character="Deprived", tier=3, block=[b], dodge=[d], upgradeSlots=2)
HandItem(name="Painting Guardian's Curved Sword", character="Deprived", tier=3, upgradeSlots=2)
HandItem(name="Great Club", character="Deprived", tier=3, twoHanded=True, block=[b], resist=[b], upgradeSlots=1)

Armor(name="Herald Armour", character="Herald", tier=1, block=[b], resist=[b], dodge=[d])
Armor(name="Cathedral Knight Armour", character="Herald", tier=2, block=[u], resist=[b, b], upgradeSlots=2)
Upgrade(name="Tiny Being's Ring", character="Herald", tier=3, type="armor", turnHeal=2)
HandItem(name="Spear", character="Herald", tier=1)
HandItem(name="Talisman", character="Herald", tier=1)
HandItem(name="Kite Shield", character="Herald", tier=1, block=[b])
HandItem(name="Replenishment", character="Herald", tier=2)
HandItem(name="Lothric's Holy Sword", character="Herald", tier=2, resist=[b], upgradeSlots=1)
HandItem(name="Golden Wing Crest Shield", character="Herald", tier=2, block=[u], resist=[u], upgradeSlots=1)
HandItem(name="Saint Bident", character="Herald", tier=3, block=[b], resist=[b], upgradeSlots=2)
HandItem(name="Partizan", character="Herald", tier=3, twoHanded=True, block=[u], resist=[b], upgradeSlots=1)
HandItem(name="Grass Crest Shield", character="Herald", tier=3, block=[u], resist=[o])
HandItem(name="Bountiful Sunlight", character="Herald", tier=3)
HandItem(name="Bountiful Light", character="Herald", tier=3)

Armor(name="Knight Armour", character="Knight", tier=1, block=[u], resist=[b])
Armor(name="Lothric Knight Armour", character="Knight", tier=2, block=[u], resist=[u], upgradeSlots=2)
Armor(name="Faraam Armour", character="Knight", tier=3, block=[o], resist=[u], upgradeSlots=2)
Armor(name="Elite Knight Armour", character="Knight", tier=3, block=[u, u], resist=[b], upgradeSlots=2)
Upgrade(name="Sun Princess Ring", character="Herald", tier=3, type="armor", turnHeal=1)
HandItem(name="Long Sword", character="Knight", tier=1)
HandItem(name="Kite Shield", character="Knight", tier=1, block=[b])
HandItem(name="Spider Shield", character="Knight", tier=2, block=[b, b], immunities=set(["poison"]))
HandItem(name="Broadsword", character="Knight", tier=2, block=[b], resist=[b], upgradeSlots=1)
HandItem(name="Twin Dragon Greatshield", character="Knight", tier=3, block=[u, u], resist=[u])
HandItem(name="Falchion", character="Knight", tier=3, block=[b], resist=[u], upgradeSlots=2)
HandItem(name="Black Iron Greatshield", character="Knight", tier=3, block=[u], resist=[u, u])

Armor(name="Sellsword Armour", character="Mercenary", tier=1, block=[b], resist=[b], dodge=[d])
Armor(name="Black Leather Armour", character="Mercenary", tier=2, block=[b], resist=[b], dodge=[d], upgradeSlots=1)
Armor(name="Eastern Armour", character="Mercenary", tier=3, block=[b, b], resist=[b, b], dodge=[d, d], upgradeSlots=2)
Upgrade(name="Ring of Favour", character="Mercenary", tier=2, type="armor", multiAttackStamina=1)
Upgrade(name="Wolf Ring", character="Mercenary", tier=3, type="armor", rerollDefense=True)
HandItem(name="Sellsword Twinblades", character="Mercenary", tier=1, twoHanded=True)
HandItem(name="Wooden Shield", character="Mercenary", tier=1, dodge=[d])
HandItem(name="Warden Twinblades", character="Mercenary", tier=2, twoHanded=True, block=[b], upgradeSlots=1)
HandItem(name="Crystal Straight Sword", character="Mercenary", tier=2, upgradeSlots=1)
HandItem(name="Crest Shield", character="Mercenary", tier=2, block=[b], dodge=[d])
HandItem(name="Onikiri and Ubadachi", character="Mercenary", tier=3, twoHanded=True, dodge=[d], upgradeSlots=1)
HandItem(name="Large Leather Shield", character="Mercenary", tier=3, block=[u], resist=[b], dodge=[d])
HandItem(name="Drang Hammers", character="Mercenary", tier=3, twoHanded=True, resist=[b], dodge=[d], upgradeSlots=1)

Armor(name="Pyromancer Garb", character="Pyromancer", tier=1, resist=[b, b], dodge=[d])
Armor(name="Cornyx's Robes", block=[u], resist=[o], upgradeSlots=2)
Upgrade(name="Carthus Flame Arc", character="Pyromancer", tier=3, type="weapon", magic=True, damageMod=1)
HandItem(name="Pyromancy Flame", character="Pyromancer", tier=1)
HandItem(name="Caduceus Round Shield", character="Pyromancer", tier=1, block=[u])
HandItem(name="Hand Axe", character="Pyromancer", tier=1)
HandItem(name="Immolation Tinder", character="Pyromancer", tier=2, twoHanded=True, resist=[b], upgradeSlots=2)
HandItem(name="Great Combustion", character="Pyromancer", tier=2)
HandItem(name="Fire Surge", character="Pyromancer", tier=2)
HandItem(name="Stone Parma", character="Pyromancer", tier=3, block=[u], resist=[u], upgradeSlots=1)
HandItem(name="Rapport", character="Pyromancer", tier=3)
HandItem(name="Great Chaos Fireball", character="Pyromancer", tier=3)
HandItem(name="Fire Whip", character="Pyromancer", tier=3)

Armor(name="Sorcerer Robes", character="Sorcerer", tier=1, block=[b], resist=[u])
Armor(name="Dragonscale Armour", character="Sorcerer", tier=2, block=[b], resist=[b, u], dodge=[d], upgradeSlots=1)
Upgrade(name="Faron Flashsword", character="Sorcerer", tier=2, type="weapon", magic=True, attackRangeMod=1, attackRangeLimit={0,})
Upgrade(name="Crystal Magic Weapon", character="Sorcerer", tier=3, type="weapon", magic=True, damageMod=1)
HandItem(name="Sorcerer's Catalyst", character="Sorcerer", tier=1)
HandItem(name="Mail Breaker", character="Sorcerer", tier=1, character="Sorcerer", tier=1)
HandItem(name="Leather Shield", character="Sorcerer", tier=1, resist=[b], dodge=[d])
HandItem(name="Torch", character="Sorcerer", tier=2, character="Sorcerer", tier=2)
HandItem(name="Magic Shield", character="Sorcerer", tier=2, block=[b], resist=[o])
HandItem(name="Aural Decoy", character="Sorcerer", tier=2)
HandItem(name="Soul Greatsword", character="Sorcerer", tier=3)
HandItem(name="Homing Crystal Soulmass", character="Sorcerer", tier=3)
HandItem(name="Crystal Hail", character="Sorcerer", tier=3)

Armor(name="Deserter Armour", character="Thief", tier=1, block=[b], resist=[b], dodge=[d])
Armor(name="Black Hand Armour (Thief)", character="Thief", tier=2, block=[u], resist=[b], dodge=[d], upgradeSlots=2)
Upgrade(name="Obscuring Ring", character="Thief", tier=2, type="armor", dodgeMod=2, dodgeModRange=2)
HandItem(name="Shortbow", character="Thief", tier=1, twoHanded=True)
HandItem(name="Bandit Knife", character="Thief", tier=1)
HandItem(name="Iron Round Shield", character="Thief", tier=1, canUseWithTwoHanded=True, dodge=[d])
HandItem(name="Small Leather Shield", character="Thief", tier=2, canUseWithTwoHanded=True, block=[b], resist=[b], dodge=[d])
HandItem(name="Shotel", character="Thief", tier=2, dodge=[d], upgradeSlots=1)
HandItem(name="Royal Dirk", character="Thief", tier=3, block=[b], resist=[b], dodge=[d], upgradeSlots=1)
HandItem(name="Man Serpent Hatchet", character="Thief", tier=3, upgradeSlots=1)
HandItem(name="Hawkwood's Shield", character="Thief", tier=3, canUseWithTwoHanded=True, block=[u], resist=[u], dodge=[d])
HandItem(name="Dragonrider Bow", character="Thief", tier=3, twoHanded=True, dodge=[d], upgradeSlots=1)

Armor(name="Northern Armour", character="Warrior", tier=1, block=[b], resist=[b], dodge=[d])
Armor(name="Fallen Knight Armour", character="Warrior", tier=3, block=[u], resist=[u], dodge=[d], upgradeSlots=2)
Upgrade(name="Knight Slayer's Ring", character="Warrior", tier=2, type="armor", staminaGainFromDamage=3)
HandItem(name="Battle Axe", character="Warrior", tier=1)
HandItem(name="Round Shield", character="Warrior", tier=1, block=[b])
HandItem(name="Spiked Mace", character="Warrior", tier=2, twoHanded=True, block=[b], resist=[b], upgradeSlots=1)
HandItem(name="Silver Knight Shield", character="Warrior", tier=2, block=[u], upgradeSlots=1)
HandItem(name="Great Wooden Hammer", character="Warrior", tier=2, twoHanded=True, block=[b], upgradeSlots=1)
HandItem(name="Caestus", character="Warrior", tier=2)
HandItem(name="Warpick", character="Warrior", tier=3, upgradeSlots=1)
HandItem(name="Great Machete", character="Warrior", tier=3, twoHanded=True, block=[b], resist=[b], upgradeSlots=1)
HandItem(name="Dragonslayer's Axe", character="Warrior", tier=3, resist=[b], upgradeSlots=1)
HandItem(name="Balder Side Sword", character="Warrior", tier=3, resist=[b], upgradeSlots=1)
