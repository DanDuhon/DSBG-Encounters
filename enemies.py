from json import dump
from os import path


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []


class Enemy:
    def __init__(self, name, set, numberOfModels, health, armor, resist, attacks, attackType, dodge, move, attackRange, attackEffect=[], difficulty=0) -> None:
        enemiesDict[name] = self
        enemies.append(self)
        self.name = name
        self.set = set
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
        
        if "Hollow" in self.name:
            self.group = "Hollow"
        elif "Alonne" in self.name:
            self.group = "Alonne"
        elif "Skeleton" in self.name:
            self.group = "Skeleton"
        elif "Scarecrow" in self.name:
            self.group = "Scarecrow"
        elif "Silver Knight" in self.name:
            self.group = "Silver Knight"
        else:
            self.group = None

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


Enemy(name="Alonne Bow Knight", set="Iron Keep", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[4], difficulty=111.75)
Enemy(name="Alonne Knight Captain", set="Iron Keep", numberOfModels=3, health=5, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficulty=479.48)
Enemy(name="Alonne Sword Knight", set="Iron Keep", numberOfModels=3, health=1, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=130.05)
Enemy(name="Black Hollow Mage", set="Executioner Chariot", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=557.57)
Enemy(name="Bonewheel Skeleton", set="Painted World of Ariamis", numberOfModels=2, health=1, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=100.49)
Enemy(name="Crossbow Hollow", set="Dark Souls The Board Game", numberOfModels=3, health=1, armor=1, resist=0, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=45.02)
Enemy(name="Crow Demon", set="Painted World of Ariamis", numberOfModels=2, health=5, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=591.94)
Enemy(name="Demonic Foliage", set="Darkroot", numberOfModels=2, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=113.27)
Enemy(name="Engorged Zombie", set="Painted World of Ariamis", numberOfModels=2, health=1, armor=2, resist=2, attacks=[4], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty=115.2)
Enemy(name="Falchion Skeleton", set="Executioner Chariot", numberOfModels=2, health=1, armor=1, resist=1, attacks=[3], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[2], attackRange=[0], difficulty=56.02)
Enemy(name="Firebomb Hollow", set="Explorers", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3], attackType=["magic"], dodge=1, move=[1], attackRange=[2], difficulty=47.65)
Enemy(name="Giant Skeleton Archer", set="Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], dodge=2, move=[0, 0], attackRange=[0, 4], difficulty=414.31)
Enemy(name="Giant Skeleton Soldier", set="Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], dodge=1, move=[1, 1], attackRange=[0, 1], difficulty=253.87)
Enemy(name="Hollow Soldier", set="Dark Souls The Board Game", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=34.76)
Enemy(name="Ironclad Soldier", set="Iron Keep", numberOfModels=3, health=5, armor=3, resist=2, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=464.27)
Enemy(name="Large Hollow Soldier", set="Dark Souls The Board Game", numberOfModels=2, health=5, armor=1, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=114.11)
Enemy(name="Mushroom Child", set="Darkroot", numberOfModels=1, health=5, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=145.01)
Enemy(name="Mushroom Parent", set="Darkroot", numberOfModels=1, health=10, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=341.81)
Enemy(name="Necromancer", set="Tomb of Giants", numberOfModels=2, health=5, armor=1, resist=2, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=205.7)
Enemy(name="Phalanx", set="Painted World of Ariamis", numberOfModels=1, health=5, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=233.09)
Enemy(name="Phalanx Hollow", set="Painted World of Ariamis", numberOfModels=5, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=34.76)
Enemy(name="Plow Scarecrow", set="Darkroot", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty=109.08)
Enemy(name="Sentinel", set="Dark Souls The Board Game", numberOfModels=2, health=10, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=778.12)
Enemy(name="Shears Scarecrow", set="Darkroot", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3,3], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=60.49)
Enemy(name="Silver Knight Greatbowman", set="Dark Souls The Board Game", numberOfModels=3, health=1, armor=2, resist=0, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=90.76)
Enemy(name="Silver Knight Spearman", set="Explorers", numberOfModels=3, health=1, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[1], difficulty=113.69)
Enemy(name="Silver Knight Swordsman", set="Dark Souls The Board Game", numberOfModels=3, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=161.85)
Enemy(name="Skeleton Archer", set="Tomb of Giants", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=77.34)
Enemy(name="Skeleton Beast", set="Tomb of Giants", numberOfModels=1, health=5, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty=431.7)
Enemy(name="Skeleton Soldier", set="Tomb of Giants", numberOfModels=3, health=1, armor=2, resist=1, attacks=[2], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=21.69)
Enemy(name="Snow Rat", set="Painted World of Ariamis", numberOfModels=2, health=1, armor=0, resist=1, attacks=[3], attackType=["physical"], attackEffect=["poison"], dodge=1, move=[4], attackRange=[0], difficulty=63.61)
Enemy(name="Stone Guardian", set="Darkroot", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4,5], attackType=["physical", "physical"], dodge=1, move=[1, 1], attackRange=[0, 0], difficulty=412.2)
Enemy(name="Stone Knight", set="Darkroot", numberOfModels=2, health=5, armor=3, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty=737.67)
Enemy(name="Standard Invader/Hungry Mimic", set=None, numberOfModels=0, health=0, armor=0, resist=0, attacks=[0], attackType=["physical"], dodge=0, move=[0], attackRange=[0], difficulty=0)
Enemy(name="Advanced Invader/Voracious Mimic", set=None, numberOfModels=0, health=0, armor=0, resist=0, attacks=[0], attackType=["physical"], dodge=0, move=[0], attackRange=[0], difficulty=0)
Enemy(name="Mimic", set="The Sunless City", numberOfModels=1, health=5, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty=513.34)
Enemy(name="Crossbow Hollow (TSC)", set="The Sunless City", numberOfModels=3, health=1, armor=1, resist=0, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=45.02)
Enemy(name="Hollow Soldier (TSC)", set="The Sunless City", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=34.76)
Enemy(name="Sentinel (TSC)", set="The Sunless City", numberOfModels=1, health=10, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=778.12)
Enemy(name="Silver Knight Greatbowman (TSC)", set="The Sunless City", numberOfModels=2, health=1, armor=2, resist=0, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty=90.76)
Enemy(name="Silver Knight Swordsman (TSC)", set="The Sunless City", numberOfModels=2, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=161.85)

# Enemy(name="Hungry Mimic - Raking Slash", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Hungry Mimic - Heavy Punch", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Hungry Mimic - Leaping Spin Kick", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Hungry Mimic - Stomping Kick", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Hungry Mimic - Charging Chomp", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[3,4], attackType=["physical","physical"], dodge=3, move=[3,0], attackRange=[0,0], difficulty=0)
# Enemy(name="Hungry Mimic - Vicous Chomp", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[0], attackRange=[0], difficulty=0)
# Enemy(name="Hungry Mimic - Aggressive Grab", set="Explorers", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Voracious Mimic - Raking Slash", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Voracious Mimic - Heavy Punch", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Voracious Mimic - Leaping Spin Kick", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Voracious Mimic - Stomping Kick", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[7], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Voracious Mimic - Charging Chomp", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[3,5], attackType=["physical","physical"], dodge=3, move=[3,0], attackRange=[0,0], difficulty=0)
# Enemy(name="Voracious Mimic - Vicous Chomp", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[7], attackType=["physical"], dodge=2, move=[0], attackRange=[0], difficulty=0)
# Enemy(name="Voracious Mimic - Aggressive Grab", set="Explorers", numberOfModels=0, health=6, armor=2, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Melinda the Butcher - Double Smash", set="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[3,3], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Melinda the Butcher - Cleaving Strikes", set="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[4,4], attackType=["physical","physical"], dodge=1, move=[0,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Melinda the Butcher - Jumping Cleave", set="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[3,3,3], attackType=["physical","physical","physical"], dodge=1, move=[0,4,4], attackRange=[0,0,0], difficulty=0)
# Enemy(name="Melinda the Butcher - Greataxe Sweep", set="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Melinda the Butcher - Sweeping Advance", set="Phantoms", numberOfModels=0, health=20, armor=0, resist=0, attacks=[4,4], attackType=["physical", "physical"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)

# Enemy(name="Maldron the Assassin - Greatlance Lunge", set="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Maldron the Assassin - Double Lance Lunge", set="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[4,4], attackType=["physical","physical"], dodge=2, move=[1,1], attackRange=[1,1], difficulty=0)
# Enemy(name="Maldron the Assassin - Leaping Lance Strike", set="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Maldron the Assassin - Jousting Charge", set="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=3, move=[2], attackRange=[1], difficulty=0)
# Enemy(name="Maldron the Assassin - Corrosive Urn Toss", set="Phantoms", numberOfModels=0, health=13, armor=1, resist=1, attacks=[3], attackType=["magic"], attackEffect=["poison"], dodge=2, move=[0], attackRange=[4], difficulty=0)

# Enemy(name="Oliver the Collector - Bone Fist Punches", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4,4], attackType=["physical","physical"], dodge=2, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Oliver the Collector - Minotaur Helm Charge", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Oliver the Collector - Puzzling Stone Sword Strike", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Oliver the Collector - Majestic Greatsword Slash", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Oliver the Collector - Santier's Spear Lunge", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Oliver the Collector - Smelter Hammer Whirlwind", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4,4,4], attackType=["physical","physical","physical"], dodge=1, move=[0,0,0], attackRange=[1,1,1], difficulty=0)
# Enemy(name="Oliver the Collector - Ricard's Rapier Thrust", set="Phantoms", numberOfModels=0, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[1], difficulty=0)

# Enemy(name="Xanthous King Jeremiah - Great Chaos Fireball", set="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Chaos Fire Whip", set="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[4], attackType=["magic"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Chaos Storm", set="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[3,3], attackType=["magic","magic"], dodge=2, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Firey Retreat", set="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Xanthous King Jeremiah - Whiplash", set="Phantoms", numberOfModels=0, health=14, armor=0, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Kirk, Knight of Thorns - Forward Roll", set="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[3,3], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Shield Bash", set="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Shield Charge", set="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Overhead Chop", set="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Kirk, Knight of Thorns - Barbed Sword Thrust", set="Phantoms", numberOfModels=0, health=12, armor=1, resist=1, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[0], attackRange=[1], difficulty=0)

# Enemy(name="Maneater Mildred - Death Blow", set="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Maneater Mildred - Executioner Strike", set="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Maneater Mildred - Guillotine", set="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Maneater Mildred - Butcher Chop", set="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Maneater Mildred - Butchery", set="Phantoms", numberOfModels=0, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Paladin Leeroy - Advancing Grant Slam", set="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty=0)
# Enemy(name="Paladin Leeroy - Grant Slam Withdrawal", set="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Paladin Leeroy - Sanctus Shield Slam", set="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Paladin Leeroy - Sanctus Shield Dash", set="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[4,4], attackType=["physical","physical"], dodge=2, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Paladin Leeroy - Wrath of the Gods", set="Phantoms", numberOfModels=0, health=16, armor=2, resist=1, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[1], difficulty=0)

# Enemy(name="Armorer Dennis - toughness only", set="Phantoms", numberOfModels=0, health=16, armor=1, resist=2, attacks=[], attackType=[], dodge=1, move=[], attackRange=[], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Spear Launch", set="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Greatsword", set="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[6], attackType=["magic"], dodge=1, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Vortex", set="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[4,4], attackType=["magic","magic"], dodge=1, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Armorer Dennis - Soul Flash", set="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[4], attackType=["magic"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Armorer Dennis - Upward Slash", set="Phantoms", numberOfModels=0, health=6, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Spear Launch", set="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Greatsword", set="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[6], attackType=["magic"], dodge=2, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Vortex", set="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[4,4], attackType=["magic","magic"], dodge=2, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Soul Flash", set="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[4], attackType=["magic"], dodge=3, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Armorer Dennis (heat up) - Upward Slash", set="Phantoms", numberOfModels=0, health=10, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)

# Enemy(name="Invader Brylex - Leaping Strike", set="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[7], attackType=["physical"], dodge=1, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Invader Brylex - Blade Dervish", set="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[4,4], attackRange=[0,0], difficulty=0)
# Enemy(name="Invader Brylex - Trampling Charge", set="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[4,4,4], attackType=["physical","physical","physical"], dodge=1, move=[1,1,1], attackRange=[0,0,0], difficulty=0)
# Enemy(name="Invader Brylex - Fire Surge", set="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Invader Brylex - Fire Whip", set="Phantoms", numberOfModels=0, health=15, armor=2, resist=2, attacks=[6], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficulty=0)

# Enemy(name="Marvelous Chester - Crossbow Volley", set="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[0,0], attackRange=[4,4], difficulty=0)
# Enemy(name="Marvelous Chester - Crossbow Snipe", set="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=4, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Marvelous Chester - Throwing Knife Volley", set="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[4,4], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=2, move=[0,0], attackRange=[2,2], difficulty=0)
# Enemy(name="Marvelous Chester - Throwing Knife Flurry", set="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[3,3,3], attackType=["physical","physical","physical"], attackEffect=["bleed","bleed","bleed"], dodge=1, move=[0,0,0], attackRange=[2,2,2], difficulty=0)
# Enemy(name="Marvelous Chester - Spinning Low Kick", set="Phantoms", numberOfModels=0, health=17, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[0], difficulty=0)

# Enemy(name="Longfinger Kirk - Rolling Barbs", set="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[4,4], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)
# Enemy(name="Longfinger Kirk - Lunging Stab", set="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=3, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Longfinger Kirk - Cleave", set="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[6], attackType=["physical"], attackEffect=["bleed"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Longfinger Kirk - Crushing Blow", set="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=3, move=[4], attackRange=[0], difficulty=0)
# Enemy(name="Longfinger Kirk - Barbed Sword Strikes", set="Phantoms", numberOfModels=0, health=14, armor=2, resist=2, attacks=[5,5], attackType=["physical","physical"], attackEffect=["bleed","bleed"], dodge=1, move=[0,0], attackRange=[1,1], difficulty=0)

# Enemy(name="Fencer Sharron - Puzzling Stone Sword Charge", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Puzzling Stone Sword Whip", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[0], attackRange=[1], difficulty=0)
# Enemy(name="Fencer Sharron - Spider Fang Sword Strike", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Spider Fang Sword Charge", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Spider Fang Web Blast", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty=0)
# Enemy(name="Fencer Sharron - Dual Sword Slash", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[0], difficulty=0)
# Enemy(name="Fencer Sharron - Dual Sword Assault", set="Phantoms", numberOfModels=0, health=20, armor=1, resist=1, attacks=[5,5], attackType=["physical","physical"], dodge=1, move=[1,1], attackRange=[0,0], difficulty=0)

for i, enemy in enumerate(enemiesDict):
    enemyIds[i] = enemiesDict[enemy]
    enemiesDict[enemy].id = i