"""
Concept of "risk" or exposure for an attack:
    - Stamina Cost = Average stamina cost to move into range (similar to reach mod for enemies) + Stamina cost of attack
    - 11 - Stamina Cost = safety score
Expected damage vs score tier defense / safety = overall attack score

Could also give a range of scores for items that have upgrade slots.  Brute force upgrade combos and calculate the average for 1, 2, and 3 upgrades.

For defense, I'll need to calculate average damage for each level of dodge because I can't just take an average of that.
    Those will be modified by their presence in the tier.

"""