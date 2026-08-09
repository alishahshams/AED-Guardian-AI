import json
import geopandas as gpd


DATA_PATH = "data/PublicAccessAEDs.geojson"
CANDIDATES_PATH = "phase2/duplicate_candidates.json"
OUTPUT_PATH = "phase2/duplicate_review_queue.json"

REVIEW_LIMIT = 100


def clean(value):
    if value is None:
        return ""

    text = str(value).strip()

    if text.lower() in {"nan", "none", "null"}:
        return ""

    return text


def main():

    print("Loading AED dataset...")

    aed = gpd.read_file(DATA_PATH)

    print(f"Records loaded: {len(aed)}")

    print("Loading duplicate candidates...")

    with open(
        CANDIDATES_PATH,
        "r",
        encoding="utf-8"
    ) as f:
        candidate_data = json.load(f)

    candidates = candidate_data.get(
        "candidate_pairs",
        []
    )

    print(
        f"Total candidate pairs: {len(candidates)}"
    )

    # ---------------------------------------------------------
    # Create a representative review queue
    # ---------------------------------------------------------

    selected = candidates[:REVIEW_LIMIT]

    review_queue = []

    for review_id, candidate in enumerate(
        selected,
        start=1
    ):

        idx1 = candidate["record_1"]
        idx2 = candidate["record_2"]

        row1 = aed.iloc[idx1]
        row2 = aed.iloc[idx2]

        review_item = {
            "review_id": review_id,

            "record_1": idx1,
            "record_2": idx2,

            "AED_ID_1": clean(
                row1.get("AED_ID")
            ),
            "AED_ID_2": clean(
                row2.get("AED_ID")
            ),

            "building_1": clean(
                row1.get("BUILDING_NAME")
            ),
            "building_2": clean(
                row2.get("BUILDING_NAME")
            ),

            "road_1": clean(
                row1.get("ROAD_NAME")
            ),
            "road_2": clean(
                row2.get("ROAD_NAME")
            ),

            "postal_code_1": clean(
                row1.get("POSTAL_CODE")
            ),
            "postal_code_2": clean(
                row2.get("POSTAL_CODE")
            ),

            "location_description_1": clean(
                row1.get(
                    "AED_LOCATION_DESCRIPTION"
                )
            ),
            "location_description_2": clean(
                row2.get(
                    "AED_LOCATION_DESCRIPTION"
                )
            ),

            "latitude_1": clean(
                row1.get("LATITUDE")
            ),
            "longitude_1": clean(
                row1.get("LONGITUDE")
            ),

            "latitude_2": clean(
                row2.get("LATITUDE")
            ),
            "longitude_2": clean(
                row2.get("LONGITUDE")
            ),

            "rule": candidate.get(
                "rule",
                ""
            ),

            "confidence": candidate.get(
                "confidence",
                ""
            ),

            "distance_meters": candidate.get(
                "distance_meters"
            ),

            "reason": candidate.get(
                "reason",
                ""
            ),

            # Human reviewer fields
            "human_label": "UNREVIEWED",
            "reviewer_note": ""
        }

        review_queue.append(
            review_item
        )

    output = {
        "purpose": (
            "Human-in-the-loop review queue for "
            "possible AED registry duplicate pairs."
        ),

        "important_boundary": (
            "Candidate pairs are not confirmed duplicates. "
            "Human review is required."
        ),

        "total_candidates": len(candidates),

        "review_sample_size": len(review_queue),

        "allowed_human_labels": [
            "DUPLICATE",
            "NOT_DUPLICATE",
            "UNCERTAIN"
        ],

        "review_queue": review_queue
    }

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False
        )

    print("\n=== DUPLICATE HUMAN REVIEW QUEUE ===")

    print(
        f"Candidate pairs available: "
        f"{len(candidates)}"
    )

    print(
        f"Pairs selected for review: "
        f"{len(review_queue)}"
    )

    print(
        "\nAllowed labels:"
    )

    print("DUPLICATE")
    print("NOT_DUPLICATE")
    print("UNCERTAIN")

    print(
        f"\nReview queue saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()
