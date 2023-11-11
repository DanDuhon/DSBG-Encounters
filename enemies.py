from json import dump
from os import path


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []


class Enemy:
    def __init__(self, name, expansion, numberOfModels, health, armor, resist, attacks, attackType, dodge, move, attackRange, attackEffect=[], difficulty=0) -> None:
        enemiesDict[name] = self
        enemies.append(self)
        self.name = name
        self.expansion = expansion
        self.numberOfModels = numberOfModels
        self.health = health
        self.armor = armor
        self.resist = resist
        self.attacks = attacks
        self.attackType = attackType
        self.dodge = dodge
        self.move = move
        self.attackRange = attackRange
        self.attackEffect = attackEffect
        self.difficulty = difficulty
        
        if "Hollow" in self.name and self.health == 1:
            self.gang = "Hollow"
        elif "Alonne" in self.name and self.health == 1:
            self.gang = "Alonne"
        elif "Skeleton" in self.name and self.health == 1:
            self.gang = "Skeleton"
        elif "Scarecrow" in self.name:
            self.gang = "Scarecrow"
        else:
            self.gang = None

        self.bleeding = False
        self.deaths = 0
        self.damageDone = 0
        self.bleedDamage = 0
        self.damagingAttacks = 0
        self.totalAttacks = 0
        self.loadoutDamage = {}
        self.imagePath = baseFolder + "\\images\\" + name + ".png"

        for i, m in enumerate(self.move):
            reach.append(m + self.attackRange[i])


    def reset(self):
        with open(baseFolder + "\\enemies\\" + self.name + ".json", "w") as enemyFile:
            dump({"deaths": 0, "totalAttacks": 0, "damagingAttacks": 0, "damageDone": 0, "bleedDamage": 0, "loadoutDamage": {}}, enemyFile)


Enemy(name="Alonne Bow Knight", expansion="Iron Keep", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[4], difficulty=111.75)
Enemy(name="Alonne Knight Captain", expansion="Iron Keep", numberOfModels=3, health=5, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficulty=479.48)
Enemy(name="Alonne Sword Knight", expansion="Iron Keep", numberOfModels=3, health=1, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=130.05)
Enemy(name="Black Hollow Mage", expansion="Executioner Chariot", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=557.57)
Enemy(name="Bonewheel Skeleton", expansion="Painted World of Ariamis", numberOfModels=2, health=1, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=100.49)
Enemy(name="Crossbow Hollow", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=1, resist=0, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=45.02)
Enemy(name="Crow Demon", expansion="Painted World of Ariamis", numberOfModels=2, health=5, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=591.94)
Enemy(name="Demonic Foliage", expansion="Darkroot", numberOfModels=2, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=113.27)
Enemy(name="Engorged Zombie", expansion="Painted World of Ariamis", numberOfModels=2, health=1, armor=2, resist=2, attacks=[4], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty=115.2)
Enemy(name="Falchion Skeleton", expansion="Executioner Chariot", numberOfModels=2, health=1, armor=1, resist=1, attacks=[3], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[2], attackRange=[0], difficulty=56.02)
Enemy(name="Firebomb Hollow", expansion="Explorers", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3], attackType=["magic"], dodge=1, move=[1], attackRange=[2], difficulty=47.65)
Enemy(name="Giant Skeleton Archer", expansion="Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], dodge=2, move=[0, 0], attackRange=[0, 4], difficulty=414.31)
Enemy(name="Giant Skeleton Soldier", expansion="Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], dodge=1, move=[1, 1], attackRange=[0, 1], difficulty=253.87)
Enemy(name="Hollow Soldier", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=34.76)
Enemy(name="Ironclad Soldier", expansion="Iron Keep", numberOfModels=3, health=5, armor=3, resist=2, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=464.27)
Enemy(name="Large Hollow Soldier", expansion="Dark Souls The Board Game", numberOfModels=2, health=5, armor=1, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=114.11)
Enemy(name="Mushroom Child", expansion="Darkroot", numberOfModels=1, health=5, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=145.01)
Enemy(name="Mushroom Parent", expansion="Darkroot", numberOfModels=1, health=10, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=341.81)
Enemy(name="Necromancer", expansion="Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=2, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=205.7)
Enemy(name="Phalanx", expansion="Painted World of Ariamis", numberOfModels=1, health=5, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=233.09)
Enemy(name="Phalanx Hollow", expansion="Painted World of Ariamis", numberOfModels=5, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=34.76)
Enemy(name="Plow Scarecrow", expansion="Darkroot", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty=109.08)
Enemy(name="Sentinel", expansion="Dark Souls The Board Game", numberOfModels=2, health=10, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=778.12)
Enemy(name="Shears Scarecrow", expansion="Darkroot", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3,3], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=60.49)
Enemy(name="Silver Knight Greatbowman", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=2, resist=0, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=90.76)
Enemy(name="Silver Knight Spearman", expansion="Explorers", numberOfModels=3, health=1, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[1], difficulty=113.69)
Enemy(name="Silver Knight Swordsman", expansion="Dark Souls The Board Game", numberOfModels=3, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=161.85)
Enemy(name="Skeleton Archer", expansion="Tomb of Giants", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=77.34)
Enemy(name="Skeleton Beast", expansion="Tomb of Giants", numberOfModels=1, health=5, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=431.7)
Enemy(name="Skeleton Soldier", expansion="Tomb of Giants", numberOfModels=3, health=1, armor=2, resist=1, attacks=[2], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=21.69)
Enemy(name="Snow Rat", expansion="Painted World of Ariamis", numberOfModels=2, health=1, armor=0, resist=1, attacks=[3], attackType=["physical"], attackEffect=["poison"], dodge=1, move=[4], attackRange=[0], difficulty=63.61)
Enemy(name="Stone Guardian", expansion="Darkroot", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4,5], attackType=["physical", "physical"], dodge=1, move=[1, 1], attackRange=[0, 0], difficulty=412.2)
Enemy(name="Stone Knight", expansion="Darkroot", numberOfModels=2, health=5, armor=3, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty=737.67)
Enemy(name="Standard Invader/Hungry Mimic", expansion=None, numberOfModels=0, health=0, armor=0, resist=0, attacks=[0], attackType=["physical"], dodge=0, move=[0], attackRange=[0], difficulty=0)
Enemy(name="Advanced Invader/Voracious Mimic", expansion=None, numberOfModels=0, health=0, armor=0, resist=0, attacks=[0], attackType=["physical"], dodge=0, move=[0], attackRange=[0], difficulty=0)
Enemy(name="Mimic", expansion="The Sunless City", numberOfModels=1, health=5, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty=513.34)
Enemy(name="Crossbow Hollow (TSC)", expansion="The Sunless City", numberOfModels=3, health=1, armor=1, resist=0, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=45.02)
Enemy(name="Hollow Soldier (TSC)", expansion="The Sunless City", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=34.76)
Enemy(name="Sentinel (TSC)", expansion="The Sunless City", numberOfModels=1, health=10, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=778.12)
Enemy(name="Silver Knight Greatbowman (TSC)", expansion="The Sunless City", numberOfModels=2, health=1, armor=2, resist=0, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=90.76)
Enemy(name="Silver Knight Swordsman (TSC)", expansion="The Sunless City", numberOfModels=2, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=161.85)

# Enemy(name="Hungry Mimic - Raking Slash", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Hungry Mimic - Heavy Punch", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Hungry Mimic - Leaping Spin Kick", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Hungry Mimic - Stomping Kick", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Hungry Mimic - Charging Chomp", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[3,4], attackType=["physical","physical"], dodge=3, move=[3,0], attackRange=[0,0], difficulty=0)
# Enemy(name="Hungry Mimic - Vicous Chomp", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[0], difficulty=0)
# Enemy(name="Hungry Mimic - Aggressive Grab", expansion="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Voracious Mimic - Raking Slash", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Voracious Mimic - Heavy Punch", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Voracious Mimic - Leaping Spin Kick", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Voracious Mimic - Stomping Kick", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[7], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Voracious Mimic - Charging Chomp", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[3,5], attackType=["physical","physical"], dodge=3, move=[3,0], attackRange=[0,0], difficulty=0)
# Enemy(name="Voracious Mimic - Vicous Chomp", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[7], attackType=["physical"], dodge=2, move=[0], attackRange=[0], difficulty=0)
# Enemy(name="Voracious Mimic - Aggressive Grab", expansion="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Melinda the Butcher - Double Smash", expansion="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[3,3], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Melinda the Butcher - Cleaving Strikes", expansion="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[4,4], attackType=["physical","physical"], dodge=1, move=[0,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Melinda the Butcher - Jumping Cleave", expansion="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[3,3,3], attackType=["physical","physical","physical"], dodge=1, move=[0,4,4], attackRange=[0,0,0], difficulty=0)
# Enemy(name="Melinda the Butcher - Greataxe Sweep", expansion="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Melinda the Butcher - Sweeping Advance", expansion="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[4,4], attackType=["physical", "physical"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)

# Enemy(name="Maldron the Assassin - Greatlance Lunge", expansion="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Maldron the Assassin - Double Lance Lunge", expansion="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[4,4], attackType=["physical","physical"], dodge=2, move=[1,1], attackRange=[1,1], difficulty=0)
# Enemy(name="Maldron the Assassin - Leaping Lance Strike", expansion="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Maldron the Assassin - Jousting Charge", expansion="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=3, move=[2], attackRange=[1], difficulty=0)
# Enemy(name="Maldron the Assassin - Corrosive Urn Toss", expansion="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[3], attackType=["magic"], attackEffect=["poison"], dodge=2, move=[0], attackRange=[4], difficulty=0)

# Enemy(name="Oliver the Collector - Bone Fist Punches", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4,4], attackType=["physical","physical"], dodge=2, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Oliver the Collector - Minotaur Helm Charge", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Oliver the Collector - Puzzling Stone Sword Strike", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Oliver the Collector - Majestic Greatsword Slash", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Oliver the Collector - Santier's Spear Lunge", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Oliver the Collector - Smelter Hammer Whirlwind", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4,4,4], attackType=["physical","physical","physical"], dodge=1, move=[0,0,0], attackRange=[1,1,1], difficulty=0)
# Enemy(name="Oliver the Collector - Ricard's Rapier Thrust", expansion="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[1], difficulty=0)

# Enemy(name="Xanthous King Jeremiah - Great Chaos Fireball", expansion="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Chaos Fire Whip", expansion="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[4], attackType=["magic"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Chaos Storm", expansion="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[3,3], attackType=["magic","magic"], dodge=2, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Firey Retreat", expansion="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Whiplash", expansion="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Kirk, Knight of Thorns - Forward Roll", expansion="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[3,3], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Shield Bash", expansion="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Shield Charge", expansion="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Overhead Chop", expansion="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Barbed Sword Thrust", expansion="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[0], attackRange=[1], difficulty=0)

# Enemy(name="Maneater Mildred - Death Blow", expansion="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Maneater Mildred - Executioner Strike", expansion="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Maneater Mildred - Guillotine", expansion="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Maneater Mildred - Butcher Chop", expansion="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Maneater Mildred - Butchery", expansion="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Paladin Leeroy - Advancing Grant Slam", expansion="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Paladin Leeroy - Grant Slam Withdrawal", expansion="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Paladin Leeroy - Sanctus Shield Slam", expansion="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Paladin Leeroy - Sanctus Shield Dash", expansion="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[4,4], attackType=["physical","physical"], dodge=2, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Paladin Leeroy - Wrath of the Gods", expansion="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[1], difficulty=0)

# Enemy(name="Armorer Dennis - toughness only", expansion="Phantoms", numberOfModels=0, health=16, armor=1, resist=2, attacks=[], attackType=[], dodge=1, move=[], attackRange=[], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Spear Launch", expansion="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Greatsword", expansion="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[6], attackType=["magic"], dodge=1, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Vortex", expansion="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[4,4], attackType=["magic","magic"], dodge=1, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Flash", expansion="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[4], attackType=["magic"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Armorer Dennis - Upward Slash", expansion="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Spear Launch", expansion="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Greatsword", expansion="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[6], attackType=["magic"], dodge=2, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Vortex", expansion="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[4,4], attackType=["magic","magic"], dodge=2, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Flash", expansion="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[4], attackType=["magic"], dodge=3, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Upward Slash", expansion="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)

# Enemy(name="Invader Brylex - Leaping Strike", expansion="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[7], attackType=["physical"], dodge=1, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Invader Brylex - Blade Dervish", expansion="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[4,4], attackRange=[0,0], difficulty=0)
# Enemy(name="Invader Brylex - Trampling Charge", expansion="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[4,4,4], attackType=["physical","physical","physical"], dodge=1, move=[1,1,1], attackRange=[0,0,0], difficulty=0)
# Enemy(name="Invader Brylex - Fire Surge", expansion="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Invader Brylex - Fire Whip", expansion="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[6], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Marvelous Chester - Crossbow Volley", expansion="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Marvelous Chester - Crossbow Snipe", expansion="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=4, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Marvelous Chester - Throwing Knife Volley", expansion="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[4,4], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=2, move=[0,0], attackRange=[2,2], difficulty=0)
# Enemy(name="Marvelous Chester - Throwing Knife Flurry", expansion="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[3,3,3], attackType=["physical","physical","physical"], attackEffect=["bleed","bleed","bleed"], dodge=1, move=[0,0,0], attackRange=[2,2,2], difficulty=0)
# Enemy(name="Marvelous Chester - Spinning Low Kick", expansion="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)

# Enemy(name="Longfinger Kirk - Rolling Barbs", expansion="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[4,4], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Longfinger Kirk - Lunging Stab", expansion="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Longfinger Kirk - Cleave", expansion="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[6], attackType=["physical"], attackEffect=["bleed"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Longfinger Kirk - Crushing Blow", expansion="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=3, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Longfinger Kirk - Barbed Sword Strikes", expansion="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[5,5], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=1, move=[0,0], attackRange=[1,1], difficulty=0)

# Enemy(name="Fencer Sharron - Puzzling Stone Sword Charge", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Puzzling Stone Sword Whip", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Fencer Sharron - Spider Fang Sword Strike", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Spider Fang Sword Charge", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Spider Fang Web Blast", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Fencer Sharron - Dual Sword Slash", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Dual Sword Assault", expansion="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)

for i, enemy in enumerate(enemiesDict):
    enemyIds[i] = enemiesDict[enemy]
    enemiesDict[enemy].id = i