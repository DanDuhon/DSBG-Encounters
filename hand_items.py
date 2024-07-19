from treasure_item_tiers import a
from statistics import mean


handItems = []
handItemsDict = {}
handItemUpgrades = []
handItemUpgradesDict = {}

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

reachMod = {
    1: 0.44970414201183434,
    2: 0.8224852071005917,
    3: 0.9763313609467456,
    4: 1
}


class HandItem:
    def __init__(self, name, block=[], resist=[], dodge=[], attacks=[], magicDamageBonus=[], magicStaminaCost=0, healthDuringUpkeep=0, boss=True, upgradeSlots=0, blockMod=0, resistMod=0, twoHanded=False, canUseWithTwoHanded=False, canDodge=True, immunities=set()) -> None:
        handItems.append(self)
        handItemsDict[name] = self
        self.name = name
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
        self.attacks = attacks
        self.healthDuringUpkeep = healthDuringUpkeep
        self.boss = boss
        self.magicDamageBonus = magicDamageBonus
        self.magicStaminaCost = magicStaminaCost
        self.tier = {
            "Assassin":     1 if name == "None1" or name in set(a["Assassin"]["weapon"][1]) else       2 if name == "None2" or name in set(a["Assassin"]["weapon"][2]) else    3 if name in set(a["Assassin"]["weapon"][3]) else None,
            "Cleric":       1 if name == "None1" or name in set(a["Cleric"]["weapon"][1]) else         2 if name == "None2" or name in set(a["Cleric"]["weapon"][2]) else      3 if name in set(a["Cleric"]["weapon"][3]) else None,
            "Deprived":     1 if name == "None1" or name in set(a["Deprived"]["weapon"][1]) else       2 if name == "None2" or name in set(a["Deprived"]["weapon"][2]) else    3 if name in set(a["Deprived"]["weapon"][3]) else None,
            "Herald":       1 if name == "None1" or name in set(a["Herald"]["weapon"][1]) else         2 if name == "None2" or name in set(a["Herald"]["weapon"][2]) else      3 if name in set(a["Herald"]["weapon"][3]) else None,
            "Knight":       1 if name == "None1" or name in set(a["Knight"]["weapon"][1]) else         2 if name == "None2" or name in set(a["Knight"]["weapon"][2]) else      3 if name in set(a["Knight"]["weapon"][3]) else None,
            "Mercenary":    1 if name == "None1" or name in set(a["Mercenary"]["weapon"][1]) else      2 if name == "None2" or name in set(a["Mercenary"]["weapon"][2]) else   3 if name in set(a["Mercenary"]["weapon"][3]) else None,
            "Pyromancer":   1 if name == "None1" or name in set(a["Pyromancer"]["weapon"][1]) else     2 if name == "None2" or name in set(a["Pyromancer"]["weapon"][2]) else  3 if name in set(a["Pyromancer"]["weapon"][3]) else None,
            "Sorcerer":     1 if name == "None1" or name in set(a["Sorcerer"]["weapon"][1]) else       2 if name == "None2" or name in set(a["Sorcerer"]["weapon"][2]) else    3 if name in set(a["Sorcerer"]["weapon"][3]) else None,
            "Thief":        1 if name == "None1" or name in set(a["Thief"]["weapon"][1]) else          2 if name == "None2" or name in set(a["Thief"]["weapon"][2]) else       3 if name in set(a["Thief"]["weapon"][3]) else None,
            "Warrior":      1 if name == "None1" or name in set(a["Warrior"]["weapon"][1]) else        2 if name == "None2" or name in set(a["Warrior"]["weapon"][2]) else     3 if name in set(a["Warrior"]["weapon"][3]) else None
        }


class HandItemUpgrade:
    def __init__(self, name, damage=[], damageMod=0, bleed=False, highestStaminaMod=0, staminaCostMod=0, magic=False, range0GetRange1=False, poison=False, highestStaminaModIfBoss=0) -> None:
        handItemUpgrades.append(self)
        handItemUpgradesDict[name] = self
        self.name = name
        self.damage = damage
        self.bleed = bleed
        self.highestStaminaModIfBoss = highestStaminaModIfBoss
        self.damageMod = damageMod
        self.magic = magic
        self.poison = poison
        self.range0GetRange1 = range0GetRange1
        self.staminaCostMod = staminaCostMod
        self.highestStaminaMod = highestStaminaMod


class Attack:
    def __init__(self, staminaCost=0, damage=[[]], damageMod=0, staminaRecovery=0, block=[], resist=[], heal=0, attacksAreMagic=False, attacksMagicDamageBonus=0, shiftAfterAttack=0, attackRange=0, magic=False, bleed=False, poison=False, ignoreDefense=False, damageBonus=set(), noRange0=False) -> None:
        # Uses reachMod to calculate the odds of stamina cost to get into range (1 stamina, 2 stamina, 3 stamina).
        self.staminaCost = staminaCost + (0 if not damage[0] and (staminaRecovery or heal) else (1 - reachMod[min([4, attackRange + 1])]) + (1 - reachMod[min([4, attackRange + 2])]) + (1 - reachMod[min([4, attackRange + 3])]))
        self.attackRange = attackRange
        self.damage = damage
        self.damageMod = damageMod
        self.magic = magic
        self.bleed = bleed
        self.poison = poison
        self.ignoreDefense = ignoreDefense
        self.damageBonus = damageBonus
        self.noRange0 = noRange0
        self.staminaRecovery = staminaRecovery
        self.heal = heal
        self.block = block
        self.resist = resist
        self.attacksAreMagic = attacksAreMagic
        self.attacksMagicDamageBonus = attacksMagicDamageBonus
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


HandItem(name="None1", canUseWithTwoHanded=True)
HandItem(name="None2", canUseWithTwoHanded=True)
HandItem(name="Abyss Greatsword", twoHanded=True, block=[b], resist=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b,b]], staminaCost=1), Attack(damage=[[u,u,u]], staminaCost=4)])
HandItem(name="Aged Smelter Sword", twoHanded=True, block=[b], resist=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,b,b,u]], magic=True, staminaCost=2, attackRange=1), Attack(damage=[[u,o,o]], magic=True, staminaCost=5, attackRange=1)])
HandItem(name="Alonne Greatbow", twoHanded=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b,b]], staminaCost=2, attackRange=3, noRange0=True), Attack(damage=[[b,b,u]], staminaCost=4, attackRange=3, noRange0=True)])
HandItem(name="Avelyn", twoHanded=True, dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u],[u],[u]], staminaCost=1, attackRange=3, noRange0=True), Attack(damage=[[o],[o],[o]], staminaCost=4, attackRange=3, noRange0=True)])
HandItem(name="Balder Side Sword", resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=0), Attack(damage=[[o,o]], staminaCost=4, attackRange=1)])
HandItem(name="Bandit Knife", attacks=[Attack(damage=[[b]], staminaCost=0), Attack(damage=[[b,b]], staminaCost=3)])
HandItem(name="Battle Axe", attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,b]], staminaCost=2)])
HandItem(name="Bewitched Alonne Sword", twoHanded=True, boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,b,u]], staminaCost=3), Attack(damage=[[b,b,u,u]], staminaCost=0)])
HandItem(name="Black Bow of Pharis", twoHanded=True, dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u]], staminaCost=0, attackRange=4, noRange0=True), Attack(damage=[[b,u]], staminaCost=2, attackRange=4, noRange0=True), Attack(damage=[[b,u]], staminaCost=4, attackRange=4, noRange0=True)])
HandItem(name="Black Firebombs", attacks=[Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=1)])
HandItem(name="Black Iron Greatshield", block=[u], resist=[u, u])
HandItem(name="Black Knight Greataxe", twoHanded=True, block=[b], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=1), Attack(damage=[[u,u]], staminaCost=4), Attack(damage=[[u,u]], staminaCost=4)])
HandItem(name="Black Knight Shield (Deprived)", block=[b], dodge=[d], upgradeSlots=2, attacks=[Attack(damage=[[u]], staminaCost=2), Attack(damage=[[o]], staminaCost=4)])
HandItem(name="Black Knight Shield (Black Knight)", block=[u], resist=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=2)])
HandItem(name="Black Knight Halberd", twoHanded=True, block=[b], resist=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,b,b]], staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[b,b,u]], staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Black Knight Sword", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[u,u,b]], staminaCost=4)])
HandItem(name="Blacksteel Katana", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=1, attackRange=1), Attack(damage=[[b,b,b]], staminaCost=3, attackRange=1)])
HandItem(name="Blinding Bolt", attacks=[Attack(damage=[[u],[u],[u],[u],[u]], magic=True, staminaCost=2, attackRange=1)])
HandItem(name="Bloodshield", block=[u], resist=[b], immunities=set(["bleed", "poison"]), attacks=[Attack(damage=[[b,b]], staminaCost=1)])
HandItem(name="Blue Wooden Shield", block=[b])
HandItem(name="Bonewheel Shield", block=[u], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=1), Attack(damage=[[b,b],[b,b],[b,b],[b,b]], staminaCost=5)])
HandItem(name="Bountiful Light", attacks=[Attack(attackRange=1, staminaCost=4, heal=2)])
HandItem(name="Bountiful Sunlight", attacks=[Attack(attackRange=3, staminaRecovery=6)])
HandItem(name="Brigand Axe", resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,u]], staminaCost=3)])
HandItem(name="Broadsword", block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,u]], staminaCost=2, attackRange=1), Attack(damage=[[u,u]], staminaCost=4, attackRange=1)])
HandItem(name="Broken Straight Sword", upgradeSlots=2, attacks=[Attack(damage=[[b,b,b]], damageMod=-2, staminaCost=0), Attack(damage=[[u,u,u]], damageMod=-2, staminaCost=3)])
HandItem(name="Buckler", canUseWithTwoHanded=True, block=[b], dodge=[d])
HandItem(name="Butcher Knife", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=1, attackRange=1, heal=1), Attack(damage=[[u,u]], staminaCost=4, attackRange=1, heal=1)])
HandItem(name="Caduceus Round Shield", block=[u], attacks=[])
HandItem(name="Caestus", attacks=[Attack(damage=[[b, b]], staminaCost=0)], canUseWithTwoHanded=True)
HandItem(name="Carthus Curved Greatsword", twoHanded=True, dodge=[d], upgradeSlots=2, attacks=[Attack(damage=[[b,b]], bleed=True, staminaCost=0), Attack(damage=[[b,b,b]], bleed=True, staminaCost=3)])
HandItem(name="Carthus Curved Sword", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], damageMod=-1, staminaCost=1), Attack(damage=[[u,u,u]], damageMod=-1, staminaCost=3)])
HandItem(name="Chariot Lance", block=[b], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[o]], bleed=True, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[u,o]], bleed=True, staminaCost=3, attackRange=1, noRange0=True)])
HandItem(name="Claws", twoHanded=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b],[b,b]], staminaCost=2), Attack(damage=[[u,u],[u,u]], staminaCost=4)])
HandItem(name="Claymore", twoHanded=True, block=[b], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], damageMod=1, staminaCost=1, attackRange=1), Attack(damage=[[o,o]], damageMod=1, staminaCost=4, attackRange=1)])
HandItem(name="Cleric's Candlestick", upgradeSlots=1, attacks=[Attack(damage=[[b,u]], magic=True, staminaCost=1), Attack(damage=[[b,b,u]], magic=True, staminaCost=4)])
HandItem(name="Club", attacks=[Attack(damage=[[b]], staminaCost=0), Attack(damage=[[b,b]], staminaCost=3)])
HandItem(name="Composite Bow", twoHanded=True, dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageMod=-1, staminaCost=0, attackRange=4, noRange0=True), Attack(damage=[[b,b,b]], damageMod=-1, staminaCost=3, attackRange=4, noRange0=True)])
HandItem(name="Crescent Axe", upgradeSlots=2, attacks=[Attack(damage=[[u]], staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[u,u]], damageMod=1, staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Crescent Moon Sword", upgradeSlots=2, attacks=[Attack(damage=[[u]], magic=True, staminaCost=0), Attack(damage=[[u]], magic=True, staminaCost=3, attackRange=3)])
HandItem(name="Crest Shield", block=[b], dodge=[d])
HandItem(name="Crystal Hail", attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0, attackRange=4), Attack(damage=[[b,b]], magic=True, staminaCost=5)])
HandItem(name="Crystal Shield", block=[b], immunities=set(["bleed", "poison"]), attacks=[Attack(damage=[[b,b,b]], staminaCost=3)])
HandItem(name="Crystal Straight Sword", upgradeSlots=1, attacks=[Attack(damage=[[u]], damageMod=1, staminaCost=0), Attack(damage=[[b,u]], damageMod=1, staminaCost=3)])
HandItem(name="Cursed Greatsword of Artorias", twoHanded=True, block=[b], resist=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u,b]], staminaCost=0), Attack(damage=[[u,o]], staminaCost=4)])
HandItem(name="Dancer's Enchanted Swords", twoHanded=True, dodge=[d], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[u], [u]], magic=True, staminaCost=2, attackRange=1), Attack(damage=[[b,u], [b,u]], magic=True, staminaCost=4, attackRange=1)])
HandItem(name="Dark Silver Tracer", boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u,u]], damageMod=-1, staminaCost=0), Attack(damage=[[u,u]], damageMod=-1, poison=True, staminaCost=3)])
HandItem(name="Dark Sword", upgradeSlots=2, attacks=[Attack(damage=[[u]], staminaCost=0), Attack(damage=[[u,u]], staminaCost=2), Attack(damage=[[o,o]], staminaCost=5, attackRange=1)])
HandItem(name="Demon's Great Hammer", twoHanded=True, boss=True, upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=1, attackRange=1), Attack(damage=[[o,o]], staminaCost=4, attackRange=1)])
HandItem(name="Dragon Crest Shield", block=[u], resist=[u])
HandItem(name="Dragon King Greataxe", twoHanded=True, block=[b], resist=[o], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[o,o]], staminaCost=1), Attack(damage=[[o]], magic=True, staminaCost=5, attackRange=1)])
HandItem(name="Dragon Tooth", twoHanded=True, block=[b], resist=[u], upgradeSlots=1, attacks=[Attack(damage=[[u,o,o]], staminaCost=4, attackRange=1), Attack(damage=[[u,o,o]], staminaCost=6, attackRange=1)])
HandItem(name="Dragonrider Bow", twoHanded=True, dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[o]], staminaCost=1, attackRange=3, noRange0=True), Attack(damage=[[o]], ignoreDefense=True, staminaCost=4)])
HandItem(name="Dragonslayer Greatbow", twoHanded=True, upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=2, attackRange=3, noRange0=True), Attack(damage=[[u,o]], staminaCost=4, attackRange=3, noRange0=True)])
HandItem(name="Dragonslayer Spear", boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,u]], magic=True, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b,u,u]], magic=True, staminaCost=4, attackRange=1, noRange0=True), Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=4, noRange0=True)])
HandItem(name="Dragonslayer's Axe", resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[o]], magic=True, staminaCost=0), Attack(damage=[[u,o]], magic=True, staminaCost=3, attackRange=1)])
HandItem(name="Drake Sword", attacks=[Attack(damage=[[u,u]], staminaCost=2), Attack(damage=[[o,o]], staminaCost=4), Attack(damage=[[u,u]], staminaCost=4, attackRange=3)])
HandItem(name="Drakewing Ultra Greatsword", twoHanded=True, dodge=[d], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u,o]], staminaCost=2, attackRange=1), Attack(damage=[[o,o]], staminaCost=5, attackRange=3)])
HandItem(name="Drang Hammers", twoHanded=True, resist=[b], dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], damageMod=1, staminaCost=0), Attack(damage=[[u,u], [u,u]], staminaCost=3), Attack(damage=[[u,u], [u,u]], damageMod=1, staminaCost=5)])
HandItem(name="Dung Pie", attacks=[Attack(poison=True, staminaCost=0, attackRange=1)])
HandItem(name="East-West Shield", block=[b], resist=[u], dodge=[d])
HandItem(name="Eastern Iron Shield", block=[u], dodge=[d])
HandItem(name="Effigy Shield", canUseWithTwoHanded=True, block=[b], resist=[b])
HandItem(name="Elkhorn Round Shield", canUseWithTwoHanded=True, block=[b], resist=[b, b], dodge=[d])
HandItem(name="Estoc", attacks=[Attack(damage=[[b,b]], damageMod=-1, staminaCost=0), Attack(damage=[[b,b,b]], damageMod=-1, staminaCost=3)])
HandItem(name="Exile Greatsword", twoHanded=True, block=[b], resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[u,b]], staminaCost=2), Attack(damage=[[u,b]], staminaCost=4), Attack(damage=[[u,o]], staminaCost=5)])
HandItem(name="Falchion", block=[b], resist=[u], upgradeSlots=2, attacks=[Attack(damage=[[u,u]], staminaCost=0), Attack(damage=[[o,o]], staminaCost=3)])
HandItem(name="Fire Surge", attacks=[Attack(damage=[[u]], magic=True, staminaCost=0, attackRange=2), Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=2)])
HandItem(name="Fire Whip", attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0), Attack(damage=[[o,o]], magic=True, staminaCost=4)])
HandItem(name="Fireball", attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0, attackRange=2), Attack(damage=[[o,o]], magic=True, staminaCost=5, attackRange=2)])
HandItem(name="Firebombs", attacks=[Attack(damage=[[b,b,b]], magic=True, staminaCost=4, attackRange=1)])
HandItem(name="Flamberge", twoHanded=True, dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[o]], bleed=True, staminaCost=2), Attack(damage=[[u,u]], bleed=True, staminaCost=4)])
HandItem(name="Force")
HandItem(name="Four Kings Sword", block=[b], resist=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[o]], staminaCost=0), Attack(damage=[[u,u]], magic=True, staminaCost=3)])
HandItem(name="Four-Pronged Plow", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u]], staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[u,u]], staminaCost=3, attackRange=1, noRange0=True)])
HandItem(name="Fume Ultra Greatsword", twoHanded=True, block=[u], resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[u,o]], staminaCost=2, attackRange=1), Attack(damage=[[u,u,o]], staminaCost=5, attackRange=1), Attack(damage=[[u,o]], staminaCost=4, attackRange=1)])
HandItem(name="Gargoyle Tail Axe", twoHanded=True, resist=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=1), Attack(damage=[[u,u,u]], staminaCost=4)])
HandItem(name="Gargoyle's Halberd", twoHanded=True, block=[b], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[o]], staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[o,o]], staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Gargoyle's Shield", block=[b], resist=[u,u])
HandItem(name="Giant Stone Axe", twoHanded=True, block=[u], resist=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,u]], staminaCost=1, attackRange=1), Attack(damage=[[u,o]], staminaCost=4, attackRange=1)])
HandItem(name="Giant's Halberd", twoHanded=True, block=[u], upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[b,o]], staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Gold Tracer", boss=True, upgradeSlots=2, attacks=[Attack(damage=[[o,o]], damageMod=-1, staminaCost=0), Attack(damage=[[o,o]], damageMod=-1, bleed=True, staminaCost=3)])
HandItem(name="Golden Ritual Spear", resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[u,u]], magic=True, staminaCost=3, attackRange=1, noRange0=True), Attack(damage=[[u,u]], magic=True, staminaCost=5, attackRange=3, noRange0=True)])
HandItem(name="Golden Wing Crest Shield", block=[u], resist=[u], upgradeSlots=1, attacks=[Attack(damage=[[b]], staminaCost=0)])
HandItem(name="Gotthard Twinswords", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b], [b,b]], staminaCost=1), Attack(damage=[[u,u], [u,u]], staminaCost=4), Attack(damage=[[u,u]], staminaCost=3, attackRange=1)])
HandItem(name="Grass Crest Shield", block=[u], resist=[o])
HandItem(name="Gravelord Sword", twoHanded=True, block=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,u]], poison=True, staminaCost=2), Attack(damage=[[b,o]], poison=True, staminaCost=4)])
HandItem(name="Gravelord Sword Dance", attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=1, attackRange=3), Attack(damage=[[u,u]], magic=True, staminaCost=3, attackRange=3)])
HandItem(name="Greataxe", twoHanded=True, block=[u], upgradeSlots=2, attacks=[Attack(damage=[[u,u]], staminaCost=0), Attack(damage=[[o,o]], staminaCost=3), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Great Chaos Fireball", attacks=[Attack(damage=[[o]], magic=True, staminaCost=1, attackRange=2), Attack(damage=[[u,u,u]], magic=True, staminaCost=4, attackRange=2)])
HandItem(name="Great Club", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[o]], staminaCost=0, attackRange=1), Attack(damage=[[o,o]], staminaCost=3, attackRange=1)])
HandItem(name="Great Combustion", attacks=[Attack(damage=[[u]], magic=True, staminaCost=1, attackRange=2), Attack(damage=[[o]], magic=True, staminaCost=3, attackRange=2)])
HandItem(name="Great Heal", attacks=[Attack(heal=6, staminaCost=2), Attack(staminaCost=4, heal=6)])
HandItem(name="Great Mace", twoHanded=True, block=[b], resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[u]], damageMod=1, staminaCost=0), Attack(damage=[[u,u]], damageMod=1, staminaCost=3)])
HandItem(name="Great Machete", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u,u,u]], staminaCost=1), Attack(damage=[[b,b,o,o]], staminaCost=4), Attack(damage=[[u,u,u]], staminaCost=4)])
HandItem(name="Great Magic Weapon", attacks=[Attack(attacksAreMagic=True), Attack(attacksAreMagic=True, attacksMagicDamageBonus=1, staminaCost=2)])
HandItem(name="Great Scythe", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b,b]], damageMod=-1, staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[o,o]], damageMod=-1, staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Great Wooden Hammer", twoHanded=True, block=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b,b]], staminaCost=0), Attack(damage=[[b,b,b]], staminaCost=3)])
HandItem(name="Greatshield of Artorias", block=[o], resist=[u], immunities=set(["bleed", "poison"]))
HandItem(name="Greatsword", twoHanded=True, block=[b], resist=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=1), Attack(damage=[[b,o]], staminaCost=4)])
HandItem(name="Greatsword of Artorias", twoHanded=True, block=[u], resist=[o], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u,b]], magic=True, staminaCost=0), Attack(damage=[[u,o]], magic=True, staminaCost=4)])
HandItem(name="Halberd", twoHanded=True, block=[u], upgradeSlots=2, attacks=[Attack(damage=[[u]], damageMod=1, staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[u,u]], damageMod=1, staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Hand Axe", attacks=[Attack(damage=[[b]], staminaCost=0), Attack(damage=[[b,b]], staminaCost=3)])
HandItem(name="Havel's Greatshield", block=[o,b], resist=[u], attacks=[Attack(staminaCost=2, block=[b])])
HandItem(name="Hawkwood's Shield", canUseWithTwoHanded=True, block=[u], resist=[u], dodge=[d])
HandItem(name="Heal", attacks=[Attack(attackRange=3, staminaRecovery=1, heal=1), Attack(attackRange=3, staminaCost=3, heal=4)])
HandItem(name="Heal Aid", attacks=[Attack(attackRange=3, staminaRecovery=1, heal=1)])
HandItem(name="Hollow Soldier Shield", block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageBonus={"hollow",}, staminaCost=2)])
HandItem(name="Homing Crystal Soulmass", attacks=[Attack(damage=[[o],[o],[o],[o],[o]], magic=True, staminaCost=5, attackRange=3)])
HandItem(name="Immolation Tinder", twoHanded=True, resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[u]], magic=True, staminaCost=0, attackRange=1), Attack(damage=[[b,b]], magic=True, staminaCost=2, attackRange=1), Attack(damage=[[b,b]], magic=True, staminaCost=4, attackRange=3)])
HandItem(name="Irithyll Rapier", block=[b], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,u]], staminaCost=2)])
HandItem(name="Irithyll Straight Sword", boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageMod=1, staminaCost=0), Attack(damage=[[b,b,u]], staminaCost=3)])
HandItem(name="Iron King Hammer", block=[b], resist=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[o]], magic=True, staminaCost=2), Attack(damage=[[b,u],[b,u]], staminaCost=4, attackRange=1)])
HandItem(name="Iron Round Shield", canUseWithTwoHanded=True, dodge=[d])
HandItem(name="Kite Shield", block=[b])
HandItem(name="Kukris", attacks=[Attack(attackRange=1, bleed=True)])
HandItem(name="Large Leather Shield", block=[u], resist=[b], dodge=[d])
HandItem(name="Leather Shield", resist=[b], dodge=[d])
HandItem(name="Lifehunt Scythe", twoHanded=True, block=[u], resist=[b], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u,u]], damageMod=-1, bleed=True, staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[o,o]], damageMod=-1, bleed=True, staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Long Sword", attacks=[Attack(damage=[[u]], staminaCost=0), Attack(damage=[[b,u]], staminaCost=4)])
HandItem(name="Longbow", twoHanded=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0, attackRange=4, noRange0=True), Attack(damage=[[b,b,b]], staminaCost=3, attackRange=4, noRange0=True)])
HandItem(name="Lothric Knight Greatsword", twoHanded=True, block=[b], upgradeSlots=2, attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0, attackRange=1), Attack(damage=[[b,b,b]], magic=True, staminaCost=3, attackRange=1)])
HandItem(name="Lothric's Holy Sword", resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u]], magic=True, staminaCost=1, staminaRecovery=1), Attack(damage=[[b,u]], magic=True, staminaCost=3, staminaRecovery=1)])
HandItem(name="Lucerne", twoHanded=True, block=[b], resist=[b], dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b,b,u]], damageMod=-1, staminaCost=1), Attack(damage=[[b,b,b,u]], damageMod=-1, staminaCost=4)])
HandItem(name="Mace", resist=[b], attacks=[Attack(damage=[[u]], staminaCost=0), Attack(damage=[[b,b]], staminaCost=2)])
HandItem(name="Magic Barrier", resist=[u])
HandItem(name="Magic Shield", block=[b], resist=[o])
HandItem(name="Mail Breaker", attacks=[Attack(damage=[[b]], staminaCost=0), Attack(damage=[[u]], staminaCost=2)])
HandItem(name="Man Serpent Hatchet", upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=0), Attack(damage=[[b,u]], ignoreDefense=True, staminaCost=3)])
HandItem(name="Mannikin Claws", twoHanded=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b], [b,b]], staminaCost=2, attackRange=1), Attack(damage=[[u,u], [u,u]], staminaCost=4, attackRange=1)])
HandItem(name="Manus Catalyst", resist=[b], boss=True, upgradeSlots=2, magicDamageBonus=[b], magicStaminaCost=1, attacks=[Attack(damage=[[u,u]], staminaCost=1), Attack(damage=[[o,o]], staminaCost=4)])
HandItem(name="Med Heal", attacks=[Attack(heal=2), Attack(staminaCost=3, heal=2)])
HandItem(name="Melinda's Greataxe", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[o,o]], staminaCost=2), Attack(damage=[[o,o]], staminaCost=4)])
HandItem(name="Moonlight Greatsword", twoHanded=True, block=[b], upgradeSlots=2, attacks=[Attack(damage=[[b,u]], magic=True, staminaCost=0), Attack(damage=[[u,u,u]], magic=True, staminaCost=3), Attack(damage=[[u,u,u]], magic=True, staminaCost=4, attackRange=3)])
HandItem(name="Morion Blade", upgradeSlots=2, attacks=[Attack(damage=[[b]], bleed=True, staminaCost=0), Attack(damage=[[b,b]], bleed=True, staminaCost=3)])
HandItem(name="Morne's Great Hammer", twoHanded=True, block=[b, b], resist=[b, b], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=2), Attack(damage=[[u,o]], staminaCost=4), Attack(damage=[[o,o]], staminaCost=6)])
HandItem(name="Morning Star", resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u]], staminaCost=0), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Murakamo", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b]], staminaCost=0), Attack(damage=[[b,b,b]], staminaCost=3)])
HandItem(name="Notched Whip", upgradeSlots=2, attacks=[Attack(damage=[[u]], bleed=True, staminaCost=0, attackRange=1), Attack(damage=[[o]], bleed=True, staminaCost=3, attackRange=1)])
HandItem(name="Obsidian Greatsword", twoHanded=True, block=[u], resist=[u], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[o,o]], staminaCost=1), Attack(damage=[[u,u]], magic=True, staminaCost=5, attackRange=1)])
HandItem(name="Old Dragonslayer Spear", boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b,b,b]], magic=True, staminaCost=3, attackRange=1, noRange0=True), Attack(damage=[[b,b]], magic=True, staminaCost=3, attackRange=3, noRange0=True)])
HandItem(name="Onikiri and Ubadachi", twoHanded=True, dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u], [u]], staminaCost=0), Attack(damage=[[u,u], [u,u]], staminaCost=3), Attack(damage=[[o,o]], staminaCost=4, attackRange=1)])
HandItem(name="Painting Guardian's Curved Sword", upgradeSlots=2, attacks=[Attack(damage=[[b,b]], bleed=True, staminaCost=0, attackRange=1), Attack(damage=[[b,b,b]], bleed=True, staminaCost=3, attackRange=1)])
HandItem(name="Parrying Dagger", block=[b], dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageMod=-1, staminaCost=0), Attack(damage=[[b,b]], staminaCost=2)])
HandItem(name="Partizan", twoHanded=True, block=[u], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[u,u,o]], staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Phoenix Parma Shield", canUseWithTwoHanded=True, resist=[b], dodge=[d])
HandItem(name="Pierce Shield", block=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=2)])
HandItem(name="Pike", twoHanded=True, block=[b], upgradeSlots=2, attacks=[Attack(damage=[[b]], damageMod=1, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b,b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True), Attack(damage=[[b,b,b]], damageMod=1, staminaCost=5, attackRange=2, noRange0=True)])
HandItem(name="Poison Mist", attacks=[Attack(poison=True, staminaCost=1, attackRange=1), Attack(poison=True, staminaCost=3, attackRange=1)])
HandItem(name="Poison Throwing Knives", attacks=[Attack(damage=[[b,b]], poison=True, staminaCost=3, attackRange=1)])
HandItem(name="Porcine Shield", block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u]], staminaCost=1)])
HandItem(name="Priscilla's Dagger", dodge=[d], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[]], bleed=True, staminaCost=0), Attack(damage=[[o]], bleed=True, staminaCost=3, attackRange=1)])
HandItem(name="Pursuer's Greatshield", block=[b,o])
HandItem(name="Pursuer's Ultra Greatsword", twoHanded=True, block=[b], resist=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u,u]], staminaCost=2, attackRange=1), Attack(damage=[[u,u,o]], staminaCost=5, attackRange=1)])
HandItem(name="Pursuers", attacks=[Attack(damage=[[b,b],[b,b],[b,b],[b,b],[b,b]], magic=True, staminaCost=5, attackRange=2)])
HandItem(name="Pyromancy Flame", attacks=[Attack(damage=[[b]], magic=True, staminaCost=0, attackRange=2), Attack(damage=[[b,b]], magic=True, staminaCost=4, attackRange=2)])
HandItem(name="Rapier", block=[b], upgradeSlots=1, attacks=[Attack(damage=[[b]], damageMod=1, staminaCost=0), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Red and White Round Shield", canUseWithTwoHanded=True, block=[b], resist=[b,b])
HandItem(name="Reinforced Club", upgradeSlots=2, attacks=[Attack(damage=[[u]], staminaCost=0), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Replenishment", attacks=[Attack(attackRange=1, staminaRecovery=1), Attack(attackRange=1, staminaCost=2, heal=1)])
HandItem(name="Rotten Ghru Dagger", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageMod=-1, poison=True, staminaCost=0), Attack(damage=[[b,b,b]], damageMod=-1, poison=True, staminaCost=3)])
HandItem(name="Rotten Ghru Spear", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageMod=-1, poison=True, staminaCost=0, attackRange=1), Attack(damage=[[b,b]], poison=True, staminaCost=3, attackRange=1)])
HandItem(name="Round Shield", block=[b])
HandItem(name="Royal Dirk", block=[b], resist=[b], dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u]], staminaCost=0), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Sacred Chime", attacks=[Attack(attackRange=2, heal=1), Attack(attackRange=2, heal=3, staminaCost=3)])
HandItem(name="Sacred Oath", block=[u])
HandItem(name="Saint Bident", block=[b], resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[u,u]], staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b,u,u]], staminaCost=3, attackRange=1, noRange0=True)])
HandItem(name="Sanctus", block=[u], resist=[b,b], healthDuringUpkeep=1)
HandItem(name="Santier's Spear", twoHanded=True, upgradeSlots=1, attacks=[Attack(damage=[[u,u]], damageMod=1, staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[u,u]], staminaCost=3, attackRange=1), Attack(damage=[[u,u,u]], staminaCost=4)])
HandItem(name="Scimitar", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[o,o]], damageMod=-1, staminaCost=3)])
HandItem(name="Sellsword Twinblades", twoHanded=True, attacks=[Attack(damage=[[b], [b]], staminaCost=0), Attack(damage=[[b,b], [b,b]], staminaCost=2)])
HandItem(name="Shield Crossbow", twoHanded=True, block=[u], resist=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,b]], staminaCost=0, attackRange=3, noRange0=True), Attack(damage=[[u,u]], staminaCost=4, attackRange=3, noRange0=True)])
HandItem(name="Shortbow", twoHanded=True, attacks=[Attack(damage=[[u]], staminaCost=0, attackRange=3, noRange0=True), Attack(damage=[[b,b]], staminaCost=3, attackRange=3, noRange0=True)])
HandItem(name="Shortsword", upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,b,b]], staminaCost=2)])
HandItem(name="Shotel", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b]], staminaCost=0), Attack(damage=[[b]], ignoreDefense=True, staminaCost=2), Attack(damage=[[u]], ignoreDefense=True, staminaCost=4)])
HandItem(name="Silver Eagle Kite Shield", block=[u])
HandItem(name="Silver Knight Shield", block=[u], upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=1), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Silver Knight Spear", resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[u]], damageMod=1, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b,b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)])
HandItem(name="Silver Knight Straight Sword", dodge=[d], upgradeSlots=2, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,u]], staminaCost=3)])
HandItem(name="Skull Lantern", dodge=[d], attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=3)])
HandItem(name="Small Leather Shield", canUseWithTwoHanded=True, block=[b], resist=[b], dodge=[d])
HandItem(name="Smelter Sword", twoHanded=True, block=[b], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[b,b,b]], staminaCost=2, attackRange=1), Attack(damage=[[o,o]], staminaCost=5, attackRange=1)])
HandItem(name="Smough's Hammer", twoHanded=True, boss=True, upgradeSlots=1, attacks=[Attack(damage=[[u,o]], staminaCost=2, attackRange=1, heal=1), Attack(damage=[[u,u,o,o]], staminaCost=6, attackRange=1, heal=1)])
HandItem(name="Soothing Sunlight", attacks=[Attack(attackRange=1, heal=4, staminaCost=4)])
HandItem(name="Sorcerer's Catalyst", attacks=[Attack(damage=[[u]], magic=True, staminaCost=1, attackRange=3), Attack(damage=[[b,b]], magic=True, staminaCost=3, attackRange=3)])
HandItem(name="Sorcerer's Staff", twoHanded=True, resist=[u], dodge=[d], upgradeSlots=2, attacks=[Attack(damage=[[u]], staminaCost=0, attackRange=1), Attack(damage=[[u,u]], staminaCost=3, attackRange=1), Attack(damage=[[o]], magic=True, staminaCost=3, attackRange=3)])
HandItem(name="Soul Arrow", attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=0, attackRange=3), Attack(damage=[[b,b,b]], magic=True, staminaCost=4, attackRange=3)])
HandItem(name="Soul Greatsword", attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=1, attackRange=1), Attack(damage=[[o,o]], magic=True, staminaCost=3, attackRange=1)])
HandItem(name="Soul Spear", attacks=[Attack(damage=[[b]], magic=True, staminaCost=1, attackRange=3), Attack(damage=[[b,b,b]], magic=True, staminaCost=4, attackRange=3)])
HandItem(name="Soulstream", attacks=[Attack(damage=[[b]], magic=True, staminaCost=0, attackRange=1), Attack(damage=[[u]], magic=True, staminaCost=2, attackRange=2), Attack(damage=[[o]], magic=True, staminaCost=4, attackRange=3)])
HandItem(name="Spear", attacks=[Attack(damage=[[b]], staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)])
HandItem(name="Spider Shield", block=[b, b], immunities=set(["poison"]))
HandItem(name="Spiked Mace", twoHanded=True, block=[b], resist=[b], upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=1), Attack(damage=[[b,u,u]], staminaCost=3), Attack(damage=[[b,u,u]], staminaCost=5)])
HandItem(name="Spiked Shield", block=[b], resist=[b], attacks=[Attack(staminaCost=2, bleed=True)])
HandItem(name="Spitfire Spear", block=[b], resist=[u], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[o]], magic=True, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=3, noRange0=True)])
HandItem(name="Spotted Whip", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], damageMod=-1, poison=True, staminaCost=0, attackRange=1), Attack(damage=[[b,u]], damageMod=-1, poison=True, staminaCost=3, attackRange=1)])
HandItem(name="Stone Greataxe", twoHanded=True, block=[b], resist=[b], attacks=[Attack(damage=[[u,u]], staminaCost=2, attackRange=1), Attack(damage=[[u,u,u]], staminaCost=5, attackRange=1)])
HandItem(name="Stone Greatshield", block=[u], resist=[o,b], canDodge=False, attacks=[Attack(staminaCost=2, resist=[b])])
HandItem(name="Stone Greatsword", twoHanded=True, block=[b], attacks=[Attack(damage=[[b,u]], magic=True, staminaCost=1), Attack(damage=[[b,b,u]], magic=True, staminaCost=4)])
HandItem(name="Stone Parma", block=[u], resist=[u], upgradeSlots=1, attacks=[Attack(damage=[[o]], staminaCost=3)])
HandItem(name="Sunlight Shield", block=[b,b], resist=[b])
HandItem(name="Sunlight Straight Sword", upgradeSlots=1, attacks=[Attack(damage=[[b,u]], staminaCost=0), Attack(damage=[[u,u]], staminaCost=3)])
HandItem(name="Sunset Shield", block=[b], resist=[u])
HandItem(name="Talisman", attacks=[Attack(attackRange=2, staminaRecovery=1), Attack(attackRange=2, staminaCost=3, staminaRecovery=6)])
HandItem(name="Target Shield", dodge=[d])
HandItem(name="Thorolund Talisman", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], magic=True, staminaCost=2, attackRange=3), Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=3)])
HandItem(name="Thrall Axe", upgradeSlots=2, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[b,u]], staminaCost=3)])
HandItem(name="Titanite Catch Pole", block=[b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b,u]], magic=True, staminaCost=1, attackRange=1, noRange0=True), Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=1, noRange0=True), Attack(damage=[[u,u]], magic=True, staminaCost=4, attackRange=2, noRange0=True)])
HandItem(name="Torch", attacks=[Attack(damage=[[b]], magic=True, staminaCost=0), Attack(damage=[[u]], magic=True, staminaCost=2)])
HandItem(name="Tower Shield", block=[u], resist=[u], canDodge=False, boss=True)
HandItem(name="Twin Dragon Greatshield", block=[u, u], resist=[u])
HandItem(name="Uchigatana", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b,b]], staminaCost=0), Attack(damage=[[u,u]], staminaCost=2)])
HandItem(name="Umbral Dagger", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[u,u]], damageMod=-1, staminaCost=0), Attack(damage=[[o,o]], damageMod=-1, staminaCost=2), Attack(damage=[[u,o,o]], damageMod=-1, staminaCost=3)])
HandItem(name="Velka's Rapier", dodge=[d], upgradeSlots=1, attacks=[Attack(damage=[[b]], magic=True, staminaCost=0), Attack(damage=[[b,b]], magic=True, staminaCost=2)])
HandItem(name="Vordt's Great Hammer", twoHanded=True, block=[b], resist=[b,b], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[u,u,u]], staminaCost=2, attackRange=1), Attack(damage=[[u,u,u,u]], staminaCost=4, attackRange=1)])
HandItem(name="Warpick", upgradeSlots=1, attacks=[Attack(damage=[[u,o]], staminaCost=1), Attack(damage=[[u,o,o]], staminaCost=4)])
HandItem(name="Warden Twinblades", twoHanded=True, block=[b], upgradeSlots=1, attacks=[Attack(damage=[[b], [b]], staminaCost=0), Attack(damage=[[b,b], [b,b]], staminaCost=2), Attack(damage=[[u,u], [u,u]], staminaCost=5)])
HandItem(name="Washing Pole", twoHanded=True, dodge=[d], upgradeSlots=2, attacks=[Attack(damage=[[b,b]], staminaCost=0, attackRange=2, noRange0=True), Attack(damage=[[u,u]], staminaCost=2, attackRange=2, noRange0=True), Attack(damage=[[u,u]], bleed=True, staminaCost=4, attackRange=2, noRange0=True)])
HandItem(name="Winged Knight Halberd", twoHanded=True, block=[u], boss=True, upgradeSlots=2, attacks=[Attack(damage=[[u]], staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[u,u]], staminaCost=3, attackRange=1, noRange0=True), Attack(damage=[[u,u]], staminaCost=4, attackRange=1, noRange0=True)])
HandItem(name="Winged Knight Twin Axes", twoHanded=True, dodge=[d], boss=True, upgradeSlots=1, attacks=[Attack(damage=[[b],[b]], damageMod=1, staminaCost=0), Attack(damage=[[u],[u]], damageMod=1, staminaCost=2), Attack(damage=[[o],[o]], damageMod=1, staminaCost=4)])
HandItem(name="Winged Spear", twoHanded=True, block=[b], resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[b]], damageMod=1, staminaCost=0, attackRange=1, noRange0=True), Attack(damage=[[b,b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)])
HandItem(name="Witch's Locks", resist=[b], upgradeSlots=2, attacks=[Attack(damage=[[u]], magic=True, staminaCost=1, attackRange=1), Attack(damage=[[b,u]], magic=True, staminaCost=4, attackRange=1)])
HandItem(name="Wooden Shield", dodge=[d])
HandItem(name="Zweihander", twoHanded=True, block=[b], upgradeSlots=2, attacks=[Attack(damage=[[b,u,u]], staminaCost=2, attackRange=1), Attack(damage=[[b,o,o]], staminaCost=5, attackRange=1)])

HandItemUpgrade(name="Blessed Gem", damage=[b])
HandItemUpgrade(name="Blood Gem", bleed=True)
HandItemUpgrade(name="Carthus Flame Arc", magic=True, damageMod=1)
HandItemUpgrade(name="Crystal Gem", damage=[b])
HandItemUpgrade(name="Crystal Magic Weapon", magic=True, damageMod=1)
HandItemUpgrade(name="Demon Titanite", damageMod=1, highestStaminaModIfBoss=-1)
HandItemUpgrade(name="Faron Flashsword", magic=True, range0GetRange1=True)
HandItemUpgrade(name="Heavy Gem", damage=[b])
HandItemUpgrade(name="Lightning Gem", magic=True)
HandItemUpgrade(name="Poison Gem", poison=True)
HandItemUpgrade(name="Raw Gem", damageMod=2, staminaCostMod=2)
HandItemUpgrade(name="Sharp Gem", damage=[b])
HandItemUpgrade(name="Simple Gem", highestStaminaMod=-1)
HandItemUpgrade(name="Titanite Shard", damageMod=1)
HandItemUpgrade(name="Titanite Shard", damageMod=1)
