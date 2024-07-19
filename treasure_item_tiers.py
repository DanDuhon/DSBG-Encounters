from math import floor
from characters import mean_soul_cost, soulCost
from json import dump
from os import path


treasures = {
    "Abyss Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Adventurer's Armour": {"expansions": set(["Characters Expansion", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 14, "dexterity": 22, "intelligence": 14, "faith": 0},
    "Adventurer's Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "tiersPossible": set([1,2,3]), "character": None, "strength": 22, "dexterity": 32, "intelligence": 22, "faith": 0},
    "Aged Smelter Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 33, "dexterity": 0, "intelligence": 33, "faith": 0},
    "Alonne Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 21, "intelligence": 35, "faith": 0},
    "Alonne Captain Armour": {"expansions": set(["Iron Keep"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 25, "dexterity": 0, "intelligence": 25, "faith": 0},
    "Alonne Greatbow": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
    "Alonne Knight Armour": {"expansions": set(["Iron Keep"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 0, "intelligence": 20, "faith": 0},
    "Alva Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Assassin", "tiersPossible": set([2,3]), "strength": 24, "dexterity": 38, "intelligence": 24, "faith": 0},
    "Antiquated Robes": {"expansions": set(["Darkroot"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 20},
    "Assassin Armour": {"expansions": set(), "type": "armor", "character": "Assassin", "strength": 10, "dexterity": 14, "intelligence": 0, "faith": 0},
    "Archdeacon Robe": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Cleric", "tiersPossible": set([2,3]), "strength": 17, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Armour of Thorns": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 32, "dexterity": 18, "intelligence": 0, "faith": 0},
    "Aural Decoy": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 0},
    "Avelyn": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 30, "intelligence": 23, "faith": 0},
    "Balder Side Sword": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([2,3]), "strength": 33, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Bandit Knife": {"expansions": set(), "type": "weapon", "character": "Thief", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Battle Axe": {"expansions": set(), "type": "weapon", "character": "Warrior", "strength": 14, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Bewitched Alonne Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 24, "intelligence": 18, "faith": 0},
    "Black Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Black Bow of Pharis": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Black Firebombs": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 20},
    "Black Hand Armour (Thief)": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "armor", "character": "Thief", "tiersPossible": set([1,2]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
    "Black Hand Armour": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Black Iron Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 12},
    "Black Iron Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 32, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Black Iron Greatshield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "tiersPossible": set([2,3]), "strength": 27, "dexterity": 37, "intelligence": 17, "faith": 0},
    "Black Knight Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 26, "dexterity": 16, "intelligence": 0, "faith": 16},
    "Black Knight Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 32, "dexterity": 22, "intelligence": 0, "faith": 22},
    "Black Knight Greataxe": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 0, "intelligence": 20, "faith": 20},
    "Black Knight Halberd": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 32, "dexterity": 0, "intelligence": 0, "faith": 18},
    "Black Knight Shield (Deprived)": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "tiersPossible": set([2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Black Knight Shield (Black Knight)": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 24, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Black Knight Sword": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Black Leather Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Mercenary", "tiersPossible": set([1,2]), "strength": 24, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Blacksteel Katana": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Blessed Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Blinding Bolt": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 40},
    "Blood Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Bloodshield": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Blue Tearstone Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgradeArmor", "character": "Knight", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 25, "intelligence": 0, "faith": 25},
    "Blue Wooden Shield": {"expansions": set(), "type": "weapon", "character": "Cleric", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Bonewheel Shield": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 25, "dexterity": 15, "intelligence": 0, "faith": 0},
    "Bountiful Light": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Bountiful Sunlight": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 20, "faith": 35},
    "Brass Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Deprived", "tiersPossible": set([1,2]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Brigand Axe": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 19, "dexterity": 0, "intelligence": 16, "faith": 0},
    "Broadsword": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "tiersPossible": set([1,2]), "strength": 30, "dexterity": 28, "intelligence": 0, "faith": 0},
    "Broken Straight Sword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "tiersPossible": set([1,2]), "strength": 20, "dexterity": 20, "intelligence": 0, "faith": 0},
    "Buckler": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 20, "intelligence": 10, "faith": 0},
    "Butcher Knife": {"expansions": set(), "type": "weapon", "character": None, "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Caduceus Shield": {"expansions": set(), "type": "weapon", "character": "Pyromancer", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Caestus": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Calamity Ring": {"expansions": set(), "type": "upgradeArmor", "character": None, "tiersPossible": set([3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Carthus Curved Greatsword": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 30, "intelligence": 19, "faith": 0},
    "Carthus Curved Sword": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 35, "intelligence": 25, "faith": 0},
    "Carthus Flame Arc": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "upgradeWeapon", "character": "Pyromancer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Carthus Milkring": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgradeArmor", "character": "Deprived", "tiersPossible": set([2,3]), "strength": 24, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Catarina Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 22, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Catarina Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Cathedral Knight Armour": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "armor", "character": "Herald", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 18, "faith": 22},
    "Chariot Lance": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 22, "dexterity": 33, "intelligence": 22, "faith": 0},
    "Chester's Set": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 20, "intelligence": 30, "faith": 0},
    "Chloranthy Ring": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgradeArmor", "character": None, "tiersPossible": set([1,2,3]), "strength": 18, "dexterity": 18, "intelligence": 18, "faith": 18},
    "Claws": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Claymore": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 30, "dexterity": 26, "intelligence": 0, "faith": 0},
    "Cleric Armour": {"expansions": set(["Tomb of Giants"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Cleric's Candlestick": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 21, "intelligence": 0, "faith": 29},
    "Cleric Robes": {"expansions": set(), "type": "armor", "character": "Cleric", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 12},
    "Club": {"expansions": set(), "type": "weapon", "character": "Deprived", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Composite Bow": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([1,2]), "strength": 15, "dexterity": 21, "intelligence": 0, "faith": 0},
    "Cornyx's Robes": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "armor", "character": "Pyromancer", "tiersPossible": set([1,2]), "strength": 21, "dexterity": 0, "intelligence": 21, "faith": 0},
    "Court Sorcerer Robes": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 17, "intelligence": 22, "faith": 0},
    "Crescent Moon Sword": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 17, "intelligence": 0, "faith": 17},
    "Cresent Axe": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 22, "dexterity": 17, "intelligence": 0, "faith": 15},
    "Crest Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "tiersPossible": set([1,2]), "strength": 16, "dexterity": 22, "intelligence": 0, "faith": 0},
    "Crimson Robes": {"expansions": set(["Characters Expansion", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 12, "intelligence": 22, "faith": 12},
    "Crimson Robes (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 0, "dexterity": 22, "intelligence": 32, "faith": 22},
    "Crystal Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 0},
    "Crystal Hail": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 25, "intelligence": 35, "faith": 0},
    "Crystal Magic Weapon": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgradeWeapon", "character": "Sorcerer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Crystal Shield": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 28},
    "Crystal Straight Sword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 21, "faith": 0},
    "Cursed Greatsword of Artorias": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 24, "dexterity": 14, "intelligence": 14, "faith": 14},
    "Dancer Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 35, "intelligence": 25, "faith": 25},
    "Dancer's Enchanted Swords": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
    "Dark Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 20, "intelligence": 20, "faith": 0},
    "Dark Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 0, "dexterity": 28, "intelligence": 28, "faith": 0},
    "Dark Silver Tracer": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 25, "intelligence": 20, "faith": 0},
    "Dark Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 30, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Deacon Robes": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Demon Titanite": {"expansions": set(["Painted World of Ariamis"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 10, "faith": 10},
    "Demon's Great Hammer": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 24, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Deserter Armour": {"expansions": set(), "type": "armor", "character": "Thief", "strength": 0, "dexterity": 13, "intelligence": 10, "faith": 0},
    "Drake Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 27, "dexterity": 17, "intelligence": 17, "faith": 0},
    "Drakewing Ultra Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 0, "dexterity": 33, "intelligence": 23, "faith": 0},
    "Dragon Crest Shield": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 21},
    "Dragon King Greataxe": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 33, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Dragon Tooth": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 37, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Dragonrider Bow": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 0},
    "Dragonscale Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Sorcerer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 23, "intelligence": 23, "faith": 0},
    "Dragonslayer Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Dragonslayer Greatbow": {"expansions": set(["Explorers", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 23, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Dragonslayer Spear": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 27},
    "Dragonslayer's Axe": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 15, "intelligence": 15, "faith": 15},
    "Drang Armour": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 18, "dexterity": 14, "intelligence": 0, "faith": 0},
    "Drang Hammers": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "tiersPossible": set([2,3]), "strength": 33, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Dung Pie": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Dusk Crown Ring": {"expansions": set(["Darkroot"]), "type": "upgradeArmor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "East-West Shield": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 28, "faith": 0},
    "Eastern Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Mercenary", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
    "Eastern Iron Shield": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 28, "intelligence": 0, "faith": 0},
    "Effigy Shield": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 10, "dexterity": 0, "intelligence": 0, "faith": 10},
    "Elite Knight Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Elkhorn Round Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([2,3]), "strength": 16, "dexterity": 34, "intelligence": 16, "faith": 0},
    "Embraced Armour of Favour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Embraced Armour of Favour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 33},
    "Estoc": {"expansions": set(), "type": "weapon", "character": "Assassin", "strength": 0, "dexterity": 14, "intelligence": 0, "faith": 0},
    "Exile Armour": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 26, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Exile Greatsword": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Falchion": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "tiersPossible": set([2,3]), "strength": 37, "dexterity": 30, "intelligence": 0, "faith": 23},
    "Fallen Knight Armour": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "armor", "character": "Warrior", "tiersPossible": set([2,3]), "strength": 30, "dexterity": 0, "intelligence": 22, "faith": 0},
    "Faraam Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "tiersPossible": set([2,3]), "strength": 29, "dexterity": 0, "intelligence": 19, "faith": 0},
    "Faron Flashsword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgradeWeapon", "character": "Sorcerer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 15},
    "Fire Surge": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([1,2]), "strength": 22, "dexterity": 0, "intelligence": 26, "faith": 0},
    "Fire Whip": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 34, "faith": 18},
    "Fireball": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 23, "faith": 0},
    "Firebombs": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 15},
    "Firelink Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Flameberge": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Four Kings Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 0, "dexterity": 24, "intelligence": 24, "faith": 30},
    "Four-Pronged Plow": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Fume Ultra Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 37, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Gargoyle Tail Axe": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 25, "dexterity": 25, "intelligence": 0, "faith": 0},
    "Gargoyle's Halberd": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Gargoyle's Shield": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 25},
    "Giant's Halberd": {"expansions": set(["Explorers", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Giant Stone Axe": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 34, "dexterity": 24, "intelligence": 0, "faith": 0},
    "Gold Tracer": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 35, "intelligence": 25, "faith": 0},
    "Gold-Hemmed Black Robes": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 14, "intelligence": 14, "faith": 14},
    "Gold-Hemmed Black Robes (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 0, "dexterity": 28, "intelligence": 28, "faith": 28},
    "Golden Ritual Spear": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 24, "faith": 21},
    "Golden Wing Crest Shield": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([1,2]), "strength": 26, "dexterity": 0, "intelligence": 0, "faith": 26},
    "Gotthard Twinswords": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 25, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Grass Crest Shield": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([2,3]), "strength": 28, "dexterity": 0, "intelligence": 0, "faith": 28},
    "Gravelord Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 32, "intelligence": 18, "faith": 0},
    "Gravelord Sword Dance": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Great Chaos Fireball": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 37, "faith": 27},
    "Great Club": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Great Combustion": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 26, "faith": 22},
    "Great Heal": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 40},
    "Great Mace": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 28},
    "Great Machete": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([2,3]), "strength": 40, "dexterity": 35, "intelligence": 0, "faith": 0},
    "Great Magic Weapon": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 12},
    "Great Scythe": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 32, "dexterity": 21, "intelligence": 0, "faith": 0},
    "Great Wooden Hammer": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Greataxe": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 32, "dexterity": 22, "intelligence": 0, "faith": 0},
    "Greatshield of Artorias": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 23, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Greatsword of Artorias": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 24, "dexterity": 20, "intelligence": 20, "faith": 20},
    "Guardian Armour": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 22, "intelligence": 22, "faith": 0},
    "Guardian Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 0, "dexterity": 28, "intelligence": 28, "faith": 0},
    "Halberd": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 18, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Hand Axe": {"expansions": set(), "type": "weapon", "character": "Pyromancer", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Hard Leather Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 26, "dexterity": 26, "intelligence": 26, "faith": 0},
    "Havel's Armour": {"expansions": set(["Characters Expansion", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 23, "dexterity": 0, "intelligence": 23, "faith": 0},
    "Havel's Armour (Legendary)": {"expansions": set(["Characters Expansion"]), "type": "armor", "character": None, "strength": 27, "dexterity": 0, "intelligence": 27, "faith": 0},
    "Havel's Greatshield": {"expansions": set(["Explorers", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 35, "dexterity": 0, "intelligence": 13, "faith": 13},
    "Hawkwood's Shield": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "tiersPossible": set([2,3]), "strength": 23, "dexterity": 33, "intelligence": 0, "faith": 23},
    "Heal": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Heal Aid": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 13},
    "Heavy Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 25, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Herald Armour": {"expansions": set(), "type": "armor", "character": "Herald", "strength": 10, "dexterity": 0, "intelligence": 0, "faith": 10},
    "Hollow Soldier Shield": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 16, "dexterity": 0, "intelligence": 0, "faith": 19},
    "Homing Crystal Soulmass": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 40, "faith": 0},
    "Hornet Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgradeArmor", "character": "Assassin", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Hunter Armour": {"expansions": set(["Darkroot"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 34, "intelligence": 17, "faith": 0},
    "Immolation Tinder": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 28, "faith": 21},
    "Irithyll Straight Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 23, "dexterity": 0, "intelligence": 23, "faith": 0},
    "Irithyll Rapier": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 24, "intelligence": 24, "faith": 0},
    "Iron King Hammer": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 34, "dexterity": 23, "intelligence": 23, "faith": 0},
    "Iron Round Shield": {"expansions": set(), "type": "weapon", "character": "Thief", "strength": 0, "dexterity": 10, "intelligence": 10, "faith": 0},
    "Kite Shield (Herald)": {"expansions": set(), "type": "weapon", "character": "Herald", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Kite Shield": {"expansions": set(), "type": "weapon", "character": "Knight", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Knight Armour": {"expansions": set(), "type": "armor", "character": "Knight", "strength": 12, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Knight Slayer's Ring": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "upgradeArmor", "character": "Warrior", "tiersPossible": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Kukris": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 15, "intelligence": 0, "faith": 0},
    "Large Leather Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "tiersPossible": set([2,3]), "strength": 17, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Leather Shield": {"expansions": set(), "type": "weapon", "character": "Sorcerer", "strength": 0, "dexterity": 12, "intelligence": 0, "faith": 0},
    "Life Ring": {"expansions": set(["Iron Keep"]), "type": "upgradeArmor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Lifehunt Scythe": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 32, "intelligence": 23, "faith": 0},
    "Lightning Gem": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Loincloth": {"expansions": set(), "type": "armor", "character": "Deprived", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Longbow": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 18, "intelligence": 0, "faith": 0},
    "Long Sword": {"expansions": set(), "type": "weapon", "character": "Knight", "strength": 13, "dexterity": 12, "intelligence": 0, "faith": 0},
    "Lothric Knight Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Knight", "tiersPossible": set([1,2]), "strength": 21, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Lothric Knight Greatsword": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 20, "intelligence": 13, "faith": 13},
    "Lothric's Holy Sword": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([1,2]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Lucerne": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 31, "intelligence": 31, "faith": 0},
    "Mace": {"expansions": set(), "type": "weapon", "character": "Cleric", "strength": 12, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Magic Barrier": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 24},
    "Magic Shield": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 27, "faith": 14},
    "Magic Stoneplate Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgradeArmor", "character": "Cleric", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 32},
    "Mail Breaker": {"expansions": set(), "type": "weapon", "character": "Sorcerer", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Man Serpent Hatchet": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 0},
    "Mannikin Claws": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 24, "intelligence": 24, "faith": 0},
    "Manus Catalyst": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 26, "dexterity": 0, "intelligence": 26, "faith": 0},
    "Mask of the Child": {"expansions": set(["Tomb of Giants"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 19, "faith": 13},
    "Master's Attire": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 30, "intelligence": 18, "faith": 0},
    "Med Heal": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Melinda's Greataxe": {"expansions": set(["The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 34, "dexterity": 17, "intelligence": 0, "faith": 0},
    "Mirrah Armour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "armor", "character": "Deprived", "tiersPossible": set([2,3]), "strength": 27, "dexterity": 0, "intelligence": 0, "faith": 27},
    "Moonlight Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 21, "dexterity": 21, "intelligence": 31, "faith": 0},
    "Morion Blade": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 24, "dexterity": 24, "intelligence": 0, "faith": 0},
    "Morne's Great Hammer": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Morning Star": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 16, "dexterity": 0, "intelligence": 0, "faith": 19},
    "Murakumo": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 27, "intelligence": 17, "faith": 0},
    "Northern Armour": {"expansions": set(), "type": "armor", "character": "Warrior", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Notched Whip": {"expansions": set(["The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 33, "intelligence": 0, "faith": 0},
    "Obscuring Ring": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "upgradeArmor", "character": "Thief", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 28, "intelligence": 0, "faith": 20},
    "Obsidian Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 33},
    "Old Dragonslayer Spear": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Old Ironclad Armour": {"expansions": set(["Iron Keep"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 34, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Old Leo Ring": {"expansions": set(), "type": "upgradeArmor", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 18, "intelligence": 18, "faith": 0},
    "Onikiri And Ubadachi": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 36, "intelligence": 26, "faith": 0},
    "Outrider Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 24, "intelligence": 0, "faith": 24},
    "Painting Guardian Armour": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 32, "intelligence": 14, "faith": 0},
    "Painting Guardian Curved Sword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Deprived", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 26, "intelligence": 26, "faith": 26},
    "Paladin Armour": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 24, "dexterity": 24, "intelligence": 0, "faith": 24},
    "Parrying Dagger": {"expansions": set(["Explorers", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 21, "intelligence": 21, "faith": 21},
    "Partizan": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([2,3]), "strength": 28, "dexterity": 17, "intelligence": 0, "faith": 35},
    "Phoenix Parma Shield": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Pierce Shield": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 16, "dexterity": 10, "intelligence": 0, "faith": 0},
    "Pike": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 23},
    "Plank Shield": {"expansions": set(), "type": "weapon", "character": "Deprived", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Poison Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 15, "intelligence": 0, "faith": 0},
    "Poison Mist": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 11, "intelligence": 16, "faith": 0},
    "Poison Throwing Knives": {"expansions": set(["Explorers", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 14, "intelligence": 14, "faith": 0},
    "Pontiff's Left Eye": {"expansions": set(), "type": "upgradeArmor", "character": None, "tiersPossible": set([3]), "strength": 0, "dexterity": 0, "intelligence": 21, "faith": 21},
    "Porcine Shield": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 24, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Priscilla's Dagger": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 31, "faith": 0},
    "Pursuer's Greatshield": {"expansions": set(), "type": "weapon", "character": None, "strength": 38, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Pursuer's Ultra Greatsword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Pursuers": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 0, "dexterity": 0, "intelligence": 35, "faith": 0},
    "Pyromancer Flame": {"expansions": set(), "type": "weapon", "character": "Pyromancer", "strength": 0, "dexterity": 0, "intelligence": 14, "faith": 0},
    "Pyromancer Garb": {"expansions": set(), "type": "armor", "character": "Pyromancer", "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 0},
    "Rapier": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 21, "intelligence": 21, "faith": 0},
    "Rapport": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 36, "faith": 0},
    "Raw Gem": {"expansions": set(["Explorers", "The Sunless City"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Red and White Round Shield": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 10},
    "Red Tearstone Ring": {"expansions": set(["Painted World of Ariamis"]), "type": "upgradeArmor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Reinforced Club": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 23, "dexterity": 0, "intelligence": 0, "faith": 16},
    "Replenishment": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Ring of Favour": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgradeArmor", "character": "Mercenary", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 21, "intelligence": 0, "faith": 21},
    "Rotten Ghru Dagger": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 17, "intelligence": 17, "faith": 0},
    "Rotten Ghru Spear": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 21, "intelligence": 12, "faith": 0},
    "Round Shield": {"expansions": set(), "type": "weapon", "character": "Warrior", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Royal Dirk": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 31, "intelligence": 0, "faith": 31},
    "Royal Swordsman Armour": {"expansions": set(["The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set[1,2,3], "strength": 24, "dexterity": 0, "intelligence": 14, "faith": 14},
    "Sacred Chime": {"expansions": set(), "type": "weapon", "character": "Cleric", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 14},
    "Sacred Oath": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 14, "faith": 30},
    "Saint Bident": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Herald", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 35},
    "Sanctum Priestess Tiara": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 27, "faith": 27},
    "Sanctus": {"expansions": set(), "type": "weapon", "tiersPossible": set([2,3]), "character": None, "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 33},
    "Santier's Spear": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 20, "dexterity": 30, "intelligence": 0, "faith": 0},
    "Scimitar": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 20, "intelligence": 18, "faith": 0},
    "Sellsword Armour": {"expansions": set(), "type": "armor", "character": "Mercenary", "strength": 0, "dexterity": 16, "intelligence": 8, "faith": 0},
    "Sellsword Twinblade": {"expansions": set(), "type": "weapon", "character": "Mercenary", "strength": 0, "dexterity": 12, "intelligence": 0, "faith": 0},
    "Shadow Armour": {"expansions": set(["Dark Souls The Board Game"]), "type": "armor", "character": "Assassin", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 34, "intelligence": 0, "faith": 17},
    "Sharp Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 25, "intelligence": 0, "faith": 0},
    "Shield Crossbow": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Shortbow": {"expansions": set(), "type": "weapon", "character": "Thief", "strength": 0, "dexterity": 12, "intelligence": 0, "faith": 0},
    "Shortsword": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 15, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Shotel": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 29, "intelligence": 26, "faith": 0},
    "Silver Eagle Kite Shield": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Silver Knight Armour": {"expansions": set(["Explorers"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 26, "dexterity": 26, "intelligence": 0, "faith": 0},
    "Silver Knight Shield": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([1,2]), "strength": 31, "dexterity": 23, "intelligence": 0, "faith": 0},
    "Silver Knight Spear": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 22, "intelligence": 0, "faith": 26},
    "Silver Knight Straight Sword": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 20, "intelligence": 20, "faith": 20},
    "Simple Gem": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 15},
    "Skull Lantern": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 13, "intelligence": 14, "faith": 0},
    "Small Leather Shield": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Thief", "tiersPossible": set([1,2]), "strength": 15, "dexterity": 30, "intelligence": 0, "faith": 15},
    "Smelter Demon Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 21},
    "Smelter Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Smough's Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 37, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Smough's Hammer": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 37, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Soothing Sunlight": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 38},
    "Sorcerer's Catalyst": {"expansions": set(), "type": "weapon", "character": "Sorcerer", "strength": 0, "dexterity": 0, "intelligence": 16, "faith": 0},
    "Sorcerer Robes": {"expansions": set(), "type": "armor", "character": "Sorcerer", "strength": 0, "dexterity": 0, "intelligence": 12, "faith": 0},
    "Sorcerer's Staff": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 15, "dexterity": 0, "intelligence": 30, "faith": 0},
    "Soul Arrow": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 16, "faith": 0},
    "Soul Greatsword": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 0, "intelligence": 35, "faith": 15},
    "Soul Spear": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 25, "faith": 15},
    "Soulstream": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 22, "faith": 0},
    "Spear": {"expansions": set(), "type": "weapon", "character": "Herald", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Spider Shield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "tiersPossible": set([1,2]), "strength": 27, "dexterity": 0, "intelligence": 15, "faith": 0},
    "Spiked Mace": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([1,2]), "strength": 32, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Spiked Shield": {"expansions": set(), "type": "weapon", "character": None, "strength": 22, "dexterity": 12, "intelligence": 0, "faith": 0},
    "Spitfire Spear": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 33},
    "Spotted Whip": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 30, "intelligence": 23, "faith": 0},
    "Steel Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 21, "dexterity": 21, "intelligence": 20, "faith": 20},
    "Stone Greataxe": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 35, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Stone Greatshield": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 33, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Stone Greatsword": {"expansions": set(["Darkroot"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 22, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Stone Knight Armour": {"expansions": set(["Darkroot"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Stone Parma": {"expansions": set(["Characters Expansion", "Tomb of Giants", "The Sunless City"]), "type": "weapon", "character": "Pyromancer", "tiersPossible": set([2,3]), "strength": 15, "dexterity": 0, "intelligence": 35, "faith": 0},
    "Sun Princess Ring": {"expansions": set(["Dark Souls The Board Game"]), "type": "upgradeArmor", "character": "Knight", "tiersPossible": set([1,2]), "strength": 30, "dexterity": 0, "intelligence": 0, "faith": 25},
    "Sunless Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 13, "dexterity": 0, "intelligence": 0, "faith": 13},
    "Sunlight Shield": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 30},
    "Sunlight Straight Sword": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 15, "dexterity": 15, "intelligence": 0, "faith": 30},
    "Sunset Armour": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Sunset Shield": {"expansions": set(["Characters Expansion", "Tomb of Giants"]), "type": "weapon", "character": "Cleric", "tiersPossible": set([1,2]), "strength": 15, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Talisman": {"expansions": set(), "type": "weapon", "character": "Herald", "strength": 12, "dexterity": 0, "intelligence": 0, "faith": 12},
    "Target Shield": {"expansions": set(), "type": "weapon", "character": "Assassin", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Thorolund Talisman": {"expansions": set(["Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 31},
    "Thrall Axe": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 16, "dexterity": 16, "intelligence": 0, "faith": 0},
    "Throwing Knives": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 14, "intelligence": 12, "faith": 0},
    "Tiny Being's Ring": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "upgradeArmor", "character": "Herald", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 20},
    "Titanite Catch Pole": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 28, "dexterity": 22, "intelligence": 0, "faith": 0},
#    "Titanite Shard": {"expansions": set(), "type": "upgradeWeapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Torch": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Sorcerer", "tiersPossible": set([1,2]), "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Tower Shield": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 25, "dexterity": 16, "intelligence": 0, "faith": 22},
    "Twin Dragon Greatshield": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Knight", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 35, "intelligence": 15, "faith": 15},
    "Uchigatana": {"expansions": set(["Explorers"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 32, "intelligence": 0, "faith": 14},
    "Umbral Dagger": {"expansions": set(["Dark Souls The Board Game"]), "type": "weapon", "character": "Assassin", "tiersPossible": set([2,3]), "strength": 0, "dexterity": 35, "intelligence": 35, "faith": 0},
    "Velka's Rapier": {"expansions": set(["Painted World of Ariamis"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 19, "intelligence": 27, "faith": 0},
    "Vordt's Great Hammer": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([3]), "strength": 33, "dexterity": 0, "intelligence": 33, "faith": 0},
    "Warden Twinblades": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "weapon", "character": "Mercenary", "tiersPossible": set([1,2]), "strength": 17, "dexterity": 25, "intelligence": 17, "faith": 0},
    "Warpick": {"expansions": set(["Dark Souls The Board Game", "The Sunless City"]), "type": "weapon", "character": "Warrior", "tiersPossible": set([2,3]), "strength": 35, "dexterity": 25, "intelligence": 0, "faith": 0},
    "Washing Pole": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 0, "dexterity": 37, "intelligence": 0, "faith": 21},
    "Winged Knight Armour": {"expansions": set(), "type": "armor", "character": None, "tiersPossible": set([2,3]), "strength": 24, "dexterity": 0, "intelligence": 0, "faith": 24},
    "Winged Knight Halberd": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 32, "dexterity": 16, "intelligence": 16, "faith": 16},
    "Winged Knight Twin Axes": {"expansions": set(), "type": "weapon", "character": None, "tiersPossible": set([2,3]), "strength": 30, "dexterity": 34, "intelligence": 0, "faith": 0},
    "Winged Spear": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 20, "dexterity": 0, "intelligence": 0, "faith": 22},
    "Witch's Locks": {"expansions": set(["Iron Keep"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 31, "faith": 0},
    "Wolf Ring": {"expansions": set(["Characters Expansion", "Painted World of Ariamis"]), "type": "upgradeArmor", "character": "Mercenary", "tiersPossible": set([2,3]), "strength": 25, "dexterity": 35, "intelligence": 25, "faith": 0},
    "Wooden Shield": {"expansions": set(), "type": "weapon", "character": "Mercenary", "strength": 0, "dexterity": 0, "intelligence": 0, "faith": 0},
    "Worker Armour": {"expansions": set(["Dark Souls The Board Game", "Painted World of Ariamis", "The Sunless City"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 12, "dexterity": 12, "intelligence": 12, "faith": 12},
    "Xanthous Robes": {"expansions": set(["Painted World of Ariamis"]), "type": "armor", "character": None, "tiersPossible": set([1,2,3]), "strength": 0, "dexterity": 0, "intelligence": 23, "faith": 20},
    "Zweihander": {"expansions": set(["Dark Souls The Board Game", "Tomb of Giants"]), "type": "weapon", "character": None, "tiersPossible": set([1,2,3]), "strength": 35, "dexterity": 25, "intelligence": 0, "faith": 0},
}

tiers = {
    "armor": {},
    "weapon": {},
    "upgradeArmor": {},
    "upgradeWeapon": {}
}


def generate_treasure_soul_cost(setsAvailable, charactersActive):
    maxStr = max([len(soulCost[c]["strength"]) for c in charactersActive])
    maxDex = max([len(soulCost[c]["dexterity"]) for c in charactersActive])
    maxInt = max([len(soulCost[c]["intelligence"]) for c in charactersActive])
    maxFai = max([len(soulCost[c]["faith"]) for c in charactersActive])

    #i = progress.progressVar.get()

    for t in [t for t in treasures if not treasures[t]["character"] or treasures[t]["character"] in charactersActive]:
        # Don't attempt to calculate soul cost for items that can't be equipped by anyone in the party.
        if any([
            treasures[t]["strength"] > maxStr,
            treasures[t]["dexterity"] > maxDex,
            treasures[t]["intelligence"] > maxInt,
            treasures[t]["faith"] > maxFai
            ]):
            continue

        treasures[t]["soulCost"] = mean_soul_cost(treasures[t], setsAvailable, charactersActive)

        stats = [
            ("strength", treasures[t]["strength"]),
            ("dexterity", treasures[t]["dexterity"]),
            ("intelligence", treasures[t]["intelligence"]),
            ("faith", treasures[t]["faith"])
        ]
        
        stats.sort(key=lambda x: x[1], reverse=True)
        treasures[t]["statOrder"] = [
            set(s[0] for s in stats if s[1] == stats[0][1]),
            set(s[0] for s in stats if s[1] == stats[1][1]),
            set(s[0] for s in stats if s[1] == stats[2][1]),
            set(s[0] for s in stats if s[1] == stats[3][1])
        ]

    
def populate_treasure_tiers(character):
    armor = sorted([t for t in treasures if (
        treasures[t]["type"] == "armor"
        and ((
                not treasures[t]["character"]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[0] & soulCost[list(character)[0]]["statOrder"][0]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[1] & soulCost[list(character)[0]]["statOrder"][1]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[2] & soulCost[list(character)[0]]["statOrder"][2]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[3] & soulCost[list(character)[0]]["statOrder"][3]
            ) or {treasures[t]["character"],} == character)
        and "soulCost" in treasures[t])
        ], key=lambda x: treasures[x]["soulCost"])
    armorLen = len(armor)
    weapon = sorted([t for t in treasures if (
        treasures[t]["type"] == "weapon"
        and ((
                not treasures[t]["character"]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[0] & soulCost[list(character)[0]]["statOrder"][0]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[1] & soulCost[list(character)[0]]["statOrder"][1]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[2] & soulCost[list(character)[0]]["statOrder"][2]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[3] & soulCost[list(character)[0]]["statOrder"][3]
            ) or {treasures[t]["character"],} == character)
        and "soulCost" in treasures[t])
        ], key=lambda x: treasures[x]["soulCost"])
    weaponLen = len(weapon)
    upgradeArmor = [t for t in treasures if (
        treasures[t]["type"] == "upgradeArmor"
        and ((
                not treasures[t]["character"]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[0] & soulCost[list(character)[0]]["statOrder"][0]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[1] & soulCost[list(character)[0]]["statOrder"][1]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[2] & soulCost[list(character)[0]]["statOrder"][2]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[3] & soulCost[list(character)[0]]["statOrder"][3]
            ) or {treasures[t]["character"],} == character)
        and "soulCost" in treasures[t])
        ]
    upgradeWeapon = [t for t in treasures if (
        treasures[t]["type"] == "upgradeWeapon"
        and ((
                not treasures[t]["character"]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[0] & soulCost[list(character)[0]]["statOrder"][0]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[1] & soulCost[list(character)[0]]["statOrder"][1]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[2] & soulCost[list(character)[0]]["statOrder"][2]
                and treasures[t].get("statOrder", [set(), set(), set(), set()])[3] & soulCost[list(character)[0]]["statOrder"][3]
            ) or {treasures[t]["character"],} == character)
        and "soulCost" in treasures[t])
        ]

    # Split the treasures into 3 nearly-equal tiers based on soul cost.
    tiers["armor"][1] = [a for a in armor[:floor(armorLen/3)] if 1 in treasures[a].get("tiersPossible", {1, 2, 3})]
    tiers["armor"][2] = ([a for a in armor[floor(armorLen/3):floor(armorLen/3)*2] if 2 in treasures[a].get("tiersPossible", {1, 2, 3})]
                         + [a for a in armor[:floor(armorLen/3)] if 1 not in treasures[a].get("tiersPossible", {1, 2, 3}) and 2 in treasures[a].get("tiersPossible", {1, 2, 3})])
    tiers["armor"][3] = ([a for a in armor[floor(armorLen/3)*2:] if 3 in treasures[a].get("tiersPossible", {1, 2, 3})]
                         + [a for a in armor[:floor(armorLen/3)] if 1 not in treasures[a].get("tiersPossible", {1, 2, 3}) and 2 not in treasures[a].get("tiersPossible", {1, 2, 3})]
                         + [a for a in armor[floor(armorLen/3):floor(armorLen/3)*2] if 2 not in treasures[a].get("tiersPossible", {1, 2, 3}) and 3 in treasures[a].get("tiersPossible", {1, 2, 3})])

    tiers["weapon"][1] = [w for w in weapon[:floor(weaponLen/3)] if 1 in treasures[w].get("tiersPossible", {1, 2, 3})]
    tiers["weapon"][2] = ([w for w in weapon[floor(weaponLen/3):floor(weaponLen/3)*2] if 2 in treasures[w].get("tiersPossible", {1, 2, 3})]
                         + [w for w in weapon[:floor(weaponLen/3)] if 1 not in treasures[w].get("tiersPossible", {1, 2, 3}) and 2 in treasures[w].get("tiersPossible", {1, 2, 3})])
    tiers["weapon"][3] = ([w for w in weapon[floor(weaponLen/3)*2:] if 3 in treasures[w].get("tiersPossible", {1, 2, 3})]
                         + [w for w in weapon[:floor(weaponLen/3)] if 1 not in treasures[w].get("tiersPossible", {1, 2, 3}) and 2 not in treasures[w].get("tiersPossible", {1, 2, 3})]
                         + [w for w in weapon[floor(weaponLen/3):floor(weaponLen/3)*2] if 2 not in treasures[w].get("tiersPossible", {1, 2, 3}) and 3 in treasures[w].get("tiersPossible", {1, 2, 3})])

    a[c]["upgradeArmor"] = upgradeArmor

    a[c]["upgradeWeapon"] = upgradeWeapon + ["Titanite Shard", "Titanite Shard"]

    # Push the tier back to the treasure.
    for treasure in treasures:
        if any([treasure in set(tiers["armor"][1]), treasure in set(tiers["weapon"][1])]):
            treasures[treasure]["tier"] = 1
        elif any([treasure in set(tiers["armor"][2]), treasure in set(tiers["weapon"][2])]):
            treasures[treasure]["tier"] = 2
        elif any([treasure in set(tiers["armor"][3]), treasure in set(tiers["weapon"][3])]):
            treasures[treasure]["tier"] = 3
        else:
            treasures[treasure]["tier"] = 0

    
def populate_treasure_tiers_deprived():
    armor = sorted([t for t in treasures if (
        treasures[t]["type"] == "armor"
        and ((
                not treasures[t]["character"]
                and ((len(treasures[t].get("statOrder", [set(), set(), set(), set()])[0]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[0])]))
                    or (len(treasures[t].get("statOrder", [set(), set(), set(), set()])[1]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[1])]))
                    or (len(treasures[t].get("statOrder", [set(), set(), set(), set()])[2]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[2])]))
                    or (len(treasures[t].get("statOrder", [set(), set(), set(), set()])[3]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[3])]))
                    or [treasures[t]["strength"], treasures[t]["dexterity"], treasures[t]["intelligence"], treasures[t]["faith"]].count(0) <= 1)
            ) or treasures[t]["character"] == "Deprived")
        and "soulCost" in treasures[t])
        ], key=lambda x: treasures[x]["soulCost"])
    armorLen = len(armor)
    weapon = sorted([t for t in treasures if (
        treasures[t]["type"] == "weapon"
        and ((
                not treasures[t]["character"]
                and ((len(treasures[t].get("statOrder", [set(), set(), set(), set()])[0]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[0])]))
                    or (len(treasures[t].get("statOrder", [set(), set(), set(), set()])[1]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[1])]))
                    or (len(treasures[t].get("statOrder", [set(), set(), set(), set()])[2]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[2])]))
                    or (len(treasures[t].get("statOrder", [set(), set(), set(), set()])[3]) > 1 and all([treasures[t][s] > 0 for s in list(treasures[t].get("statOrder", [[], [], [], []])[3])]))
                    or [treasures[t]["strength"], treasures[t]["dexterity"], treasures[t]["intelligence"], treasures[t]["faith"]].count(0) <= 1)
            ) or treasures[t]["character"] == "Deprived")
        and "soulCost" in treasures[t])
        ], key=lambda x: treasures[x]["soulCost"])
    weaponLen = len(weapon)
    upgradeArmor = [t for t in treasures if (
        treasures[t]["type"] == "upgradeArmor"
        and ((
                not treasures[t]["character"]
            ) or treasures[t]["character"] == "Deprived")
        and "soulCost" in treasures[t])
        ]
    upgradeWeapon = [t for t in treasures if (
        treasures[t]["type"] == "upgradeWeapon"
        and ((
                not treasures[t]["character"]
            ) or treasures[t]["character"] == "Deprived")
        and "soulCost" in treasures[t])
        ]

    # Split the treasures into 3 nearly-equal tiers based on soul cost.
    tiers["armor"][1] = [a for a in armor[:floor(armorLen/3)] if 1 in treasures[a].get("tiersPossible", {1, 2, 3})]
    tiers["armor"][2] = ([a for a in armor[floor(armorLen/3):floor(armorLen/3)*2] if 2 in treasures[a].get("tiersPossible", {1, 2, 3})]
                         + [a for a in armor[:floor(armorLen/3)] if 1 not in treasures[a].get("tiersPossible", {1, 2, 3}) and 2 in treasures[a].get("tiersPossible", {1, 2, 3})])
    tiers["armor"][3] = ([a for a in armor[floor(armorLen/3)*2:] if 3 in treasures[a].get("tiersPossible", {1, 2, 3})]
                         + [a for a in armor[:floor(armorLen/3)] if 1 not in treasures[a].get("tiersPossible", {1, 2, 3}) and 2 not in treasures[a].get("tiersPossible", {1, 2, 3})]
                         + [a for a in armor[floor(armorLen/3):floor(armorLen/3)*2] if 2 not in treasures[a].get("tiersPossible", {1, 2, 3}) and 3 in treasures[a].get("tiersPossible", {1, 2, 3})])

    tiers["weapon"][1] = [w for w in weapon[:floor(weaponLen/3)] if 1 in treasures[w].get("tiersPossible", {1, 2, 3})]
    tiers["weapon"][2] = ([w for w in weapon[floor(weaponLen/3):floor(weaponLen/3)*2] if 2 in treasures[w].get("tiersPossible", {1, 2, 3})]
                         + [w for w in weapon[:floor(weaponLen/3)] if 1 not in treasures[w].get("tiersPossible", {1, 2, 3}) and 2 in treasures[w].get("tiersPossible", {1, 2, 3})])
    tiers["weapon"][3] = ([w for w in weapon[floor(weaponLen/3)*2:] if 3 in treasures[w].get("tiersPossible", {1, 2, 3})]
                         + [w for w in weapon[:floor(weaponLen/3)] if 1 not in treasures[w].get("tiersPossible", {1, 2, 3}) and 2 not in treasures[w].get("tiersPossible", {1, 2, 3})]
                         + [w for w in weapon[floor(weaponLen/3):floor(weaponLen/3)*2] if 2 not in treasures[w].get("tiersPossible", {1, 2, 3}) and 3 in treasures[w].get("tiersPossible", {1, 2, 3})])

    a["Deprived"]["upgradeArmor"] = upgradeArmor

    a["Deprived"]["upgradeWeapon"] = upgradeWeapon + ["Titanite Shard", "Titanite Shard"]

    # Push the tier back to the treasure.
    for treasure in treasures:
        if any([treasure in set(tiers["armor"][1]), treasure in set(tiers["weapon"][1])]):
            treasures[treasure]["tier"] = 1
        elif any([treasure in set(tiers["armor"][2]), treasure in set(tiers["weapon"][2])]):
            treasures[treasure]["tier"] = 2
        elif any([treasure in set(tiers["armor"][3]), treasure in set(tiers["weapon"][3])]):
            treasures[treasure]["tier"] = 3
        else:
            treasures[treasure]["tier"] = 0

baseFolder = path.dirname(__file__)
a = {}
for c in ["Assassin", "Cleric", "Herald", "Knight", "Mercenary", "Pyromancer", "Sorcerer", "Thief", "Warrior"]:
    if c not in a:
        a[c] = {"armor": {}, "weapon": {}, "upgradeArmor": {}, "upgradeWeapon": {}}
    generate_treasure_soul_cost({"Darkroot", "Executioner Chariot", "Manus, Father of the Abyss", "Painted World of Ariamis", "Gaping Dragon", "Iron Keep", "Asylum Demon", "The Last Giant", "The Sunless City", "Black Dragon Kalameet", "Old Iron King", "Characters Expansion", "Phantoms", "Dark Souls The Board Game", "Guardian Dragon", "Explorers", "Tomb of Giants", "Vordt of the Boreal Valley", "The Four Kings"}, set([c]))
    populate_treasure_tiers(set([c]))
    for x in range(1, 4):
        a[c]["armor"][x] = [t for t in treasures if treasures[t]["type"] == "armor" and treasures[t]["tier"] == x]
        a[c]["weapon"][x] = [t for t in treasures if treasures[t]["type"] == "weapon" and treasures[t]["tier"] == x]

a["Deprived"] = {"armor": {}, "weapon": {}, "upgradeArmor": {}, "upgradeWeapon": {}}
generate_treasure_soul_cost({"Darkroot", "Executioner Chariot", "Manus, Father of the Abyss", "Painted World of Ariamis", "Gaping Dragon", "Iron Keep", "Asylum Demon", "The Last Giant", "The Sunless City", "Black Dragon Kalameet", "Old Iron King", "Characters Expansion", "Phantoms", "Dark Souls The Board Game", "Guardian Dragon", "Explorers", "Tomb of Giants", "Vordt of the Boreal Valley", "The Four Kings"}, {"Deprived",})
populate_treasure_tiers_deprived()
for x in range(1, 4):
    a["Deprived"]["armor"][x] = [t for t in treasures if treasures[t]["type"] == "armor" and treasures[t]["tier"] == x]
    a["Deprived"]["weapon"][x] = [t for t in treasures if treasures[t]["type"] == "weapon" and treasures[t]["tier"] == x]

# with open(baseFolder + "\\tiers.json", "w") as f:
#     dump(a, f)
