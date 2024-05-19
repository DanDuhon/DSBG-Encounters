from json import dump
from os import path

from enemies import enemiesDict, enemyIds, enemies


baseFolder = path.dirname(__file__)


def calculate_rank(l, level, sortByToughness=False):
    diff = {}

    # We're not treating level 4s different from level 3s in the difficulty tier.
    if level == 4:
        level = 3
    
    if sortByToughness:
        for d in range(1, 5):
            a = {}
            for i, num in enumerate(sorted(l, key=lambda x: (-enemyIds[x].difficultyTiers[level]["toughness"], enemyIds[x].difficultyTiers[level]["difficulty"][d]))):
                if num not in a:
                    a[num] = [sum([1 for e in sorted(l, key=lambda x: (-enemyIds[x].difficultyTiers[level]["toughness"], enemyIds[x].difficultyTiers[level]["difficulty"][d]))[:i] if enemyIds[e].difficultyTiers[level]["toughness"] >= enemyIds[num].difficultyTiers[level]["toughness"]])]
                else:
                    a[num].append(sum([1 for e in sorted(l, key=lambda x: (-enemyIds[x].difficultyTiers[level]["toughness"], enemyIds[x].difficultyTiers[level]["difficulty"][d]))[:i] if enemyIds[e].difficultyTiers[level]["toughness"] >= enemyIds[num].difficultyTiers[level]["toughness"]]))

            diff[d] = [a[e][l[:i].count(e)] for i, e in enumerate(l)]
    else:
        for d in range(1, 5):
            a = {}
            for i, num in enumerate(sorted(l, key=lambda x: enemyIds[x].difficultyTiers[level]["difficulty"][d])):
                if num not in a:
                    a[num] = [sum([1 for e in sorted(l, key=lambda x: enemyIds[x].difficultyTiers[level]["difficulty"][d])[:i] if enemyIds[e].difficultyTiers[level]["difficulty"][d] <= enemyIds[num].difficultyTiers[level]["difficulty"][d]])]
                else:
                    a[num].append(sum([1 for e in sorted(l, key=lambda x: enemyIds[x].difficultyTiers[level]["difficulty"][d])[:i] if enemyIds[e].difficultyTiers[level]["difficulty"][d] <= enemyIds[num].difficultyTiers[level]["difficulty"][d]]))

            diff[d] = [a[e][l[:i].count(e)] for i, e in enumerate(l)]

    return diff


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
sh = enemiesDict["Shears Scarecrow"].id
skg = enemiesDict["Silver Knight Greatbowman"].id
skp = enemiesDict["Silver Knight Spearman"].id
sks = enemiesDict["Silver Knight Swordsman"].id
sa = enemiesDict["Skeleton Archer"].id
sb = enemiesDict["Skeleton Beast"].id
ss = enemiesDict["Skeleton Soldier"].id
sr = enemiesDict["Snow Rat"].id
sg = enemiesDict["Stone Guardian"].id
sk = enemiesDict["Stone Knight"].id
m = enemiesDict["Mimic"].id

asylum = "Asylum Demon"
kalameet = "Black Dragon Kalameet"
chariot = "Executioner Chariot"
gaping = "Gaping Dragon"
guardian = "Guardian Dragon"
manus = "Manus, Father of the Abyss"
iron = "Old Iron King"
kings = "The Four Kings"
last = "The Last Giant"
vordt = "Vordt of the Boreal Valley"

dsbg = "Dark Souls The Board Game"
dark = "Darkroot"
exp = "Explorers"
keep = "Iron Keep"
phan = "Phantoms"
paint = "Painted World of Ariamis"
tomb = "Tomb of Giants"
sun = "The Sunless City"

encounters = {
    "Ash Gardens": {"enemies": [[skg,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Ashen Hollow": {"enemies": [[ch,hs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Broken Passageway": {"enemies": [[sks,hs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Dark Hollow": {"enemies": [[lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Forsaken Depths": {"enemies": [[hs,ch,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Ghostly Keep": {"enemies": [[hs,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Hollow Cave": {"enemies": [[hs,hs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Ruined Keep": {"enemies": [[ch,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Shattered Dungeon": {"enemies": [[hs,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "The Deeps": {"enemies": [[sks,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "The Forgotten": {"enemies": [[hs,hs,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},
    "Unlighted Chamber": {"enemies": [[hs,ch,sks],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": dsbg},

    "Blackroot Well": {"enemies": [[df,ps,ps],[],[]], "enemyExpansions": set([dark]), "level": 1, "spawns": [[],[],[]], "expansion": dark},
    "Fearful Woods": {"enemies": [[ps,sh,mc],[],[]], "enemyExpansions": set([dark]), "level": 1, "spawns": [[],[],[]], "expansion": dark},
    "Leafy Grotto": {"enemies": [[sh,ps,df],[],[]], "enemyExpansions": set([dark]), "level": 1, "spawns": [[],[],[]], "expansion": dark},
    "Misty Woods": {"enemies": [[sh,sh,ps],[],[]], "enemyExpansions": set([dark]), "level": 1, "spawns": [[],[],[]], "expansion": dark},
    "Overgrown Caves": {"enemies": [[mc,df],[],[]], "enemyExpansions": set([dark]), "level": 1, "spawns": [[],[],[]], "expansion": dark},
    "Wild Glades": {"enemies": [[ps,sh,ps],[],[]], "enemyExpansions": set([dark]), "level": 1, "spawns": [[],[],[]], "expansion": dark},

    "Blazing Plaza": {"enemies": [[ask,ch,ch],[],[]], "enemyExpansions": set([keep,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": keep},
    "Burning Hold": {"enemies": [[abk,hs,ch],[],[]], "enemyExpansions": set([keep,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": keep},
    "Charred Keep": {"enemies": [[hs,ch,hs,abk],[],[]], "enemyExpansions": set([keep,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": keep},
    "Flaming Passageway": {"enemies": [[abk,ask],[],[]], "enemyExpansions": set([keep]), "level": 1, "spawns": [[],[],[]], "expansion": keep},
    "Furnace Room": {"enemies": [[ask,ch,abk],[],[]], "enemyExpansions": set([keep,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": keep},
    "Threshold Bridge": {"enemies": [[abk,hs,ch],[],[]], "enemyExpansions": set([keep,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": keep},

    "Burning Swamp": {"enemies": [[hs,ch,fh],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": exp},
    "Halls of the Forsworn": {"enemies": [[lhs,fh,hs],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": exp},
    "Lothric Castle": {"enemies": [[hs,fh,fh],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": exp},
    "Unholy Tunnels": {"enemies": [[skp,hs,fh],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": exp},
    "Wicked Vault": {"enemies": [[skp,fh],[],[]], "enemyExpansions": set([exp]), "level": 1, "spawns": [[],[],[]], "expansion": exp},

    "Quiet Graveyard": {"enemies": [[fs,skg,hs],[],[]], "enemyExpansions": set([chariot,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": chariot},
    "Silent Pathway": {"enemies": [[fs,hs,ch],[],[]], "enemyExpansions": set([chariot,dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": chariot},
    
    "Cloak and Feathers": {"enemies": [[cd],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "Frozen Sentries": {"enemies": [[ph,ph],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "No Safe Haven": {"enemies": [[sr,sr],[ez],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "Painted Passage": {"enemies": [[sr,sr,ph],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "Promised Respite": {"enemies": [[ph,sr],[sr,ez],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "Roll Out": {"enemies": [[bs,bs],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "Skittering Frenzy": {"enemies": [[sr,sr],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    "The First Bastion": {"enemies": [[sr],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[sr,ph,ez],[],[]], "expansion": paint},
    "Unseen Scurrying": {"enemies": [[sr,sr],[],[]], "enemyExpansions": set([paint]), "level": 1, "spawns": [[],[],[]], "expansion": paint},
    
    "Abandoned Storeroom": {"enemies": [[gss],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Bridge Too Far": {"enemies": [[ss,sa,ss],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Dark Resurrection": {"enemies": [[ss,n],[ss,ss,n],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Deathly Magic": {"enemies": [[ss,ss,n],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Grave Matters": {"enemies": [[ss,sa,ss,sa],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Last Rites": {"enemies": [[ss,ss],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Puppet Master": {"enemies": [[gss,n],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "Rain of Filth": {"enemies": [[sa,sa],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    "The Beast From the Depths": {"enemies": [[sb],[],[]], "enemyExpansions": set([tomb]), "level": 1, "spawns": [[],[],[]], "expansion": tomb},
    
    "Aged Sentinel": {"enemies": [[s],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    "Broken Passageway (TSC)": {"enemies": [[hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    "Dark Alleyway": {"enemies": [[sks,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    "Illusionary Doorway": {"enemies": [[ch,sks],[skg,hs,skg],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    "Kingdom's Messengers": {"enemies": [[hs,sks],[ch,ch,sks],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    "Shattered Keep": {"enemies": [[skg,ch,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    "Tempting Maw": {"enemies": [[skg,hs,hs,ch],[],[]], "enemyExpansions": set([dsbg,sun]), "level": 1, "spawns": [[m],[],[]], "expansion": sun},
    "The Bell Tower": {"enemies": [[ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[hs,hs],[],[]], "expansion": sun},
    "Undead Sanctum": {"enemies": [[hs,ch,ch],[hs,hs,sks],[]], "enemyExpansions": set([dsbg]), "level": 1, "spawns": [[],[],[]], "expansion": sun},
    
    "Black Dungeon": {"enemies": [[sks,sks,skg,sks],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Burned Gardens": {"enemies": [[lhs,sks,sks],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Demon Ruins": {"enemies": [[skg,sks,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Forgotten Gorge": {"enemies": [[hs,hs,skg,hs,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "High Wall of Lothric": {"enemies": [[lhs,hs,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Lightless Passage": {"enemies": [[lhs,hs,hs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Lost Labyrinth": {"enemies": [[lhs,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Prison Tower": {"enemies": [[sks,skg,sks],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Sentinel's Wrath": {"enemies": [[s],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Sunrise Pass": {"enemies": [[skg,skg,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Temple of the Deeps": {"enemies": [[hs,hs,ch,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    "Weathered Peak": {"enemies": [[sks,sks,ch,skg,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": dsbg},
    
    "Black Bog": {"enemies": [[df,sh,df,ps],[],[]], "enemyExpansions": set([dark]), "level": 2, "spawns": [[],[],[]], "expansion": dark},
    "Boggy Hollow": {"enemies": [[sg,mc],[],[]], "enemyExpansions": set([dark]), "level": 2, "spawns": [[],[],[]], "expansion": dark},
    "Haunted Ruins": {"enemies": [[sk,df],[],[]], "enemyExpansions": set([dark]), "level": 2, "spawns": [[],[],[]], "expansion": dark},
    "Murky Roots": {"enemies": [[mp,mc],[],[]], "enemyExpansions": set([dark]), "level": 2, "spawns": [[],[],[]], "expansion": dark},
    "Stone Hollow": {"enemies": [[ps,sh,sg],[],[]], "enemyExpansions": set([dark]), "level": 2, "spawns": [[],[],[]], "expansion": dark},
    "Withered Thicket": {"enemies": [[mp,mc,ps],[],[]], "enemyExpansions": set([dark]), "level": 2, "spawns": [[],[],[]], "expansion": dark},
    
    "Brass Sanctum": {"enemies": [[akc,abk,abk],[],[]], "enemyExpansions": set([keep]), "level": 2, "spawns": [[],[],[]], "expansion": keep},
    "Bronze Spire": {"enemies": [[abk,ics],[],[]], "enemyExpansions": set([keep]), "level": 2, "spawns": [[],[],[]], "expansion": keep},
    "Iron Depths": {"enemies": [[abk,abk,akc],[],[]], "enemyExpansions": set([keep]), "level": 2, "spawns": [[],[],[]], "expansion": keep},
    "Pyre of Souls": {"enemies": [[ics,ch],[],[]], "enemyExpansions": set([keep,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": keep},
    "Searing Hallway": {"enemies": [[ics,ask],[],[]], "enemyExpansions": set([keep]), "level": 2, "spawns": [[],[],[]], "expansion": keep},
    "Smouldering Labyrinth": {"enemies": [[akc,abk,ask],[],[]], "enemyExpansions": set([keep]), "level": 2, "spawns": [[],[],[]], "expansion": keep},
    
    "Lost Grotto": {"enemies": [[skp,skg,skp],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": exp},
    "Spirit Tomb": {"enemies": [[sks,skp,skg],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": exp},
    "Sunken Stairwell": {"enemies": [[skg,sks,skp],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": exp},
    "The Void Pit": {"enemies": [[fh,fh,lhs,fh],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": exp},
    "Unhallowed Caves": {"enemies": [[skp,skp,fh],[],[]], "enemyExpansions": set([exp]), "level": 2, "spawns": [[],[],[]], "expansion": exp},
    
    "Mausoleum Ruins": {"enemies": [[lhs,fs,ch,ch],[],[]], "enemyExpansions": set([chariot,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": chariot},
    "Misty Burial Site": {"enemies": [[ch,sks,hs,fs],[],[]], "enemyExpansions": set([chariot,dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": chariot},
    
    "Abandoned and Forgotten": {"enemies": [[],[],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[ph,ez,cd],[],[]], "expansion": paint},
    "Cold Snap": {"enemies": [[sr,sr],[ph,ez,ph],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    "Corrupted Hovel": {"enemies": [[sr,ez,ph,ez],[],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    "Distant Tower": {"enemies": [[ph,ph,sr],[bs,bs],[cd]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    "Gnashing Beaks": {"enemies": [[sr,sr],[cd],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[ph,ph,cd],[],[]], "expansion": paint},
    "Inhospitable Ground": {"enemies": [[sr,ez],[p],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    "Monstrous Maw": {"enemies": [[sr],[],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    "Skeletal Spokes": {"enemies": [[ez,ez],[bs,bs],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    "Snowblind": {"enemies": [[ph,bs],[ph,cd],[]], "enemyExpansions": set([paint]), "level": 2, "spawns": [[],[],[]], "expansion": paint},
    
    "Altar of Bones": {"enemies": [[ss,gsa],[ss,sa,gss],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    "In Deep Water": {"enemies": [[gsa,ss,ss,ss],[],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[sa,sa],[],[]], "expansion": tomb},
    "Far From the Sun": {"enemies": [[ss,gss],[ss,n,ss],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    "Lost Chapel": {"enemies": [[ss,ss,n],[sa,sa,n,ss],[sb]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    "Maze of the Dead": {"enemies": [[ss,n],[sb],[sa,ss,ss]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    "Pitch Black": {"enemies": [[sa,n,ss],[ss,ss,n],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    "The Abandoned Chest": {"enemies": [[ss,ss],[sa,n],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[gss,gsa],[]], "expansion": tomb},
    "The Mass Grave": {"enemies": [[gss],[ss,ss,gss],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    "Urns of the Fallen": {"enemies": [[sa,ss,ss],[sa,ss],[]], "enemyExpansions": set([tomb]), "level": 2, "spawns": [[],[],[]], "expansion": tomb},
    
    "The Fountainhead": {"enemies": [[ch,hs,hs,ch,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": sun},
    "Parish Gates": {"enemies": [[ch,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[hs,hs],[]], "expansion": sun},
    "Parish Church": {"enemies": [[hs,hs,skg],[sks,skg,hs],[ch,ch,ch,sks]], "enemyExpansions": set([dsbg,sun]), "level": 2, "spawns": [[],[],[m]], "expansion": sun},
    "The Hellkite Bridge": {"enemies": [[sks,ch,ch],[hs,hs,sks],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": sun},
    "The Shine of Gold": {"enemies": [[hs,hs,m],[],[]], "enemyExpansions": set([dsbg,sun]), "level": 2, "spawns": [[],[],[]], "expansion": sun},
    "Deathly Tolls": {"enemies": [[sks,sks],[skg,hs,hs,skg,ch],[]], "enemyExpansions": set([dsbg,sun]), "level": 2, "spawns": [[],[m],[]], "expansion": sun},
    "Flooded Fortress": {"enemies": [[ch,hs,m],[ch,ch],[]], "enemyExpansions": set([dsbg,sun]), "level": 2, "spawns": [[],[],[]], "expansion": sun},
    "Gleaming Silver": {"enemies": [[sks,skg],[hs,sks,skg],[]], "enemyExpansions": set([dsbg,sun]), "level": 2, "spawns": [[],[m],[]], "expansion": sun},
    "The Iron Golem": {"enemies": [[s],[],[]], "enemyExpansions": set([dsbg]), "level": 2, "spawns": [[],[],[]], "expansion": sun},
    
    "Cemetery of Ash": {"enemies": [[lhs,sks,sks,lhs,skg,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Central Irithyll": {"enemies": [[lhs,s,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Desecrated Church": {"enemies": [[sks,sks,skg,lhs,sks,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Dilapidated Bridge": {"enemies": [[lhs,hs,ch,lhs,hs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Empty Crypt": {"enemies": [[s,s],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Lost Shrine": {"enemies": [[sks,sks,skg,sks,skg,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Perished Depths": {"enemies": [[s,hs,hs,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Pit of the Dead": {"enemies": [[s,s,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Profane Shrine": {"enemies": [[sks,sks,sks,lhs,hs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Silent Tombs": {"enemies": [[lhs,sks,sks,lhs,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Untended Graves": {"enemies": [[skg,skg,s,sks],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    "Wretched Gardens": {"enemies": [[s,skg,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": dsbg},
    
    "Abandoned Tower": {"enemies": [[df,ps,ps,sk,ps],[],[]], "enemyExpansions": set([dark]), "level": 3, "spawns": [[],[],[]], "expansion": dark},
    "Corpselight Fens": {"enemies": [[sk,df,sg,df],[],[]], "enemyExpansions": set([dark]), "level": 3, "spawns": [[],[],[]], "expansion": dark},
    "Dark Woods": {"enemies": [[sg,sg,sk],[],[]], "enemyExpansions": set([dark]), "level": 3, "spawns": [[],[],[]], "expansion": dark},
    "Desolate Hinterland": {"enemies": [[sk,mp,mc],[],[]], "enemyExpansions": set([dark]), "level": 3, "spawns": [[],[],[]], "expansion": dark},
    "Hydra Lake": {"enemies": [[mp,df,mc,sk],[],[]], "enemyExpansions": set([dark]), "level": 3, "spawns": [[],[],[]], "expansion": dark},
    "Sodden Mire": {"enemies": [[df,ps,df,ps,sk],[],[]], "enemyExpansions": set([dark]), "level": 3, "spawns": [[],[],[]], "expansion": dark},
    
    "Castle Aflame": {"enemies": [[ask,ics,abk,akc],[],[]], "enemyExpansions": set([keep]), "level": 3, "spawns": [[],[],[]], "expansion": keep},
    "Hollowed Threshold": {"enemies": [[abk,akc,abk,abk,akc],[],[]], "enemyExpansions": set([keep]), "level": 3, "spawns": [[],[],[]], "expansion": keep},
    "Melting Gallery": {"enemies": [[akc,akc,akc],[],[]], "enemyExpansions": set([keep]), "level": 3, "spawns": [[],[],[]], "expansion": keep},
    "Shrine of the Torch": {"enemies": [[ask,ask,akc,abk,abk],[],[]], "enemyExpansions": set([keep]), "level": 3, "spawns": [[],[],[]], "expansion": keep},
    "Smoking Gallery": {"enemies": [[ask,ask,ask,abk,akc],[],[]], "enemyExpansions": set([keep]), "level": 3, "spawns": [[],[],[]], "expansion": keep},
    "Sweltering Sanctum": {"enemies": [[ics,ics,abk],[],[]], "enemyExpansions": set([keep]), "level": 3, "spawns": [[],[],[]], "expansion": keep},
    
    "Gallery of the Hidden Warrior": {"enemies": [[skp,skp,skg,skp,skg,skg],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": exp},
    "Giant's Keep": {"enemies": [[skp,sks,skg,skp,sks],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": exp},
    "Hidden Chamber": {"enemies": [[s,fh,fh,ch,lhs],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": exp},
    "Refuge of Silence": {"enemies": [[lhs,skp,fh,lhs,skp,fh],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": exp},
    "Scarlet Battlement": {"enemies": [[lhs,fh,hs,lhs,skp,fh],[],[]], "enemyExpansions": set([exp,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": exp},
    
    "Corrupted Crypt": {"enemies": [[fs,bhm,lhs,ch],[],[]], "enemyExpansions": set([chariot,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": chariot},
    "Desolate Cemetery": {"enemies": [[fs,skg,fs,bhm],[],[]], "enemyExpansions": set([chariot,dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": chariot},
    
    "Central Plaza": {"enemies": [[ph,ph,ph],[ez,ez],[sr,sr,cd]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[]], "expansion": paint},
    "Corvian Host": {"enemies": [[ph,ph,cd],[ph,ph,cd],[]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[cd,cd]], "expansion": paint},
    "Deathly Freeze": {"enemies": [[sr,sr,ez,ph],[bs,bs,ez],[]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[]], "expansion": paint},
    "Draconic Decay": {"enemies": [[bs],[bs,ez],[cd,ph,ph]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[]], "expansion": paint},
    "Eye of the Storm": {"enemies": [[ph,ph],[ph,ph,ez],[]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[p]], "expansion": paint},
    "Frozen Revolutions": {"enemies": [[sr,sr,ph,ph],[ph,ph],[bs,bs]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[]], "expansion": paint},
    "The Last Bastion": {"enemies": [[p,cd],[],[]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[]], "expansion": paint},
    "Trecherous Tower": {"enemies": [[ph,ph],[],[]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[ph,ez,cd],[]], "expansion": paint},
    "Velka's Chosen": {"enemies": [[ez,ez],[cd,sr,sr],[]], "enemyExpansions": set([paint]), "level": 3, "spawns": [[],[],[]], "expansion": paint},
    
    "A Trusty Ally": {"enemies": [[sa,ss,sa,gss],[ss,ss,sb],[]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[]], "expansion": tomb},
    "Death's Precipice": {"enemies": [[sa,ss,ss],[gsa,gss],[gsa,gss,sb]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[]], "expansion": tomb},
    "Giant's Coffin": {"enemies": [[gss,gsa],[gss,gsa],[]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[gsa,gss],[]], "expansion": tomb},
    "Honour Guard": {"enemies": [[ss,sa,ss,ss,sa],[],[]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[]], "expansion": tomb},
    "Lakeview Refuge": {"enemies": [[n,ss,ss],[sa,sa],[n,gsa,gss]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[sb]], "expansion": tomb},
    "Last Shred of Light": {"enemies": [[sb,ss,sa],[gsa],[]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[]], "expansion": tomb},
    "Skeleton Overlord": {"enemies": [[gss],[],[]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[ss,ss],[],[]], "expansion": tomb},
    "The Locked Grave": {"enemies": [[gsa,ss],[gss,n],[gsa,sa,sa]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[sb]], "expansion": tomb},
    "The Skeleton Ball": {"enemies": [[n,gsa],[sa,gss],[gsa,n,ss,ss]], "enemyExpansions": set([tomb]), "level": 3, "spawns": [[],[],[]], "expansion": tomb},
    
    "Grim Reunion": {"enemies": [[hs,hs,ch,skg],[s,sks],[skg,hs,sks,ch]], "enemyExpansions": set([dsbg,sun]), "level": 3, "spawns": [[],[],[m]], "expansion": sun},
    "Castle Break In": {"enemies": [[hs,hs,s],[hs,ch,ch],[sks,skg,skg]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": sun},
    "Archive Entrance": {"enemies": [[m,skg,skg,s],[],[]], "enemyExpansions": set([dsbg,sun]), "level": 3, "spawns": [[],[],[]], "expansion": sun},
    "Central Plaza (TSC)": {"enemies": [[sks,sks,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[s],[],[]], "expansion": sun},
    "Hanging Rafters": {"enemies": [[ch,sks,skg],[skg,ch,hs,sks],[]], "enemyExpansions": set([dsbg]), "level": 3, "spawns": [[],[],[]], "expansion": sun},
    "Depths of the Cathedral": {"enemies": [[sks,hs,hs,hs],[sks,hs,skg,hs],[ch,ch,s,ch,hs]], "enemyExpansions": set([dsbg,sun]), "level": 3, "spawns": [[],[m],[]], "expansion": sun},
    "Trophy Room": {"enemies": [[hs,m,hs,hs],[sks,ch,sks,ch],[]], "enemyExpansions": set([dsbg,sun]), "level": 3, "spawns": [[],[],[]], "expansion": sun},
    "The Grand Hall": {"enemies": [[ch,ch,sks],[sks,s,skg,sks],[s,skg,skg]], "enemyExpansions": set([dsbg,sun]), "level": 3, "spawns": [[],[m],[]], "expansion": sun},
    "Twilight Falls": {"enemies": [[sks,sks,skg,skg],[ch,hs,m],[s,hs,ch,ch,sks]], "enemyExpansions": set([dsbg,sun]), "level": 3, "spawns": [[],[],[]], "expansion": sun},

    "Asylum's North Hall": {"enemies": [[sk,skp,ps,fh,ps,fh,sk,skp],[],[]], "enemyExpansions": set([exp, dark]), "level": 4, "spawns": [[],[],[]], "expansion": asylum},
    "Cells of the Dead": {"enemies": [[ics,sks,ch,sks,ch,ch,ics],[],[]], "enemyExpansions": set([dsbg, keep]), "level": 4, "spawns": [[],[],[]], "expansion": asylum},
    "Demon's Antechamber": {"enemies": [[lhs,hs,hs,skg,ch,ch,s,ch,lhs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": asylum},
    "Shattered Cell": {"enemies": [[lhs,hs,sks,skg,ch,sks,skg,ch,lhs,hs,hs],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": asylum},

    "Gough's Perch": {"enemies": [[lhs,ch,sk,ps,sk,ch,lhs,ps],[],[]], "enemyExpansions": set([dsbg, dark]), "level": 4, "spawns": [[],[],[]], "expansion": kalameet},
    "Great Stone Bridge": {"enemies": [[s,sks,ch,sks,ch,s,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": kalameet},
    "Perilous Crossing": {"enemies": [[lhs,ch,sks,sks,skg,lhs,ch,sks,skg,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": kalameet},
    "Royal Woods Passage": {"enemies": [[sg,ps,akc,abk,sg,ps,abk,ps],[],[]], "enemyExpansions": set([keep, dark]), "level": 4, "spawns": [[],[],[]], "expansion": kalameet},

    "Brume Tower": {"enemies": [[fs,bhm,enemiesDict["Maldron the Assassin"].id,ics],[],[]], "enemyExpansions": set([keep, phan, chariot]), "level": 4, "spawns": [[],[],[]], "expansion": chariot},
    "Gate of Peril": {"enemies": [[bhm,sg,fs,hs,fs,hs,df],[],[]], "enemyExpansions": set([dark, dsbg, chariot]), "level": 4, "spawns": [[],[],[]], "expansion": chariot},
    "Huntsman's Copse": {"enemies": [[bhm,bhm,ch,fs,hs],[],[]], "enemyExpansions": set([dsbg, chariot]), "level": 4, "spawns": [[],[],[]], "expansion": chariot},
    "Undead Purgatory": {"enemies": [[fs,ch,bhm,s,sks],[],[]], "enemyExpansions": set([chariot, dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": chariot},

    "Darkened Chamber": {"enemies": [[sk,mc,df,sk,mp,df],[],[]], "enemyExpansions": set([dark]), "level": 4, "spawns": [[],[],[]], "expansion": gaping},
    "Outskirts of Blighttown": {"enemies": [[s,skg,s,skg,lhs,ch,lhs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": gaping},
    "Sewers of Lordran": {"enemies": [[lhs,ch,ch,enemiesDict["Longfinger Kirk"].id,lhs,fh,fh,skp,skg],[],[]], "enemyExpansions": set([exp, phan, dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": gaping},
    "The Depths": {"enemies": [[sks,ch,ch,lhs,skg,sks,sks,ch,lhs,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": gaping},

    "Dragon Shrine": {"enemies": [[s,ch,hs,hs,hs,sks,sks,sks,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": guardian},
    "Manor Foregarden": {"enemies": [[sk,ics,df,df,sk,ics],[],[]], "enemyExpansions": set([dark, keep]), "level": 4, "spawns": [[],[],[]], "expansion": guardian},
    "Research Library": {"enemies": [[sks,sks,fh,skp,ch,skp,ch,sks,skg,skg],[],[]], "enemyExpansions": set([exp, dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": guardian},
    "Scholars' Hall": {"enemies": [[lhs,ch,s,hs,s,hs,lhs,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": guardian},

    "Entryway of the Chasm": {"enemies": [[sks,skg,sks,skg,sks,skg,ch,lhs,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": manus},
    "Ruined Walkway": {"enemies": [[sk,sk,akc,abk,akc],[],[]], "enemyExpansions": set([dark, keep]), "level": 4, "spawns": [[],[],[]], "expansion": manus},
    "Shadow of the Abyss": {"enemies": [[sk,lhs,mc,lhs,sk,sg],[],[]], "enemyExpansions": set([dark, dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": manus},
    "The Desecrated Grave": {"enemies": [[lhs,lhs,ch,ch,s,s],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": manus},

    "Blazing Furnace": {"enemies": [[akc,ask,fh,fh,ics,enemiesDict["Fencer Sharron"].id],[],[]], "enemyExpansions": set([exp, keep, phan]), "level": 4, "spawns": [[],[],[]], "expansion": iron},
    "Fortress Gates": {"enemies": [[enemiesDict["Armorer Dennis"].id, abk,akc,ask,ics],[],[]], "enemyExpansions": set([phan, keep]), "level": 4, "spawns": [[],[],[]], "expansion": iron},
    "Ironhearth Hall": {"enemies": [[sks,s,ch,ch,lhs,hs,hs,lhs,skg,skg],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": iron},
    "Lava Path": {"enemies": [[sks,ch,sks,ch,ch,s,s],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": iron},

    "Cursed Cavern": {"enemies": [[lhs,skg,lhs,skg,s,ch,s,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": kings},
    "Edge of the Abyss": {"enemies": [[s,hs,lhs,ch,ch,skg,skg,sks,sks],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": kings},
    "Hall of Wraiths": {"enemies": [[sk,sk,fh,skp,mp,mc],[],[]], "enemyExpansions": set([dark, exp]), "level": 4, "spawns": [[],[],[]], "expansion": kings},
    "New Londo Ruins": {"enemies": [[akc,ch,ch,ics,ics,ask,abk],[],[]], "enemyExpansions": set([keep, dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": kings},

    "Base of Cardinal Tower": {"enemies": [[skp,fh,skp,abk,abk,skp,abk,ics,fh],[],[]], "enemyExpansions": set([keep, exp]), "level": 4, "spawns": [[],[],[]], "expansion": last},
    "Forest of Fallen Giants": {"enemies": [[sks,lhs,ch,hs,ch,s,sks,lhs],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": last},
    "The Petrified Fallen": {"enemies": [[sg,ps,mp,mc,df,sg,ps],[],[]], "enemyExpansions": set([dark]), "level": 4, "spawns": [[],[],[]], "expansion": last},
    "Wanderers Wood": {"enemies": [[s,ch,ch,hs,ch,hs,hs,s],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": last},

    "Courtyard of Lothric": {"enemies": [[lhs,ch,fh,sks,skp,lhs,ch,fh,enemiesDict["Voracious Mimic"].id],[],[]], "enemyExpansions": set([exp, dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": vordt},
    "Guarded Path": {"enemies": [[s,hs,hs,hs,s,skg,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": vordt},
    "The Castle Grounds": {"enemies": [[akc,ask,akc,ask,akc,ask,abk,abk],[],[]], "enemyExpansions": set([keep]), "level": 4, "spawns": [[],[],[]], "expansion": vordt},
    "The Dog's Domain": {"enemies": [[lhs,sks,skg,lhs,sks,s,ch,ch],[],[]], "enemyExpansions": set([dsbg]), "level": 4, "spawns": [[],[],[]], "expansion": vordt}
}

allEncounters = {}

# For these encounters, it made more sense to sort the enemies
# by toughness rather than difficulty.
toughnessSortedEncounters = {
    "Cold Snap",
    "Dark Alleyway",
    "Deathly Freeze",
    "No Safe Haven"
}

for encounter in encounters:
    encounterEnemies = (encounters[encounter]["enemies"][0]
                        + encounters[encounter]["spawns"][0]
                        + encounters[encounter]["enemies"][1]
                        + encounters[encounter]["spawns"][1]
                        + encounters[encounter]["enemies"][2]
                        + encounters[encounter]["spawns"][2])
    if any([enemyIds[enemy].expansion not in encounters[encounter]["enemyExpansions"] for enemy in encounterEnemies]):
        pass
    if encounters[encounter]["enemyExpansions"] - set([enemyIds[enemy].expansion for enemy in encounterEnemies]):
        pass
    if encounters[encounter]["level"] < 4 and encounters[encounter]["expansion"] not in set([e.expansion for e in enemies]):
        pass
    
    allEncounters[encounter] = {
        "name": encounter,
        "expansion": encounters[encounter]["expansion"],
        "level": encounters[encounter]["level"],
        "tiles": {"1": {"enemies": [], "spawns": []}, "2": {"enemies": [], "spawns": []}, "3": {"enemies": [], "spawns": []}},
        "difficultyOrder": calculate_rank(encounterEnemies, encounters[encounter]["level"], sortByToughness=encounter in toughnessSortedEncounters)
    }

    for i in range(1, 4):
        if (encounters[encounter]["enemies"][i-1]
                or encounters[encounter]["spawns"][i-1]
                or (encounter == "Abandoned and Forgotten" and i < 3)
                or encounter == "Trecherous Tower"):
            allEncounters[encounter]["tiles"][str(i)] = {"enemies": encounters[encounter]["enemies"][i-1], "spawns": encounters[encounter]["spawns"][i-1]}
            if i > 1 and not encounters[encounter]["enemies"][i-1] and not encounters[encounter]["spawns"][i-1]:
                allEncounters[encounter]["tiles"][str(i)] = {"enemies": [], "spawns": []}

    # Lakeview Refuge spawns a number of Skeleton Soldiers equal to the number of characters.
    if encounter == "Lakeview Refuge":
        for i in range(1, 5):
            encounterEnemies.extend([ss])
            allEncounters[encounter]["difficultyOrder"][i] = calculate_rank(encounterEnemies, encounters[encounter]["level"])[i]

with open(baseFolder + "\\encounters\\all_encounters.json", "w") as file:
    dump(allEncounters, file)
