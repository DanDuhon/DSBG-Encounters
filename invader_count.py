import os
import json
import glob
from collections import Counter

# Directory containing your encounter JSON files
ENCOUNTERS_DIR = r"C:\Users\lenle\Documents\GitHub\DSBG-Encounters\encounters"

# Threshold
THRESHOLD = 34

def count_greater_than_threshold(sublist, threshold):
    """Count how many ints in sublist are > threshold."""
    return sum(
        1
        for x in sublist
        if isinstance(x, int) and x > threshold
    )

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

def main():
    pattern = os.path.join(ENCOUNTERS_DIR, "*.json")
    json_files = glob.glob(pattern)

    if not json_files:
        print(f"No JSON files found in {ENCOUNTERS_DIR}")
        return

    overall_max = 0
    overall_detail = None  # (filename, key, sublist_index, count, sublist)
    overall_counter = Counter()

    print(f"Scanning JSON files in: {ENCOUNTERS_DIR}\n")

    for filepath in json_files:
        file_max, max_detail, file_counter = process_file(filepath, THRESHOLD)
        filename = os.path.basename(filepath)

        # Merge file histogram into overall histogram
        overall_counter.update(file_counter)

        # Report per-file maximum
        print(f"{filename}: max count of ints > {THRESHOLD} = {file_max}")
        if max_detail is not None:
            key, index, count, sublist = max_detail
            print(f"  - occurred in alternatives['{key}'][{index}] = {sublist}")

        # Update overall maximum
        if file_max > overall_max:
            overall_max = file_max
            if max_detail is not None:
                key, index, count, sublist = max_detail
                overall_detail = (filename, key, index, count, sublist)

        print()  # blank line between files

    # Print overall result
    print("==== Overall maximum across all files ====")
    print(f"Greatest number of ints > {THRESHOLD} in any sublist: {overall_max}")

    if overall_detail is not None:
        filename, key, index, count, sublist = overall_detail
        print(f"Found in file: {filename}")
        print(f"Location: alternatives['{key}'][{index}]")
        print(f"Sublist: {sublist}")

    # Print histogram of counts
    print("\n==== Histogram of counts (ints > {0}) across ALL files ====".format(THRESHOLD))
    # Sort by count (the key), ascending
    for count in sorted(overall_counter.keys()):
        num_sublists = overall_counter[count]
        print(f"{num_sublists:5} sublists have {count} ints > {THRESHOLD}")
    input()

if __name__ == "__main__":
    main()
