import csv
import json
import random
from dataclasses import dataclass
from itertools import product
from math import comb
from statistics import mean
from typing import List, Dict, Any, Optional
import collections
import re

# ---------- Dice definitions ----------

DICE_FACES: Dict[str, List[int]] = {
    "black":  [0, 1, 1, 1, 2, 2],
    "blue":   [1, 1, 2, 2, 2, 3],
    "orange": [1, 2, 2, 3, 3, 4],
    # dodge die is implicit: 0,0,0,1,1,1 -> success p = 0.5
}

# ---------- Data classes ----------

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
    threat_profile: Dict[str, float]

@dataclass
class Attack:
    damage_type: str
    dice: List[str]
    flat_mod: int
    stamina_cost: int
    min_range: int = 0
    max_range: int = 0
    shaft: bool = False

@dataclass
class Character:
    name: str
    block_phys_dice: List[str]
    block_magic_dice: List[str]
    dodge_dice: int
    attacks: List[Attack]

# ---------- Level 1 starter characters ----------

def make_level1_chars() -> List[Character]:
    # Assassin
    assassin = Character(
        name="Assassin",
        block_phys_dice=["black"],
        block_magic_dice=["black"],
        dodge_dice=2,
        attacks=[
            Attack("physical", ["black", "black"], flat_mod=-1, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["black", "black", "black"], flat_mod=-1, stamina_cost=3, min_range=0, max_range=0),
        ]
    )
    # Knight
    knight = Character(
        name="Knight",
        block_phys_dice=["blue", "black"],
        block_magic_dice=["black"],  # uses resist line vs magic
        dodge_dice=0,
        attacks=[
            Attack("physical", ["blue"], flat_mod=0, stamina_cost=0, min_range=0, max_range=0),
            Attack("physical", ["blue", "black"], flat_mod=0, stamina_cost=4, min_range=0, max_range=0),
        ]
    )
    # Herald
    herald = Character(
        name="Herald",
        block_phys_dice=["black", "black"],
        block_magic_dice=["black"],
        dodge_dice=1,
        attacks=[
            Attack("physical", ["black"], flat_mod=0, stamina_cost=0, min_range=1, max_range=1, shaft=True),
            Attack("physical", ["black"], flat_mod=1, stamina_cost=3, min_range=1, max_range=1, shaft=True),
        ]
    )
    # Sorcerer
    sorcerer = Character(
        name="Sorcerer",
        block_phys_dice=["black"],
        block_magic_dice=["blue", "black"],
        dodge_dice=1,
        attacks=[
            Attack("magic", ["blue"], flat_mod=0, stamina_cost=1, min_range=1, max_range=3),
            Attack("magic", ["black", "black"], flat_mod=0, stamina_cost=3, min_range=1, max_range=3),
        ]
    )
    return [assassin, knight, herald, sorcerer]

# ---------- Core math helpers (new dodge+block rules) ----------

def dodge_fail_prob(n_dodge: int, difficulty: int) -> float:
    """Probability that the player fails the dodge check."""
    if n_dodge <= 0:
        return 1.0
    p_fail = 0.0
    for k in range(0, min(difficulty, n_dodge + 1)):
        p_fail += comb(n_dodge, k) * (0.5 ** n_dodge)
    return p_fail

def expected_block_damage(base_damage: int, def_dice: List[str]) -> float:
    """Expected damage after rolling defense dice (block or resist)."""
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

def expected_damage_to_avg_char(
    base_damage: int,
    damage_type: str,
    dodge_difficulty: int,
    chars: List[Character],
) -> float:
    vals = [
        expected_damage_to_char(base_damage, damage_type, dodge_difficulty, c)
        for c in chars
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

def enemy_DPR(enemy: Enemy, party_size: int, chars: List[Character]) -> float:
    """
    Total expected damage this enemy does in one activation vs a P-player party,
    assuming it's in range and executes its actions.
    """
    total = 0.0
    for action in enemy.actions:
        per_char = expected_damage_to_avg_char(
            base_damage=action.damage,
            damage_type=action.damage_type,
            dodge_difficulty=enemy.dodge_difficulty,
            chars=chars,
        )
        targets = min(party_size, action.max_targets)  # node cap = 3 models
        total += per_char * targets
    if enemy.repeat > 1:
        total *= enemy.repeat
    return total

def team_DPS_4p(enemy: Enemy, chars: List[Character]) -> float:
    total = 0.0
    for c in chars:
        atk = choose_baseline_attack(c, enemy)
        total += expected_attack_damage_vs_enemy(atk, enemy)
    return total

def enemy_TTK(enemy: Enemy, party_size: int, chars: List[Character]) -> float:
    dps4 = team_DPS_4p(enemy, chars)
    if dps4 <= 0:
        return float("inf")
    team_dps_p = dps4 * (party_size / 4.0)
    return enemy.hp / team_dps_p

def enemy_threat(enemy: Enemy, party_size: int, chars: List[Character]) -> float:
    """
    Threat(P) = DPR(P) * TTK(P)
    = roughly "expected damage this enemy outputs before it dies vs a P-player party".
    """
    dpr = enemy_DPR(enemy, party_size, chars)
    ttk = enemy_TTK(enemy, party_size, chars)
    return dpr * ttk

# ---------- CSV parsing into Enemy / EnemyAction ----------

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

    # Skip purely non-damaging utility actions
    if "resurrect" in lower or "summon" in lower:
        return None
    # Pure movement (no damage keyword)
    if lower.startswith("move ") or lower.startswith("move-attack "):
        if damage_pattern.search(t) is None:
            return None
    if lower.startswith("leap to "):
        # movement-only leap (e.g. Snow Rat "Leap to aggro")
        return None

    # Determine kind
    if lower.startswith("move-attack"):
        kind = "move-attack"
    elif "leap-attack" in lower:
        kind = "leap-attack"
    elif lower.startswith("attack"):
        kind = "attack"
    else:
        # unknown kind; if it has damage, treat as basic attack
        kind = "attack"

    m = damage_pattern.search(t)
    if not m:
        # No explicit damage; ignore
        return None

    dmg = int(m.group(1))
    dmg_type = m.group(2).lower()  # "physical" or "magic"

    # AoE / multi-target detection
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
    """
    Infer some useful tags: melee/ranged/leaper, hp_band, etc.
    """
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

            # Parse actions
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
                threat_profile={},  # to be filled later
            )
            enemies.append(enemy)
    return enemies

# ---------- Threat profile computation ----------

def compute_threat_profile(enemy: Enemy, chars: List[Character]) -> Dict[str, float]:
    profile: Dict[str, float] = {}
    for p in (1, 2, 3, 4):
        profile[f"p{p}"] = enemy_threat(enemy, p, chars)
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

def build_enemy_threat_json(csv_path: str, json_out_path: str) -> List[Enemy]:
    chars = make_level1_chars()
    enemies = load_enemies_from_csv(csv_path)
    for e in enemies:
        e.threat_profile = compute_threat_profile(e, chars)
    data = enemies_to_json_serializable(enemies)
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
    return enemies  # also return in-memory list for further use

# ---------- Encounter + alternative generation ----------

@dataclass
class EncounterEnemySpec:
    enemy_name: str
    count: int
    tile: Optional[int] = None

@dataclass
class EncounterSpec:
    name: str
    level: int
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

def compute_encounter_threat(enc: EncounterSpec, name_to_enemy: Dict[str, Enemy]) -> Dict[int, float]:
    totals = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    for ee in enc.enemies:
        e = name_to_enemy[ee.enemy_name]
        for p in (1, 2, 3, 4):
            totals[p] += e.threat_profile[f"p{p}"] * ee.count
    return totals

def compute_hp_counts_for_encounter(enc: EncounterSpec, name_to_enemy: Dict[str, Enemy]):
    c = collections.Counter()
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

def average_threat(enemy: Enemy) -> float:
    return mean(enemy.threat_profile[f"p{p}"] for p in (1, 2, 3, 4))

def compute_encounter_threat_from_enemies(enemies_list: List[Enemy]) -> Dict[int, float]:
    totals = {1: 0.0, 2: 0.0, 3: 0.0, 4: 0.0}
    for e in enemies_list:
        for p in (1, 2, 3, 4):
            totals[p] += e.threat_profile[f"p{p}"]
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
    max_candidates: int = 10,
    max_tries: int = 5000,
    threat_tolerance: float = 0.2,
) -> List[Dict[str, Any]]:
    """
    Generate alternative enemy sets for an encounter that:
      - keep the same total enemy groups
      - keep the same HP-band counts
      - keep the same effective melee/ranged counts
      - keep total threat within 'threat_tolerance' relative error for P=1..4
      - ensure the "boss slot" (highest-threat original enemy) is replaced
        with the highest-threat enemy in the new set.
    """
    name_to_enemy = {e.name: e for e in enemies}

    target_hp_counts, slots = compute_hp_counts_for_encounter(enc, name_to_enemy)
    target_melee, target_ranged = compute_effective_role_counts_for_encounter(enc, name_to_enemy)
    orig_threat = compute_encounter_threat(enc, name_to_enemy)
    num_slots = len(slots)

    # Build pools by HP band
    band_pools: Dict[str, List[Enemy]] = {}
    for e in enemies:
        band = e.tags["hp_band"]
        band_pools.setdefault(band, []).append(e)

    # Original multiset of names for dedupe
    orig_names_sorted = tuple(sorted(s.orig_enemy_name for s in slots))

    seen = set()
    seen.add(orig_names_sorted)
    candidates: List[Dict[str, Any]] = []

    tries = 0
    while len(candidates) < max_candidates and tries < max_tries:
        tries += 1

        cand_enemies: List[Enemy] = []

        # Step 1: choose enemies by HP band
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

        # Step 2: check effective melee / ranged counts
        melee, ranged = compute_effective_role_counts(cand_enemies)
        if melee != target_melee or ranged != target_ranged:
            continue

        # Step 3: threat similarity
        cand_threat = compute_encounter_threat_from_enemies(cand_enemies)
        dist = threat_distance(orig_threat, cand_threat)
        if dist > threat_tolerance:
            continue

        # Step 4: dedupe by multiset of names
        key = tuple(sorted(e.name for e in cand_enemies))
        if key in seen:
            continue
        if key == orig_names_sorted:
            continue
        seen.add(key)

        # Step 5: boss slot logic
        slot_orig_enemies = [name_to_enemy[s.orig_enemy_name] for s in slots]
        avg_ths = [average_threat(e) for e in slot_orig_enemies]
        boss_idx = max(range(num_slots), key=lambda i: avg_ths[i])

        cand_avgs = [average_threat(e) for e in cand_enemies]
        boss_candidate_idx = max(range(num_slots), key=lambda i: cand_avgs[i])

        cand_enemies[boss_idx], cand_enemies[boss_candidate_idx] = cand_enemies[boss_candidate_idx], cand_enemies[boss_idx]

        # Build assignment by tile
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

# ---------- Example CLI usage ----------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python build_enemies.py <enemies.csv> <output_enemies.json>")
        print("       (then optionally edit the script to define encounters and call generate_alternatives)")
        sys.exit(1)

    csv_path = sys.argv[1]
    out_path = sys.argv[2]

    # 1) Build enemies + threat JSON
    enemies = build_enemy_threat_json(csv_path, out_path)
    print(f"Wrote enemies with threat to {out_path}")

    # 2) Example: generate alternatives for the 'No Safe Haven' encounter
    # No Safe Haven:
    #   Level 1
    #   Tile 1: Snow Rat x2
    #   Tile 2: Engorged Zombie
    no_safe_haven = EncounterSpec(
        name="No Safe Haven",
        level=1,
        enemies=[
            EncounterEnemySpec(enemy_name="Snow Rat", count=2, tile=1),
            EncounterEnemySpec(enemy_name="Engorged Zombie", count=1, tile=2),
        ],
    )

    alts = generate_alternatives(
        no_safe_haven,
        enemies,
        max_candidates=5,
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
