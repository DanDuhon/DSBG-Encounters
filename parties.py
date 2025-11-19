from itertools import combinations, product
from typing import List, Dict

from models import Character, BuildKey
from builds import CLASS_NAMES, TIER_CONFIG, PLAYER_COUNTS

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
                key: BuildKey = (cls, tlabel, party_size)
                if key in builds:
                    opts.append(builds[key])
            if not opts:
                skip_subset = True
                break
            options_per_cls.append(opts)
        if skip_subset:
            continue

        for combo in product(*options_per_cls):
            parties.append(list(combo))

    return parties
