import csv
import re
from typing import List, Dict, Any, Optional

from models import Enemy, EnemyAction

damage_pattern = re.compile(r"(\d+)\s+(physical|magic)", re.IGNORECASE)

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
