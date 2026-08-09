import json
import geopandas as gpd

from operating_hours import parse_operating_hours


DATA_PATH = "data/PublicAccessAEDs.geojson"
OUTPUT_PATH = "phase2/operating_hours_quality_report.json"


def main():

    print("Loading AED dataset...")

    aed = gpd.read_file(DATA_PATH)

    print(f"Records loaded: {len(aed)}")

    results = []

    for value in aed["OPERATING_HOURS"]:
        results.append(parse_operating_hours(value))

    status_counts = {}
    confidence_counts = {}

    for result in results:

        status = result["status"]
        confidence = result["confidence"]

        status_counts[status] = status_counts.get(status, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1

    total = len(results)

    status_percentages = {
        status: round((count / total) * 100, 2)
        for status, count in status_counts.items()
    }

    confidence_percentages = {
        confidence: round((count / total) * 100, 2)
        for confidence, count in confidence_counts.items()
    }

    ambiguous_examples = []

    for index, result in enumerate(results):

        if result["status"] in {"AMBIGUOUS", "UNPARSED", "MISSING"}:

            value = aed.iloc[index]["OPERATING_HOURS"]

            ambiguous_examples.append({
                "record_index": int(index),
                "operating_hours": None if value is None else str(value),
                "status": result["status"],
                "confidence": result["confidence"],
                "reason": result["reason"],
            })

    report = {
        "dataset": "SCDF Public Access AEDs",
        "records_analyzed": total,

        "status_distribution": status_counts,
        "status_percentage": status_percentages,

        "confidence_distribution": confidence_counts,
        "confidence_percentage": confidence_percentages,

        "review_queue_count": len(ambiguous_examples),

        "review_queue_examples": ambiguous_examples[:20],

        "interpretation": {
            "scope": (
                "This report evaluates registry operating-hours "
                "text quality only."
            ),
            "not_current_availability": (
                "Parsed operating hours do not establish current "
                "AED accessibility or operational readiness."
            ),
            "human_review": (
                "Ambiguous, missing, or unparsed records should be "
                "reviewed by a human registry reviewer."
            ),
        },
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n=== OPERATING-HOURS QUALITY REPORT ===")

    print("\nStatus distribution:")
    for status, count in status_counts.items():
        percentage = status_percentages[status]
        print(f"{status}: {count} ({percentage}%)")

    print("\nConfidence distribution:")
    for confidence, count in confidence_counts.items():
        percentage = confidence_percentages[confidence]
        print(f"{confidence}: {count} ({percentage}%)")

    print(f"\nHuman-review queue: {len(ambiguous_examples)} records")

    print(f"\nReport saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
