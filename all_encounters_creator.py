import numpy

from enemies import enemiesDict, enemyIds, enemies


def calculate_rank(l):
    a = {}
    for i, num in enumerate(sorted(l, key=lambda x: enemyIds[x].difficulty[1])):
        if num not in a:
            a[num] = [sum([1 for e in sorted(l, key=lambda x: enemyIds[x].difficulty[1])[:i] if enemyIds[e].difficulty[1] <= enemyIds[num].difficulty[1]])]
        else:
            a[num].append(sum([1 for e in sorted(l, key=lambda x: enemyIds[x].difficulty[1])[:i] if enemyIds[e].difficulty[1] <= enemyIds[num].difficulty[1]]))

    return [a[e][l[:i].count(e)] for i, e in enumerate(l)]


abk = enemiesDict["Alonne Bow Knight"].id
akc = enemiesDict["Alonne Knight Captain"].id
ask = enemiesDict["Alonne Sword Knight"].id
bhm = enemiesDict["Black Hollow Mage"].id
bs = enemiesDict["Bonewheel Skeleton"].id
ch = enemiesDict["Crossbow Hollow"].id
cd = enemiesDict["Crow Demon"].id
df = enemiesDict["Demonic Foliage"].id
ez = enemiesDict["Engorged Zombie"].id
fs = enemiesDict["Falchion Skeleton"].id
fh = enemiesDict["Firebomb Hollow"].id
gsa = enemiesDict["Giant Skeleton Archer"].id
gss = enemiesDict["Giant Skeleton Soldier"].id
hs = enemiesDict["Hollow Soldier"].id
ics = enemiesDict["Ironclad Soldier"].id
lhs = enemiesDict["Large Hollow Soldier"].id
mc = enemiesDict["Mushroom Child"].id
mp = enemiesDict["Mushroom Parent"].id
n = enemiesDict["Necromancer"].id
p = enemiesDict["Phalanx"].id
ph = enemiesDict["Phalanx Hollow"].id
ps = enemiesDict["Plow Scarecrow"].id
s = enemiesDict["Sentinel"].id
ss = enemiesDict["Shears Scarecrow"].id
skg = enemiesDict["Silver Knight Greatbowman"].id
skp = enemiesDict["Silver Knight Spearman"].id
sks = enemiesDict["Silver Knight Swordsman"].id
sa = enemiesDict["Skeleton Archer"].id
sb = enemiesDict["Skeleton Beast"].id
sd = enemiesDict["Skeleton Soldier"].id
sr = enemiesDict["Snow Rat"].id
sg = enemiesDict["Stone Guardian"].id
sk = enemiesDict["Stone Knight"].id
m = enemiesDict["Mimic"].id

encounters = {
    "Asylum's North Hall": {"enemies": [[sk,skp,ps,fh,ps,fh,sk,skp],[],[]], "enemyExpansions": set(["Explorers", "Darkroot"]), "level": 4, "spawns": [], "expansion": "Asylum Demon"},
    "Base of Cardinal Tower": {"enemies": [[skp,fh,skp,abk,abk,skp,abk,ics,fh],[],[]], "enemyExpansions": set(["Iron Keep", "Explorers"]), "level": 4, "spawns": [], "expansion": "The Last Giant"},
    "Blazing Furnace": {"enemies": [[akc,ask,fh,fh,ics,enemiesDict["Fencer Sharron"].id],[],[]], "enemyExpansions": set(["Explorers", "Iron Keep", "Phantoms"]), "level": 4, "spawns": [], "expansion": "Old Iron King"},
    "Brume Tower": {"enemies": [[fs,bhm,enemiesDict["Maldron the Assassin"].id,ics],[],[]], "enemyExpansions": set(["Iron Keep", "Phantoms", "Executioner Chariot"]), "level": 4, "spawns": [], "expansion": "Executioner Chariot"},
    "Cells of the Dead": {"enemies": [[ics,sks,ch,sks,ch,ch,ics],[],[]], "enemyExpansions": set(["Dark Souls The Board Game", "Iron Keep"]), "level": 4, "spawns": [], "expansion": "Asylum Demon"},
    "Courtyard of Lothric": {"enemies": [[lhs,ch,fh,sks,skp,lhs,ch,fh,enemiesDict["Voracious Mimic"].id],[],[]], "enemyExpansions": set(["Explorers", "Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Vordt of the Boreal Valley"},
    "Cursed Cavern": {"enemies": [[lhs,skg,lhs,skg,s,ch,s,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "The Four Kings"},
    "Darkened Chamber": {"enemies": [[sk,mc,df,sk,mp,df],[],[]], "enemyExpansions": set(["Darkroot"]), "level": 4, "spawns": [], "expansion": "Gaping Dragon"},
    "Demon's Antechamber": {"enemies": [[lhs,hs,hs,skg,ch,ch,s,ch,lhs,hs],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Asylum Demon"},
    "Dragon Shrine": {"enemies": [[s,ch,hs,hs,hs,sks,sks,sks,ch,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Guardian Dragon"},
    "Edge of the Abyss": {"enemies": [[s,hs,lhs,ch,ch,skg,skg,sks,sks],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "The Four Kings"},
    "Entryway of the Chasm": {"enemies": [[sks,skg,sks,skg,sks,skg,ch,lhs,lhs],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Manus, Father of the Abyss"},
    "Forest of Fallen Giants": {"enemies": [[sks,lhs,ch,hs,ch,s,sks,lhs],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "The Last Giant"},
    "Fortress Gates": {"enemies": [[enemiesDict["Armorer Dennis"].id, abk,akc,ask,ics],[],[]], "enemyExpansions": set(["Phantoms", "Iron Keep"]), "level": 4, "spawns": [], "expansion": "Old Iron King"},
    "Gate of Peril": {"enemies": [[bhm,sg,fs,hs,fs,hs],[],[]], "enemyExpansions": set(["Darkroot", "Dark Souls The Board Game", "Executioner Chariot"]), "level": 4, "spawns": [], "expansion": "Executioner Chariot"},
    "Gough's Perch": {"enemies": [[lhs,ch,sk,ps,sk,ch,lhs,ps],[],[]], "enemyExpansions": set(["Dark Souls The Board Game", "Darkroot"]), "level": 4, "spawns": [], "expansion": "Black Dragon Kalameet"},
    "Great Stone Bridge": {"enemies": [[s,sks,ch,sks,ch,s,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Black Dragon Kalameet"},
    "Guarded Path": {"enemies": [[s,hs,hs,hs,s,skg,ch,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Vordt of the Boreal Valley"},
    "Hall of Wraiths": {"enemies": [[sk,sk,fh,skp,mp,mc],[],[]], "enemyExpansions": set(["Iron Keep", "Darkroot", "Explorers"]), "level": 4, "spawns": [], "expansion": "The Four Kings"},
    "Huntsman's Copse": {"enemies": [[bhm,bhm,ch,fs,hs],[],[]], "enemyExpansions": set(["Dark Souls The Board Game", "Executioner Chariot"]), "level": 4, "spawns": [], "expansion": "Executioner Chariot"},
    "Ironhearth Hall": {"enemies": [[sks,s,ch,ch,lhs,hs,hs,lhs,skg,skg],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Old Iron King"},
    "Lava Path": {"enemies": [[sks,ch,sks,ch,ch,s,s],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Lava Path"},
    "Manor Foregarden": {"enemies": [[sk,ics,df,df,sk,ics],[],[]], "enemyExpansions": set(["Darkroot", "Iron Keep"]), "level": 4, "spawns": [], "expansion": "Guardian Dragon"},
    "New Londo Ruins": {"enemies": [[akc,ch,ch,ics,ics,ask,abk],[],[]], "enemyExpansions": set(["Iron Keep", "Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "The Four Kings"},
    "Outskirts of Blighttown": {"enemies": [[s,sks,s,sks,lhs,ch,lhs,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Gaping Dragon"},
    "Perilous Crossing": {"enemies": [[lhs,ch,sks,sks,skg,lhs,ch,sks,skg,skg],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Black Dragon Kalameet"},
    "Research Library": {"enemies": [[sks,sks,fh,skp,ch,skp,ch,skp,skg,skg],[],[]], "enemyExpansions": set(["Explorers", "Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Guardian Dragon"},
    "Royal Woods Passage": {"enemies": [[sg,ps,akc,abk,sg,ps,abk,ps],[],[]], "enemyExpansions": set(["Iron Keep", "Darkroot"]), "level": 4, "spawns": [], "expansion": "Black Dragon Kalameet"},
    "Ruined Walkway": {"enemies": [[sk,sk,akc,abk,akc],[],[]], "enemyExpansions": set(["Darkroot", "Iron Keep"]), "level": 4, "spawns": [], "expansion": "Manus, Father of the Abyss"},
    "Scholars' Hall": {"enemies": [[lhs,ch,s,hs,s,hs,lhs,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Guardian Dragon"},
    "Sewers of Lordran": {"enemies": [[lhs,ch,ch,enemiesDict["Longfinger Kirk"].id,lhs,fh,fh,skp,skg],[],[]], "enemyExpansions": set(["Explorers", "Phantoms", "Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Gaping Dragon"},
    "The Desecrated Grave": {"enemies": [[lhs,lhs,ch,ch,s,s],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Manus, Father of the Abyss"},
    "Shadow of the Abyss": {"enemies": [[sk,lhs,mc,lhs,sk,sg],[],[]], "enemyExpansions": set(["Darkroot", "Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Manus, Father of the Abyss"},
    "Shattered Cell": {"enemies": [[lhs,hs,skp,skg,hs,sks,skg,ch,sks,skg,ch,lhs,hs,hs],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Asylum Demon"},
    "The Castle Grounds": {"enemies": [[akc,ask,akc,ask,akc,ask,abk,abk],[],[]], "enemyExpansions": set(["Iron Keep"]), "level": 4, "spawns": [], "expansion": "Vordt of the Boreal Valley"},
    "The Depths": {"enemies": [[sks,ch,ch,lhs,skg,sks,sks,ch,lhs,skg],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Gaping Dragon"},
    "The Dog's Domain": {"enemies": [[lhs,sks,skg,lhs,sks,s,ch,ch],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Vordt of the Boreal Valley"},
    "The Petrified Fallen": {"enemies": [[sg,ps,mp,mc,df,sg,ps],[],[]], "enemyExpansions": set(["Darkroot"]), "level": 4, "spawns": [], "expansion": "The Last Giant"},
    "Undead Purgatory": {"enemies": [[fs,ch,bhm,s,sks],[],[]], "enemyExpansions": set(["Executioner Chariot", "Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "Executioner Chariot"},
    "Wanderers Wood": {"enemies": [[s,ch,ch,hs,ch,hs,hs,s],[],[]], "enemyExpansions": set(["Dark Souls The Board Game"]), "level": 4, "spawns": [], "expansion": "The Last Giant"}
}

allEncounters = {}

for encounter in encounters:
    if any([enemyIds[enemy].expansion not in encounters[encounter]["enemyExpansions"] for enemy in encounters[encounter]["enemies"][0] + encounters[encounter]["enemies"][1] + encounters[encounter]["enemies"][2]]):
        pass
    if any([enemyIds[enemy].expansion not in encounters[encounter]["enemyExpansions"] for enemy in encounters[encounter]["spawns"]]):
        pass
    if encounters[encounter]["level"] < 4 and encounters[encounter]["expansion"] not in set([e.expansion for e in enemies]):
        pass
    
    allEncounters[encounter] = {
        "name": encounter,
        "expansion": encounters[encounter]["expansion"],
        "level": encounters[encounter]["level"],
        "tiles": {},
        "difficultyOrder": calculate_rank(encounters[encounter]["enemies"][0] + encounters[encounter]["enemies"][1] + encounters[encounter]["enemies"][2])
    }