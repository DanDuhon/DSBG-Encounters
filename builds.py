from typing import Dict

from models import Character, Attack, BuildKey

# ---------- Class & tier config ----------

CLASS_NAMES = [
    "Assassin", "Cleric", "Deprived", "Herald", "Knight",
    "Mercenary", "Pyromancer", "Sorcerer", "Thief", "Warrior",
]

TIER_LABELS = ["T0", "T1", "T2", "T3"]

PLAYER_COUNTS = [1, 2, 3, 4]

# Tier -> allowed build tiers
# Tier 1: T0 & T1 builds
# Tier 2: T1 & T2 builds
# Tier 3: T2 & T3 builds
TIER_CONFIG = {
    "tier1": ("T0", "T1"),
    "tier2": ("T1", "T2"),
    "tier3": ("T2", "T3"),
}

# ---------- Placeholder (for classes not yet defined) ----------

def make_placeholder_build(cls_name: str, tier: str, party_size: int) -> Character:
    """
    TEMP: simple placeholder builds so the pipeline runs.
    Replace this gradually as you add real class builders.
    """
    tier_idx = TIER_LABELS.index(tier)  # 0..3

    # Defense scales a bit with tier
    block_phys = ["black"]
    block_magic = ["black"]
    dodge = 1
    if tier_idx >= 1:
        block_phys = ["black", "black"]
    if tier_idx >= 2:
        block_magic = ["black", "black"]
    if tier_idx >= 3:
        dodge = 2

    atk_dice = ["black"] * (1 + tier_idx)   # T0: 1 die, T1: 2 dice, etc.

    attacks = [
        Attack("physical", atk_dice, flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
    ]

    return Character(
        cls_name=cls_name,
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

# ---------- Real Knight builds ----------

def make_knight_build(tier: str, party_size: int) -> Character:
    """
    Knight builds T0–T3.

    T0 starter Knight from your description.
    Higher tiers here are illustrative; swap dice/stamina to match your real design.
    """
    if tier == "T0":
        block_phys = ["blue", "black"]
        block_magic = ["black"]
        dodge = 0
        attacks = [
            Attack("physical", ["blue"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["blue", "black"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]

    elif tier == "T1":
        block_phys = ["blue", "black"]
        block_magic = ["black"]
        dodge = 0
        attacks = [
            Attack("physical", ["blue", "black"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["blue", "orange"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]

    elif tier == "T2":
        block_phys = ["blue", "blue", "black"]
        block_magic = ["black", "black"]
        dodge = 0
        attacks = [
            Attack("physical", ["blue", "orange"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["orange", "orange"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]

    elif tier == "T3":
        block_phys = ["blue", "blue", "black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            Attack("physical", ["blue", "orange"], flat_mod=1, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["orange", "orange"], flat_mod=1, stamina_cost=3, min_range=0, max_range=0),
        ]

    else:
        return make_placeholder_build("Knight", tier, party_size)

    # Optionally branch on party_size here if you want solo/4p variants.

    return Character(
        cls_name="Knight",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

# ---------- Real Sorcerer builds ----------

def make_sorcerer_build(tier: str, party_size: int) -> Character:
    """
    Sorcerer builds T0–T3.
    """
    if tier == "T0":
        block_phys = ["black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            Attack("magic", ["blue"], flat_mod=0, stamina_cost=1, min_range=1, max_range=3),
            Attack("magic", ["black", "black"], flat_mod=0, stamina_cost=3, min_range=1, max_range=3),
        ]

    elif tier == "T1":
        block_phys = ["black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            Attack("magic", ["blue"], flat_mod=0, stamina_cost=0, min_range=1, max_range=3),
            Attack("magic", ["blue", "black"], flat_mod=0, stamina_cost=3, min_range=1, max_range=3),
        ]

    elif tier == "T2":
        block_phys = ["black", "black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            Attack("magic", ["blue", "black"], flat_mod=0, stamina_cost=0, min_range=1, max_range=3),
            Attack("magic", ["blue", "blue"], flat_mod=0, stamina_cost=3, min_range=1, max_range=3),
        ]

    elif tier == "T3":
        block_phys = ["black"]
        block_magic = ["blue", "blue", "black"]
        dodge = 2
        attacks = [
            Attack("magic", ["blue", "black"], flat_mod=1, stamina_cost=0, min_range=1, max_range=3),
            Attack("magic", ["blue", "blue"], flat_mod=1, stamina_cost=3, min_range=1, max_range=3),
        ]

    else:
        return make_placeholder_build("Sorcerer", tier, party_size)

    return Character(
        cls_name="Sorcerer",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

# ---------- Router + bulk builder ----------

def make_build_for(cls_name: str, tier: str, party_size: int) -> Character:
    """
    Main entry point for building a Character for (class, tier, party_size).
    Extend this with more classes as you define them.
    """
    if cls_name == "Knight":
        return make_knight_build(tier, party_size)
    elif cls_name == "Sorcerer":
        return make_sorcerer_build(tier, party_size)
    else:
        return make_placeholder_build(cls_name, tier, party_size)


def build_all_builds() -> Dict[BuildKey, Character]:
    builds: Dict[BuildKey, Character] = {}
    for cls in CLASS_NAMES:
        for tier in TIER_LABELS:
            for P in PLAYER_COUNTS:
                key: BuildKey = (cls, tier, P)
                builds[key] = make_build_for(cls, tier, P)
    return builds
