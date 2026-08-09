import json
import re
import geopandas as gpd

DATA_PATH = "data/PublicAccessAEDs.geojson"
OUTPUT_PATH = "phase2/indoor_location_ambiguity_report.json"


def clean(value):
    if value is None:
        return ""

    text = str(value).strip()

    if text.lower() in {"nan", "none", "null"}:
        return ""

    return text


def has_floor(value):
    text = clean(value).lower()

    if not text:
        return False

    floor_patterns = [
        r"\bfloor\b",
        r"\blvl\b",
        r"\blevel\b",
        r"\bstorey\b",
        r"\bst\b",
        r"\bground\b",
        r"\bbasement\b",
        r"\bmezzanine\b",
    ]

    return any(
        re.search(pattern, text)
        for pattern in floor_patterns
    )


def has_unit(value):
    text = clean(value).lower()

    if not text:
        return False

    return bool(
        re.search(
            r"\b(unit|#|suite|shop|room)\b",
            text
        )
    )


def analyze_location(row):
    building = clean(row.get("BUILDING_NAME"))
    floor = clean(row.get("AED_LOCATION_FLOOR_LEVEL"))
    unit = clean(row.get("UNIT_NUMBER"))
    description = clean(row.get("AED_LOCATION_DESCRIPTION"))
    road = clean(row.get("ROAD_NAME"))
    house = clean(row.get("HOUSE_NUMBER"))

    concerns = []

    # ---------------------------------------------------------
    # Building information
    # ---------------------------------------------------------

    if not building:
        concerns.append("MISSING_BUILDING")

    # ---------------------------------------------------------
    # Floor information
    # ---------------------------------------------------------

    if not floor:
        if description and has_floor(description):
            floor_status = "INFERRED_FROM_DESCRIPTION"
        else:
            floor_status = "MISSING"
            concerns.append("MISSING_FLOOR")
    else:
        floor_status = "PRESENT"

    # ---------------------------------------------------------
    # Unit information
    # ---------------------------------------------------------

    if unit:
        unit_status = "PRESENT"
    elif description and has_unit(description):
        unit_status = "INFERRED_FROM_DESCRIPTION"
    else:
        unit_status = "MISSING"

    # ---------------------------------------------------------
    # Location description
    # ---------------------------------------------------------

    if not description:
        concerns.append("MISSING_LOCATION_DESCRIPTION")
        description_status = "MISSING"

    elif len(description) < 8:
        concerns.append("VERY_SHORT_LOCATION_DESCRIPTION")
        description_status = "VAGUE"

    else:
        description_status = "PRESENT"

    # ---------------------------------------------------------
    # Address context
    # ---------------------------------------------------------

    if not road:
        concerns.append("MISSING_ROAD")

    if not house:
        concerns.append("MISSING_HOUSE_NUMBER")

    # ---------------------------------------------------------
    # Ambiguity classification
    # ---------------------------------------------------------

    if (
        "MISSING_LOCATION_DESCRIPTION" in concerns
        or "MISSING_BUILDING" in concerns
    ):
        status = "HIGH_AMBIGUITY"
        confidence = "HIGH"

    elif (
        "MISSING_FLOOR" in concerns
        or "VERY_SHORT_LOCATION_DESCRIPTION" in concerns
    ):
        status = "MEDIUM_AMBIGUITY"
        confidence = "MEDIUM"

    elif concerns:
        status = "LOW_AMBIGUITY"
        confidence = "MEDIUM"

    else:
        status = "SUFFICIENT_LOCATION_DETAIL"
        confidence = "HIGH"

    if concerns:
        reason = (
            "Registry location information contains "
            "one or more fields requiring human review."
        )
    else:
        reason = (
            "Available registry fields provide sufficient "
            "location detail for this quality check."
        )

    return {
        "status": status,
        "confidence": confidence,
        "building_status": (
            "PRESENT" if building else "MISSING"
        ),
        "floor_status": floor_status,
        "unit_status": unit_status,
        "description_status": description_status,
        "concerns": concerns,
        "reason": reason,
    }


def main():

    print("Loading AED dataset...")

    aed = gpd.read_file(DATA_PATH)

    print(f"Records loaded: {len(aed)}")

    results = []

    for index, row in aed.iterrows():

        result = analyze_location(row)

        result["record_index"] = int(index)

        result["AED_ID"] = clean(
            row.get("AED_ID")
        )

        results.append(result)

    status_counts = {}

    confidence_counts = {}

    concern_counts = {}

    for result in results:

        status = result["status"]

        status_counts[status] = (
            status_counts.get(status, 0) + 1
        )

        confidence = result["confidence"]

        confidence_counts[confidence] = (
            confidence_counts.get(confidence, 0) + 1
        )

        for concern in result["concerns"]:

            concern_counts[concern] = (
                concern_counts.get(concern, 0) + 1
            )

    ambiguous_records = [
        result
        for result in results
        if result["status"] != "SUFFICIENT_LOCATION_DETAIL"
    ]

    output = {

        "purpose": (
            "Registry-quality screening for ambiguous "
            "or incomplete AED location information."
        ),

        "important_boundary": (
            "This analysis evaluates registry information "
            "quality only. It does not determine AED "
            "accessibility, availability, operational status, "
            "or emergency readiness."
        ),

        "total_records": len(results),

        "ambiguous_records": len(
            ambiguous_records
        ),

        "status_distribution": status_counts,

        "confidence_distribution": confidence_counts,

        "concern_distribution": concern_counts,

        "records": results,
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

    print("\n=== INDOOR LOCATION AMBIGUITY ANALYSIS ===")

    print("\nStatus distribution:")

    for status, count in status_counts.items():
        print(f"{status}: {count}")

    print("\nConfidence distribution:")

    for confidence, count in confidence_counts.items():
        print(f"{confidence}: {count}")

    print("\nConcern distribution:")

    for concern, count in concern_counts.items():
        print(f"{concern}: {count}")

    print(
        f"\nAmbiguous/incomplete records: "
        f"{len(ambiguous_records)}"
    )

    print(
        f"\nResults saved to: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    main()