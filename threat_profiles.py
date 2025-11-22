import json
from typing import Dict, List, Optional

from models import Enemy, BuildKey, Character
from builds import PLAYER_COUNTS, build_all_builds
from enemies_io import load_enemies_from_csv
from parties import iter_parties_for_tier
from mobility import enemy_threat_vs_party

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

def enemies_to_json_serializable(enemies: List[Enemy]) -> List[Dict]:
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
        builds = build_all_builds()

    enemies = load_enemies_from_csv(csv_path)
    for e in enemies:
        e.threat_profile = compute_enemy_threat_profile_all_tiers(e, builds)

    #    Phalanx special case: when Phalanx dies, it becomes 3 Phalanx Hollows.
    #    So for each tier/player-count entry, we add 3 * Phalanx Hollow threat
    #    onto Phalanx's own threat profile.
    by_name: Dict[str, Enemy] = {e.name: e for e in enemies}

    phalanx = by_name.get("Phalanx")
    phalanx_hollow = by_name.get("Phalanx Hollow")

    if phalanx is not None and phalanx_hollow is not None:
        for tier_name, tier_vals in phalanx.threat_profile.items():
            hollow_tier_vals = phalanx_hollow.threat_profile.get(tier_name, {})
            for p_key, base_val in list(tier_vals.items()):
                base = float(base_val or 0.0)
                hollow_val = float(hollow_tier_vals.get(p_key, 0.0) or 0.0)
                # Phalanx effective threat = Phalanx + 3 × Phalanx Hollow
                tier_vals[p_key] = base + 3.0 * hollow_val

    data = enemies_to_json_serializable(enemies)
    with open(json_out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

    return enemies
