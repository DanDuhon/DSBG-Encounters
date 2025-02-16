from statistics import mean
from item_tier import itemTier


handItems = []
handItemTiers = {
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


class HandItem:
    def __init__(self, name, block=[], resist=[], dodge=[], blockMod=0, resistMod=0, twoHanded=False, canUseWithTwoHanded=False, canDodge=True, immunities=set()) -> None:
        if name not in itemTier:
            return
        handItems.append(self)
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
        self.tier = itemTier[name]
        handItemTiers[self.tier].append(self)


HandItem(name=None, canUseWithTwoHanded=True)
HandItem(name="Abyss Greatsword", twoHanded=True, block=[b], resist=[b])
HandItem(name="Aged Smelter Sword", twoHanded=True, block=[b], resist=[u])
HandItem(name="Alonne Greatbow", twoHanded=True)
HandItem(name="Atonement")
HandItem(name="Aural Decoy")
HandItem(name="Avelyn", twoHanded=True, dodge=[d])
HandItem(name="Balder Side Sword", resist=[b])
HandItem(name="Bandit Knife")
HandItem(name="Battle Axe")
HandItem(name="Bewitched Alonne Sword", twoHanded=True)
HandItem(name="Black Bow of Pharis", twoHanded=True, dodge=[d])
HandItem(name="Black Firebombs")
HandItem(name="Black Iron Greatshield", block=[u], resist=[u, u])
HandItem(name="Black Knight Greataxe", twoHanded=True, block=[b])
HandItem(name="Black Knight Shield (Deprived)", block=[b], dodge=[d])
HandItem(name="Black Knight Shield", block=[u], resist=[b])
HandItem(name="Black Knight Halberd", twoHanded=True, block=[b], resist=[u])
HandItem(name="Black Knight Sword")
HandItem(name="Blacksteel Katana")
HandItem(name="Blinding Bolt")
HandItem(name="Bloodshield", block=[u], resist=[b], immunities=set(["bleed", "poison"]))
HandItem(name="Blue Wooden Shield", block=[b])
HandItem(name="Bonewheel Shield", block=[u])
HandItem(name="Bountiful Light")
HandItem(name="Bountiful Sunlight")
HandItem(name="Brigand Axe", resist=[b])
HandItem(name="Broadsword", block=[b], resist=[b])
HandItem(name="Broken Straight Sword")
HandItem(name="Buckler", canUseWithTwoHanded=True, block=[b], dodge=[d])
HandItem(name="Butcher Knife")
HandItem(name="Caduceus Round Shield", block=[u])
HandItem(name="Caestus")
HandItem(name="Carthus Curved Greatsword", twoHanded=True, dodge=[d])
HandItem(name="Carthus Curved Sword", dodge=[d])
HandItem(name="Chariot Lance", block=[b])
HandItem(name="Claws", twoHanded=True)
HandItem(name="Claymore", twoHanded=True, block=[b])
HandItem(name="Cleric's Candlestick")
HandItem(name="Club")
HandItem(name="Composite Bow", twoHanded=True, dodge=[d])
HandItem(name="Crescent Axe")
HandItem(name="Crescent Moon Sword")
HandItem(name="Crest Shield", block=[b], dodge=[d])
HandItem(name="Crystal Hail")
HandItem(name="Crystal Shield", block=[b], immunities=set(["bleed", "poison"]))
HandItem(name="Crystal Straight Sword")
HandItem(name="Cursed Greatsword of Artorias", twoHanded=True, block=[b], resist=[u])
HandItem(name="Dancer's Enchanted Swords", twoHanded=True, dodge=[d])
HandItem(name="Dark Silver Tracer")
HandItem(name="Dark Sword")
HandItem(name="Demon's Great Hammer", twoHanded=True)
HandItem(name="Dragon Crest Shield", block=[u], resist=[u])
HandItem(name="Dragon King Greataxe", twoHanded=True, block=[b], resist=[o])
HandItem(name="Dragon Tooth", twoHanded=True, block=[b], resist=[u])
HandItem(name="Dragonrider Bow", twoHanded=True, dodge=[d])
HandItem(name="Dragonslayer Greatbow", twoHanded=True)
HandItem(name="Dragonslayer Spear")
HandItem(name="Dragonslayer's Axe", resist=[b])
HandItem(name="Drake Sword")
HandItem(name="Drakewing Ultra Greatsword", twoHanded=True, dodge=[d])
HandItem(name="Drang Hammers", twoHanded=True, resist=[b], dodge=[d])
HandItem(name="Dung Pie")
HandItem(name="East-West Shield", block=[b], resist=[u], dodge=[d])
HandItem(name="Eastern Iron Shield", block=[u], dodge=[d])
HandItem(name="Effigy Shield", canUseWithTwoHanded=True, block=[b], resist=[b])
HandItem(name="Elkhorn Round Shield", canUseWithTwoHanded=True, block=[b], resist=[b, b], dodge=[d])
HandItem(name="Estoc")
HandItem(name="Exile Greatsword", twoHanded=True, block=[b], resist=[b])
HandItem(name="Falchion", block=[b], resist=[u])
HandItem(name="Fire Surge")
HandItem(name="Fire Whip")
HandItem(name="Fireball")
HandItem(name="Firebombs")
HandItem(name="Flamberge", twoHanded=True, dodge=[d])
HandItem(name="Force")
HandItem(name="Four Kings Sword", block=[b], resist=[b])
HandItem(name="Four-Pronged Plow", twoHanded=True, block=[b], resist=[b])
HandItem(name="Fume Ultra Greatsword", twoHanded=True, block=[u], resist=[b])
HandItem(name="Gargoyle Tail Axe", twoHanded=True, resist=[b])
HandItem(name="Gargoyle's Halberd", twoHanded=True, block=[b])
HandItem(name="Gargoyle's Shield", block=[b], resist=[u,u])
HandItem(name="Giant Stone Axe", twoHanded=True, block=[u], resist=[u])
HandItem(name="Giant's Halberd", twoHanded=True, block=[u])
HandItem(name="Gold Tracer")
HandItem(name="Golden Ritual Spear", resist=[b])
HandItem(name="Golden Wing Crest Shield", block=[u], resist=[u])
HandItem(name="Gotthard Twinswords", twoHanded=True, block=[b], resist=[b])
HandItem(name="Grass Crest Shield", block=[u], resist=[o])
HandItem(name="Gravelord Sword", twoHanded=True, block=[u])
HandItem(name="Gravelord Sword Dance")
HandItem(name="Greataxe", twoHanded=True, block=[u])
HandItem(name="Great Chaos Fireball")
HandItem(name="Great Club", twoHanded=True, block=[b], resist=[b])
HandItem(name="Great Combustion")
HandItem(name="Great Heal")
HandItem(name="Great Mace", twoHanded=True, block=[b], resist=[b])
HandItem(name="Great Machete", twoHanded=True, block=[b], resist=[b])
HandItem(name="Great Magic Weapon")
HandItem(name="Great Scythe", twoHanded=True, block=[b], resist=[b])
HandItem(name="Great Wooden Hammer", twoHanded=True, block=[b])
HandItem(name="Greatshield of Artorias", block=[o], resist=[u], immunities=set(["bleed", "poison"]))
HandItem(name="Greatsword", twoHanded=True, block=[b], resist=[b])
HandItem(name="Greatsword of Artorias", twoHanded=True, block=[u], resist=[o])
HandItem(name="Halberd", twoHanded=True, block=[u])
HandItem(name="Hand Axe")
HandItem(name="Havel's Greatshield", block=[o,b], resist=[u])
HandItem(name="Hawkwood's Shield", canUseWithTwoHanded=True, block=[u], resist=[u], dodge=[d])
HandItem(name="Heal")
HandItem(name="Heal Aid")
HandItem(name="Hollow Soldier Shield", block=[b], resist=[b])
HandItem(name="Homing Crystal Soulmass")
HandItem(name="Immolation Tinder", twoHanded=True, resist=[b])
HandItem(name="Irithyll Rapier", block=[b])
HandItem(name="Irithyll Straight Sword")
HandItem(name="Iron King Hammer", block=[b], resist=[b])
HandItem(name="Iron Round Shield", canUseWithTwoHanded=True, dodge=[d])
HandItem(name="Kite Shield", block=[b])
HandItem(name="Kukris")
HandItem(name="Large Leather Shield", block=[u], resist=[b], dodge=[d])
HandItem(name="Leather Shield", resist=[b], dodge=[d])
HandItem(name="Lifehunt Scythe", twoHanded=True, block=[u], resist=[b])
HandItem(name="Long Sword")
HandItem(name="Longbow", twoHanded=True)
HandItem(name="Lothric Knight Greatsword", twoHanded=True, block=[b])
HandItem(name="Lothric's Holy Sword", resist=[b])
HandItem(name="Lucerne", twoHanded=True, block=[b], resist=[b], dodge=[d])
HandItem(name="Mace", resist=[b])
HandItem(name="Magic Barrier", resist=[u])
HandItem(name="Magic Shield", block=[b], resist=[o])
HandItem(name="Mail Breaker")
HandItem(name="Man Serpent Hatchet")
HandItem(name="Mannikin Claws", twoHanded=True)
HandItem(name="Manus Catalyst", resist=[b])
HandItem(name="Med Heal")
HandItem(name="Melinda's Greataxe", twoHanded=True, block=[b], resist=[b])
HandItem(name="Moonlight Greatsword", twoHanded=True, block=[b])
HandItem(name="Morion Blade")
HandItem(name="Morne's Great Hammer", twoHanded=True, block=[b, b], resist=[b, b])
HandItem(name="Morning Star", resist=[b])
HandItem(name="Murakamo", dodge=[d])
HandItem(name="Notched Whip")
HandItem(name="Obsidian Greatsword", twoHanded=True, block=[u], resist=[u])
HandItem(name="Old Dragonslayer Spear")
HandItem(name="Onikiri and Ubadachi", twoHanded=True, dodge=[d])
HandItem(name="Painting Guardian's Curved Sword")
HandItem(name="Parrying Dagger", block=[b], dodge=[d])
HandItem(name="Partizan", twoHanded=True, block=[u], resist=[b])
HandItem(name="Phoenix Parma Shield", canUseWithTwoHanded=True, resist=[b], dodge=[d])
HandItem(name="Pierce Shield", block=[b])
HandItem(name="Pike", twoHanded=True, block=[b])
HandItem(name="Poison Mist")
HandItem(name="Poison Throwing Knives")
HandItem(name="Porcine Shield", block=[b], resist=[b])
HandItem(name="Priscilla's Dagger", dodge=[d])
HandItem(name="Pursuer's Greatshield", block=[b,o])
HandItem(name="Pursuer's Ultra Greatsword", twoHanded=True, block=[b], resist=[u])
HandItem(name="Pursuers")
HandItem(name="Pyromancy Flame")
HandItem(name="Rapier", block=[b])
HandItem(name="Red and White Round Shield", canUseWithTwoHanded=True, block=[b], resist=[b,b])
HandItem(name="Reinforced Club")
HandItem(name="Replenishment")
HandItem(name="Rotten Ghru Dagger")
HandItem(name="Rotten Ghru Spear")
HandItem(name="Round Shield", block=[b])
HandItem(name="Royal Dirk", block=[b], resist=[b], dodge=[d])
HandItem(name="Sacred Chime")
HandItem(name="Sacred Oath", block=[u])
HandItem(name="Saint Bident", block=[b], resist=[b])
HandItem(name="Sanctus", block=[u], resist=[b,b])
HandItem(name="Santier's Spear", twoHanded=True)
HandItem(name="Scimitar")
HandItem(name="Sellsword Twinblades", twoHanded=True)
HandItem(name="Shield Crossbow", twoHanded=True, block=[u], resist=[u])
HandItem(name="Shortbow", twoHanded=True)
HandItem(name="Shortsword")
HandItem(name="Shotel", dodge=[d])
HandItem(name="Silver Eagle Kite Shield", block=[u])
HandItem(name="Silver Knight Shield", block=[u])
HandItem(name="Silver Knight Spear", resist=[b])
HandItem(name="Silver Knight Straight Sword", dodge=[d])
HandItem(name="Skull Lantern", dodge=[d])
HandItem(name="Small Leather Shield", canUseWithTwoHanded=True, block=[b], resist=[b], dodge=[d])
HandItem(name="Smelter Sword", twoHanded=True, block=[b])
HandItem(name="Smough's Hammer", twoHanded=True)
HandItem(name="Soothing Sunlight")
HandItem(name="Sorcerer's Catalyst")
HandItem(name="Sorcerer's Staff", twoHanded=True, resist=[u], dodge=[d])
HandItem(name="Soul Arrow")
HandItem(name="Soul Greatsword")
HandItem(name="Soul Spear")
HandItem(name="Soulstream")
HandItem(name="Spear")
HandItem(name="Spider Shield", block=[b, b], immunities=set(["poison"]))
HandItem(name="Spiked Mace", twoHanded=True, block=[b], resist=[b])
HandItem(name="Spiked Shield", block=[b], resist=[b])
HandItem(name="Spitfire Spear", block=[b], resist=[u])
HandItem(name="Spotted Whip", dodge=[d])
HandItem(name="Stone Greataxe", twoHanded=True, block=[b], resist=[b])
HandItem(name="Stone Greatshield", block=[u], resist=[o,b], canDodge=False)
HandItem(name="Stone Greatsword", twoHanded=True, block=[b])
HandItem(name="Stone Parma", block=[u], resist=[u])
HandItem(name="Sunlight Shield", block=[b,b], resist=[b])
HandItem(name="Sunlight Straight Sword")
HandItem(name="Sunset Shield", block=[b], resist=[u])
HandItem(name="Talisman")
HandItem(name="Target Shield", dodge=[d])
HandItem(name="Thorolund Talisman", dodge=[d])
HandItem(name="Thrall Axe")
HandItem(name="Titanite Catch Pole", block=[b])
HandItem(name="Torch")
HandItem(name="Tower Shield", block=[u], resist=[u], canDodge=False)
HandItem(name="Twin Dragon Greatshield", block=[u, u], resist=[u])
HandItem(name="Uchigatana", dodge=[d])
HandItem(name="Umbral Dagger", dodge=[d])
HandItem(name="Velka's Rapier", dodge=[d])
HandItem(name="Vordt's Great Hammer", twoHanded=True, block=[b], resist=[b,b])
HandItem(name="Warpick")
HandItem(name="Warden Twinblades", twoHanded=True, block=[b])
HandItem(name="Washing Pole", twoHanded=True, dodge=[d])
HandItem(name="Winged Knight Halberd", twoHanded=True, block=[u])
HandItem(name="Winged Knight Twin Axes", twoHanded=True, dodge=[d])
HandItem(name="Winged Spear", twoHanded=True, block=[b], resist=[b])
HandItem(name="Witch's Locks", resist=[b])
HandItem(name="Wooden Shield", dodge=[d])
HandItem(name="Zweihander", twoHanded=True, block=[b])
