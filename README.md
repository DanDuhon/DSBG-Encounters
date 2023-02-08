# DSBG-Encounters
Code for calculating enemy strength and generating encounter alternatives for https://github.com/DanDuhon/DSBG-Shuffle.

This stuff is done separately from DSBG-Shuffle so it doesn't have to be done at runtime.

These scripts are the back-end generators for DSGB-Shuffle.

armor.py - all armor in official releases (as of 1/1/2023), used to generate loadouts

attacks.py - each attack for all weapons in official releases, used to calculate enemy toughness

encounters.py - generates alternative enemies for encounters based on enemy strength

enemies.py - defines an enemy, referenced by other scripts

enemy_strength.py - scores enemies based on damage and toughness

hand_items.py - all weapons, spells, shields, etc. in official releases, used to generate loadouts

loadouts.py - generates combinations of items into loadouts that are used to calculate enemy damage
