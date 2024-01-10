from json import dump
from os import path


baseFolder = path.dirname(__file__)
enemies = []
enemyIds = {}
enemiesDict = {}
reach = []


class Enemy:
    def __init__(self, name, expansion, numberOfModels, health, armor, resist, attacks, attackType, dodge, move, attackRange, nodeAttack=[], nodesAttacked=0, attackEffect=[], difficulty=0) -> None:
        enemiesDict[name] = self
        enemies.append(self)
        self.name = name
        self.expansion = expansion
        self.numberOfModels = numberOfModels
        self.health = health
        self.armor = armor
        self.resist = resist
        self.attacks = attacks
        self.nodeAttack = nodeAttack if nodeAttack else [False for _ in self.attacks]
        self.nodesAttacked = nodesAttacked if nodesAttacked else [0 for _ in self.attacks]
        self.attackType = attackType
        self.dodge = dodge
        self.move = move
        self.attackRange = attackRange
        self.attackEffect = attackEffect
        self.difficulty = difficulty

        check = set()
        check.add(len(self.attacks))
        check.add(len(self.attackRange))
        check.add(len(self.attackType))
        check.add(len(self.nodeAttack))
        check.add(len(self.nodesAttacked))
        if self.attackEffect:
            check.add(len(self.attackEffect))
        if len(check) > 1:
            raise
        
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

        self.deaths = 0
        self.damageDone1 = 0
        self.damageDone2 = 0
        self.damageDone3 = 0
        self.damageDone4 = 0
        self.bleedDamage1 = 0
        self.bleedDamage2 = 0
        self.bleedDamage3 = 0
        self.bleedDamage4 = 0
        self.damagingAttacks = 0
        self.totalAttacks = 0
        self.loadoutDamage = {}
        self.imagePath = baseFolder + "\\images\\" + name + ".png"

        for i, m in enumerate(self.move):
            reach.append(m + self.attackRange[i])


    def reset(self):
        with open(baseFolder + "\\enemies\\" + self.name + ".json", "w") as enemyFile:
            dump({"deaths": 0, "totalAttacks": 0, "damagingAttacks": 0, "damageDone": 0, "bleedDamage": 0, "loadoutDamage": {}}, enemyFile)


# Regular enemies
Enemy(name="Alonne Bow Knight", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[0], attackRange=[4], difficulty={1: 111.73, 2: 111.73, 3: 111.73, 4: 111.73})
Enemy(name="Alonne Knight Captain", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=5, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[2], attackRange=[0], difficulty={1: 394.36, 2: 394.36, 3: 394.36, 4: 394.36})
Enemy(name="Alonne Sword Knight", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[2], attackRange=[0], difficulty={1: 130.05, 2: 130.05, 3: 130.05, 4: 130.05})
Enemy(name="Black Hollow Mage", expansion="Executioner Chariot", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4], attackType=["magic"], dodge=2, move=[0], attackRange=[4], difficulty={1: 557.57, 2: 557.57, 3: 557.57, 4: 557.57})
Enemy(name="Bonewheel Skeleton", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty={1: 100.49, 2: 108.22, 3: 115.95, 4: 125.46})
Enemy(name="Crossbow Hollow", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=0, attacks=[3], attackType=["magic"], dodge=1, move=[0], attackRange=[4], difficulty={1: 45.02, 2: 45.02, 3: 45.02, 4: 45.02})
Enemy(name="Crow Demon", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=2, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[4], attackRange=[0], difficulty={1: 591.94, 2: 637.48, 3: 683.01, 4: 739.05})
Enemy(name="Demonic Foliage", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1], difficulty={1: 113.27, 2: 113.27, 3: 113.27, 4: 113.27})
Enemy(name="Engorged Zombie", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=2, resist=2, attacks=[4], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty={1: 51.81, 2: 51.81, 3: 51.81, 4: 51.81})
Enemy(name="Falchion Skeleton", expansion="Executioner Chariot", enemyType="regular", numberOfModels=2, health=1, armor=1, resist=1, attacks=[3], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[2], attackRange=[0], difficulty={1: 56.02, 2: 56.02, 3: 56.02, 4: 56.02})
Enemy(name="Firebomb Hollow", expansion="Explorers", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=1, move=[1], attackRange=[2], difficulty={1: 46.52, 2: 50.1, 3: 53.67, 4: 58.08})
Enemy(name="Giant Skeleton Archer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0, 0], attackRange=[0, 4], difficulty={1: 414.31, 2: 414.7, 3: 415.09, 4: 415.57})
Enemy(name="Giant Skeleton Soldier", expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=1, attacks=[2,5], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=1, move=[1, 1], attackRange=[0, 1], difficulty={1: 253.87, 2: 255.28, 3: 256.69, 4: 258.42})
Enemy(name="Hollow Soldier", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty={1: 34.76, 2: 34.76, 3: 34.76, 4: 34.76})
Enemy(name="Ironclad Soldier", expansion="Iron Keep", enemyType="regular", numberOfModels=3, health=5, armor=3, resist=2, attacks=[5], attackType=["physical"], nodeAttack=[True], attackEffect=["stagger"], dodge=2, move=[1], attackRange=[0], difficulty={1: 464.27, 2: 499.98, 3: 535.7, 4: 579.65})
Enemy(name="Large Hollow Soldier", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=0, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[0], difficulty={1: 114.11, 2: 122.89, 3: 131.67, 4: 142.47})
Enemy(name="Mimic", expansion="The Sunless City", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty={1: 513.34, 2: 513.34, 3: 513.34, 4: 513.34})
Enemy(name="Mushroom Child", expansion="Darkroot", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[0], difficulty={1: 145.01, 2: 145.01, 3: 145.01, 4: 145.01})
Enemy(name="Mushroom Parent", expansion="Darkroot", enemyType="regular", numberOfModels=1, health=10, armor=1, resist=2, attacks=[6], attackType=["physical"], nodeAttack=[True], attackEffect=["stagger"], dodge=1, move=[1], attackRange=[0], difficulty={1: 341.81, 2: 368.1, 3: 394.39, 4: 426.75})
Enemy(name="Necromancer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=2, health=5, armor=1, resist=2, attacks=[3], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4], difficulty={1: 205.69, 2: 221.51, 3: 237.33, 4: 256.81})
Enemy(name="Phalanx", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=1, health=5, armor=1, resist=1, attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=1, move=[0,1], attackRange=[1,0], difficulty={1: 128.8, 2: 138.71, 3: 148.61, 4: 160.81})
Enemy(name="Phalanx Hollow", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=5, health=1, armor=1, resist=1, attacks=[4,0], attackType=["physical", "physical"], dodge=1, move=[0,1], attackRange=[1,0], difficulty={1: 34.76, 2: 34.76, 3: 34.76, 4: 34.76})
Enemy(name="Plow Scarecrow", expansion="Darkroot", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=2, move=[2], attackRange=[1], difficulty={1: 109.08, 2: 109.08, 3: 109.08, 4: 109.08})
Enemy(name="Sentinel", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=2, health=10, armor=2, resist=1, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1], difficulty={1: 778.12, 2: 837.97, 3: 897.83, 4: 971.5})
Enemy(name="Shears Scarecrow", expansion="Darkroot", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, attacks=[3,3], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty={1: 60.49, 2: 65.15, 3: 69.8, 4: 75.53})
Enemy(name="Silver Knight Greatbowman", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=0, attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4], difficulty={1: 90.76, 2: 97.75, 3: 104.73, 4: 113.32})
Enemy(name="Silver Knight Spearman", expansion="Explorers", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, attacks=[6,0], attackType=["physical", "physical"], dodge=2, move=[0,1], attackRange=[1,0], difficulty={1: 113.69, 2: 113.69, 3: 113.69, 4: 113.69})
Enemy(name="Silver Knight Swordsman", expansion="Dark Souls The Board Game", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[0], difficulty={1: 161.85, 2: 174.3, 3: 186.75, 4: 202.08})
Enemy(name="Skeleton Archer", expansion="Tomb of Giants", enemyType="regular", numberOfModels=3, health=1, armor=1, resist=1, attacks=[4], attackType=["physical"], dodge=1, move=[0], attackRange=[4], difficulty={1: 77.34, 2: 77.34, 3: 77.34, 4: 77.34})
Enemy(name="Skeleton Beast", expansion="Tomb of Giants", enemyType="regular", numberOfModels=1, health=5, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=2, move=[1, 1], attackRange=[0, 0], difficulty={1: 431.7, 2: 464.91, 3: 498.12, 4: 538.99})
Enemy(name="Skeleton Soldier", expansion="Tomb of Giants", enemyType="regular", numberOfModels=3, health=1, armor=2, resist=1, attacks=[2], attackType=["physical"], nodeAttack=[True], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0], difficulty={1: 21.69, 2: 23.35, 3: 25.02, 4: 27.07})
Enemy(name="Snow Rat", expansion="Painted World of Ariamis", enemyType="regular", numberOfModels=2, health=1, armor=0, resist=1, attacks=[3], attackType=["physical"], attackEffect=["poison"], dodge=1, move=[4], attackRange=[0], difficulty={1: 63.61, 2: 63.61, 3: 63.61, 4: 63.61})
Enemy(name="Stone Guardian", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=5, armor=2, resist=3, attacks=[4,5], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=1, move=[1, 0], attackRange=[0, 1], difficulty={1: 412.2, 2: 443.91, 3: 475.62, 4: 514.64})
Enemy(name="Stone Knight", expansion="Darkroot", enemyType="regular", numberOfModels=2, health=5, armor=3, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[1], attackRange=[0], difficulty={1: 331.73, 2: 331.73, 3: 331.73, 4: 331.73})

# Invaders
Enemy(name="Armorer Dennis - Soul Spear Launch", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[5], attackType=["magic"], dodge=1, move=[0], attackRange=[4])
Enemy(name="Armorer Dennis - Soul Greatsword", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[6], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[1])
Enemy(name="Armorer Dennis - Soul Vortex", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[4,4], attackType=["magic", "magic"], nodeAttack=[True, True], dodge=1, move=[0,0], attackRange=[4,4])
Enemy(name="Armorer Dennis - Soul Flash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[4], attackType=["magic"], dodge=2, move=[2], attackRange=[0])
Enemy(name="Armorer Dennis - Upward Slash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0])
Enemy(name="Armorer Dennis - Soul Spear Launch (heat up)", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
Enemy(name="Armorer Dennis - Soul Greatsword (heat up)", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[6], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[1])
Enemy(name="Armorer Dennis - Soul Vortex (heat up)", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[4,4], attackType=["magic", "magic"], nodeAttack=[True, True], dodge=2, move=[0,0], attackRange=[4,4])
Enemy(name="Armorer Dennis - Soul Flash (heat up)", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[4], attackType=["magic"], dodge=3, move=[2], attackRange=[0])
Enemy(name="Armorer Dennis - Upward Slash (heat up)", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=1, resist=2, attacks=[6], attackType=["physical"], dodge=2, move=[1], attackRange=[0])
Enemy(name="Fencer Sharron - Puzzling Stone Sword Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0])
Enemy(name="Fencer Sharron - Puzzling Stone Sword Whip", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[6,0], attackType=["physical", "physical"], dodge=1, move=[0,-1], attackRange=[1,1])
Enemy(name="Fencer Sharron - Spider Fang Sword Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], dodge=1, move=[1], attackRange=[0])
Enemy(name="Fencer Sharron - Spider Fang Sword Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=2, move=[2], attackRange=[0])
Enemy(name="Fencer Sharron - Spider Fang Web Blast", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
Enemy(name="Fencer Sharron - Dual Sword Assault", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[5,5], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[0,0])
Enemy(name="Fencer Sharron - Dual Sword Slash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=1, resist=1, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[1], attackRange=[0])
Enemy(name="Invader Brylex - Leaping Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, attacks=[7], attackType=["physical"], nodeAttack=[True], dodge=1, move=[4], attackRange=[0])
Enemy(name="Invader Brylex - Trampling Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, attacks=[4,4,4], attackType=["physical", "physical", "physical"], nodeAttack=[True, True, True], dodge=1, move=[1,1,1], attackRange=[0,0,0])
Enemy(name="Invader Brylex - Blade Dervish", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, attacks=[5,5], attackType=["physical", "physical"], dodge=1, move=[4,4], attackRange=[0,0])
Enemy(name="Invader Brylex - Fire Surge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
Enemy(name="Invader Brylex - Fire Whip", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=2, resist=2, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=1, move=[2], attackRange=[0])
Enemy(name="Kirk, Knight of Thorns - Forward Roll", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, attacks=[3,3], attackType=["physical", "physical"], nodeAttack=[True, True], attackEffect=["bleed","bleed"], dodge=1, move=[1,1], attackRange=[0,0])
Enemy(name="Kirk, Knight of Thorns - Shield Bash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=2, move=[1], attackRange=[0])
Enemy(name="Kirk, Knight of Thorns - Shield Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], nodeAttack=[True], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0])
Enemy(name="Kirk, Knight of Thorns - Overhead Chop", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[1], attackRange=[0])
Enemy(name="Kirk, Knight of Thorns - Barbed Sword Thrust", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=12, armor=1, resist=1, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=1, move=[0], attackRange=[1])
Enemy(name="Longfinger Kirk - Rolling Barbs", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True, True], attackEffect=["bleed", "bleed"], dodge=1, move=[1,1], attackRange=[0,0])
Enemy(name="Longfinger Kirk - Lunging Stab", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=3, move=[1], attackRange=[0])
Enemy(name="Longfinger Kirk - Cleave", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, attacks=[6], attackType=["physical"], nodeAttack=[True], attackEffect=["bleed"], dodge=2, move=[1], attackRange=[0])
Enemy(name="Longfinger Kirk - Crushing Blow", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["bleed"], dodge=3, move=[4], attackRange=[0])
Enemy(name="Longfinger Kirk - Barbed Sword Strikes", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=2, resist=2, attacks=[5,5], attackType=["physical", "physical"], attackEffect=["bleed", "bleed"], dodge=2, move=[0,0], attackRange=[1,1])
Enemy(name="Maldron the Assassin - Greatlance Lunge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, attacks=[4,0], attackType=["physical", "physical"], dodge=3, move=[1,-1], attackRange=[0,1])
Enemy(name="Maldron the Assassin - Double Lance Lunge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[1,1])
Enemy(name="Maldron the Assassin - Leaping Lance Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[4,-2], attackRange=[0,2])
Enemy(name="Maldron the Assassin - Jousting Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, attacks=[5], attackType=["physical"], dodge=3, move=[2], attackRange=[1])
Enemy(name="Maldron the Assassin - Corrosive Urn Toss", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=13, armor=1, resist=1, attacks=[3], attackType=["magic"], attackEffect=["poison"], dodge=2, move=[0], attackRange=[4])
Enemy(name="Maneater Mildred - Death Blow", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
Enemy(name="Maneater Mildred - Executioner Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[0])
Enemy(name="Maneater Mildred - Guillotine", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[0])
Enemy(name="Maneater Mildred - Butcher Chop", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=2, move=[1], attackRange=[1])
Enemy(name="Maneater Mildred - Butchery", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=18, armor=0, resist=0, attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[0])
Enemy(name="Marvelous Chester - Crossbow Volley", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, attacks=[5,5], attackType=["physical", "physical"], dodge=1, move=[0,0], attackRange=[4,4])
Enemy(name="Marvelous Chester - Crossbow Snipe", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, attacks=[5], attackType=["physical"], dodge=4, move=[0], attackRange=[4])
Enemy(name="Marvelous Chester - Throwing Knife Volley", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, attacks=[4,0,4,0], attackType=["physical", "physical", "physical", "physical"], attackEffect=["bleed", "bleed", "bleed", "bleed"], dodge=2, move=[0, -1, 0, -1], attackRange=[2,2,2,2])
Enemy(name="Marvelous Chester - Throwing Knife Flurry", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, attacks=[3,0,3,0,3,0], attackType=["physical", "physical", "physical", "physical", "physical", "physical"], attackEffect=["bleed", "bleed", "bleed", "bleed", "bleed", "bleed"], dodge=1, move=[0,-1,0,-1,0,-1], attackRange=[2,2,2,2,2,2])
Enemy(name="Marvelous Chester - Spinning Low Kick", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=17, armor=1, resist=2, attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=3, move=[1,-1], attackRange=[0,1])
Enemy(name="Melinda the Butcher - Double Smash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[3,3], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[0,0])
Enemy(name="Melinda the Butcher - Cleaving Strikes", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[4,0,4,0], attackType=["physical", "physical", "physical", "physical"], dodge=1, move=[0,1,0,1], attackRange=[0,0,0,0])
Enemy(name="Melinda the Butcher - Jumping Cleave", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[3,0,3,0,3,0], attackType=["physical", "physical", "physical", "physical", "physical", "physical"], dodge=1, move=[0,4,0,4,0,4], attackRange=[0,0,0,0,0,0])
Enemy(name="Melinda the Butcher - Greataxe Sweep", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=2, move=[1], attackRange=[0])
Enemy(name="Melinda the Butcher - Sweeping Advance", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=20, armor=0, resist=0, attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=1, move=[1,1], attackRange=[0,0])
Enemy(name="Oliver the Collector - Bone Fist Punches", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[0,0])
Enemy(name="Oliver the Collector - Minotaur Helm Charge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[5,5], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=1, move=[1,1], attackRange=[0,0])
Enemy(name="Oliver the Collector - Puzzling Stone Sword Strike", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[4], attackType=["physical"], dodge=3, move=[1], attackRange=[0])
Enemy(name="Oliver the Collector - Majestic Greatsword Slash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[4,0], attackType=["physical", "physical"], dodge=2, move=[1,-1], attackRange=[0,1])
Enemy(name="Oliver the Collector - Santier's Spear Lunge", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[5], attackType=["physical"], dodge=1, move=[1], attackRange=[1])
Enemy(name="Oliver the Collector - Smelter Hammer Whirlwind", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[4,4,4], attackType=["physical", "physical", "physical"], nodeAttack=[True, True, True], dodge=1, move=[0,0,0], attackRange=[1,1,1])
Enemy(name="Oliver the Collector - Ricard's Rapier Thrust", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=15, armor=1, resist=0, attacks=[4,0], attackType=["physical", "physical"], dodge=2, move=[0,-1], attackRange=[1,1])
Enemy(name="Paladin Leeroy - Advancing Grant Slam", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
Enemy(name="Paladin Leeroy - Grant Slam Withdrawal", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, attacks=[6,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=1, move=[0,-1], attackRange=[1,1])
Enemy(name="Paladin Leeroy - Sanctus Shield Slam", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, attacks=[5], attackType=["physical"], dodge=3, move=[1], attackRange=[0])
Enemy(name="Paladin Leeroy - Sanctus Shield Dash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, attacks=[4,4], attackType=["physical", "physical"], dodge=2, move=[1,1], attackRange=[0,0])
Enemy(name="Paladin Leeroy - Wrath of the Gods", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=16, armor=2, resist=1, attacks=[5], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[1])
Enemy(name="Xanthous King Jeremiah - Great Chaos Fireball", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, attacks=[5], attackType=["magic"], nodeAttack=[True], dodge=1, move=[0], attackRange=[4])
Enemy(name="Xanthous King Jeremiah - Chaos Fire Whip", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, attacks=[4], attackType=["magic"], dodge=2, move=[1], attackRange=[1])
Enemy(name="Xanthous King Jeremiah - Chaos Storm", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, attacks=[3,3], attackType=["magic","magic"], nodeAttack=[True, True], dodge=2, move=[0,0], attackRange=[4,4])
Enemy(name="Xanthous King Jeremiah - Firey Retreat", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, attacks=[4], attackType=["magic"], nodeAttack=[True], dodge=2, move=[0], attackRange=[4])
Enemy(name="Xanthous King Jeremiah - Whiplash", expansion="Phantoms", enemyType="invader", numberOfModels=1, health=14, armor=0, resist=1, attacks=[4], attackType=["physical"], attackEffect=["bleed"], nodeAttack=[True], dodge=1, move=[2], attackRange=[0])

# Mini Bosses
Enemy(name="Old Dragonslayer - Darkness Bolt", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[4], attackType=["magic"], dodge=3, move=[0], attackRange=[3])
Enemy(name="Old Dragonslayer - Spear Lunge", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[5], attackType=["physical"], dodge=2, move=[1], attackRange=[2])
Enemy(name="Old Dragonslayer - Leaping Darkness", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[4], attackType=["magic"], nodesAttacked=[12], dodge=1, move=[4], attackRange=[1])
Enemy(name="Old Dragonslayer - Skewering Charge", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=1, move=[1,1], attackRange=[0,0])
Enemy(name="Old Dragonslayer - Spear Sweep", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[6,0], dodge=2, move=[0,1], attackRange=[2,0])
Enemy(name="Old Dragonslayer - Darkness Falls", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[5], attackType=["magic"], nodesAttacked=[6], dodge=1, move=[4], attackRange=[2])
Enemy(name="Old Dragonslayer - Massive Sweep", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[14,0], dodge=2, move=[0,1], attackRange=[2,0])
Enemy(name="Old Dragonslayer - Lunging Combo", expansion="Explorers", enemyType="mini boss", numberOfModels=1, health=20, armor=2, resist=2, attacks=[5,5], attackType=["physical", "physical"], dodge=2, move=[0,1], attackRange=[1,1])
Enemy(name="Asylum Demon - Mighty Hammer Smash", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=1, move=[4], attackRange=[0])
Enemy(name="Asylum Demon - Leaping Hammer Smash", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=1, move=[4], attackRange=[0])
Enemy(name="Asylum Demon - Ground Pound", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5], attackType=["physical"], attackEffect=["stagger"], nodesAttacked=[12], dodge=1, move=[0], attackRange=[1])
Enemy(name="Asylum Demon - Delayed Hammer Drive", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5,5], attackType=["physical", "physical"], attackEffect=["stagger", "stagger"], nodeAttack=[True, True], dodge=1, move=[1,1], attackRange=[0])
Enemy(name="Asylum Demon - Hammer Drive", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], attackEffect=["stagger", "stagger"], nodeAttack=[True, True], dodge=2, move=[1,1], attackRange=[0])
Enemy(name="Asylum Demon - Retreating Sweep", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=1, move=[0,-1], attackRange=[1,1])
Enemy(name="Asylum Demon - Lumbering Swings", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], nodesAttacked=[14, 14], dodge=1, move=[2,2], attackRange=[1,1])
Enemy(name="Asylum Demon - Sweeping Strikes", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[4,4], attackType=["physical", "physical"], nodesAttacked=[7,7], dodge=2, move=[1,0], attackRange=[1,1])
Enemy(name="Asylum Demon - Crusing Leaps", expansion="Asylum Demon", enemyType="mini boss", numberOfModels=1, health=34, armor=1, resist=1, attacks=[5,5], attackType=["physical", "physical"], nodeAttack=[True, True], dodge=1, move=[4,4], attackRange=[0,0])
Enemy(name="Boreal Outrider Knight - Backhand Slashes", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[4,4], attackType=["physical", "physical"], attackEffect=["frostbite", "frostbite"], nodesAttacked=[7,7], dodge=2, move=[1,1], attackRange=[1,1])
Enemy(name="Boreal Outrider Knight - Overhead Slash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[0], attackRange=[1])
Enemy(name="Boreal Outrider Knight - Sweeping Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=1, move=[0,-1], attackRange=[1,1])
Enemy(name="Boreal Outrider Knight - Chilling Thrust", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[4], attackType=["magic"], attackEffect=["frostbite"], dodge=2, move=[2], attackRange=[1])
Enemy(name="Boreal Outrider Knight - Leaping Frost", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[4,0,4,0], attackType=["physical", "physical"], attackEffect=["frostbite", None, "frostbite", None], nodesAttacked=[7,0,7,0], dodge=1, move=[0,4,0,4], attackRange=[1,1,1,1])
Enemy(name="Boreal Outrider Knight - Lunging Triple Slash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[4,4,4], attackType=["physical", "physical", "physical"], nodesAttacked=[4,4,4], dodge=1, move=[1,1,1], attackRange=[1,1,1])
Enemy(name="Boreal Outrider Knight - Uppercut Slam", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[5,5], attackType=["physical", "physical"], attackEffect=["frostbite", "frostbite"], dodge=2, move=[2,2], attackRange=[1,1])
Enemy(name="Boreal Outrider Knight - Frost Breath", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=26, armor=2, resist=3, attacks=[6], attackType=["magic"], nodesAttacked=[10], attackEffect=["frostbite"], dodge=1, move=[0], attackRange=[1])
Enemy(name="Winged Knight - Backhand Shaft Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
Enemy(name="Winged Knight - Overhand Smash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[5], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[1])
Enemy(name="Winged Knight - Double Slash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[6,6], attackType=["physical", "physical"], nodesAttacked=[10,10], dodge=2, move=[1,1], attackRange=[1,1])
Enemy(name="Winged Knight - Whirlwind", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[4,4,4], attackType=["physical", "physical", "physical"], nodesAttacked=[12,12,12], dodge=1, move=[1,1,1], attackRange=[1,1,1])
Enemy(name="Winged Knight - Pillars of Light", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[5], attackType=["magic"], nodesAttacked=[16], dodge=1, move=[0], attackRange=[4])
Enemy(name="Winged Knight - Sweeping Blade Swing", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[5], attackType=["physical"], nodesAttacked=[7], dodge=1, move=[1], attackRange=[1])
Enemy(name="Winged Knight - Diagonal Uppercut", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=1, move=[0,-1], attackRange=[1,0])
Enemy(name="Winged Knight - Charging Assault", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=24, armor=3, resist=1, attacks=[4,4], attackType=["physical", "physical"], nodesAttacked=[4,4], dodge=2, move=[1,1], attackRange=[1,1])
Enemy(name="Black Knight - Overhead Swing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[6,0], dodge=2, move=[0,2], attackRange=[2,0])
Enemy(name="Black Knight - Heavy Slash", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[5,0], attackType=["physical", "physical"], attackEffect=["stagger", None], nodeAttack=[True, False], dodge=1, move=[0,1], attackRange=[2,0])
Enemy(name="Black Knight - Backswing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[5,0], attackType=["physical", "physical"], attackEffect=["stagger", None], nodeAttack=[True, False], dodge=1, move=[0,-2], attackRange=[2,2])
Enemy(name="Black Knight - Vicious Hack", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[5,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=1, move=[0,2], attackRange=[2,2])
Enemy(name="Black Knight - Defensive Strike", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0,1], attackRange=[2,2])
Enemy(name="Black Knight - Wide Swing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[7,0], dodge=2, move=[0,1], attackRange=[2,2])
Enemy(name="Black Knight - Massive Swing", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[5], attackType=["physical"], nodesAttacked=[14], dodge=2, move=[0], attackRange=[2])
Enemy(name="Black Knight - Hacking Slash", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[5,4,4], attackType=["physical", "physical", "physical"], nodesAttacked=[4,0,0], attackEffect=["stagger", None, None], nodeAttack=[False, True, True], dodge=2, move=[0,1,1], attackRange=[2,0,0])
Enemy(name="Black Knight - Charge", expansion="Tomb of Giants", enemyType="mini boss", numberOfModels=1, health=20, armor=3, resist=2, attacks=[6,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0,3], attackRange=[2,0])
Enemy(name="Heavy Knight - Defensive Swipe", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[4,0], attackType=["physical", "physical"], nodesAttacked=[10,0], dodge=3, move=[0,-2], attackRange=[1,2])
Enemy(name="Heavy Knight - Charging Chop", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[2], attackRange=[1])
Enemy(name="Heavy Knight - Defensive Chop", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[5,0], attackType=["physical", "physical"], nodeAttack=[True, False], dodge=2, move=[0,-2], attackRange=[1,2])
Enemy(name="Heavy Knight - Overhead Chop", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[5], attackType=["physical"], attackEffect=["stagger"], nodeAttack=[True], dodge=1, move=[1], attackRange=[1])
Enemy(name="Heavy Knight - Shield Swipe", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[4], attackType=["physical"], attackEffect=["stagger"], nodesAttacked=[10], dodge=2, move=[1], attackRange=[1])
Enemy(name="Heavy Knight - Double Slash", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[4,4], attackType=["physical", "physical"], attackEffect=["stagger", "stagger"], nodesAttacked=[10,10], dodge=1, move=[0,0], attackRange=[1,1])
Enemy(name="Heavy Knight - Slashing Blade", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[4], attackType=["physical"], attackEffect=["stagger"], nodesAttacked=[10], dodge=1, move=[1], attackRange=[1])
Enemy(name="Heavy Knight - Double Chop", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[5,5], attackType=["physical", "physical"], attackEffect=["stagger", "stagger"], nodeAttack=[True, True], dodge=1, move=[0,0], attackRange=[1,1])
Enemy(name="Heavy Knight - Shield Smash", expansion="Painted World of Ariamis", enemyType="mini boss", numberOfModels=1, health=25, armor=2, resist=2, attacks=[4], attackType=["physical"], nodeAttack=[True], dodge=3, move=[1], attackRange=[1])
Enemy(name="Titanite Demon - Double Swing", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[4,4], attackType=["physical", "physical"], nodesAttacked=[4,4], dodge=1, move=[1,1], attackRange=[1,1])
Enemy(name="Titanite Demon - Tail Whip", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[4], attackType=["physical"], nodesAttacked=[10], dodge=2, move=[2], attackRange=[1])
Enemy(name="Titanite Demon - Grab & Smash", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[6], attackType=["physical"], dodge=1, move=[0], attackRange=[1])
Enemy(name="Titanite Demon - Lightning Bolt", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[5], attackType=["magic"], dodge=2, move=[0], attackRange=[4])
Enemy(name="Titanite Demon - Vicious Swing", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[5], attackType=["physical"], nodesAttacked=[10], dodge=1, move=[0], attackRange=[1])
Enemy(name="Titanite Demon - Sweeping Strike", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[6], attackType=["physical"], nodesAttacked=[14], dodge=1, move=[-2], attackRange=[2])
Enemy(name="Titanite Demon - Vaulting Slam", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[6], attackType=["physical"], nodeAttack=[True], dodge=2, move=[4], attackRange=[0])
Enemy(name="Titanite Demon - Double Pole Crush", expansion="Dark Souls The Board Game", enemyType="mini boss", numberOfModels=1, health=22, armor=3, resist=2, attacks=[5,0,5,0], attackType=["physical", "physical", "physical", "physical"], nodesAttacked=[4,0,4,0], dodge=1, move=[0,-1,0,-1], attackRange=[2,2,2,2])
Enemy(name="Gargoyle - ", expansion="Dark Souls the Board Game", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="main boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])
Enemy(name=" - ", expansion="", enemyType="mega boss", numberOfModels=1, health=, armor=, resist=, attacks=[], attackType=["physical"], nodesAttacked=[], dodge=, move=[], attackRange=[])

for i, enemy in enumerate(enemiesDict):
    enemyIds[i] = enemiesDict[enemy]
    enemiesDict[enemy].id = i