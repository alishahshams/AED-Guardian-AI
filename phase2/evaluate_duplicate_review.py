import json
from collections import Counter

QUEUE_PATH = "phase2/duplicate_review_queue.json"


def main():

    print("Loading reviewed duplicate pairs...")

    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    queue = data.get("review_queue", [])

    labels = [
        item.get("human_label", "UNREVIEWED")
        for item in queue
    ]

    total = len(labels)

    counts = Counter(labels)

    duplicate = counts["DUPLICATE"]
    not_duplicate = counts["NOT_DUPLICATE"]
    uncertain = counts["UNCERTAIN"]
    unreviewed = counts["UNREVIEWED"]

    reviewed = duplicate + not_duplicate + uncertain

    print()
    print("======================================")
    print(" DUPLICATE HUMAN REVIEW EVALUATION")
    print("======================================")

    print(f"Total pairs      : {total}")
    print(f"Reviewed pairs   : {reviewed}")
    print(f"DUPLICATE        : {duplicate}")
    print(f"NOT_DUPLICATE    : {not_duplicate}")
    print(f"UNCERTAIN        : {uncertain}")
    print(f"UNREVIEWED       : {unreviewed}")

    if reviewed > 0:
        abstention_rate = uncertain / reviewed

        print()
        print(f"Abstention rate  : {abstention_rate:.3f}")

    print()
    print("Human review successfully completed.")
    print("======================================")


if __name__ == "__main__":
    main()
