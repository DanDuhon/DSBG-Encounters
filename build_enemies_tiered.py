import csv
import json
import random
import re
from dataclasses import dataclass
from itertools import product, combinations
from math import comb
from statistics import mean
from typing import List, Dict, Any, Optional, Tuple

# ---------- Dice definitions ----------

DICE_FACES: Dict[str, List[int]] = {
    "black":  [0, 1, 1, 1, 2, 2],
    "blue":   [1, 1, 2, 2, 2, 3],
    "orange": [1, 2, 2, 3, 3, 4],
    # dodge die is implicit: 0,0,0,1,1,1 -> success p = 0.5
}

# ---------- Core data classes ----------

@dataclass
class EnemyAction:
    kind: str              # "attack", "move-attack", "leap-attack"
    damage: int
    damage_type: str       # "physical" or "magic"
    max_targets: int       # 1 or 3
    raw_text: str          # original text

@dataclass
class Enemy:
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

@dataclass
class Attack:
    damage_type: str               # "physical" or "magic"
    dice: List[str]                # e.g. ["black", "black"]
    flat_mod: int
    stamina_cost: int
    min_range: int = 0
    max_range: int = 0
    shaft: bool = False           # cannot hit at 0 range if True

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

# ---------- Classes, tiers, and builds ----------

CLASS_NAMES = [
    "Assassin", "Cleric", "Deprived", "Herald", "Knight",
    "Mercenary", "Pyromancer", "Sorcerer", "Thief", "Warrior",
]

TIER_LABELS = ["T0", "T1", "T2", "T3"]

# How party "tiers" map to which builds are allowed
# Tier 1: T0 & T1 builds
# Tier 2: T1 & T2 builds
# Tier 3: T2 & T3 builds
TIER_CONFIG: Dict[str, Tuple[str, str]] = {
    "tier1": ("T0", "T1"),
    "tier2": ("T1", "T2"),
    "tier3": ("T2", "T3"),
}

PLAYER_COUNTS = [1, 2, 3, 4]

BuildKey = Tuple[str, str, int]  # (cls_name, tier_label, party_size)

# ---------- Combat math: new dodge+block rules ----------

def dodge_fail_prob(n_dodge: int, difficulty: int) -> float:
    """
    Probability that the player FAILS the dodge check.
    Each dodge die: 0,0,0,1,1,1 -> p(success) = 0.5
    """
    if n_dodge <= 0:
        return 1.0
    p_fail = 0.0
    for k in range(0, min(difficulty, n_dodge + 1)):
        p_fail += comb(n_dodge, k) * (0.5 ** n_dodge)
    return p_fail

def expected_block_damage(base_damage: int, def_dice: List[str]) -> float:
    """
    Expected damage after rolling defense dice (block or resist).
    """
    if base_damage <= 0:
        return 0.0
    if not def_dice:
        return float(base_damage)

    face_lists = [DICE_FACES[d] for d in def_dice]
    total_damage = 0.0
    total_outcomes = 0

    for faces in product(*face_lists):
        block_val = sum(faces)
        dmg = max(0, base_damage - block_val)
        total_damage += dmg
        total_outcomes += 1

    return total_damage / total_outcomes

def expected_damage_to_char(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    char: Character,
) -> float:
    """
    New rules: roll dodge AND block/resist.
    If dodge succeeds => 0 damage, else damage reduced by block/resist.
    """
    if damage_type == "physical":
        def_dice = char.block_phys_dice
    else:
        def_dice = char.block_magic_dice

    p_fail = dodge_fail_prob(char.dodge_dice, dodge_difficulty)
    e_block = expected_block_damage(base_damage, def_dice)
    return p_fail * e_block

def expected_damage_to_avg_char_for_party(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    party: List[Character],
) -> float:
    vals = [
        expected_damage_to_char(base_damage, damage_type, dodge_difficulty, c)
        for c in party
    ]
    return sum(vals) / len(vals)

def expected_attack_damage_vs_enemy(atk: Attack, enemy: Enemy) -> float:
    """Expected damage this attack deals to this enemy in one use."""
    defense = enemy.armor if atk.damage_type == "physical" else enemy.resist

    if not atk.dice:
        raw_vals = [atk.flat_mod]
    else:
        face_lists = [DICE_FACES[d] for d in atk.dice]
        raw_vals = [sum(faces) + atk.flat_mod for faces in product(*face_lists)]

    vals = [max(0, v - defense) for v in raw_vals]
    return sum(vals) / len(vals)

def choose_baseline_attack(char: Character, enemy: Enemy) -> Attack:
    """
    Pick a sustainable attack to use for TTK calculations.
    v1: prefer low-stamina attacks, ignore range/shaft positioning.
    """
    candidates = [a for a in char.attacks if a.stamina_cost <= 1]
    if not candidates:
        candidates = char.attacks
    return max(
        candidates,
        key=lambda atk: expected_attack_damage_vs_enemy(atk, enemy)
    )

def enemy_DPR_vs_party(enemy: Enemy, party: List[Character]) -> float:
    """
    Total expected damage this enemy does in one activation vs this party,
    assuming it is in range and executes its actions.
    """
    P = len(party)
    total = 0.0
    for action in enemy.actions:
        per_char = expected_damage_to_avg_char_for_party(
            base_damage=action.damage,
            damage_type=action.damage_type,
            dodge_difficulty=enemy.dodge_difficulty,
            party=party,
        )
        targets = min(P, action.max_targets)  # up to 3 models on a node
        total += per_char * targets
    if enemy.repeat > 1:
        total *= enemy.repeat
    return total

def team_DPS_vs_party(enemy: Enemy, party: List[Character]) -> float:
    total = 0.0
    for c in party:
        atk = choose_baseline_attack(c, enemy)
        total += expected_attack_damage_vs_enemy(atk, enemy)
    return total

def enemy_TTK_vs_party(enemy: Enemy, party: List[Character]) -> float:
    dps = team_DPS_vs_party(enemy, party)
    if dps <= 0:
        return float("inf")
    return enemy.hp / dps

def enemy_threat_vs_party(enemy: Enemy, party: List[Character]) -> float:
    """
    Threat(party) = DPR(party) * TTK(party)
    """
    dpr = enemy_DPR_vs_party(enemy, party)
    ttk = enemy_TTK_vs_party(enemy, party)
    return dpr * ttk

# ---------- Parse enemies.csv into Enemy / EnemyAction ----------

damage_pattern = re.compile(r"(\d+)\s+(physical|magic)", re.IGNORECASE)

def parse_action_text(text: str) -> Optional[EnemyAction]:
    """
    Turn a raw action string into an EnemyAction if it actually deals damage.
    Returns None for pure movement / utility actions.
    """
    if not text:
        return None

    t = text.strip()
    if not t:
        return None
    lower = t.lower()

    # skip pure utility
    if "resurrect" in lower or "summon" in lower:
        return None

    # pure movement
    if lower.startswith("move ") or lower.startswith("move-attack "):
        if damage_pattern.search(t) is None:
            return None
    if lower.startswith("leap to "):
        # movement-only leap
        return None

    # classify kind
    if lower.startswith("move-attack"):
        kind = "move-attack"
    elif "leap-attack" in lower:
        kind = "leap-attack"
    elif lower.startswith("attack"):
        kind = "attack"
    else:
        kind = "attack"

    m = damage_pattern.search(t)
    if not m:
        return None

    dmg = int(m.group(1))
    dmg_type = m.group(2).lower()   # "physical" or "magic"

    # AoE / node / move-attack = hits up to 3
    max_targets = 1
    if "node" in lower or kind in ("move-attack", "leap-attack"):
        max_targets = 3

    return EnemyAction(
        kind=kind,
        damage=dmg,
        damage_type=dmg_type,
        max_targets=max_targets,
        raw_text=t,
    )

def hp_band(hp: int) -> str:
    if hp <= 1:
        return "1"
    elif hp >= 5:
        return "5+"
    else:
        return "2-4"

def infer_tags(row: Dict[str, str], actions: List[EnemyAction]) -> Dict[str, Any]:
    hp_value = int(row["HP (data)"])

    range_raw = row.get("Range (behavior)", "")
    rng: Optional[int] = None
    if range_raw not in ("", None):
        try:
            rng = int(float(range_raw))
        except ValueError:
            rng = None

    raw_actions_text = " ".join([
        row.get("Action 1", "") or "",
        row.get("Action 2", "") or "",
        row.get("Action 3", "") or "",
    ]).lower()
    is_leaper = "leap-attack" in raw_actions_text or "leap to " in raw_actions_text

    is_ranged = False
    if rng is not None and rng >= 1:
        is_ranged = True

    is_melee = not is_ranged

    return {
        "hp_band": hp_band(hp_value),
        "is_ranged": is_ranged,
        "is_melee": is_melee,
        "is_leaper": is_leaper,
    }

def parse_int_like(val: Any) -> int:
    if val in ("", None):
        raise ValueError("Missing numeric value")
    s = str(val)
    m = re.search(r"-?\d+", s)
    if not m:
        raise ValueError(f"Could not parse integer from {s!r}")
    return int(m.group(0))

def load_enemies_from_csv(csv_path: str) -> List[Enemy]:
    enemies: List[Enemy] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["Name (data)"]

            models = parse_int_like(row["Models"])
            hp = parse_int_like(row["HP (data)"])
            armor = parse_int_like(row["Armor (data)"])
            resist = parse_int_like(row["Resist (data)"])
            dodge_diff = parse_int_like(row["Dodge Difficulty (behavior)"])
            threat_initiative = parse_int_like(row["Threat (data)"])
            on_death = row.get("On Death") or None

            range_behavior_raw = row.get("Range (behavior)", "")
            range_behavior: Optional[int] = None
            if range_behavior_raw not in ("", None):
                try:
                    range_behavior = int(float(range_behavior_raw))
                except ValueError:
                    range_behavior = None

            repeat_raw = row.get("Repeat", "")
            repeat = 1
            if repeat_raw not in ("", None):
                try:
                    repeat = int(float(repeat_raw))
                except ValueError:
                    repeat = 1

            # actions
            actions: List[EnemyAction] = []
            for col in ("Action 1", "Action 2", "Action 3"):
                raw = row.get(col) or ""
                act = parse_action_text(raw)
                if act is not None:
                    actions.append(act)

            tags = infer_tags(row, actions)

            enemy = Enemy(
                name=name,
                models=models,
                hp=hp,
                armor=armor,
                resist=resist,
                dodge_difficulty=dodge_diff,
                range_behavior=range_behavior,
                repeat=repeat,
                threat_initiative=threat_initiative,
                on_death=on_death,
                actions=actions,
                tags=tags,
                threat_profile={},
            )
            enemies.append(enemy)
    return enemies

# ---------- Placeholder builds (you'll replace these) ----------

def make_placeholder_build(cls_name: str, tier: str, party_size: int) -> Character:
    """
    TEMP: simple placeholder builds so the pipeline runs.
    - All classes identical.
    - Higher tiers get slightly more dice.
    You can replace this function with your real build definitions.
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

    # Offense scales a bit with tier
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

def build_all_placeholder_builds() -> Dict[BuildKey, Character]:
    """
    Build placeholder entries for every (class, tier, party_size).

    TODO: Replace this with your real builds. For example, you might:
      - Hardcode each build here, or
      - Load them from a JSON file and construct Character objects.
    """
    builds: Dict[BuildKey, Character] = {}
    for cls in CLASS_NAMES:
        for tier in TIER_LABELS:
            for P in PLAYER_COUNTS:
                key: BuildKey = (cls, tier, P)
                builds[key] = make_placeholder_build(cls, tier, P)
    return builds

def make_build_for(cls_name: str, tier: str, party_size: int) -> Character:
    """
    Main entry point for building a Character for (class, tier, party_size).

    - Knight + Sorcerer have explicit builds below.
    - Other classes currently fall back to a simple placeholder.
      You can add more `elif cls_name == ...` blocks as you define them.
    """
    if cls_name == "Knight":
        return make_knight_build(tier, party_size)
    elif cls_name == "Sorcerer":
        return make_sorcerer_build(tier, party_size)
    else:
        return make_placeholder_build(cls_name, tier, party_size)
    
def build_all_builds() -> Dict[BuildKey, Character]:
    """
    Build all Character objects for every (class, tier, party_size).
    This is what you pass into build_enemy_threat_json().
    """
    builds: Dict[BuildKey, Character] = {}
    for cls in CLASS_NAMES:
        for tier in TIER_LABELS:      # "T0", "T1", "T2", "T3"
            for P in PLAYER_COUNTS:   # 1..4
                key: BuildKey = (cls, tier, P)
                builds[key] = make_build_for(cls, tier, P)
    return builds

def make_knight_build(tier: str, party_size: int) -> Character:
    """
    Knight builds T0-T3.

    T0 is your starter Knight:
      - Block: 1 blue + 1 black (physical)
      - Resist: 1 black (magic)
      - Dodge: 0
      - Att1: 0 stamina, range 0, 1 blue physical
      - Att2: 4 stamina, range 0, 1 blue + 1 black physical

    Higher tiers here are a simple illustrative progression.
    Swap out dice / stamina / range to match your real designs.
    """
    # Base defensive line per tier
    if tier == "T0":
        block_phys = ["blue", "black"]
        block_magic = ["black"]
        dodge = 0
        attacks = [
            Attack("physical", ["blue"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["blue", "black"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]

    elif tier == "T1":
        # Slightly better armor / damage
        block_phys = ["blue", "black"]
        block_magic = ["black"]
        dodge = 0
        attacks = [
            # Better basic swing: blue+black, still free
            Attack("physical", ["blue", "black"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            # Heavy overhead: blue+orange, still 4 stamina
            Attack("physical", ["blue", "orange"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]

    elif tier == "T2":
        # Heavy armor knight with big hits
        block_phys = ["blue", "blue", "black"]   # more physical block
        block_magic = ["black", "black"]         # better magic res
        dodge = 0
        attacks = [
            # Solid free swing: blue+orange
            Attack("physical", ["blue", "orange"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            # Big stamina attack: 2x orange
            Attack("physical", ["orange", "orange"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]

    elif tier == "T3":
        # Very tanky with a bit of dodge
        block_phys = ["blue", "blue", "black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            # Free attack is now strong but reliable
            Attack("physical", ["blue", "orange"], flat_mod=1, stamina_cost=0, min_range=0, max_range=0),
            # Big burst attack
            Attack("physical", ["orange", "orange"], flat_mod=1, stamina_cost=3, min_range=0, max_range=0),
        ]

    else:
        # Safety fallback, shouldn't hit
        block_phys = ["black"]
        block_magic = ["black"]
        dodge = 0
        attacks = [
            Attack("physical", ["black"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0)
        ]

    # If you want party-size-specific tweaks, branch on party_size here
    # Example: solo Knight slightly tougher, 4p Knight slightly more offensive.
    # For now this example keeps stats identical across party sizes.

    return Character(
        cls_name="Knight",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

def make_sorcerer_build(tier: str, party_size: int) -> Character:
    """
    Sorcerer builds T0–T3.

    T0 starter Sorcerer:
      - Block: 1 black (physical)
      - Resist: 1 blue + 1 black (magic)
      - Dodge: 1
      - Att1: 1 stamina, range 1-3, 1 blue magic
      - Att2: 3 stamina, range 1-3, 2 black magic
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
        # Slightly better magic power, same defenses
        block_phys = ["black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            # Free basic pebble now costs 0 stamina (better economy)
            Attack("magic", ["blue"], flat_mod=0, stamina_cost=0, min_range=1, max_range=3),
            # Stronger heavy spell
            Attack("magic", ["blue", "black"], flat_mod=0, stamina_cost=3, min_range=1, max_range=3),
        ]

    elif tier == "T2":
        # More magic dice, slightly better physical block
        block_phys = ["black", "black"]
        block_magic = ["blue", "black"]
        dodge = 1
        attacks = [
            # Good free cast
            Attack("magic", ["blue", "black"], flat_mod=0, stamina_cost=0, min_range=1, max_range=3),
            # Heavy cast
            Attack("magic", ["blue", "blue"], flat_mod=0, stamina_cost=3, min_range=1, max_range=3),
        ]

    elif tier == "T3":
        # Glass cannon with strong dodge and magic
        block_phys = ["black"]
        block_magic = ["blue", "blue", "black"]
        dodge = 2
        attacks = [
            # Free but strong basic spell
            Attack("magic", ["blue", "black"], flat_mod=1, stamina_cost=0, min_range=1, max_range=3),
            # Big nuke
            Attack("magic", ["blue", "blue"], flat_mod=1, stamina_cost=3, min_range=1, max_range=3),
        ]

    else:
        block_phys = ["black"]
        block_magic = ["black"]
        dodge = 1
        attacks = [
            Attack("magic", ["black"], flat_mod=0, stamina_cost=1, min_range=1, max_range=3)
        ]

    # Again, if you want party-size specific sorcerer builds, branch on party_size.

    return Character(
        cls_name="Sorcerer",
        tier=tier,
        party_size=party_size,
        block_phys_dice=block_phys,
        block_magic_dice=block_magic,
        dodge_dice=dodge,
        attacks=attacks,
    )

# ---------- Party generation per tier ----------

def iter_parties_for_tier(
    party_size: int,
    tier_name: str,
    builds: Dict[BuildKey, Character],
) -> List[List[Character]]:
    """
    Generate all parties for:
      - given party size (1–4)
      - given tier_name ("tier1"/"tier2"/"tier3")

    Rules:
      - at most one of each class in the party
      - each class may choose one of the allowed build tiers for this tier:
          tier1: T0 or T1
          tier2: T1 or T2
          tier3: T2 or T3
    """
    allowed_tiers = TIER_CONFIG[tier_name]
    parties: List[List[Character]] = []

    for cls_subset in combinations(CLASS_NAMES, party_size):
        options_per_cls: List[List[Character]] = []
        skip_subset = False
        for cls in cls_subset:
            opts: List[Character] = []
            for tlabel in allowed_tiers:
                key = (cls, tlabel, party_size)
                if key in builds:
                    opts.append(builds[key])
            if not opts:
                skip_subset = True
                break
            options_per_cls.append(opts)
        if skip_subset:
            continue

        # Build combos of builds (2^party_size per subset)
        for combo in product(*options_per_cls):
            parties.append(list(combo))

    return parties

# ---------- Threat profiles for all tiers ----------

def compute_enemy_threat_profile_all_tiers(
    enemy: Enemy,
    builds: Dict[BuildKey, Character],
) -> Dict[str, Dict[str, float]]:
    """
    For each tier ("tier1", "tier2", "tier3") and each P=1..4:
      - enumerate all valid parties
      - compute Threat(enemy, party)
      - store the average
    """
    profile: Dict[str, Dict[str, float]] = {}

    for tier_name in ("tier1", "tier2", "tier3"):
        tier_results: Dict[str, float] = {}
        for P in PLAYER_COUNTS:
            parties = iter_parties_for_tier(P, tier_name, builds)
            if not parties:
                tier_results[f"p{P}"] = 0.0
                continue
            total_threat = 0.0
            for party in parties:
                total_threat += enemy_threat_vs_party(enemy, party)
            avg_threat = total_threat / len(parties)
            tier_results[f"p{P}"] = avg_threat
        profile[tier_name] = tier_results

    return profile

def enemies_to_json_serializable(enemies: List[Enemy]) -> List[Dict[str, Any]]:
    serializable = []
    for e in enemies:
        edict = {
            "name": e.name,
            "models": e.models,
            "hp": e.hp,
            "armor": e.armor,
            "resist": e.resist,
            "dodge_difficulty": e.dodge_difficulty,
            "range_behavior": e.range_behavior,
            "repeat": e.repeat,
            "threat_initiative": e.threat_initiative,
            "on_death": e.on_death,
            "tags": e.tags,
            "actions": [
                {
                    "kind": a.kind,
                    "damage": a.damage,
                    "damage_type": a.damage_type,
                    "max_targets": a.max_targets,
                    "raw_text": a.raw_text,
                }
                for a in e.actions
            ],
            "threat_profile": e.threat_profile,
        }
        serializable.append(edict)
    return serializable

def build_enemy_threat_json(
    csv_path: str,
    json_out_path: str,
    builds: Optional[Dict[BuildKey, Character]] = None,
) -> List[Enemy]:
    """
    Main pipeline:
      - load enemies from CSV
      - compute tiered threat profiles with given builds
      - write JSON
      - return in-memory enemy list
    """
    if builds is None:
        builds = build_all_placeholder_builds()

    enemies = load_enemies_from_csv(csv_path)
    for e in enemies:
        e.threat_profile = compute_enemy_threat_profile_all_tiers(e, builds)

    data = enemies_to_json_serializable(enemies)
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    return enemies

# ---------- Encounter & alternative generation (unchanged behavior, tier-aware) ----------

@dataclass
class EncounterEnemySpec:
    enemy_name: str
    count: int
    tile: Optional[int] = None

@dataclass
class EncounterSpec:
    name: str
    level: int             # 1,2,3 etc; mapped to tier1/tier2/tier3
    enemies: List[EncounterEnemySpec]

@dataclass
class Slot:
    tile: Optional[int]
    orig_enemy_name: str

def build_slots(enc: EncounterSpec) -> List[Slot]:
    slots: List[Slot] = []
    for ee in enc.enemies:
        for _ in range(ee.count):
            slots.append(Slot(tile=ee.tile, orig_enemy_name=ee.enemy_name))
    return slots

def compute_encounter_threat(
    enc: EncounterSpec,
    name_to_enemy: Dict[str, Enemy],
    tier_name: str,
) -> Dict[int, float]:
    totals = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    for ee in enc.enemies:
        e = name_to_enemy[ee.enemy_name]
        for p in (1, 2, 3, 4):
            totals[p] += e.threat_profile[tier_name][f"p{p}"] * ee.count
    return totals

def compute_hp_counts_for_encounter(enc: EncounterSpec, name_to_enemy: Dict[str, Enemy]):
    from collections import Counter
    c = Counter()
    slots = build_slots(enc)
    for s in slots:
        e = name_to_enemy[s.orig_enemy_name]
        c[e.tags["hp_band"]] += 1
    return c, slots

def compute_effective_role_counts(enemies_list: List[Enemy]):
    melee = 0
    ranged = 0
    for e in enemies_list:
        is_leaper = e.tags.get("is_leaper", False)
        is_ranged = e.tags.get("is_ranged", False)
        is_melee = e.tags.get("is_melee", False)
        if is_melee or is_leaper:
            melee += 1
        if is_ranged or is_leaper:
            ranged += 1
    return melee, ranged

def compute_effective_role_counts_for_encounter(enc: EncounterSpec, name_to_enemy: Dict[str, Enemy]):
    slots = build_slots(enc)
    enemies_list = [name_to_enemy[s.orig_enemy_name] for s in slots]
    return compute_effective_role_counts(enemies_list)

def average_threat(enemy: Enemy, tier_name: str) -> float:
    return mean(enemy.threat_profile[tier_name][f"p{p}"] for p in (1, 2, 3, 4))

def compute_encounter_threat_from_enemies(enemies_list: List[Enemy], tier_name: str) -> Dict[int, float]:
    totals = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    for e in enemies_list:
        for p in (1, 2, 3, 4):
            totals[p] += e.threat_profile[tier_name][f"p{p}"]
    return totals

def threat_distance(orig_threat: Dict[int, float], cand_threat: Dict[int, float]) -> float:
    errs: List[float] = []
    for p in (1, 2, 3, 4):
        t0 = orig_threat[p]
        t1 = cand_threat[p]
        if t0 <= 0:
            errs.append(abs(t1 - t0))
        else:
            errs.append(abs(t1 - t0) / t0)
    return max(errs)

def generate_alternatives(
    enc: EncounterSpec,
    enemies: List[Enemy],
    tier_name: str,
    max_candidates: int = 10,
    max_tries: int = 5000,
    threat_tolerance: float = 0.2,
) -> List[Dict[str, Any]]:
    """
    Same as before, but now uses the tiered threat profile.
    """
    name_to_enemy = {e.name: e for e in enemies}

    target_hp_counts, slots = compute_hp_counts_for_encounter(enc, name_to_enemy)
    target_melee, target_ranged = compute_effective_role_counts_for_encounter(enc, name_to_enemy)
    orig_threat = compute_encounter_threat(enc, name_to_enemy, tier_name)
    num_slots = len(slots)

    band_pools: Dict[str, List[Enemy]] = {}
    for e in enemies:
        band = e.tags["hp_band"]
        band_pools.setdefault(band, []).append(e)

    orig_names_sorted = tuple(sorted(s.orig_enemy_name for s in slots))
    seen = set()
    seen.add(orig_names_sorted)

    candidates: List[Dict[str, Any]] = []
    tries = 0

    while len(candidates) < max_candidates and tries < max_tries:
        tries += 1

        cand_enemies: List[Enemy] = []
        feasible = True
        for band, count in target_hp_counts.items():
            pool = band_pools.get(band)
            if not pool:
                feasible = False
                break
            for _ in range(count):
                cand_enemies.append(random.choice(pool))
        if not feasible:
            break

        melee, ranged = compute_effective_role_counts(cand_enemies)
        if melee != target_melee or ranged != target_ranged:
            continue

        cand_threat = compute_encounter_threat_from_enemies(cand_enemies, tier_name)
        dist = threat_distance(orig_threat, cand_threat)
        if dist > threat_tolerance:
            continue

        key = tuple(sorted(e.name for e in cand_enemies))
        if key in seen or key == orig_names_sorted:
            continue
        seen.add(key)

        slot_orig_enemies = [name_to_enemy[s.orig_enemy_name] for s in slots]
        avg_ths = [average_threat(e, tier_name) for e in slot_orig_enemies]
        boss_idx = max(range(num_slots), key=lambda i: avg_ths[i])

        cand_avgs = [average_threat(e, tier_name) for e in cand_enemies]
        boss_candidate_idx = max(range(num_slots), key=lambda i: cand_avgs[i])

        cand_enemies[boss_idx], cand_enemies[boss_candidate_idx] = cand_enemies[boss_candidate_idx], cand_enemies[boss_idx]

        assignment = [
            {"tile": slots[i].tile, "enemy": cand_enemies[i].name}
            for i in range(num_slots)
        ]

        candidates.append(
            {
                "assignment": assignment,
                "threat": cand_threat,
                "distance": dist,
            }
        )

    return candidates

# ---------- CLI example ----------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python build_enemies_tiered.py <enemies.csv> <output_enemies.json>")
        sys.exit(1)

    csv_path = sys.argv[1]
    out_path = sys.argv[2]

    builds = build_all_builds()
    enemies = build_enemy_threat_json(csv_path, out_path, builds=builds)
    print(f"Wrote enemies with tiered threat profiles to {out_path}")

    # Example: "No Safe Haven" encounter
    no_safe_haven = EncounterSpec(
        name="No Safe Haven",
        level=1,  # maps to "tier1"
        enemies=[
            EncounterEnemySpec(enemy_name="Snow Rat", count=2, tile=1),
            EncounterEnemySpec(enemy_name="Engorged Zombie", count=1, tile=2),
        ],
    )

    tier_name = f"tier{no_safe_haven.level}"
    alts = generate_alternatives(
        no_safe_haven,
        enemies,
        tier_name,
        max_candidates=3,
        max_tries=20000,
        threat_tolerance=0.2,
    )

    print("Example alternatives for 'No Safe Haven':")
    for i, alt in enumerate(alts, start=1):
        print(f"Alternative {i}: distance={alt['distance']:.3f}")
        for slot in alt["assignment"]:
            print(f"  Tile {slot['tile']}: {slot['enemy']}")
        print(f"  Threat: {alt['threat']}")
        print()
