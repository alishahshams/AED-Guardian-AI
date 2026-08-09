import json
import geopandas as gpd

from operating_hours import parse_operating_hours


DATA_PATH = "data/PublicAccessAEDs.geojson"
OUTPUT_PATH = "phase2/human_review_queue.json"


def main():

    print("Loading AED dataset...")

    aed = gpd.read_file(DATA_PATH)

    review_queue = []

    for index, row in aed.iterrows():

        result = parse_operating_hours(row["OPERATING_HOURS"])

        if result["status"] in {"AMBIGUOUS", "UNPARSED", "MISSING"}:

            review_queue.append({
                "record_index": int(index),
                "AED_ID": str(row.get("AED_ID", "")),
                "BUILDING_NAME": str(row.get("BUILDING_NAME", "")),
                "ROAD_NAME": str(row.get("ROAD_NAME", "")),
                "POSTAL_CODE": str(row.get("POSTAL_CODE", "")),
                "OPERATING_HOURS": (
                    None
                    if row["OPERATING_HOURS"] is None
                    else str(row["OPERATING_HOURS"])
                ),
                "OH_STATUS": result["status"],
                "OH_CONFIDENCE": result["confidence"],
                "OH_REASON": result["reason"],
            })

    output = {
        "purpose": (
            "Human-in-the-loop review queue for registry "
            "operating-hours data-quality concerns."
        ),
        "scope": (
            "Flags indicate possible registry text-quality issues "
            "and do not confirm real-world AED faults."
        ),
        "total_flagged_records": len(review_queue),
        "records": review_queue,
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print("\n=== HUMAN REVIEW QUEUE ===")
    print(f"Flagged records: {len(review_queue)}")

    for item in review_queue:
        print(
            f"\nRecord {item['record_index']}"
            f"\nAED ID: {item['AED_ID']}"
            f"\nOperating hours: {item['OPERATING_HOURS']}"
            f"\nStatus: {item['OH_STATUS']}"
            f"\nConfidence: {item['OH_CONFIDENCE']}"
            f"\nReason: {item['OH_REASON']}"
        )

    print(f"\nReview queue saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
