from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple

# ---------- Core game models ----------

@dataclass
class EnemyAction:
    kind: str              # "attack", "move-attack", "leap-attack"
    damage: int
    damage_type: str       # "physical" or "magic"
    max_targets: int       # 1 or 3
    raw_text: str          # original text
    apply_bleed: bool = False
    apply_poison: bool = False
    apply_frostbite: bool = False
    apply_stagger: bool = False


@dataclass
class Enemy:
    enemy_id: int
    name: str
    models: int
    hp: int
    armor: int
    resist: int
    dodge_difficulty: int
    range_behavior: Optional[int]
    repeat: int
    threat_initiative: int
    on_death: Optional[str]
    actions: List[EnemyAction]
    tags: Dict[str, Any]
    # threat_profile[tier_name]["p1"/"p2"/"p3"/"p4"]
    threat_profile: Dict[str, Dict[str, float]]
    move_speed: float = 0.0
    has_push: bool = False
    has_leap: bool = False
    is_ranged_or_leap: bool = False
    can_bleed: bool = False
    can_poison: bool = False
    can_frostbite: bool = False
    can_stagger: bool = False


@dataclass
class Attack:
    dice: List[str]                # e.g. ["black", "black"]
    damage_type: str = "physical"  # "physical" or "magic"
    flat_mod: int = 0
    max_range: int = 0
    shift: bool = False
    apply_bleed: bool = False
    apply_poison: bool = False
    apply_stagger: bool = False
    apply_frostbite: bool = False
    push: bool = False
    ignore_armor: bool = False
    repeat: int = 1


@dataclass
class Character:
    """
    A single character *build* (class + tier + party size).
    """
    cls_name: str                  # "Knight", "Assassin", etc.
    tier: str                      # "T0", "T1", "T2", "T3"
    party_size: int                # 1–4
    block_phys_dice: List[str]
    block_magic_dice: List[str]
    dodge_dice: int
    attacks: List[Attack]

# Convenience type for build dictionary keys
BuildKey = Tuple[str, str, int]  # (cls_name, tier_label, party_size)


# ---------- Encounters / slots ----------

@dataclass
class EncounterEnemySpec:
    enemy_name: str
    count: int
    tile: Optional[int] = None


@dataclass
class EncounterSpec:
    name: str
    level: int             # 1,2,3 etc.; maps to tier1/2/3
    enemies: List[EncounterEnemySpec]


@dataclass
class Slot:
    tile: Optional[int]
    orig_enemy_name: str
