import csv
import re
from typing import List, Dict, Any, Optional

from models import Enemy, EnemyAction

damage_pattern = re.compile(r"(\d+)\s+(physical|magic)", re.IGNORECASE)
move_attack_pattern = re.compile(r"\bmove-attack\s+(\d+)", re.IGNORECASE)
move_pattern = re.compile(r"\bmove\s+(\d+)", re.IGNORECASE)
enemy_ids = {
    "Alonne Bow Knight": 1,
    "Alonne Knight Captain": 2,
    "Alonne Sword Knight": 3,
    "Black Hollow Mage": 4,
    "Bonewheel Skeleton": 5,
    "Crossbow Hollow": 6,
    "Crow Demon": 7,
    "Demonic Foliage": 8,
    "Engorged Zombie": 9,
    "Falchion Skeleton": 10,
    "Firebomb Hollow": 11,
    "Giant Skeleton Archer": 12,
    "Giant Skeleton Soldier": 13,
    "Hollow Soldier": 14,
    "Ironclad Soldier": 15,
    "Large Hollow Soldier": 16,
    "Mushroom Child": 17,
    "Mushroom Parent": 18,
    "Necromancer": 19,
    "Phalanx": 20,
    "Phalanx Hollow": 21,
    "Plow Scarecrow": 22,
    "Sentinel": 23,
    "Shears Scarecrow": 24,
    "Silver Knight Greatbowman": 25,
    "Silver Knight Spearman": 26,
    "Silver Knight Swordsman": 27,
    "Skeleton Archer": 28,
    "Skeleton Beast": 29,
    "Skeleton Soldier": 30,
    "Snow Rat": 31,
    "Stone Guardian": 32,
    "Stone Knight": 33,
    "Mimic": 34,
    "Armorer Dennis": 35,
    "Fencer Sharron": 36,
    "Invader Brylex": 37,
    "Kirk, Knight of Thorns": 38,
    "Longfinger Kirk": 39,
    "Maldron the Assassin": 40,
    "Maneater Mildred": 41,
    "Marvelous Chester": 42,
    "Melinda the Butcher": 43,
    "Oliver the Collector": 44,
    "Paladin Leeroy": 45,
    "Xanthous King Jeremiah": 46,
    "Hungry Mimic": 47,
    "Voracious Mimic": 48
}
id_to_enemy_name = {v: k for (k, v) in enemy_ids.items()}

def parse_action_text(text: str) -> Optional[EnemyAction]:
    if not text:
        return None
    t = text.strip()
    if not t:
        return None
    lower = t.lower()

    if "resurrect" in lower or "summon" in lower:
        return None
    if lower.startswith("move ") or lower.startswith("move-attack "):
        if damage_pattern.search(t) is None:
            return None
    if lower.startswith("leap to "):
        return None

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
    dmg_type = m.group(2).lower()
    max_targets = 1
    if "node" in lower or kind in ("move-attack", "leap-attack"):
        max_targets = 3

    # Status parsing from text
    apply_bleed = "bleed" in lower
    apply_poison = "poison" in lower
    apply_frostbite = "frostbite" in lower
    apply_stagger = "stagger" in lower

    return EnemyAction(
        kind=kind,
        damage=dmg,
        damage_type=dmg_type,
        max_targets=max_targets,
        raw_text=t,
        apply_bleed=apply_bleed,
        apply_poison=apply_poison,
        apply_frostbite=apply_frostbite,
        apply_stagger=apply_stagger,
    )

def extract_mobility_flags(
    row: Dict[str, str],
    actions: List[EnemyAction],
    range_behavior: Optional[int],
) -> Dict[str, Any]:
    """
    Parse movement, push, leap, ranged/leap flags from the CSV row + actions.

    - move_speed: max "Move X" or "Move-attack X" found; fallback to 1.0 for
      pure melee if nothing explicit is given.
    - has_push: any move-attack / leap-attack or explicit "push" in text.
    - has_leap: any leap-attack action OR any line that mentions "leap"
      (e.g. "Leap to aggro" with no damage).
    - is_ranged_or_leap: ranged enemy (range_behavior >= 1) or leaper.
    """
    move_speed = 0.0
    has_push = False

    # Start with any parsed leap-attack actions
    has_leap = any(a.kind == "leap-attack" for a in actions)

    for col in ("Action 1", "Action 2", "Action 3"):
        raw = row.get(col) or ""
        lower = raw.lower()

        if not lower:
            continue

        # Detect any leap-like movement, even if it's not an attack
        # e.g. "Leap to aggro"
        if "leap" in lower:
            has_leap = True

        # Move-attack X ...
        m1 = move_attack_pattern.search(lower)
        if m1:
            val = float(m1.group(1))
            move_speed = max(move_speed, val)

        # Move X ...
        m2 = move_pattern.search(lower)
        if m2:
            val = float(m2.group(1))
            move_speed = max(move_speed, val)

        # Any explicit "push" in text
        if "push" in lower:
            has_push = True

    # Move-attack / leap-attack in this game always push
    if any(a.kind in ("move-attack", "leap-attack") for a in actions):
        has_push = True

    # Fallback: if melee enemy and no explicit move found, assume move 1
    rb = range_behavior or 0
    if move_speed == 0.0 and rb == 0 and not has_leap:
        move_speed = 1.0

    is_ranged_or_leap = (rb >= 1) or has_leap

    return {
        "move_speed": move_speed,
        "has_push": has_push,
        "has_leap": has_leap,
        "is_ranged_or_leap": is_ranged_or_leap,
    }

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

            # Parse actions
            actions: List[EnemyAction] = []
            for col in ("Action 1", "Action 2", "Action 3"):
                raw = row.get(col) or ""
                act = parse_action_text(raw)
                if act is not None:
                    actions.append(act)

            tags = infer_tags(row, actions)
            mob = extract_mobility_flags(row, actions, range_behavior)

            can_bleed = any(a.apply_bleed for a in actions)
            can_poison = any(a.apply_poison for a in actions)
            can_frostbite = any(a.apply_frostbite for a in actions)
            can_stagger = any(a.apply_stagger for a in actions)

            enemy = Enemy(
                enemy_id=enemy_ids[name],
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
                move_speed=mob["move_speed"],
                has_push=mob["has_push"],
                has_leap=mob["has_leap"],
                is_ranged_or_leap=mob["is_ranged_or_leap"],
                can_bleed=can_bleed,
                can_poison=can_poison,
                can_frostbite=can_frostbite,
                can_stagger=can_stagger,
            )
            enemies.append(enemy)
    return enemies
