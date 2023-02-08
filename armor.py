from statistics import mean
from itertools import chain, product


armor = []

b = (0, 1, 1, 1, 2, 2)
u = (1, 1, 2, 2, 2, 3)
o = (1, 2, 2, 3, 3, 4)
d = (0, 0, 0, 1, 1, 1)
means = {
    b: mean(b),
    u: mean(u),
    o: mean(o)
}


class Armor:
    def __init__(self, name, block=[], resist=[], dodge=[], blockMod=0, resistMod=0, canDodge=True, dodgeBonus=None, immunities=set()) -> None:
        armor.append(self)
        self.name = name
        self.block = block
        self.resist = resist
        self.dodge = dodge
        self.blockMod = blockMod
        self.resistMod = resistMod
        self.canDodge = canDodge
        self.dodgeBonus = dodgeBonus
        self.immunities = immunities
        self.expectedDamageBlock = dict()
        for x in range(1, 3):
            dodgeMod = 1 - (sum([1 for do in product(*dodge) if sum(do) >= x]) / len(list(product(*dodge))))
            self.expectedDamageBlock[x] = dict()
            for y in range(2, 7):
                self.expectedDamageBlock[x][y] = (y if not block else max([0, (y - mean(chain.from_iterable(block)))])) * dodgeMod
        self.expectedDamageResist = dict()
        for x in range(1, 3):
            dodgeMod = 1 - (sum([1 for do in product(*dodge) if sum(do) >= x]) / len(list(product(*dodge))))
            self.expectedDamageResist[x] = dict()
            for y in range(2, 7):
                self.expectedDamageResist[x][y] = (y if not resist else max([0, (y - mean(chain.from_iterable(resist)))])) * dodgeMod

Armor(name="Adventurer's Armour", block=[u], resist=[b], dodge=[d])
Armor(name="Adventurer's Armour (Legendary)", block=[u,u], resist=[o], dodge=[d])
Armor(name="Alonne Armour", resist=[b], dodge=[d,d])
Armor(name="Alonne Captain Armour", block=[b,b], resist=[u], dodge=[d])
Armor(name="Alonne Knight Armour", block=[u], resist=[b], dodge=[d])
Armor(name="Alva Armour", block=[u], resist=[u], dodge=[d, d])
Armor(name="Antiquated Robes", block=[b,b], blockMod=-1, resist=[b,b], resistMod=-1, dodge=[d])
Armor(name="Armour of Thorns", block=[b,u], resist=[b,b])
Armor(name="Archdeacon Robe", block=[o], resist=[b, o])
Armor(name="Assassin Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Black Armour", block=[u], resist=[b])
Armor(name="Black Hand Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Black Hand Armour (Thief)", block=[u], resist=[b], dodge=[d])
Armor(name="Black Iron Armour", block=[o], blockMod=-1, resist=[o], resistMod=-1)
Armor(name="Black Iron Armour (Legendary)", block=[o,o], blockMod=-2, resist=[o,o], resistMod=-2)
Armor(name="Black Leather Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Black Knight Armour", block=[u], resist=[u], dodge=[d])
Armor(name="Black Knight Armour (Legendary)", block=[b,u], resist=[b,u], dodge=[d])
Armor(name="Brass Armour", block=[b, b], resist=[b, b])
Armor(name="Catarina Armour", block=[b,b], resist=[b])
Armor(name="Catarina Armour (Legendary)", block=[u,u], resist=[u])
Armor(name="Cathedral Knight Armour", block=[u], resist=[b, b])
Armor(name="Chester's Set", block=[u], resist=[o], dodge=[d], immunities=set(["bleed"]))
Armor(name="Cleric Armour", block=[u], resist=[b,u])
Armor(name="Cleric Robes", block=[b], resist=[u])
Armor(name="Cornyx's Robes", block=[u], resist=[o])
Armor(name="Court Sorcerer Robes", block=[b], resist=[u], dodge=[d])
Armor(name="Crimson Robes", block=[b], resist=[b,b], dodge=[d])
Armor(name="Crimson Robes (Legendary)", block=[u], resist=[b,u], dodge=[d,d])
Armor(name="Dancer Armour", block=[b], resist=[b], dodge=[d,d])
Armor(name="Dark Armour", block=[b], resist=[b], dodge=[d], dodgeBonus="hollow")
Armor(name="Dark Armour (Legendary)", block=[o], resist=[o], dodge=[d], dodgeBonus="hollow")
Armor(name="Deacon Robes", block=[b], resist=[b,b], dodge=[d])
Armor(name="Deserter Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Dragonscale Armour", block=[b], resist=[b, u], dodge=[d])
Armor(name="Dragonslayer Armour", block=[b,u], resist=[b,u], immunities=set(["bleed"]))
Armor(name="Drang Armour", block=[u], dodge=[d])
Armor(name="Eastern Armour", block=[b, b], resist=[b, b], dodge=[d, d])
Armor(name="Elite Knight Armour", block=[u, u], resist=[b])
Armor(name="Embraced Armour of Favor", block=[u], resist=[b,b])
Armor(name="Embraced Armour of Favor (Legendary)", block=[u], resist=[u,u], dodge=[d])
Armor(name="Exile Armour", block=[u,u])
Armor(name="Fallen Knight Armour", block=[u], resist=[u], dodge=[d])
Armor(name="Faraam Armour", block=[o], resist=[u])
Armor(name="Firelink Armour", block=[u], resist=[u])
Armor(name="Gold-Hemmed Black Robes", block=[b], resist=[b,b], dodge=[d])
Armor(name="Gold-Hemmed Black Robes (Legendary)", block=[u], resist=[u,u], dodge=[d,d])
Armor(name="Guardian Armour", block=[b,b], resist=[b,b], immunities=set(["bleed"]))
Armor(name="Guardian Armour (Legendary)", block=[b,b], blockMod=1, resist=[b,b], resistMod=1, immunities=set(["bleed"]))
Armor(name="Hard Leather Armour", block=[b], resist=[b], dodge=[d,d])
Armor(name="Havel's Armour", block=[b,u], resist=[b,u], canDodge=False)
Armor(name="Havel's Armour (Legendary)", block=[b,o], resist=[b,o], canDodge=False)
Armor(name="Herald Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Hunter Armour", dodge=[d,d])
Armor(name="Knight Armour", block=[u], resist=[b])
Armor(name="Loincloth", resist=[b])
Armor(name="Lothric Knight Armour", block=[u], resist=[u])
Armor(name="Mask of the Child", block=[b], resist=[b], dodge=[d])
Armor(name="Master's Attire", dodge=[d,d])
Armor(name="Mirrah Armour", block=[u], resist=[o], dodge=[d])
Armor(name="Northern Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Old Ironclad Armour", block=[b,u], resist=[b,b])
Armor(name="Outrider Armour", block=[b,b], resist=[b])
Armor(name="Painting Guardian Armour", dodge=[d,d])
Armor(name="Paladin Armour", block=[o], resist=[o])
Armor(name="Pyromancer Garb", resist=[b, b], dodge=[d])
Armor(name="Royal Swordsman Armour", block=[b,b], resist=[u])
Armor(name="Sellsword Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Shadow Armour", dodge=[d, d])
Armor(name="Silver Knight Armour", block=[b,u], dodge=[d])
Armor(name="Smelter Demon Armour", block=[u,u], resist=[o])
Armor(name="Smough's Armour", block=[u,u], resist=[u,u], canDodge=False)
Armor(name="Sorcerer Robes", block=[b], resist=[u])
Armor(name="Steel Armour", block=[u], resist=[u])
Armor(name="Steel Armour (upgraded)", block=[u,b], resist=[u,b])
Armor(name="Stone Knight Armour", block=[o], resist=[u])
Armor(name="Sunless Armour", block=[u], resist=[b])
Armor(name="Sunset Armour", block=[b,b], resist=[b], dodge=[d])
Armor(name="Winged Knight Armour", block=[o], resist=[o])
Armor(name="Worker Armour", block=[b], resist=[b], dodge=[d])
Armor(name="Xanthous Robes", block=[b], resist=[u], dodge=[d])