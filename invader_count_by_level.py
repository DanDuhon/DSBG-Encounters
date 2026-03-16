import os
import json
import glob
import re
from collections import Counter, defaultdict

# Directory containing your encounter JSON files
ENCOUNTERS_DIR = r"C:\Users\lenle\Documents\GitHub\DSBG-Encounters\encounters"

# Source of truth for encounter metadata (including level)
ALL_ENCOUNTERS_PATH = os.path.join(ENCOUNTERS_DIR, "all_encounters.json")

# Threshold (enemy IDs > THRESHOLD are treated as "invaders" by this script)
THRESHOLD = 34


def count_greater_than_threshold(sublist, threshold):
    """Count how many ints in sublist are > threshold."""
    return sum(1 for x in sublist if isinstance(x, int) and x > threshold)


def load_all_encounters(path):
    """Load the all_encounters.json map: {encounter_name: {..., level: N, ...}}."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} did not contain an object/dict at the top level.")
    return data


def resolve_encounter_name(file_stem, all_encounters):
    """
    Resolve an encounter filename stem to a name key in all_encounters.json.

    Typical files are named like:
        "Abandoned Storeroom1.json" .. "Abandoned Storeroom4.json"
    where the trailing digit is not part of the encounter name.
    """
    # Exact match first
    if file_stem in all_encounters:
        return file_stem

    # Strip trailing digits and try again
    m = re.match(r"^(.*?)(\d+)$", file_stem)
    if m:
        candidate = m.group(1).rstrip()
        if candidate in all_encounters:
            return candidate

    return file_stem  # fallback (will become "Unknown" level)


def get_encounter_level(file_stem, all_encounters):
    name = resolve_encounter_name(file_stem, all_encounters)
    level = all_encounters.get(name, {}).get("level", None)
    return name, level


def process_file(filepath, threshold):
    """
    For a single JSON file:
      - Look under 'alternatives'
      - For each sublist, count ints > threshold
      - Return:
          * max count for this file
          * details where that max occurred
          * a Counter mapping {count: number_of_sublists_with_that_count}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    alternatives = data.get("alternatives", {})
    file_max = 0
    file_counter = Counter()
    max_detail = None  # (key, sublist_index, count, sublist)

    if not isinstance(alternatives, dict):
        return 0, None, Counter()

    for key, list_of_sublists in alternatives.items():
        if not isinstance(list_of_sublists, list):
            continue

        for i, sublist in enumerate(list_of_sublists):
            if not isinstance(sublist, list):
                continue

            count = count_greater_than_threshold(sublist, threshold)
            file_counter[count] += 1

            if count > file_max:
                file_max = count
                max_detail = (key, i, count, sublist)

    return file_max, max_detail, file_counter


def _sorted_levels(levels):
    """
    Sort numeric levels first (ascending), then non-numeric labels last.
    """
    numeric = sorted([x for x in levels if isinstance(x, int)])
    non_numeric = sorted([x for x in levels if not isinstance(x, int)], key=lambda v: str(v))
    return numeric + non_numeric


def main():
    # Load encounter levels
    try:
        all_encounters = load_all_encounters(ALL_ENCOUNTERS_PATH)
    except FileNotFoundError:
        print(f"Could not find all_encounters.json at: {ALL_ENCOUNTERS_PATH}")
        return
    except Exception as e:
        print(f"Failed to load all_encounters.json ({ALL_ENCOUNTERS_PATH}): {e}")
        return

    pattern = os.path.join(ENCOUNTERS_DIR, "*.json")
    json_files = glob.glob(pattern)

    if not json_files:
        print(f"No JSON files found in {ENCOUNTERS_DIR}")
        return

    # Exclude all_encounters.json from the scan
    all_encounters_basename = os.path.basename(ALL_ENCOUNTERS_PATH).lower()
    json_files = [p for p in json_files if os.path.basename(p).lower() != all_encounters_basename]

    if not json_files:
        print(f"No encounter JSON files found in {ENCOUNTERS_DIR} (after excluding all_encounters.json).")
        return

    overall_max = 0
    overall_detail = None  # (filename, encounter_name, level, key, sublist_index, count, sublist)
    overall_counter = Counter()

    # Per-level aggregation
    level_counters = defaultdict(Counter)      # level -> Counter(count -> occurrences)
    level_file_counts = Counter()              # level -> number of files
    level_sublist_counts = Counter()           # level -> number of sublists (sum of file_counter values)
    level_max = defaultdict(int)               # level -> max invader count seen in any sublist
    level_detail = {}                          # level -> (filename, encounter_name, key, index, count, sublist)

    print(f"Scanning JSON files in: {ENCOUNTERS_DIR}")
    print(f"Using encounter levels from: {ALL_ENCOUNTERS_PATH}\n")

    for filepath in json_files:
        file_max, max_detail, file_counter = process_file(filepath, THRESHOLD)
        filename = os.path.basename(filepath)
        stem = os.path.splitext(filename)[0]

        encounter_name, level = get_encounter_level(stem, all_encounters)
        level_label = level if isinstance(level, int) else "Unknown"

        # Merge file histogram into overall histogram and per-level histogram
        overall_counter.update(file_counter)
        level_counters[level_label].update(file_counter)

        # Bookkeeping
        level_file_counts[level_label] += 1
        level_sublist_counts[level_label] += sum(file_counter.values())

        # Report per-file maximum (now includes encounter level)
        level_str = str(level_label)
        print(f"{filename} (encounter='{encounter_name}', level={level_str}): max invaders = {file_max}")
        if max_detail is not None:
            key, index, count, sublist = max_detail
            print(f"  - occurred in alternatives['{key}'][{index}] = {sublist}")

        # Update per-level maximum
        if file_max > level_max[level_label] and max_detail is not None:
            key, index, count, sublist = max_detail
            level_max[level_label] = file_max
            level_detail[level_label] = (filename, encounter_name, key, index, count, sublist)

        # Update overall maximum
        if file_max > overall_max and max_detail is not None:
            overall_max = file_max
            key, index, count, sublist = max_detail
            overall_detail = (filename, encounter_name, level_label, key, index, count, sublist)

        print()  # blank line between files

    # Overall maximum
    print("==== Overall maximum across all files ====")
    print(f"Greatest number of invaders in any sublist: {overall_max}")
    if overall_detail is not None:
        filename, encounter_name, level_label, key, index, count, sublist = overall_detail
        print(f"Found in file: {filename}")
        print(f"Encounter: {encounter_name} (level={level_label})")
        print(f"Location: alternatives['{key}'][{index}]")
        print(f"Sublist: {sublist}")

    # Overall histogram
    print("\n==== Histogram of invader counts across ALL files ====")
    for count in sorted(overall_counter.keys()):
        num_sublists = overall_counter[count]
        print(f"{num_sublists:5} sublists have {count} invaders")

    # Split out by encounter level
    print("\n==== Histogram of invader counts split by encounter level ====")
    for lvl in _sorted_levels(level_counters.keys()):
        print(f"\n---- Level {lvl} ----")
        print(f"Files scanned: {level_file_counts[lvl]}")
        print(f"Sublists scanned: {level_sublist_counts[lvl]}")
        print(f"Max invaders in any sublist at this level: {level_max[lvl]}")
        if lvl in level_detail:
            filename, encounter_name, key, index, count, sublist = level_detail[lvl]
            print(f"  - example max found in: {filename} (encounter='{encounter_name}')")
            print(f"    location: alternatives['{key}'][{index}]")
            print(f"    sublist: {sublist}")

        for count in sorted(level_counters[lvl].keys()):
            num_sublists = level_counters[lvl][count]
            print(f"{num_sublists:5} sublists have {count} invaders")

    input()


if __name__ == "__main__":
    main()
