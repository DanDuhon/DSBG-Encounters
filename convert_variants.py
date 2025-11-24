"""
Convert old behavior-variant JSON files (bucketed by difficulty) into a flatter,
Streamlit-friendly format.

Old format (per file, e.g. "Armorer Dennis - Soul Flash.json"):

{
  "1": {                             # party size (characters)
    "1.25": [                        # difficulty score / factor as string
      ["dodge1", "armor resist2"],   # variant 0
      ["dodge1"]                     # variant 1
    ],
    "1.35": [
      ...
    ],
    ...
  },
  "2": { ... },
  "3": { ... },
  "4": { ... }
}

New format:

{
  "enemy_name": "Armorer Dennis",
  "behavior_name": "Soul Flash",
  "variants": [
    {
      "id": "Soul_Flash_1_1_0",
      "party_size": 1,
      "difficulty": 1.25,
      "tokens": ["dodge1", "armor resist2"],
      "defense_tokens": ["armor resist2"]
    },
    ...
  ]
}
"""

import argparse
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple


def parse_names_from_filename(path: Path) -> Tuple[str, str]:
    """
    Derive enemy_name and behavior_name from the file name.

    Examples:
      "Armorer Dennis - Soul Flash.json" -> ("Armorer Dennis", "Soul Flash")
      "Alonne Bow Knight.json"          -> ("Alonne Bow Knight", "Alonne Bow Knight")
    """
    stem = path.stem
    if " - " in stem:
        enemy_name, behavior_name = stem.split(" - ", 1)
    else:
        enemy_name = stem
        behavior_name = stem
    return enemy_name, behavior_name


def clean_token(raw: Any) -> str:
    """
    Normalize a token into a clean string.

    Handles odd artifacts like " ('poison'],)" or "('poison',)" by extracting
    just "poison". If the token is not a string, it is cast to str().
    """
    token = str(raw).strip()

    # Handle patterns like "('poison'],)" or "('poison',)"
    if token.startswith("('") and token.endswith("'],)"):
        # "('poison'],)" -> "poison"
        return token[2:-3]
    if token.startswith("('") and token.endswith("',)"):
        # "('poison',)" -> "poison"
        return token[2:-3]

    # Fallback: just return the stripped token
    return token


def is_defense_token(token: str) -> bool:
    """
    Very simple heuristic: treat any token that looks like HP/armor/resist
    as a 'defense' modifier. This makes it easy later to enforce shared
    defense across multi-card bosses.
    """
    lower = token.lower()
    return lower.startswith("health") or lower.startswith("armor") or lower.startswith("resist")


def convert_old_data(
    old_data: Dict[str, Any],
    enemy_name: str,
    behavior_name: str
) -> Dict[str, Any]:
    """
    Convert the in-memory old JSON structure into the new format dict.
    """
    new: Dict[str, Any] = {
        "enemy_name": enemy_name,
        "behavior_name": behavior_name,
        "variants": []
    }

    variants_out: List[Dict[str, Any]] = []

    # Top-level keys are party sizes as strings ("1", "2", "3", "4")
    for party_size_str, difficulty_buckets in old_data.items():
        try:
            party_size = int(party_size_str)
        except ValueError:
            # If there are any weird keys, skip them
            continue

        if not isinstance(difficulty_buckets, dict):
            continue

        # Second-level keys are difficulty scores / factors ("1.25", "2.6", ...)
        for difficulty_str, variant_lists in difficulty_buckets.items():
            try:
                difficulty = float(difficulty_str)
            except ValueError:
                # Skip odd keys if any
                continue

            if not isinstance(variant_lists, list):
                continue

            for idx, token_list in enumerate(variant_lists):
                if not isinstance(token_list, list):
                    # Occasionally there might be a stray non-list; make it a single-token list
                    token_list = [token_list]

                # Clean and normalize tokens
                tokens = [clean_token(t) for t in token_list]
                tokens = [t for t in tokens if t]  # drop empty strings

                # Classify defense tokens for later boss logic
                defense_tokens = [t for t in tokens if is_defense_token(t)]

                # Build a somewhat stable ID
                safe_behavior = behavior_name.replace(" ", "_")
                safe_diff = difficulty_str.replace(".", "_")
                variant_id = f"{safe_behavior}_{party_size}_{safe_diff}_{idx}"

                variant_obj = {
                    "id": variant_id,
                    "party_size": party_size,
                    "difficulty": difficulty,
                    "tokens": tokens,
                    "defense_tokens": defense_tokens,
                }
                variants_out.append(variant_obj)

    # Optionally, sort by party_size then difficulty
    variants_out.sort(key=lambda v: (v["party_size"], v["difficulty"]))
    new["variants"] = variants_out
    return new


def convert_file(input_path: Path, output_path: Path) -> None:
    """
    Convert a single JSON file from old format into new format and write it.
    """
    with input_path.open("r", encoding="utf-8") as f:
        old_data = json.load(f)

    enemy_name, behavior_name = parse_names_from_filename(input_path)
    new_data = convert_old_data(old_data, enemy_name, behavior_name)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)

    print(f"Converted {input_path} -> {output_path}")


input_path = Path("old_variants")
output_path = Path("new_variants")

if input_path.is_file():
    # Single-file mode
    if output_path.is_dir():
        out_file = output_path / input_path.name
    else:
        out_file = output_path
    convert_file(input_path, out_file)
else:
    # Directory mode: convert all *.json inside
    if not output_path.exists():
        output_path.mkdir(parents=True, exist_ok=True)

    for file in input_path.glob("*.json"):
        out_file = output_path / file.name
        convert_file(file, out_file)
