from treasure_item_tiers import a


armor = []
armorDict = {}
armorUpgrades = []
armorUpgradesDict = {}

b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)


class Armor:
    def __init__(self, name, character=None, block=[], resist=[], dodge=[], blockMod=0, resistMod=0, walkBonus=0, healthPerEnemyOnNode=0, thorns=False, upgradeSlots=0, highestOneHandedStaminaDiscount=0, magicStaminaMod=0, nodeAttackStaminaDiscount=0, arcAttackDodgeBonus=0, healBonus=0, canDodge=True, canWalk=True, canRun=True, dodgeBonus=None, immunities=set()) -> None:
        armor.append(self)
        armorDict[name] = self
        self.character = character
        self.name = name
        self.block = block
        self.resist = resist
        self.dodge = dodge
        self.blockMod = blockMod
        self.resistMod = resistMod
        self.canDodge = canDodge
        self.dodgeBonus = dodgeBonus
        self.immunities = immunities
        self.upgradeSlots = upgradeSlots
        self.healBonus = healBonus
        self.arcAttackDodgeBonus = arcAttackDodgeBonus
        self.magicStaminaMod = magicStaminaMod
        self.canWalk = canWalk
        self.canRun = canRun
        self.nodeAttackStaminaDiscount = nodeAttackStaminaDiscount
        self.thorns = thorns
        self.highestOneHandedStaminaDiscount = highestOneHandedStaminaDiscount
        self.healthPerEnemyOnNode = healthPerEnemyOnNode
        self.walkBonus = walkBonus
        self.tier = {
            "Assassin": 1 if name in set(a["Assassin"]["armor"][1]) else        2 if name in set(a["Assassin"]["armor"][2]) else    3 if name in set(a["Assassin"]["armor"][3]) else None,
            "Cleric": 1 if name in set(a["Cleric"]["armor"][1]) else            2 if name in set(a["Cleric"]["armor"][2]) else      3 if name in set(a["Cleric"]["armor"][3]) else None,
            "Deprived": 1 if name in set(a["Deprived"]["armor"][1]) else        2 if name in set(a["Deprived"]["armor"][2]) else    3 if name in set(a["Deprived"]["armor"][3]) else None,
            "Herald": 1 if name in set(a["Herald"]["armor"][1]) else            2 if name in set(a["Herald"]["armor"][2]) else      3 if name in set(a["Herald"]["armor"][3]) else None,
            "Knight": 1 if name in set(a["Knight"]["armor"][1]) else            2 if name in set(a["Knight"]["armor"][2]) else      3 if name in set(a["Knight"]["armor"][3]) else None,
            "Mercenary": 1 if name in set(a["Mercenary"]["armor"][1]) else      2 if name in set(a["Mercenary"]["armor"][2]) else   3 if name in set(a["Mercenary"]["armor"][3]) else None,
            "Pyromancer": 1 if name in set(a["Pyromancer"]["armor"][1]) else    2 if name in set(a["Pyromancer"]["armor"][2]) else  3 if name in set(a["Pyromancer"]["armor"][3]) else None,
            "Sorcerer": 1 if name in set(a["Sorcerer"]["armor"][1]) else        2 if name in set(a["Sorcerer"]["armor"][2]) else    3 if name in set(a["Sorcerer"]["armor"][3]) else None,
            "Thief": 1 if name in set(a["Thief"]["armor"][1]) else              2 if name in set(a["Thief"]["armor"][2]) else       3 if name in set(a["Thief"]["armor"][3]) else None,
            "Warrior": 1 if name in set(a["Warrior"]["armor"][1]) else          2 if name in set(a["Warrior"]["armor"][2]) else     3 if name in set(a["Warrior"]["armor"][3]) else None
        }


class ArmorUpgrade:
    def __init__(self, name, character=None, block=[], resist=[], dodge=[], damage=[], damageMod=0, dodgeMod=0, dodgeIf2Away=[], twoAttackHealthBonus=0, damageBonusAfterDamaged=0, damageBonusWith4Damage=0, blockMod=0, resistMod=0, healing=0, safetyLimitBonus=0, staminaFromDamage=0, upkeepHealingOption=0, damage3StaminaBonus=0, rerollDefense=False, twoAttackStaminaBonus=0, magicStaminaMod=0, staminaRegenBonus=0) -> None:
        armorUpgrades.append(self)
        armorUpgradesDict[name] = self
        self.character = character
        self.block = block
        self.resist = resist
        self.dodge = dodge
        self.blockMod = blockMod
        self.resistMod = resistMod
        self.staminaRegenBonus = staminaRegenBonus
        self.magicStaminaMod = magicStaminaMod
        self.twoAttackStaminaBonus = twoAttackStaminaBonus
        self.rerollDefense = rerollDefense
        self.upkeepHealingOption = upkeepHealingOption
        self.damage3StaminaBonus = damage3StaminaBonus
        self.damage = damage
        self.damageMod = damageMod
        self.healing = healing
        self.staminaFromDamage = staminaFromDamage
        self.safetyLimitBonus = safetyLimitBonus
        self.damageBonusWith4Damage = damageBonusWith4Damage
        self.damageBonusAfterDamaged = damageBonusAfterDamaged
        self.dodgeMod = dodgeMod
        self.twoAttackHealthBonus = twoAttackHealthBonus
        self.dodgeIf2Away = dodgeIf2Away

Armor(name="Adventurer's Armour", block=[u], resist=[b], dodge=[d], upgradeSlots=2)
Armor(name="Adventurer's Armour (Legendary)", block=[u,u], resist=[o], dodge=[d], upgradeSlots=2)
Armor(name="Alonne Armour", resist=[b], dodge=[d,d], upgradeSlots=2)
Armor(name="Alonne Captain Armour", block=[b,b], resist=[u], dodge=[d], upgradeSlots=1)
Armor(name="Alonne Knight Armour", block=[u], resist=[b], dodge=[d], upgradeSlots=1)
Armor(name="Alva Armour", block=[u], resist=[u], dodge=[d, d], upgradeSlots=1, character="Assassin")
Armor(name="Antiquated Robes", block=[b,b], blockMod=-1, resist=[b,b], resistMod=-1, dodge=[d], upgradeSlots=2)
Armor(name="Armour of Thorns", block=[b,u], resist=[b,b], upgradeSlots=2, thorns=True)
Armor(name="Archdeacon Robe", block=[o], resist=[b, o], upgradeSlots=2, character="Cleric")
Armor(name="Assassin Armour", block=[b], resist=[b], dodge=[d], character="Assassin")
Armor(name="Black Armour", block=[u], resist=[b], dodge=[d], upgradeSlots=2)
Armor(name="Black Hand Armour (common)", block=[b], resist=[b], dodge=[d], upgradeSlots=2)
Armor(name="Black Hand Armour (Thief)", block=[u], resist=[b], dodge=[d], upgradeSlots=2, character="Thief")
Armor(name="Black Iron Armour", block=[o], blockMod=-1, resist=[o], resistMod=-1, upgradeSlots=2, nodeAttackStaminaDiscount=1)
Armor(name="Black Iron Armour (Legendary)", block=[o,o], blockMod=-2, resist=[o,o], resistMod=-2, upgradeSlots=2, nodeAttackStaminaDiscount=1)
Armor(name="Black Leather Armour", block=[b], resist=[b], dodge=[d], upgradeSlots=1, character="Deprived")
Armor(name="Black Knight Armour", block=[u], resist=[u], dodge=[d], upgradeSlots=1)
Armor(name="Black Knight Armour (Legendary)", block=[b,u], resist=[b,u], dodge=[d], upgradeSlots=1)
Armor(name="Brass Armour", block=[b, b], resist=[b, b], upgradeSlots=1, character="Deprived")
Armor(name="Catarina Armour", block=[b,b], resist=[b], upgradeSlots=2)
Armor(name="Catarina Armour (Legendary)", block=[u,u], resist=[u], upgradeSlots=2)
Armor(name="Cathedral Knight Armour", block=[u], resist=[b, b], upgradeSlots=2, character="Herald")
Armor(name="Chester's Set", block=[u], resist=[o], dodge=[d], immunities=set(["bleed"]), upgradeSlots=2)
Armor(name="Cleric Armour", block=[u], resist=[b,u], upgradeSlots=1, healBonus=1)
Armor(name="Cleric Robes", block=[b], resist=[u], character="Cleric")
Armor(name="Cornyx's Robes", block=[u], resist=[o], upgradeSlots=2, character="Pyromancer")
Armor(name="Court Sorcerer Robes", block=[b], resist=[u], dodge=[d], upgradeSlots=2)
Armor(name="Crimson Robes", block=[b], resist=[b,b], dodge=[d], upgradeSlots=1)
Armor(name="Crimson Robes (Legendary)", block=[u], resist=[b,u], dodge=[d,d], upgradeSlots=1)
Armor(name="Dancer Armour", block=[b], resist=[b], dodge=[d,d], walkBonus=1)
Armor(name="Dark Armour", block=[b], resist=[b], dodge=[d], dodgeBonus="hollow", upgradeSlots=2)
Armor(name="Dark Armour (Legendary)", block=[o], resist=[o], dodge=[d], dodgeBonus="hollow", upgradeSlots=2)
Armor(name="Deacon Robes", block=[b], resist=[b,b], dodge=[d], upgradeSlots=1)
Armor(name="Deserter Armour", block=[b], resist=[b], dodge=[d], character="Thief")
Armor(name="Dragonscale Armour", block=[b], resist=[b, u], dodge=[d], upgradeSlots=1, character="Sorcerer")
Armor(name="Dragonslayer Armour", block=[b,u], resist=[b,u], immunities=set(["bleed"]), upgradeSlots=1)
Armor(name="Drang Armour", block=[u], dodge=[d], upgradeSlots=1)
Armor(name="Eastern Armour", block=[b, b], resist=[b, b], dodge=[d, d], upgradeSlots=2, character="Deprived")
Armor(name="Elite Knight Armour", block=[u, u], resist=[b], upgradeSlots=2, character="Knight")
Armor(name="Embraced Armour of Favour", block=[u], resist=[b,b], upgradeSlots=2)
Armor(name="Embraced Armour of Favour (Legendary)", block=[u], resist=[u,u], dodge=[d], upgradeSlots=2)
Armor(name="Exile Armour", block=[u,u], upgradeSlots=2)
Armor(name="Fallen Knight Armour", block=[u], resist=[u], dodge=[d], upgradeSlots=2, character="Warrior")
Armor(name="Faraam Armour", block=[o], resist=[u], upgradeSlots=2, character="Knight")
Armor(name="Firelink Armour", block=[u], resist=[u], upgradeSlots=2)
Armor(name="Gold-Hemmed Black Robes", block=[b], resist=[b,b], dodge=[d], upgradeSlots=1)
Armor(name="Gold-Hemmed Black Robes (Legendary)", block=[u], resist=[u,u], dodge=[d,d], upgradeSlots=1)
Armor(name="Guardian Armour", block=[b,b], resist=[b,b], immunities=set(["bleed"]), upgradeSlots=1)
Armor(name="Guardian Armour (Legendary)", block=[b,b], blockMod=1, resist=[b,b], resistMod=1, immunities=set(["bleed"]), upgradeSlots=1)
Armor(name="Hard Leather Armour", block=[b], resist=[b], dodge=[d,d], upgradeSlots=1)
Armor(name="Havel's Armour", block=[b,u], resist=[b,u], canDodge=False, upgradeSlots=1, canRun=False)
Armor(name="Havel's Armour (Legendary)", block=[b,o], resist=[b,o], canDodge=False, upgradeSlots=1, canRun=False)
Armor(name="Herald Armour", block=[b], resist=[b], dodge=[d], character="Herald")
Armor(name="Hunter Armour", dodge=[d,d], upgradeSlots=2, arcAttackDodgeBonus=1)
Armor(name="Knight Armour", block=[u], resist=[b], character="Knight")
Armor(name="Loincloth", resist=[b], character="Deprived")
Armor(name="Lothric Knight Armour", block=[u], resist=[u], upgradeSlots=2, healthPerEnemyOnNode=1, character="Knight")
Armor(name="Mask of the Child", block=[b], resist=[b], dodge=[d], upgradeSlots=2)
Armor(name="Master's Attire", dodge=[d,d], upgradeSlots=2)
Armor(name="Mirrah Armour", block=[u], resist=[o], dodge=[d], upgradeSlots=1, character="Deprived")
Armor(name="Northern Armour", block=[b], resist=[b], dodge=[d], character="Warrior")
Armor(name="Old Ironclad Armour", block=[b,u], resist=[b,b], upgradeSlots=2)
Armor(name="Outrider Armour", block=[b,b], resist=[b], upgradeSlots=2)
Armor(name="Painting Guardian Armour", dodge=[d,d], upgradeSlots=1)
Armor(name="Paladin Armour", block=[o], resist=[o], upgradeSlots=1)
Armor(name="Pyromancer Garb", resist=[b, b], dodge=[d], character="Pyromancer")
Armor(name="Royal Swordsman Armour", block=[b,b], resist=[u], upgradeSlots=1, highestOneHandedStaminaDiscount=1)
Armor(name="Sellsword Armour", block=[b], resist=[b], dodge=[d], character="Mercenary")
Armor(name="Shadow Armour", dodge=[d, d], upgradeSlots=2, character="Assassin")
Armor(name="Silver Knight Armour", block=[b,u], dodge=[d], upgradeSlots=2)
Armor(name="Smelter Demon Armour", block=[u,u], resist=[o], upgradeSlots=2)
Armor(name="Smough's Armour", block=[u,u], resist=[u,u], canDodge=False, canRun=False)
Armor(name="Sorcerer Robes", block=[b], resist=[u], character="Sorcerer")
Armor(name="Steel Armour", block=[u], resist=[u], upgradeSlots=1)
Armor(name="Stone Knight Armour", block=[o], resist=[u])
Armor(name="Sunless Armour", block=[u], resist=[b], upgradeSlots=2)
Armor(name="Sunset Armour", block=[b,b], resist=[b], dodge=[d], upgradeSlots=2)
Armor(name="Winged Knight Armour", block=[o], resist=[o], upgradeSlots=2)
Armor(name="Worker Armour", block=[b], resist=[b], dodge=[d], upgradeSlots=2)
Armor(name="Xanthous Robes", block=[b], resist=[u], dodge=[d], upgradeSlots=1, magicStaminaMod=-1)

ArmorUpgrade(name="Blue Tearstone Ring", character="Knight", staminaFromDamage=1)
ArmorUpgrade(name="Calamity Ring", damageMod=1, blockMod=-1, resistMod=-1, dodgeMod=-1)
ArmorUpgrade(name="Carthus Milkring", character="Deprived", dodge=[d])
ArmorUpgrade(name="Chloranthy Ring", staminaRegenBonus=1)
ArmorUpgrade(name="Dusk Crown Ring", magicStaminaMod=-2)
ArmorUpgrade(name="Hornet Ring", character="Assassin", damage=[o], damageMod=-2)
ArmorUpgrade(name="Knight Slayer's Ring", character="Warrior", damage3StaminaBonus=1)
ArmorUpgrade(name="Life Ring", safetyLimitBonus=1)
ArmorUpgrade(name="Magic Stoneplate Ring", character="Cleric", resist=[b])
ArmorUpgrade(name="Obscuring Ring", character="Thief", dodgeIf2Away=[d,d])
ArmorUpgrade(name="Old Leo Ring", damageBonusAfterDamaged=1)
ArmorUpgrade(name="Pontiff's Left Eye", twoAttackHealthBonus=1)
ArmorUpgrade(name="Red Tearstone Ring", damageBonusWith4Damage=1)
ArmorUpgrade(name="Ring of Favour", character="Mercenary", twoAttackStaminaBonus=1)
ArmorUpgrade(name="Sun Princess Ring", character="Knight", healing=1)
ArmorUpgrade(name="Tiny Being's Ring", character="Herald", upkeepHealingOption=2)
ArmorUpgrade(name="Wolf Ring", character="Mercenary", rerollDefense=True)
