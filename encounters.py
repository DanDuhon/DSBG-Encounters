from statistics import mean
from typing import List, Dict

from models import Enemy, EncounterSpec, Slot, EncounterEnemySpec

LEVEL_TO_TIER = {
    1: "tier1",
    2: "tier2",
    3: "tier3",
}

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
) -> List[Dict]:
    """
    Generate alternative enemy sets for an encounter that:
      - keep the same total enemy groups
      - keep the same HP-band counts
      - keep the same effective melee/ranged counts
      - keep total threat within 'threat_tolerance' for P=1..4
      - ensure the "boss slot" (highest-threat original enemy) is replaced
        with the highest-threat enemy in the new set.
    """
    import random
    name_to_enemy = {e.name: e for e in enemies}

    target_hp_counts, slots = compute_hp_counts_for_encounter(enc, name_to_enemy)
    target_melee, target_ranged = compute_effective_role_counts_for_encounter(enc, name_to_enemy)
    orig_threat = compute_encounter_threat(enc, name_to_enemy, tier_name)
    num_slots = len(slots)

    # Build pools by HP band
    band_pools: Dict[str, List[Enemy]] = {}
    for e in enemies:
        band = e.tags["hp_band"]
        band_pools.setdefault(band, []).append(e)

    orig_names_sorted = tuple(sorted(s.orig_enemy_name for s in slots))
    seen = {orig_names_sorted}

    candidates: List[Dict] = []
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
        orig_avgs = [average_threat(e, tier_name) for e in slot_orig_enemies]
        boss_idx = max(range(num_slots), key=lambda i: orig_avgs[i])

        cand_avgs = [average_threat(e, tier_name) for e in cand_enemies]
        boss_candidate_idx = max(range(num_slots), key=lambda i: cand_avgs[i])

        cand_enemies[boss_idx], cand_enemies[boss_candidate_idx] = (
            cand_enemies[boss_candidate_idx],
            cand_enemies[boss_idx],
        )

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
