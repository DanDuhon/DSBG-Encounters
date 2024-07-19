from statistics import mean
from itertools import product


attacks = []
attackTiers = {
    1: [],
    2: [],
    3: []
}

b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)
means = {
    b: mean(b),
    u: mean(u),
    o: mean(o)
}

# bleedTrigger = {
#     1: {
#         0: [],
#         1: [],
#         2: [],
#         3: [],
#         4: [],
#         5: [],
#         6: []
#     },
#     2: {
#         0: [],
#         1: [],
#         2: [],
#         3: [],
#         4: [],
#         5: [],
#         6: []
#     },
#     3: {
#         0: [],
#         1: [],
#         2: [],
#         3: [],
#         4: [],
#         5: [],
#         6: []
#     }
# }

reachMod = {
    1: 0.44970414201183434,
    2: 0.8224852071005917,
    3: 0.9763313609467456,
    4: 1
}

class Attack:
    def __init__(self, name, attackNumber, staminaCost, damage=[[]], damageMod=0, attackRange=0, magic=False, bleed=False, poison=False, ignoreDefense=False, damageBonus=set(), noRange0=False) -> None:
        attacks.append(self)
        self.name = name
        self.attackNumber = attackNumber
        # Uses reachMod to calculate the odds of stamina cost to get into range (1 stamina, 2 stamina, 3 stamina).
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

        # for x in range(7): # defense
        #     for attack in self.damage:
        #         combos = list(product(*attack))
        #         bleedTrigger[self.tier][x].append((sum([1 for c in combos if sum(c) > x]) / len([c for c in combos]) if len([c for c in combos]) > 0 else 0))

Attack(name="Abyss Greatsword", attackNumber=1, damage=[[b,b,b]], staminaCost=1)
Attack(name="Abyss Greatsword", attackNumber=2, damage=[[u,u,u]], staminaCost=4)
Attack(name="Aged Smelter Sword", attackNumber=1, damage=[[b,b,b,u]], magic=True, staminaCost=2, attackRange=1)
Attack(name="Aged Smelter Sword", attackNumber=2, damage=[[u,o,o]], magic=True, staminaCost=5, attackRange=1)
Attack(name="Alonne Greatbow", attackNumber=1, damage=[[b,b,b]], staminaCost=2, attackRange=3, noRange0=True)
Attack(name="Alonne Greatbow", attackNumber=2, damage=[[b,b,u]], staminaCost=4, attackRange=3, noRange0=True)
Attack(name="Avelyn", attackNumber=1, damage=[[u],[u],[u]], staminaCost=1, attackRange=3, noRange0=True)
Attack(name="Avelyn", attackNumber=2, damage=[[o],[o],[o]], staminaCost=4, attackRange=3, noRange0=True)
Attack(name="Balder Side Sword", attackNumber=1, damage=[[u,u]], staminaCost=0)
Attack(name="Balder Side Sword", attackNumber=2, damage=[[o,o]], staminaCost=4, attackRange=1)
Attack(name="Bandit Knife", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Bandit Knife", attackNumber=2, damage=[[b,b]], staminaCost=3)
Attack(name="Battle Axe", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Battle Axe", attackNumber=2, damage=[[b,b]], staminaCost=2)
Attack(name="Bewitched Alonne Sword", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Bewitched Alonne Sword", attackNumber=2, damage=[[b,b,u]], staminaCost=3)
Attack(name="Bewitched Alonne Sword", attackNumber=3, damage=[[b,b,u,u]], staminaCost=0)
Attack(name="Black Bow of Pharis", attackNumber=1, damage=[[u]], staminaCost=0, attackRange=4, noRange0=True)
Attack(name="Black Bow of Pharis", attackNumber=2, damage=[[b,u]], staminaCost=2, attackRange=4, noRange0=True)
Attack(name="Black Bow of Pharis", attackNumber=3, damage=[[b,u]], staminaCost=4, attackRange=4, noRange0=True)
Attack(name="Black Firebombs", attackNumber=1, damage=[[u,u]], magic=True, staminaCost=4, attackRange=1)
Attack(name="Black Knight Greataxe", attackNumber=1, damage=[[u,u]], staminaCost=1)
Attack(name="Black Knight Greataxe", attackNumber=2, damage=[[u,u]], staminaCost=4)
Attack(name="Black Knight Greataxe", attackNumber=3, damage=[[u,u]], staminaCost=4)
Attack(name="Black Knight Shield (Deprived)", attackNumber=1, damage=[[u]], staminaCost=2)
Attack(name="Black Knight Shield (Deprived)", attackNumber=2, damage=[[o]], staminaCost=4)
Attack(name="Black Knight Shield (Black Knight)", attackNumber=1, damage=[[b,u]], staminaCost=2)
Attack(name="Black Knight Halberd", attackNumber=1, damage=[[b,b,b]], staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Black Knight Halberd", attackNumber=2, damage=[[b,b,u]], staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Black Knight Sword", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Black Knight Sword", attackNumber=2, damage=[[u,u,b]], staminaCost=4)
Attack(name="Blacksteel Katana", attackNumber=1, damage=[[b,b]], staminaCost=1, attackRange=1)
Attack(name="Blacksteel Katana", attackNumber=2, damage=[[b,b,b]], staminaCost=3, attackRange=1)
Attack(name="Blinding Bolt", attackNumber=1, damage=[[u],[u],[u],[u],[u]], magic=True, staminaCost=2, attackRange=1)
Attack(name="Bloodshield", attackNumber=1, damage=[[b,b]], staminaCost=1)
Attack(name="Bonewheel Shield", attackNumber=1, damage=[[b,b]], staminaCost=1)
Attack(name="Bonewheel Shield", attackNumber=2, damage=[[b,b],[b,b],[b,b],[b,b]], staminaCost=5)
Attack(name="Brigand Axe", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Brigand Axe", attackNumber=2, damage=[[b,u]], staminaCost=3)
Attack(name="Broadsword", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Broadsword", attackNumber=2, damage=[[b,u]], staminaCost=2, attackRange=1)
Attack(name="Broadsword", attackNumber=3, damage=[[u,u]], staminaCost=4, attackRange=1)
Attack(name="Broken Straight Sword", attackNumber=1, damage=[[b,b,b]], damageMod=-2, staminaCost=0)
Attack(name="Broken Straight Sword", attackNumber=2, damage=[[u,u,u]], damageMod=-2, staminaCost=3)
Attack(name="Butcher Knife", attackNumber=1, damage=[[b,b]], staminaCost=1, attackRange=1, heal=1)
Attack(name="Butcher Knife", attackNumber=2, damage=[[u,u]], staminaCost=4, attackRange=1, heal=1)
Attack(name="Caestus", attackNumber=1, damage=[[b, b]], staminaCost=0)
Attack(name="Carthus Curved Greatsword", attackNumber=1, damage=[[b,b]], bleed=True, staminaCost=0)
Attack(name="Carthus Curved Greatsword", attackNumber=2, damage=[[b,b,b]], bleed=True, staminaCost=3)
Attack(name="Carthus Curved Sword", attackNumber=1, damage=[[u,u]], damageMod=-1, staminaCost=1)
Attack(name="Carthus Curved Sword", attackNumber=2, damage=[[u,u,u]], damageMod=-1, staminaCost=3)
Attack(name="Chariot Lance", attackNumber=1, damage=[[o]], bleed=True, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Chariot Lance", attackNumber=2, damage=[[u,o]], bleed=True, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Claws", attackNumber=1, damage=[[b,b],[b,b]], staminaCost=2)
Attack(name="Claws", attackNumber=2, damage=[[u,u],[u,u]], staminaCost=4)
Attack(name="Claymore", attackNumber=1, damage=[[u,u]], damageMod=1, staminaCost=1, attackRange=1)
Attack(name="Claymore", attackNumber=2, damage=[[o,o]], damageMod=1, staminaCost=4, attackRange=1)
Attack(name="Cleric's Candlestick", attackNumber=1, damage=[[b,u]], magic=True, staminaCost=1)
Attack(name="Cleric's Candlestick", attackNumber=2, damage=[[b,b,u]], magic=True, staminaCost=4)
Attack(name="Club", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Club", attackNumber=2, damage=[[b,b]], staminaCost=3)
Attack(name="Composite Bow", attackNumber=1, damage=[[b,b]], damageMod=-1, staminaCost=0, attackRange=4, noRange0=True)
Attack(name="Composite Bow", attackNumber=2, damage=[[b,b,b]], damageMod=-1, staminaCost=3, attackRange=4, noRange0=True)
Attack(name="Crescent Axe", attackNumber=1, damage=[[u]], staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Crescent Axe", attackNumber=2, damage=[[u,u]], damageMod=1, staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Crescent Moon Sword", attackNumber=1, damage=[[u]], magic=True, staminaCost=0)
Attack(name="Crescent Moon Sword", attackNumber=2, damage=[[u]], magic=True, staminaCost=3, attackRange=3)
Attack(name="Crystal Hail", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0, attackRange=4)
Attack(name="Crystal Hail", attackNumber=2, damage=[[b,b]], magic=True, staminaCost=5)
Attack(name="Crystal Shield", attackNumber=1, damage=[[b,b,b]], staminaCost=3)
Attack(name="Crystal Straight Sword", attackNumber=1, damage=[[u]], damageMod=1, staminaCost=0)
Attack(name="Crystal Straight Sword", attackNumber=2, damage=[[b,u]], damageMod=1, staminaCost=3)
Attack(name="Cursed Greatsword of Artorias", attackNumber=1, damage=[[u,b]], staminaCost=0)
Attack(name="Cursed Greatsword of Artorias", attackNumber=2, damage=[[u,o]], staminaCost=4)
Attack(name="Dancer's Enchanted Swords", attackNumber=1, damage=[[u], [u]], magic=True, staminaCost=2, attackRange=1)
Attack(name="Dancer's Enchanted Swords", attackNumber=2, damage=[[b,u], [b,u]], magic=True, staminaCost=4, attackRange=1)
Attack(name="Dark Silver Tracer", attackNumber=1, damage=[[u,u]], damageMod=-1, staminaCost=0)
Attack(name="Dark Silver Tracer", attackNumber=2, damage=[[u,u]], damageMod=-1, poison=True, staminaCost=3)
Attack(name="Dark Sword", attackNumber=1, damage=[[u]], staminaCost=0)
Attack(name="Dark Sword", attackNumber=2, damage=[[u,u]], staminaCost=2)
Attack(name="Dark Sword", attackNumber=3, damage=[[o,o]], staminaCost=5, attackRange=1)
Attack(name="Demon's Great Hammer", attackNumber=1, damage=[[u,u]], staminaCost=1, attackRange=1)
Attack(name="Demon's Great Hammer", attackNumber=2, damage=[[o,o]], staminaCost=4, attackRange=1)
Attack(name="Dragon King Greataxe", attackNumber=1, damage=[[o,o]], staminaCost=1)
Attack(name="Dragon King Greataxe", attackNumber=2, damage=[[o]], magic=True, staminaCost=5, attackRange=1)
Attack(name="Dragon Tooth", attackNumber=1, damage=[[u,o,o]], staminaCost=4, attackRange=1)
Attack(name="Dragon Tooth", attackNumber=2, damage=[[u,o,o]], staminaCost=6, attackRange=1)
Attack(name="Dragonrider Bow", attackNumber=1, damage=[[o]], staminaCost=1, attackRange=3, noRange0=True)
Attack(name="Dragonrider Bow", attackNumber=2, damage=[[o]], ignoreDefense=True, staminaCost=4)
Attack(name="Dragonslayer Greatbow", attackNumber=1, damage=[[u,u]], staminaCost=2, attackRange=3, noRange0=True)
Attack(name="Dragonslayer Greatbow", attackNumber=2, damage=[[u,o]], staminaCost=4, attackRange=3, noRange0=True)
Attack(name="Dragonslayer Spear", attackNumber=1, damage=[[b,u]], magic=True, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Dragonslayer Spear", attackNumber=2, damage=[[b,u,u]], magic=True, staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Dragonslayer Spear", attackNumber=3, damage=[[u,u]], magic=True, staminaCost=4, attackRange=4, noRange0=True)
Attack(name="Dragonslayer's Axe", attackNumber=1, damage=[[o]], magic=True, staminaCost=0)
Attack(name="Dragonslayer's Axe", attackNumber=2, damage=[[u,o]], magic=True, staminaCost=3, attackRange=1)
Attack(name="Drake Sword", attackNumber=1, damage=[[u,u]], staminaCost=2)
Attack(name="Drake Sword", attackNumber=2, damage=[[o,o]], staminaCost=4)
Attack(name="Drake Sword", attackNumber=3, damage=[[u,u]], staminaCost=4, attackRange=3)
Attack(name="Drakewing Ultra Greatsword", attackNumber=1, damage=[[u,o]], staminaCost=2, attackRange=1)
Attack(name="Drakewing Ultra Greatsword", attackNumber=2, damage=[[o,o]], staminaCost=5, attackRange=3)
Attack(name="Drang Hammers", attackNumber=1, damage=[[u,u]], damageMod=1, staminaCost=0)
Attack(name="Drang Hammers", attackNumber=2, damage=[[u,u], [u,u]], staminaCost=3)
Attack(name="Drang Hammers", attackNumber=3, damage=[[u,u], [u,u]], damageMod=1, staminaCost=5)
Attack(name="Dung Pie", attackNumber=1, poison=True, staminaCost=0, attackRange=1)
Attack(name="Estoc", attackNumber=1, damage=[[b,b]], damageMod=-1, staminaCost=0)
Attack(name="Estoc", attackNumber=2, damage=[[b,b,b]], damageMod=-1, staminaCost=3)
Attack(name="Exile Greatsword", attackNumber=1, damage=[[u,b]], staminaCost=2)
Attack(name="Exile Greatsword", attackNumber=2, damage=[[u,b]], staminaCost=4)
Attack(name="Exile Greatsword", attackNumber=3, damage=[[u,o]], staminaCost=5)
Attack(name="Falchion", attackNumber=1, damage=[[u,u]], staminaCost=0)
Attack(name="Falchion", attackNumber=2, damage=[[o,o]], staminaCost=3)
Attack(name="Fire Surge", attackNumber=1, damage=[[u]], magic=True, staminaCost=0, attackRange=2)
Attack(name="Fire Surge", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=4, attackRange=2)
Attack(name="Fire Whip", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0)
Attack(name="Fire Whip", attackNumber=2, damage=[[o,o]], magic=True, staminaCost=4)
Attack(name="Fireball", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0, attackRange=2)
Attack(name="Fireball", attackNumber=2, damage=[[o,o]], magic=True, staminaCost=5, attackRange=2)
Attack(name="Firebombs", attackNumber=1, damage=[[b,b,b]], magic=True, staminaCost=4, attackRange=1)
Attack(name="Flamberge", attackNumber=1, damage=[[o]], bleed=True, staminaCost=2)
Attack(name="Flamberge", attackNumber=2, damage=[[u,u]], bleed=True, staminaCost=4)
Attack(name="Four Kings Sword", attackNumber=1, damage=[[o]], staminaCost=0)
Attack(name="Four Kings Sword", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=3)
Attack(name="Four-Pronged Plow", attackNumber=1, damage=[[u]], staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Four-Pronged Plow", attackNumber=2, damage=[[u,u]], staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Fume Ultra Greatsword", attackNumber=1, damage=[[u,o]], staminaCost=2, attackRange=1)
Attack(name="Fume Ultra Greatsword", attackNumber=2, damage=[[u,u,o]], staminaCost=5, attackRange=1)
Attack(name="Fume Ultra Greatsword", attackNumber=3, damage=[[u,o]], staminaCost=4, attackRange=1)
Attack(name="Gargoyle Tail Axe", attackNumber=1, damage=[[u,u]], staminaCost=1)
Attack(name="Gargoyle Tail Axe", attackNumber=2, damage=[[u,u,u]], staminaCost=4)
Attack(name="Gargoyle's Halberd", attackNumber=1, damage=[[o]], staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Gargoyle's Halberd", attackNumber=2, damage=[[o,o]], staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Giant Stone Axe", attackNumber=1, damage=[[b,u]], staminaCost=1, attackRange=1)
Attack(name="Giant Stone Axe", attackNumber=2, damage=[[u,o]], staminaCost=4, attackRange=1)
Attack(name="Giant's Halberd", attackNumber=1, damage=[[b,u]], staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Giant's Halberd", attackNumber=2, damage=[[b,o]], staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Gold Tracer", attackNumber=1, damage=[[o,o]], damageMod=-1, staminaCost=0)
Attack(name="Gold Tracer", attackNumber=2, damage=[[o,o]], damageMod=-1, bleed=True, staminaCost=3)
Attack(name="Golden Ritual Spear", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Golden Ritual Spear", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Golden Ritual Spear", attackNumber=3, damage=[[u,u]], magic=True, staminaCost=5, attackRange=3, noRange0=True)
Attack(name="Golden Wing Crest Shield", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Gotthard Twinswords", attackNumber=1, damage=[[b,b], [b,b]], staminaCost=1)
Attack(name="Gotthard Twinswords", attackNumber=2, damage=[[u,u], [u,u]], staminaCost=4)
Attack(name="Gotthard Twinswords", attackNumber=3, damage=[[u,u]], staminaCost=3, attackRange=1)
Attack(name="Gravelord Sword", attackNumber=1, damage=[[b,u]], poison=True, staminaCost=2)
Attack(name="Gravelord Sword", attackNumber=2, damage=[[b,o]], poison=True, staminaCost=4)
Attack(name="Gravelord Sword Dance", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=1, attackRange=3)
Attack(name="Gravelord Sword Dance", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=3, attackRange=3)
Attack(name="Greataxe", attackNumber=1, damage=[[u,u]], staminaCost=0)
Attack(name="Greataxe", attackNumber=2, damage=[[o,o]], staminaCost=3)
Attack(name="Greataxe", attackNumber=3, damage=[[u,u]], staminaCost=3)
Attack(name="Great Chaos Fireball", attackNumber=1, damage=[[o]], magic=True, staminaCost=1, attackRange=2)
Attack(name="Great Chaos Fireball", attackNumber=2, damage=[[u,u,u]], magic=True, staminaCost=4, attackRange=2)
Attack(name="Great Club", attackNumber=1, damage=[[o]], staminaCost=0, attackRange=1)
Attack(name="Great Club", attackNumber=2, damage=[[o,o]], staminaCost=3, attackRange=1)
Attack(name="Great Combustion", attackNumber=1, damage=[[u]], magic=True, staminaCost=1, attackRange=2)
Attack(name="Great Combustion", attackNumber=2, damage=[[o]], magic=True, staminaCost=3, attackRange=2)
Attack(name="Great Mace", attackNumber=1, damage=[[u]], damageMod=1, staminaCost=0)
Attack(name="Great Mace", attackNumber=2, damage=[[u,u]], damageMod=1, staminaCost=3)
Attack(name="Great Machete", attackNumber=1, damage=[[u,u,u]], staminaCost=1)
Attack(name="Great Machete", attackNumber=2, damage=[[b,b,o,o]], staminaCost=4)
Attack(name="Great Machete", attackNumber=3, damage=[[u,u,u]], staminaCost=4)
Attack(name="Great Scythe", attackNumber=1, damage=[[b,b,b]], damageMod=-1, staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Great Scythe", attackNumber=2, damage=[[o,o]], damageMod=-1, staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Great Wooden Hammer", attackNumber=1, damage=[[b,b,b]], staminaCost=0)
Attack(name="Great Wooden Hammer", attackNumber=2, damage=[[b,b,b]], staminaCost=3)
Attack(name="Greatsword", attackNumber=1, damage=[[b,u]], staminaCost=1)
Attack(name="Greatsword", attackNumber=2, damage=[[b,o]], staminaCost=4)
Attack(name="Greatsword of Artorias", attackNumber=1, damage=[[u,b]], magic=True, staminaCost=0)
Attack(name="Greatsword of Artorias", attackNumber=2, damage=[[u,o]], magic=True, staminaCost=4)
Attack(name="Halberd", attackNumber=1, damage=[[u]], damageMod=1, staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Halberd", attackNumber=2, damage=[[u,u]], damageMod=1, staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Hand Axe", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Hand Axe", attackNumber=2, damage=[[b,b]], staminaCost=3)
Attack(name="Hollow Soldier Shield", attackNumber=1, damage=[[b,b]], damageBonus={"hollow",}, staminaCost=2)
Attack(name="Homing Crystal Soulmass", attackNumber=1, damage=[[o],[o],[o],[o],[o]], magic=True, staminaCost=5, attackRange=3)
Attack(name="Immolation Tinder", attackNumber=1, damage=[[u]], magic=True, staminaCost=0, attackRange=1)
Attack(name="Immolation Tinder", attackNumber=2, damage=[[b,b]], magic=True, staminaCost=2, attackRange=1)
Attack(name="Immolation Tinder", attackNumber=3, damage=[[b,b]], magic=True, staminaCost=4, attackRange=3)
Attack(name="Irithyll Rapier", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Irithyll Rapier", attackNumber=2, damage=[[b,u]], staminaCost=2)
Attack(name="Irithyll Straight Sword", attackNumber=1, damage=[[b,b]], damageMod=1, staminaCost=0)
Attack(name="Irithyll Straight Sword", attackNumber=2, damage=[[b,b,u]], staminaCost=3)
Attack(name="Iron King Hammer", attackNumber=1, damage=[[o]], magic=True, staminaCost=2)
Attack(name="Iron King Hammer", attackNumber=2, damage=[[b,u],[b,u]], staminaCost=4, attackRange=1)
Attack(name="Lifehunt Scythe", attackNumber=1, damage=[[u,u]], damageMod=-1, bleed=True, staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Lifehunt Scythe", attackNumber=2, damage=[[o,o]], damageMod=-1, bleed=True, staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Long Sword", attackNumber=1, damage=[[u]], staminaCost=0)
Attack(name="Long Sword", attackNumber=2, damage=[[b,u]], staminaCost=4)
Attack(name="Longbow", attackNumber=1, damage=[[b,b]], staminaCost=0, attackRange=4, noRange0=True)
Attack(name="Longbow", attackNumber=2, damage=[[b,b,b]], staminaCost=3, attackRange=4, noRange0=True)
Attack(name="Lothric Knight Greatsword", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0, attackRange=1)
Attack(name="Lothric Knight Greatsword", attackNumber=2, damage=[[b,b,b]], magic=True, staminaCost=3, attackRange=1)
Attack(name="Lothric's Holy Sword", attackNumber=1, damage=[[u]], magic=True, staminaCost=1, staminaRecovery=1)
Attack(name="Lothric's Holy Sword", attackNumber=2, damage=[[b,u]], magic=True, staminaCost=3, staminaRecovery=1)
Attack(name="Lucerne", attackNumber=1, damage=[[b,b,u]], damageMod=-1, staminaCost=1)
Attack(name="Lucerne", attackNumber=2, damage=[[b,b,b,u]], damageMod=-1, staminaCost=4)
Attack(name="Mace", attackNumber=1, damage=[[u]], staminaCost=0)
Attack(name="Mace", attackNumber=2, damage=[[b,b]], staminaCost=2)
Attack(name="Mail Breaker", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Mail Breaker", attackNumber=2, damage=[[u]], staminaCost=2)
Attack(name="Man Serpent Hatchet", attackNumber=1, damage=[[b,u]], staminaCost=0)
Attack(name="Man Serpent Hatchet", attackNumber=2, damage=[[b,u]], ignoreDefense=True, staminaCost=3)
Attack(name="Mannikin Claws", attackNumber=1, damage=[[b,b], [b,b]], staminaCost=2, attackRange=1)
Attack(name="Mannikin Claws", attackNumber=2, damage=[[u,u], [u,u]], staminaCost=4, attackRange=1)
Attack(name="Manus Catalyst", attackNumber=1, damage=[[u,u]], staminaCost=1)
Attack(name="Manus Catalyst", attackNumber=2, damage=[[o,o]], staminaCost=4)
Attack(name="Melinda's Greataxe", attackNumber=1, damage=[[o,o]], staminaCost=2)
Attack(name="Melinda's Greataxe", attackNumber=2, damage=[[o,o]], staminaCost=4)
Attack(name="Moonlight Greatsword", attackNumber=1, damage=[[b,u]], magic=True, staminaCost=0)
Attack(name="Moonlight Greatsword", attackNumber=2, damage=[[u,u,u]], magic=True, staminaCost=3)
Attack(name="Moonlight Greatsword", attackNumber=3, damage=[[u,u,u]], magic=True, staminaCost=4, attackRange=3)
Attack(name="Morion Blade", attackNumber=1, damage=[[b]], bleed=True, staminaCost=0)
Attack(name="Morion Blade", attackNumber=2, damage=[[b,b]], bleed=True, staminaCost=3)
Attack(name="Morne's Great Hammer", attackNumber=1, damage=[[u,u]], staminaCost=2)
Attack(name="Morne's Great Hammer", attackNumber=2, damage=[[u,o]], staminaCost=4)
Attack(name="Morne's Great Hammer", attackNumber=3, damage=[[o,o]], staminaCost=6)
Attack(name="Morning Star", attackNumber=1, damage=[[u]], staminaCost=0)
Attack(name="Morning Star", attackNumber=2, damage=[[u,u]], staminaCost=3)
Attack(name="Murakamo", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Murakamo", attackNumber=2, damage=[[b,b,b]], staminaCost=3)
Attack(name="Notched Whip", attackNumber=1, damage=[[u]], bleed=True, staminaCost=0, attackRange=1)
Attack(name="Notched Whip", attackNumber=2, damage=[[o]], bleed=True, staminaCost=3, attackRange=1)
Attack(name="Obsidian Greatsword", attackNumber=1, damage=[[o,o]], staminaCost=1)
Attack(name="Obsidian Greatsword", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=5, attackRange=1)
Attack(name="Old Dragonslayer Spear", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Old Dragonslayer Spear", attackNumber=2, damage=[[b,b,b]], magic=True, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Old Dragonslayer Spear", attackNumber=3, damage=[[b,b]], magic=True, staminaCost=3, attackRange=3, noRange0=True)
Attack(name="Onikiri and Ubadachi", attackNumber=1, damage=[[u], [u]], staminaCost=0)
Attack(name="Onikiri and Ubadachi", attackNumber=2, damage=[[u,u], [u,u]], staminaCost=3)
Attack(name="Onikiri and Ubadachi", attackNumber=3, damage=[[o,o]], staminaCost=4, attackRange=1)
Attack(name="Painting Guardian's Curved Sword", attackNumber=1, damage=[[b,b]], bleed=True, staminaCost=0, attackRange=1)
Attack(name="Painting Guardian's Curved Sword", attackNumber=2, damage=[[b,b,b]], bleed=True, staminaCost=3, attackRange=1)
Attack(name="Parrying Dagger", attackNumber=1, damage=[[b,b]], damageMod=-1, staminaCost=0)
Attack(name="Parrying Dagger", attackNumber=2, damage=[[b,b]], staminaCost=2)
Attack(name="Partizan", attackNumber=1, damage=[[u,u]], staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Partizan", attackNumber=2, damage=[[u,u,o]], staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Pierce Shield", attackNumber=1, damage=[[b,b]], staminaCost=2)
Attack(name="Pike", attackNumber=1, damage=[[b]], damageMod=1, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Pike", attackNumber=2, damage=[[b,b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Pike", attackNumber=3, damage=[[b,b,b]], damageMod=1, staminaCost=5, attackRange=2, noRange0=True)
Attack(name="Poison Mist", attackNumber=1, poison=True, staminaCost=1, attackRange=1)
Attack(name="Poison Mist", attackNumber=2, poison=True, staminaCost=3, attackRange=1)
Attack(name="Poison Throwing Knives", attackNumber=1, damage=[[b,b]], poison=True, staminaCost=3, attackRange=1)
Attack(name="Porcine Shield", attackNumber=1, damage=[[u]], staminaCost=1)
Attack(name="Priscilla's Dagger", attackNumber=1, damage=[[]], bleed=True, staminaCost=0)
Attack(name="Priscilla's Dagger", attackNumber=2, damage=[[o]], bleed=True, staminaCost=3, attackRange=1)
Attack(name="Pursuer's Ultra Greatsword", attackNumber=1, damage=[[u,u]], staminaCost=2, attackRange=1)
Attack(name="Pursuer's Ultra Greatsword", attackNumber=2, damage=[[u,u,o]], staminaCost=5, attackRange=1)
Attack(name="Pursuers", attackNumber=1, damage=[[b,b],[b,b],[b,b],[b,b],[b,b]], magic=True, staminaCost=5, attackRange=2)
Attack(name="Pyromancy Flame", attackNumber=1, damage=[[b]], magic=True, staminaCost=0, attackRange=2)
Attack(name="Pyromancy Flame", attackNumber=2, damage=[[b,b]], magic=True, staminaCost=4, attackRange=2)
Attack(name="Rapier", attackNumber=1, damage=[[b]], damageMod=1, staminaCost=0)
Attack(name="Rapier", attackNumber=2, damage=[[u,u]], staminaCost=3)
Attack(name="Reinforced Club", attackNumber=1, damage=[[u]], staminaCost=0)
Attack(name="Reinforced Club", attackNumber=2, damage=[[u,u]], staminaCost=3)
Attack(name="Rotten Ghru Dagger", attackNumber=1, damage=[[b,b]], damageMod=-1, poison=True, staminaCost=0)
Attack(name="Rotten Ghru Dagger", attackNumber=2, damage=[[b,b,b]], damageMod=-1, poison=True, staminaCost=3)
Attack(name="Rotten Ghru Spear", attackNumber=1, damage=[[b,b]], damageMod=-1, poison=True, staminaCost=0, attackRange=1)
Attack(name="Rotten Ghru Spear", attackNumber=2, damage=[[b,b]], poison=True, staminaCost=3, attackRange=1)
Attack(name="Royal Dirk", attackNumber=1, damage=[[u]], staminaCost=0)
Attack(name="Royal Dirk", attackNumber=2, damage=[[u,u]], staminaCost=3)
Attack(name="Saint Bident", attackNumber=1, damage=[[u,u]], staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Saint Bident", attackNumber=2, damage=[[b,u,u]], staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Santier's Spear", attackNumber=1, damage=[[u,u]], damageMod=1, staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Santier's Spear", attackNumber=2, damage=[[u,u]], staminaCost=3, attackRange=1)
Attack(name="Santier's Spear", attackNumber=3, damage=[[u,u,u]], staminaCost=4)
Attack(name="Sellsword Twinblades", attackNumber=1, damage=[[b], [b]], staminaCost=0)
Attack(name="Sellsword Twinblades", attackNumber=2, damage=[[b,b], [b,b]], staminaCost=2)
Attack(name="Scimitar", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Scimitar", attackNumber=2, damage=[[o,o]], damageMod=-1, staminaCost=3)
Attack(name="Shield Crossbow", attackNumber=1, damage=[[b,b]], staminaCost=0, attackRange=3, noRange0=True)
Attack(name="Shield Crossbow", attackNumber=2, damage=[[u,u]], staminaCost=4, attackRange=3, noRange0=True)
Attack(name="Shortbow", attackNumber=1, damage=[[u]], staminaCost=0, attackRange=3, noRange0=True)
Attack(name="Shortbow", attackNumber=2, damage=[[b,b]], staminaCost=3, attackRange=3, noRange0=True)
Attack(name="Shortsword", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Shortsword", attackNumber=2, damage=[[b,b,b]], staminaCost=2)
Attack(name="Shotel", attackNumber=1, damage=[[b]], staminaCost=0)
Attack(name="Shotel", attackNumber=2, damage=[[b]], ignoreDefense=True, staminaCost=2)
Attack(name="Shotel", attackNumber=3, damage=[[u]], ignoreDefense=True, staminaCost=4)
Attack(name="Silver Knight Shield", attackNumber=1, damage=[[b,u]], staminaCost=1)
Attack(name="Silver Knight Shield", attackNumber=2, damage=[[u,u]], staminaCost=3)
Attack(name="Silver Knight Spear", attackNumber=1, damage=[[u]], damageMod=1, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Silver Knight Spear", attackNumber=2, damage=[[b,b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Silver Knight Straight Sword", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Silver Knight Straight Sword", attackNumber=2, damage=[[b,u]], staminaCost=3)
Attack(name="Skull Lantern", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=3)
Attack(name="Smelter Sword", attackNumber=1, damage=[[b,b,b]], staminaCost=2, attackRange=1)
Attack(name="Smelter Sword", attackNumber=2, damage=[[o,o]], staminaCost=5, attackRange=1)
Attack(name="Smough's Hammer", attackNumber=1, damage=[[u,o]], staminaCost=2, attackRange=1, heal=1)
Attack(name="Smough's Hammer", attackNumber=2, damage=[[u,u,o,o]], staminaCost=6, attackRange=1, heal=1)
Attack(name="Sorcerer's Catalyst", attackNumber=1, damage=[[u]], magic=True, staminaCost=1, attackRange=3)
Attack(name="Sorcerer's Catalyst", attackNumber=2, damage=[[b,b]], magic=True, staminaCost=3, attackRange=3)
Attack(name="Sorcerer's Staff", attackNumber=1, damage=[[u]], staminaCost=0, attackRange=1)
Attack(name="Sorcerer's Staff", attackNumber=2, damage=[[u,u]], staminaCost=3, attackRange=1)
Attack(name="Sorcerer's Staff", attackNumber=3, damage=[[o]], magic=True, staminaCost=3, attackRange=3)
Attack(name="Soul Arrow", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=0, attackRange=3)
Attack(name="Soul Arrow", attackNumber=2, damage=[[b,b,b]], magic=True, staminaCost=4, attackRange=3)
Attack(name="Soul Greatsword", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=1, attackRange=1)
Attack(name="Soul Greatsword", attackNumber=2, damage=[[o,o]], magic=True, staminaCost=3, attackRange=1)
Attack(name="Soul Spear", attackNumber=1, damage=[[b]], magic=True, staminaCost=1, attackRange=3)
Attack(name="Soul Spear", attackNumber=2, damage=[[b,b,b]], magic=True, staminaCost=4, attackRange=3)
Attack(name="Soulstream", attackNumber=1, damage=[[b]], magic=True, staminaCost=0, attackRange=1)
Attack(name="Soulstream", attackNumber=2, damage=[[u]], magic=True, staminaCost=2, attackRange=2)
Attack(name="Soulstream", attackNumber=3, damage=[[o]], magic=True, staminaCost=4, attackRange=3)
Attack(name="Spear", attackNumber=1, damage=[[b]], staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Spear", attackNumber=2, damage=[[b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Spiked Mace", attackNumber=1, damage=[[b,u]], staminaCost=1)
Attack(name="Spiked Mace", attackNumber=2, damage=[[b,u,u]], staminaCost=3)
Attack(name="Spiked Mace", attackNumber=3, damage=[[b,u,u]], staminaCost=5)
Attack(name="Spitfire Spear", attackNumber=1, damage=[[o]], magic=True, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Spitfire Spear", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=4, attackRange=3, noRange0=True)
Attack(name="Spotted Whip", attackNumber=1, damage=[[b,b]], damageMod=-1, poison=True, staminaCost=0, attackRange=1)
Attack(name="Spotted Whip", attackNumber=2, damage=[[b,u]], damageMod=-1, poison=True, staminaCost=3, attackRange=1)
Attack(name="Stone Greataxe", attackNumber=1, damage=[[u,u]], staminaCost=2, attackRange=1)
Attack(name="Stone Greataxe", attackNumber=2, damage=[[u,u,u]], staminaCost=5, attackRange=1)
Attack(name="Stone Greatsword", attackNumber=1, damage=[[b,u]], magic=True, staminaCost=1)
Attack(name="Stone Greatsword", attackNumber=2, damage=[[b,b,u]], magic=True, staminaCost=4)
Attack(name="Stone Parma", attackNumber=1, damage=[[o]], staminaCost=3)
Attack(name="Sunlight Straight Sword", attackNumber=1, damage=[[b,u]], staminaCost=0)
Attack(name="Sunlight Straight Sword", attackNumber=2, damage=[[u,u]], staminaCost=3)
Attack(name="Thorolund Talisman", attackNumber=1, damage=[[b,b]], magic=True, staminaCost=2, attackRange=3)
Attack(name="Thorolund Talisman", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=4, attackRange=3)
Attack(name="Thrall Axe", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Thrall Axe", attackNumber=2, damage=[[b,u]], staminaCost=3)
Attack(name="Titanite Catch Pole", attackNumber=1, damage=[[b,u]], magic=True, staminaCost=1, attackRange=1, noRange0=True)
Attack(name="Titanite Catch Pole", attackNumber=2, damage=[[u,u]], magic=True, staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Titanite Catch Pole", attackNumber=3, damage=[[u,u]], magic=True, staminaCost=4, attackRange=2, noRange0=True)
Attack(name="Torch", attackNumber=1, damage=[[b]], magic=True, staminaCost=0)
Attack(name="Torch", attackNumber=2, damage=[[u]], magic=True, staminaCost=2)
Attack(name="Uchigatana", attackNumber=1, damage=[[b,b]], staminaCost=0)
Attack(name="Uchigatana", attackNumber=2, damage=[[u,u]], staminaCost=2)
Attack(name="Umbral Dagger", attackNumber=1, damage=[[u,u]], damageMod=-1, staminaCost=0)
Attack(name="Umbral Dagger", attackNumber=2, damage=[[o,o]], damageMod=-1, staminaCost=2)
Attack(name="Umbral Dagger", attackNumber=3, damage=[[u,o,o]], damageMod=-1, staminaCost=3)
Attack(name="Velka's Rapier", attackNumber=1, damage=[[b]], magic=True, staminaCost=0)
Attack(name="Velka's Rapier", attackNumber=2, damage=[[b,b]], magic=True, staminaCost=2)
Attack(name="Vordt's Great Hammer", attackNumber=1, damage=[[u,u,u]], staminaCost=2, attackRange=1)
Attack(name="Vordt's Great Hammer", attackNumber=2, damage=[[u,u,u,u]], staminaCost=4, attackRange=1)
Attack(name="Warpick", attackNumber=1, damage=[[u,o]], staminaCost=1)
Attack(name="Warpick", attackNumber=2, damage=[[u,o,o]], staminaCost=4)
Attack(name="Warden Twinblades", attackNumber=1, damage=[[b], [b]], staminaCost=0)
Attack(name="Warden Twinblades", attackNumber=2, damage=[[b,b], [b,b]], staminaCost=2)
Attack(name="Warden Twinblades", attackNumber=3, damage=[[u,u], [u,u]], staminaCost=5)
Attack(name="Washing Pole", attackNumber=1, damage=[[b,b]], staminaCost=0, attackRange=2, noRange0=True)
Attack(name="Washing Pole", attackNumber=2, damage=[[u,u]], staminaCost=2, attackRange=2, noRange0=True)
Attack(name="Washing Pole", attackNumber=3, damage=[[u,u]], bleed=True, staminaCost=4, attackRange=2, noRange0=True)
Attack(name="Winged Knight Halberd", attackNumber=1, damage=[[u]], staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Winged Knight Halberd", attackNumber=2, damage=[[u,u]], staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Winged Knight Halberd", attackNumber=3, damage=[[u,u]], staminaCost=4, attackRange=1, noRange0=True)
Attack(name="Winged Knight Twin Axes", attackNumber=1, damage=[[b],[b]], damageMod=1, staminaCost=0)
Attack(name="Winged Knight Twin Axes", attackNumber=2, damage=[[u],[u]], damageMod=1, staminaCost=2)
Attack(name="Winged Knight Twin Axes", attackNumber=3, damage=[[o],[o]], damageMod=1, staminaCost=4)
Attack(name="Winged Spear", attackNumber=1, damage=[[b]], damageMod=1, staminaCost=0, attackRange=1, noRange0=True)
Attack(name="Winged Spear", attackNumber=2, damage=[[b,b]], damageMod=1, staminaCost=3, attackRange=1, noRange0=True)
Attack(name="Witch's Locks", attackNumber=1, damage=[[u]], magic=True, staminaCost=1, attackRange=1)
Attack(name="Witch's Locks", attackNumber=2, damage=[[b,u]], magic=True, staminaCost=4, attackRange=1)
Attack(name="Zweihander", attackNumber=1, damage=[[b,u,u]], staminaCost=2, attackRange=1)
Attack(name="Zweihander", attackNumber=2, damage=[[b,o,o]], staminaCost=5, attackRange=1)

# for tier in bleedTrigger:
#     for key in bleedTrigger[tier]:
#         bleedTrigger[tier][key] = mean(bleedTrigger[tier][key])
        
# This is to help calculate the difficulty for Fencer Sharron.
# Percent of attacks that have an expected damage on her of at least 3.
# for tier in range(1, 4):
#     print(sum([1 for a in attackTiers[tier] if a.expectedDamage[1] >= 3]) / len(attackTiers[tier]))

# This is to help calculate the difficulty for Black Knight.
# Percent of attacks that have an expected damage on him of less than 4 physical or 3 magical.
blackKnight = {
    1: sum([1 for a in attackTiers[1] if (not a.magic and a.expectedDamage[3] == 0) or (a.magic and a.expectedDamage[2] == 0)]) / len(attackTiers[1]),
    2: sum([1 for a in attackTiers[2] if (not a.magic and a.expectedDamage[3] == 0) or (a.magic and a.expectedDamage[2] == 0)]) / len(attackTiers[2]),
    3: sum([1 for a in attackTiers[3] if (not a.magic and a.expectedDamage[3] == 0) or (a.magic and a.expectedDamage[2] == 0)]) / len(attackTiers[3])
    }