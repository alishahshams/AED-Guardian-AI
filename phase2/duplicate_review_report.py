import json
import csv

INPUT_PATH = "phase2/duplicate_review_queue.json"
OUTPUT_PATH = "phase2/duplicate_review_report.csv"


def main():

    print("Loading duplicate review queue...")

    with open(
        INPUT_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        data = json.load(f)

    queue = data.get("review_queue", [])

    print(f"Review records loaded: {len(queue)}")

    rows = []

    for item in queue:

        rows.append({
            "review_id": item.get("review_id"),
            "AED_ID_1": item.get("AED_ID_1"),
            "AED_ID_2": item.get("AED_ID_2"),

            "building_1": item.get("building_1"),
            "building_2": item.get("building_2"),

            "road_1": item.get("road_1"),
            "road_2": item.get("road_2"),

            "postal_code_1": item.get(
                "postal_code_1"
            ),
            "postal_code_2": item.get(
                "postal_code_2"
            ),

            "location_1": item.get(
                "location_description_1"
            ),
            "location_2": item.get(
                "location_description_2"
            ),

            "latitude_1": item.get(
                "latitude_1"
            ),
            "longitude_1": item.get(
                "longitude_1"
            ),

            "latitude_2": item.get(
                "latitude_2"
            ),
            "longitude_2": item.get(
                "longitude_2"
            ),

            "distance_meters": item.get(
                "distance_meters"
            ),

            "rule": item.get("rule"),

            "confidence": item.get(
                "confidence"
            ),

            "reason": item.get(
                "reason"
            ),

            "human_label": item.get(
                "human_label",
                "UNREVIEWED"
            ),

            "reviewer_note": item.get(
                "reviewer_note",
                ""
            )
        })

    if not rows:
        print("No review records found.")
        return

    fieldnames = list(rows[0].keys())

    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(rows)

    print("\n=== DUPLICATE REVIEW REPORT ===")

    print(
        f"Records exported: {len(rows)}"
    )

    print(
        f"Saved to: {OUTPUT_PATH}"
    )

    print(
        "\nOpen the CSV in Excel and review "
        "the candidate pairs."
    )

    print(
        "\nAllowed labels:"
    )

    print("DUPLICATE")
    print("NOT_DUPLICATE")
    print("UNCERTAIN")


if __name__ == "__main__":
    main()
