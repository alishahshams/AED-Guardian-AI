import json
from datetime import datetime

AI_INPUT_FILE = "duplicate_scored_candidates.json"
HUMAN_INPUT_FILE = "duplicate_review_queue.json"
OUTPUT_FILE = "final_duplicate_review_report.json"

with open(AI_INPUT_FILE, "r", encoding="utf-8") as f:
    ai_data = json.load(f)

if isinstance(ai_data, list):
    ai_candidates = ai_data
elif isinstance(ai_data, dict):
    ai_candidates = (
        ai_data.get("candidates")
        or ai_data.get("results")
        or ai_data.get("scored_candidates")
        or ai_data.get("data")
        or []
    )
else:
    ai_candidates = []

ai_counts = {
    "DUPLICATE": 0,
    "NOT_DUPLICATE": 0,
    "UNCERTAIN": 0
}

for item in ai_candidates:
    label = (
        item.get("AI_label")
        or item.get("ai_label")
        or item.get("label")
        or "UNCERTAIN"
    )

    label = str(label).upper().strip()

    if label in ai_counts:
        ai_counts[label] += 1

try:
    with open(HUMAN_INPUT_FILE, "r", encoding="utf-8") as f:
        human_data = json.load(f)

    if isinstance(human_data, dict):
        human_queue = (
            human_data.get("review_queue")
            or human_data.get("records")
            or []
        )
    elif isinstance(human_data, list):
        human_queue = human_data
    else:
        human_queue = []

except FileNotFoundError:
    human_queue = []

human_counts = {
    "DUPLICATE": 0,
    "NOT_DUPLICATE": 0,
    "UNCERTAIN": 0,
    "UNREVIEWED": 0
}

for item in human_queue:
    label = str(
        item.get("human_label", "UNREVIEWED")
    ).upper().strip()

    if label in human_counts:
        human_counts[label] += 1
    else:
        human_counts["UNREVIEWED"] += 1

human_reviewed = (
    human_counts["DUPLICATE"]
    + human_counts["NOT_DUPLICATE"]
    + human_counts["UNCERTAIN"]
)

human_unreviewed = human_counts["UNREVIEWED"]

abstention_rate = (
    human_counts["UNCERTAIN"] / human_reviewed
    if human_reviewed > 0
    else 0
)

report = {
    "report": "AED Guardian AI - Final Duplicate Review",
    "generated_at": datetime.now().isoformat(),

    "ai_analysis": {
        "total_candidate_pairs": len(ai_candidates),
        "labels": {
            "DUPLICATE": ai_counts["DUPLICATE"],
            "NOT_DUPLICATE": ai_counts["NOT_DUPLICATE"],
            "UNCERTAIN": ai_counts["UNCERTAIN"]
        }
    },

    "human_review": {
        "total_flagged_pairs": len(human_queue),
        "reviewed_pairs": human_reviewed,
        "unreviewed_pairs": human_unreviewed,
        "labels": {
            "DUPLICATE": human_counts["DUPLICATE"],
            "NOT_DUPLICATE": human_counts["NOT_DUPLICATE"],
            "UNCERTAIN": human_counts["UNCERTAIN"]
        },
        "abstention_rate": abstention_rate,
        "status": (
            "COMPLETE"
            if human_unreviewed == 0
            else "INCOMPLETE"
        )
    },

    "safety_note": (
        "AI classifications are decision-support outputs. "
        "Candidate duplicates require human review before "
        "being treated as confirmed duplicate records."
    )
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print()
print("======================================")
print("FINAL AED GUARDIAN AI REPORT")
print("======================================")

print()
print("AI Analysis:")
print("Total candidates:", len(ai_candidates))
print("DUPLICATE:", ai_counts["DUPLICATE"])
print("UNCERTAIN:", ai_counts["UNCERTAIN"])
print("NOT_DUPLICATE:", ai_counts["NOT_DUPLICATE"])

print()
print("Human Review:")
print("Flagged:", len(human_queue))
print("Reviewed:", human_reviewed)
print("Unreviewed:", human_unreviewed)

print()
print(
    "Human Review Status:",
    "COMPLETE" if human_unreviewed == 0 else "INCOMPLETE"
)

print()
print("Final report saved:")
print(OUTPUT_FILE)