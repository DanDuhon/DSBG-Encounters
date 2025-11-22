from dataclasses import dataclass
from typing import List, Dict, Tuple

from models import Enemy, Character, BuildKey
from encounter_threat import (
    EncounterTile,
    EncounterEnemySlot,
    compute_tile_threat_profile_all_tiers,
)
from builds import build_all_builds  # optional helper for demo
from enemies_io import load_enemies_from_csv


PLAYER_COUNTS = (1, 2, 3, 4)


def level_to_tier_name(level: int) -> str:
    """
    Map encounter level -> tier name.

    You can tweak this mapping if your level scheme differs:
      level 1 -> tier1
      level 2 -> tier2
      level 3+ -> tier3
    """
    if level <= 1:
        return "tier1"
    elif level == 2:
        return "tier2"
    else:
        return "tier3"


def tile_composition_stats(
    tile: EncounterTile,
    enemies_by_name: Dict[str, Enemy],
) -> Dict[str, int]:
    """
    Basic composition stats for a tile:
      - total enemies
      - # ranged/leap vs melee
      - # with 1 HP vs >=5 HP
    """
    total = 0
    ranged_or_leap = 0
    melee = 0
    hp_1 = 0
    hp_5plus = 0

    for slot in tile.enemies:
        enemy = enemies_by_name.get(slot.name)
        if enemy is None:
            continue
        count = slot.count
        total += count

        if enemy.is_ranged_or_leap:
            ranged_or_leap += count
        else:
            melee += count

        if enemy.hp == 1:
            hp_1 += count
        if enemy.hp >= 5:
            hp_5plus += count

    return {
        "total": total,
        "ranged_or_leap": ranged_or_leap,
        "melee": melee,
        "hp_1": hp_1,
        "hp_5plus": hp_5plus,
    }


def extract_pattern(tile: EncounterTile) -> List[int]:
    """
    Extract the multiset of counts per enemy type on this tile, sorted descending.
    E.g. Snow Rat x2, Engorged Zombie x1 -> [2, 1]
    """
    counts = [slot.count for slot in tile.enemies if slot.count > 0]
    counts.sort(reverse=True)
    return counts


def profile_vector_for_tier(
    profile: Dict[str, Dict[str, float]],
    tier_name: str,
) -> List[float]:
    """
    Flatten a tile threat profile down to [p1, p2, p3, p4] for a single tier.
    Missing entries are treated as 0.0.
    """
    tier = profile.get(tier_name, {})
    return [
        float(tier.get("p1", 0.0) or 0.0),
        float(tier.get("p2", 0.0) or 0.0),
        float(tier.get("p3", 0.0) or 0.0),
        float(tier.get("p4", 0.0) or 0.0),
    ]


def profile_distance(
    target_vec: List[float],
    cand_vec: List[float],
) -> float:
    """
    Distance between two [p1..p4] vectors for a tier.

    We use squared relative error where possible:
      ((cand - target) / max(target, eps))^2
    so a 10% error on a big number counts more than a 10% error on a tiny one.
    """
    assert len(target_vec) == len(cand_vec)
    eps = 1e-6
    total = 0.0
    for t, c in zip(target_vec, cand_vec):
        denom = t if abs(t) > eps else 1.0
        diff = (c - t) / denom
        total += diff * diff
    return total


def select_candidate_enemy_pool(
    enemies_by_name: Dict[str, Enemy],
) -> List[Enemy]:
    """
    Select which enemies are allowed as building blocks for alternatives.

    For now, we simply use all enemies loaded from CSV. You can refine this later
    (e.g., exclude bosses, traps, or extremely high-HP enemies for low-level tiles).
    """
    return list(enemies_by_name.values())


def generate_alternative_tiles_for_tile(
    orig_tile: EncounterTile,
    encounter_level: int,
    enemies_by_name: Dict[str, Enemy],
    builds: Dict[BuildKey, Character],
    max_alternatives: int = 20,
    max_pattern_len: int = 3,
) -> List[Tuple[EncounterTile, float]]:
    """
    Generate alternative tiles whose threat profile is close to the original tile's,
    for the relevant tier derived from encounter_level.

    Constraints enforced:
      - same total enemy count
      - same # ranged/leap vs melee
      - same # 1 HP and 5+ HP enemies
      - same multiset of counts per enemy type (e.g. [2, 1] for 2+1 enemies)
      - at most max_pattern_len distinct enemy types (to avoid combinatorial blow-up)

    Returns a list of (tile, distance_score), sorted by increasing score.
    """
    # 1) Target profile vector for the appropriate tier
    tier_name = level_to_tier_name(encounter_level)
    target_profile = compute_tile_threat_profile_all_tiers(
        orig_tile, enemies_by_name, builds
    )
    target_vec = profile_vector_for_tier(target_profile, tier_name)

    # 2) Original composition stats and pattern
    target_stats = tile_composition_stats(orig_tile, enemies_by_name)
    pattern = extract_pattern(orig_tile)
    if len(pattern) > max_pattern_len:
        # Too many distinct enemy types; bail out or increase max_pattern_len
        return []

    total_required = target_stats["total"]

    # 3) Candidate enemy pool
    candidates = select_candidate_enemy_pool(enemies_by_name)

    # Precompute per-enemy classification to avoid repeated property lookups
    def classify_enemy(e: Enemy) -> Dict[str, int]:
        is_ranged = 1 if e.is_ranged_or_leap else 0
        is_melee = 0 if is_ranged else 1
        is_hp1 = 1 if e.hp == 1 else 0
        is_hp5p = 1 if e.hp >= 5 else 0
        return {
            "ranged": is_ranged,
            "melee": is_melee,
            "hp1": is_hp1,
            "hp5p": is_hp5p,
        }

    enemy_class = {e.name: classify_enemy(e) for e in candidates}

    # Helper to compare tiles
    def tile_is_same_as_original(a: EncounterTile, b: EncounterTile) -> bool:
        """Check if two tiles have the same multiset of (name, count)."""
        def normalize(tile: EncounterTile) -> List[Tuple[str, int]]:
            return sorted(
                [(slot.name, slot.count) for slot in tile.enemies if slot.count > 0]
            )
        return normalize(a) == normalize(b)

    # 4) Backtracking over pattern positions to assign enemy types

    best: List[Tuple[EncounterTile, float]] = []

    # We'll track stats incrementally
    def backtrack(
        pattern_idx: int,
        start_idx: int,
        assigned: List[EncounterEnemySlot],
        stats_acc: Dict[str, int],
    ):
        nonlocal best

        if pattern_idx == len(pattern):
            # Full assignment; check if stats match exactly
            if (
                stats_acc["total"] == target_stats["total"]
                and stats_acc["ranged_or_leap"] == target_stats["ranged_or_leap"]
                and stats_acc["melee"] == target_stats["melee"]
                and stats_acc["hp_1"] == target_stats["hp_1"]
                and stats_acc["hp_5plus"] == target_stats["hp_5plus"]
            ):
                candidate_tile = EncounterTile(
                    name=f"{orig_tile.name}_alt_{len(best)+1}",
                    enemies=list(assigned),
                )
                # Compute its profile and distance
                cand_profile = compute_tile_threat_profile_all_tiers(
                    candidate_tile, enemies_by_name, builds
                )
                cand_vec = profile_vector_for_tier(cand_profile, tier_name)
                score = profile_distance(target_vec, cand_vec)

                # Skip if it's exactly the same as the original (same names/counts)
                if tile_is_same_as_original(orig_tile, candidate_tile):
                    return

                # Insert into best list (sorted, capped at max_alternatives)
                best.append((candidate_tile, score))
                best.sort(key=lambda x: x[1])
                if len(best) > max_alternatives:
                    best = best[:max_alternatives]
            return

        remaining_total = total_required - stats_acc["total"]
        if remaining_total < 0:
            return

        count_here = pattern[pattern_idx]

        # Rough pruning: we know how many enemies we still need to place.
        if count_here > remaining_total:
            return

        for i in range(start_idx, len(candidates)):
            enemy = candidates[i]
            c = enemy_class[enemy.name]

            # Incremental stats when assigning this enemy with count_here
            new_stats = dict(stats_acc)
            new_stats["total"] += count_here
            new_stats["ranged_or_leap"] += c["ranged"] * count_here
            new_stats["melee"] += c["melee"] * count_here
            new_stats["hp_1"] += c["hp1"] * count_here
            new_stats["hp_5plus"] += c["hp5p"] * count_here

            # Quick pruning: don't overshoot any target stat
            if new_stats["total"] > target_stats["total"]:
                continue
            if new_stats["ranged_or_leap"] > target_stats["ranged_or_leap"]:
                continue
            if new_stats["melee"] > target_stats["melee"]:
                continue
            if new_stats["hp_1"] > target_stats["hp_1"]:
                continue
            if new_stats["hp_5plus"] > target_stats["hp_5plus"]:
                continue

            assigned.append(EncounterEnemySlot(enemy.name, count_here))
            backtrack(pattern_idx + 1, i + 1, assigned, new_stats)
            assigned.pop()

    initial_stats = {
        "total": 0,
        "ranged_or_leap": 0,
        "melee": 0,
        "hp_1": 0,
        "hp_5plus": 0,
    }

    backtrack(pattern_idx=0, start_idx=0, assigned=[], stats_acc=initial_stats)

    return best


# ---- Example CLI usage (optional helper) ----

def demo_generate_alternatives(
    csv_path: str,
    orig_tile: EncounterTile,
    encounter_level: int,
    max_alternatives: int = 10,
):
    """
    Convenience function to run from a script.
    """
    enemies = load_enemies_from_csv(csv_path)
    enemies_by_name = {e.name: e for e in enemies}
    builds = build_all_builds()

    alts = generate_alternative_tiles_for_tile(
        orig_tile=orig_tile,
        encounter_level=encounter_level,
        enemies_by_name=enemies_by_name,
        builds=builds,
        max_alternatives=max_alternatives,
    )

    print(f"Original tile: {orig_tile.name}")
    for slot in orig_tile.enemies:
        print(f"  - {slot.count}x {slot.name}")

    print("\nAlternatives:")
    for tile, score in alts:
        print(f"  {tile.name} (score={score:.4f}):")
        for slot in tile.enemies:
            print(f"    - {slot.count}x {slot.name}")
        print()