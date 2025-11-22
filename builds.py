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
        Attack("physical", atk_dice, flat_mod=0, min_range=0, max_range=0),
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

def make_knight_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["blue", "black"]
        block_magic = ["black"]
        dodge = 0
        attacks = [
            Attack(["blue"]),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["orange", "black"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "black"]),
                Attack(["blue"])
            ]

        elif tier == "T2":
            block_phys = ["black", "blue", "orange"]
            block_magic = ["black", "orange", "orange"]
            dodge = 0
            attacks = [
                Attack(["blue", "black"], flat_mod=1, shift=True),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue", "orange"]
            block_magic = ["blue", "blue", "orange"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue", "black"], flat_mod=1),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["orange", "black", "black"]
            block_magic = ["blue", "black", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "black"], shift=True)
            ]

        elif tier == "T2":
            block_phys = ["black", "blue", "orange"]
            block_magic = ["black", "blue", "orange"]
            dodge = 0
            attacks = [
                Attack(["blue", "black"], flat_mod=1, shift=True),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue", "orange"]
            block_magic = ["blue", "blue", "orange"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue", "black"], flat_mod=1),
            ]
            
    elif party_size == 3:
        if tier == "T1":
            block_phys = ["blue", "black"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "black"])
            ]

        elif tier == "T2":
            block_phys = ["orange", "black", "black"]
            block_magic = ["blue", "black", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "black"], flat_mod=1, shift=True)
            ]

        elif tier == "T3":
            block_phys = ["black", "blue", "orange"]
            block_magic = ["black", "blue", "orange"]
            dodge = 0
            attacks = [
                Attack(["blue", "black", "black"], shift=True)
            ]
            
    elif party_size == 4:
        if tier == "T1":
            block_phys = ["blue", "blue"]
            block_magic = []
            dodge = 1
            attacks = [
                Attack(["black", "black"])
            ]

        elif tier == "T2":
            block_phys = ["blue", "black"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "black"], flat_mod=1)
            ]

        elif tier == "T3":
            block_phys = ["black", "blue", "orange"]
            block_magic = ["black", "blue", "orange"]
            dodge = 0
            attacks = [
                Attack(["blue", "black", "black"], shift=True)
            ]

    return Character(
        cls_name="Knight",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_assassin_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black"]
        block_magic = ["black"]
        dodge = 2
        attacks = [
            Attack(["black", "black"], flat_mod=-1),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = []
            block_magic = []
            dodge = 2
            attacks = [
                Attack(["orange", "orange"], flat_mod=-2, apply_poison=True, max_range=1),
                Attack(["orange", "orange"], apply_bleed=True, max_range=1, flat_mod=-2)
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 4
            attacks = [
                Attack(["orange", "orange", "orange"], flat_mod=-2, apply_bleed=True, apply_poison=True),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["blue", "black", "black"]
            dodge = 5
            attacks = [
                Attack(["blue", "blue", "black", "orange", "orange"], flat_mod=-3, shift=True),
                Attack(["orange", "orange", "black", "orange", "orange"], flat_mod=-3),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = []
            block_magic = []
            dodge = 2
            attacks = [
                Attack(["black", "black", "orange", "orange"], flat_mod=-3, apply_poison=True, max_range=1),
                Attack(["orange", "orange"], apply_bleed=True, max_range=1, flat_mod=-2)
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 4
            attacks = [
                Attack(["orange", "orange", "orange"], flat_mod=-2, apply_bleed=True, apply_poison=True),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["blue", "black", "black"]
            dodge = 5
            attacks = [
                Attack(["blue", "blue", "black", "orange", "orange"], flat_mod=-3, shift=True),
                Attack(["orange", "orange", "black", "orange", "orange"], flat_mod=-3),
            ]
            
    elif party_size == 3:
        if tier == "T1":
            block_phys = []
            block_magic = []
            dodge = 2
            attacks = [
                Attack(["orange", "orange"], flat_mod=-2, apply_poison=True, max_range=1),
                Attack(["orange", "orange"], apply_bleed=True, max_range=1, flat_mod=-2)
            ]

        elif tier == "T2":
            block_phys = []
            block_magic = []
            dodge = 2
            attacks = [
                Attack(["orange", "orange"], flat_mod=-2, apply_poison=True, max_range=1),
                Attack(["orange", "orange"], apply_bleed=True, max_range=1, flat_mod=-2)
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["blue", "black", "black"]
            dodge = 4
            attacks = [
                Attack(["orange", "orange", "orange"], flat_mod=-2, apply_bleed=True, apply_poison=True),
            ]
            
    elif party_size == 4:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 1
            attacks = [
                Attack([], apply_poison=True, max_range=1),
                Attack([], apply_bleed=True, max_range=1)
            ]

        elif tier == "T2":
            block_phys = []
            block_magic = []
            dodge = 2
            attacks = [
                Attack(["orange", "orange"], flat_mod=-2, apply_poison=True, max_range=1),
                Attack(["orange", "orange"], apply_bleed=True, max_range=1, flat_mod=-2)
            ]

        elif tier == "T3":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 4
            attacks = [
                Attack(["orange", "orange", "orange"], flat_mod=-2, apply_bleed=True, apply_poison=True),
            ]

    return Character(
        cls_name="Assassin",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_sorcerer_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            Attack(damage_type="magic", dice=["blue"], max_range=3),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black"], max_range=3, apply_stagger=True),
                Attack(damage_type="magic", dice=["blue", "black"], max_range=3),
            ]

        elif tier == "T2":
            block_phys = ["blue"]
            block_magic = ["blue", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["blue"], flat_mod=2, max_range=1),
            ]

        elif tier == "T3":
            block_phys = ["blue"]
            block_magic = ["blue", "black"]
            dodge = 2
            attacks = [
                Attack(damage_type="magic", dice=["blue"], flat_mod=2, max_range=1),
                Attack(damage_type="magic", dice=["blue", "blue"], max_range=1),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black"], max_range=3, apply_stagger=True),
                Attack(damage_type="magic", dice=["blue", "black"], max_range=3),
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["blue", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black"], max_range=3, apply_stagger=True),
                Attack(damage_type="magic", dice=["blue", "black"], max_range=3),
            ]

        elif tier == "T3":
            block_phys = ["blue"]
            block_magic = ["blue", "black"]
            dodge = 2
            attacks = [
                Attack(damage_type="magic", dice=["blue"], flat_mod=2, max_range=1),
                Attack(damage_type="magic", dice=["blue", "blue"], max_range=1),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black"], max_range=3, apply_stagger=True),
                Attack(damage_type="magic", dice=["blue", "black"], max_range=3),
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["blue", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=1, shift=True),
                Attack([], push=True)
            ]

        elif tier == "T3":
            block_phys = ["black"]
            block_magic = ["blue", "black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black", "black"], flat_mod=1, max_range=1),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["blue"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["blue"], max_range=3),
                Attack(damage_type="magic", dice=["blue", "black"], max_range=3),
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black"], max_range=3, apply_stagger=True),
                Attack(damage_type="magic", dice=["blue", "black"], max_range=3),
            ]

        elif tier == "T3":
            block_phys = ["black"]
            block_magic = ["blue", "black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black", "black"], flat_mod=1, max_range=1),
            ]

    return Character(
        cls_name="Sorcerer",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_pyromancer_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["blue"]
        block_magic = ["black", "black"]
        dodge = 1
        attacks = [
            Attack(damage_type="magic", dice=["black"], max_range=2),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=2),
                Attack([], max_range=1, apply_poison=True),
            ]

        elif tier == "T2":
            block_phys = ["orange"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["blue"], max_range=2, push=True),
                Attack(["blue"], flat_mod=2, max_range=1),
            ]

        elif tier == "T3":
            block_phys = ["orange"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["orange"], max_range=2, push=True),
                Attack(["blue"], flat_mod=2, max_range=1),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=2),
                Attack([], max_range=1, apply_poison=True),
            ]

        elif tier == "T2":
            block_phys = ["blue"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], flat_mod=1, max_range=1),
            ]

        elif tier == "T3":
            block_phys = ["orange"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["orange"], max_range=2, push=True),
                Attack(["blue"], flat_mod=2, max_range=1),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=2),
                Attack([], max_range=1, apply_poison=True),
            ]

        elif tier == "T2":
            block_phys = ["blue"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], flat_mod=1, max_range=1),
            ]

        elif tier == "T3":
            block_phys = ["orange"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["orange"], max_range=2, push=True),
                Attack(["blue"], flat_mod=2, max_range=1),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["black", "black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=3)
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=2),
                Attack([], max_range=1, apply_poison=True),
            ]

        elif tier == "T3":
            block_phys = ["black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black", "black"], flat_mod=1, max_range=1),
            ]

    return Character(
        cls_name="Pyromancer",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_cleric_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black", "black"]
        block_magic = ["blue", "black"]
        dodge = 0
        attacks = [
            Attack(["blue"]),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["black", "black", "blue"]
            block_magic = ["black", "black", "blue"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["orange", "blue"]
            block_magic = ["orange", "orange"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "blue"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["orange", "black", "black", "black"]
            block_magic = ["orange", "black", "black", "black", "black", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "blue", "blue"]),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["black", "black", "blue"]
            block_magic = ["black", "black", "blue"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["orange", "black", "black"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "blue"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["orange", "black", "black", "black"]
            block_magic = ["orange", "black", "black", "black", "black", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "blue", "blue"]),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["black", "black", "blue"]
            dodge = 0
            attacks = [
                Attack(["blue"])
            ]

        elif tier == "T2":
            block_phys = ["black", "black", "blue"]
            block_magic = ["black", "black", "blue"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["black", "blue"], flat_mod=1)
            ]

        elif tier == "T3":
            block_phys = ["orange", "black", "black"]
            block_magic = ["orange", "black", "black", "black", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "blue"], flat_mod=2),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["blue", "black"]
            block_magic = ["black", "black", "blue"]
            dodge = 0
            attacks = [
                Attack(["blue"])
            ]

        elif tier == "T2":
            block_phys = ["blue", "black", "black"]
            block_magic = ["black", "black", "blue"]
            dodge = 0
            attacks = [
                Attack(["blue"], flat_mod=1)
            ]

        elif tier == "T3":
            block_phys = ["orange", "black", "black"]
            block_magic = ["orange", "black", "black", "black", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "blue"], flat_mod=2),
            ]

    return Character(
        cls_name="Cleric",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_deprived_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black"]
        block_magic = []
        dodge = 0
        attacks = [
            Attack(["black"]),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["black", "black", "black"]
            block_magic = ["black"]
            dodge = 3
            attacks = [
                Attack(["black", "blue", "blue"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["blue", "black", "black"]
            block_magic = ["orange"]
            dodge = 3
            attacks = [
                Attack(["black", "black", "black", "blue", "blue"]),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["black", "black", "black"]
            block_magic = ["black"]
            dodge = 3
            attacks = [
                Attack(["black", "blue", "blue"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["blue", "black", "black"]
            block_magic = ["orange"]
            dodge = 3
            attacks = [
                Attack(["black", "black", "black", "blue", "blue"]),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["black", "black", "black"]
            block_magic = ["black"]
            dodge = 3
            attacks = [
                Attack(["blue", "blue"], flat_mod=2),
            ]

        elif tier == "T3":
            block_phys = ["blue", "black", "black"]
            block_magic = ["orange"]
            dodge = 3
            attacks = [
                Attack(["black", "black", "black", "blue", "blue"]),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["blue", "black"]
            block_magic = ["black"]
            dodge = 2
            attacks = [
                Attack(["black", "black", "black"], max_range=3)
            ]

        elif tier == "T2":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue"]
            dodge = 3
            attacks = [
                Attack(["black", "black", "black", "blue", "blue"]),
            ]

    return Character(
        cls_name="Deprived",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_herald_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black", "black"]
        block_magic = ["black"]
        dodge = 1
        attacks = [
            Attack(["black"], max_range=1),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue", "black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=3)
            ]

        elif tier == "T2":
            block_phys = ["orange"]
            block_magic = ["orange"]
            dodge = 0
            attacks = [
                Attack(["orange", "orange"]),
            ]

        elif tier == "T3":
            block_phys = ["orange", "blue", "black"]
            block_magic = ["orange", "orange", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue", "black", "black"], flat_mod=1),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue", "black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=3)
            ]

        elif tier == "T2":
            block_phys = ["orange"]
            block_magic = ["orange"]
            dodge = 0
            attacks = [
                Attack(["orange", "orange"]),
            ]

        elif tier == "T3":
            block_phys = ["orange", "blue", "black"]
            block_magic = ["orange", "orange", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue", "black", "black"], flat_mod=1),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue", "black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], max_range=3)
            ]

        elif tier == "T2":
            block_phys = ["orange", "black", "black"]
            block_magic = ["orange", "black", "black"]
            dodge = 0
            attacks = [
                Attack(damage_type="magic", dice=["blue", "black"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["orange"]
            block_magic = ["orange", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue", "blue"]),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["blue"]
            block_magic = ["black", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["blue", "black", "black"]
            block_magic = ["blue", "black", "black"]
            dodge = 1
            attacks = [
                Attack(damage_type="magic", dice=["black", "black"], flat_mod=1, max_range=3)
            ]

        elif tier == "T3":
            block_phys = ["orange", "blue"]
            block_magic = ["orange", "orange"]
            dodge = 1
            attacks = [
                Attack(["black", "black", "blue"], flat_mod=1),
            ]

    return Character(
        cls_name="Herald",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_mercenary_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black"]
        block_magic = ["black"]
        dodge = 1
        attacks = [
            Attack(["black", "black"], repeat=2),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(["black"], repeat=2)
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 4
            attacks = [
                Attack(["blue", "blue"], flat_mod=1),
                Attack(["black", "black"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["black", "black"]
            block_magic = ["black", "black", "black"]
            dodge = 3
            attacks = [
                Attack(["blue", "blue", "black"], repeat=2),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["black", "black", "black"]
            block_magic = ["black", "black", "black"]
            dodge = 2
            attacks = [
                Attack(["black"], repeat=2)
            ]

        elif tier == "T2":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 4
            attacks = [
                Attack(["blue", "blue"], flat_mod=1),
                Attack(["black", "black"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["black", "black"]
            block_magic = ["black", "black", "black"]
            dodge = 3
            attacks = [
                Attack(["blue", "blue", "black"], repeat=2),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["blue", "black", "black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(["black"], repeat=2)
            ]

        elif tier == "T2":
            block_phys = ["black", "black", "black"]
            block_magic = ["black", "black", "black"]
            dodge = 2
            attacks = [
                Attack(["black"], repeat=2, flat_mod=1)
            ]

        elif tier == "T3":
            block_phys = ["black", "black", "black"]
            block_magic = ["black", "black", "black", "black"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue", "black"], repeat=2),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["black", "black"]
            block_magic = ["black"]
            dodge = 2
            attacks = [
                Attack(["black", "black"])
            ]

        elif tier == "T2":
            block_phys = ["blue", "black", "black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(["black", "black"], flat_mod=1, repeat=2)
            ]

        elif tier == "T3":
            block_phys = ["black", "black", "black"]
            block_magic = ["black", "black", "black", "black"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue", "black"], repeat=2),
            ]

    return Character(
        cls_name="Mercenary",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_thief_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black"]
        block_magic = ["black"]
        dodge = 2
        attacks = [
            Attack(["blue"], max_range=3),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 3
            attacks = [
                Attack(["black", "black"], max_range=4)
            ]

        elif tier == "T2":
            block_phys = ["black", "black"]
            block_magic = ["black", "black"]
            dodge = 3
            attacks = [
                Attack(["blue", "blue"], flat_mod=1, push=True, max_range=3),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["black", "blue"]
            dodge = 3
            attacks = [
                Attack(["blue", "blue", "black"], push=True, max_range=3),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 3
            attacks = [
                Attack(["black", "black"], max_range=4)
            ]

        elif tier == "T2":
            block_phys = ["blue", "black"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue"], flat_mod=1, push=True, max_range=3),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["black", "blue"]
            dodge = 3
            attacks = [
                Attack(["blue", "blue", "black"], push=True, max_range=3),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 3
            attacks = [
                Attack(["black", "black"], max_range=4)
            ]

        elif tier == "T2":
            block_phys = ["blue", "black"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue"], flat_mod=1, push=True, max_range=3),
            ]

        elif tier == "T3":
            block_phys = ["black", "black"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue", "black"], push=True, max_range=3),
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["black"]
            block_magic = ["black"]
            dodge = 2
            attacks = [
                Attack(["black", "black"], max_range=4),
            ]

        elif tier == "T2":
            block_phys = ["blue", "black"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["black", "black"], flat_mod=1, max_range=4),
            ]

        elif tier == "T3":
            block_phys = ["black", "black"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["blue", "blue", "black"], push=True, max_range=3),
            ]

    return Character(
        cls_name="Warrior",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_warrior_build(tier: str, party_size: int) -> Character:
    if tier == "T0":
        block_phys = ["black", "black"]
        block_magic = ["black"]
        dodge = 1
        attacks = [
            Attack(["black", "black"]),
        ]

    if party_size == 1:
        if tier == "T1":
            block_phys = ["orange", "black", "black"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "black", "black"])
            ]

        elif tier == "T2":
            block_phys = ["black", "blue"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["orange", "orange"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["orange", "orange", "black"], flat_mod=1),
            ]

    elif party_size == 2:
        if tier == "T1":
            block_phys = ["orange", "black", "blue"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue"])
            ]

        elif tier == "T2":
            block_phys = ["black", "blue", "black"]
            block_magic = ["black", "black"]
            dodge = 1
            attacks = [
                Attack(["orange", "orange"], flat_mod=1),
            ]

        elif tier == "T3":
            block_phys = ["black", "blue"]
            block_magic = ["black", "black"]
            dodge = 2
            attacks = [
                Attack(["orange", "orange", "black"], flat_mod=1),
            ]

    elif party_size == 3:
        if tier == "T1":
            block_phys = ["orange", "black", "black"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "black", "black"])
            ]

        elif tier == "T2":
            block_phys = ["orange", "blue"]
            block_magic = ["blue", "black"]
            dodge = 1
            attacks = [
                Attack(["blue", "blue"], flat_mod=1)
            ]

        elif tier == "T3":
            block_phys = ["orange", "blue"]
            block_magic = ["blue", "black"]
            dodge = 1
            attacks = [
                Attack(["blue", "blue", "black"], flat_mod=1)
            ]

    elif party_size == 4:
        if tier == "T1":
            block_phys = ["blue"]
            block_magic = []
            dodge = 1
            attacks = [
                Attack(["black", "black"]),
                Attack(["black", "black"]),
            ]

        elif tier == "T2":
            block_phys = ["orange", "black", "black"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["black", "black", "black"])
            ]

        elif tier == "T3":
            block_phys = ["orange", "blue"]
            block_magic = ["blue", "black"]
            dodge = 0
            attacks = [
                Attack(["blue", "blue", "black"], flat_mod=1)
            ]

    return Character(
        cls_name="Warrior",
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
    if cls_name == "Assassin":
        return make_assassin_build(tier, party_size)
    elif cls_name == "Cleric":
        return make_cleric_build(tier, party_size)
    elif cls_name == "Deprived":
        return make_deprived_build(tier, party_size)
    elif cls_name == "Herald":
        return make_herald_build(tier, party_size)
    elif cls_name == "Knight":
        return make_knight_build(tier, party_size)
    elif cls_name == "Mercenary":
        return make_mercenary_build(tier, party_size)
    elif cls_name == "Pyromancer":
        return make_pyromancer_build(tier, party_size)
    elif cls_name == "Sorcerer":
        return make_sorcerer_build(tier, party_size)
    elif cls_name == "Thief":
        return make_thief_build(tier, party_size)
    elif cls_name == "Warrior":
        return make_warrior_build(tier, party_size)
    # else:
    #     return make_placeholder_build(cls_name, tier, party_size)


def build_all_builds() -> Dict[BuildKey, Character]:
    builds: Dict[BuildKey, Character] = {}
    for cls in CLASS_NAMES:
        for tier in TIER_LABELS:
            for P in PLAYER_COUNTS:
                key: BuildKey = (cls, tier, P)
                builds[key] = make_build_for(cls, tier, P)
    return builds
