import re
import json
import geopandas as gpd

DATA_PATH = "data/PublicAccessAEDs.geojson"


def parse_operating_hours(value):
    """
    Parse AED registry operating-hours text into a structured,
    explainable representation.

    This parser evaluates registry text quality only.
    It does NOT determine current AED accessibility or readiness.
    """

    if value is None:
        return {
            "status": "MISSING",
            "confidence": "LOW",
            "schedule": {},
            "reason": "Operating-hours value is missing."
        }

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "null"}:
        return {
            "status": "MISSING",
            "confidence": "LOW",
            "schedule": {},
            "reason": "Operating-hours value is missing."
        }

    schedule = {}
    ambiguous = False
    remarks_found = False

    parts = re.split(
        r"\bRemarks\s*:",
        text,
        maxsplit=1,
        flags=re.IGNORECASE
    )

    main_part = parts[0].strip()

    if len(parts) > 1:
        remarks_found = True
        remarks = parts[1].strip()
    else:
        remarks = ""

    entries = [
        x.strip()
        for x in main_part.split(";")
        if x.strip()
    ]

    time_pattern = r"(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})"

    for entry in entries:

        closed_match = re.match(
            r"(.+?)\s+Closed$",
            entry,
            flags=re.IGNORECASE
        )

        if closed_match:
            days = closed_match.group(1).strip()
            schedule[days] = "CLOSED"
            continue

        time_match = re.search(time_pattern, entry)

        if time_match:
            start = time_match.group(1)
            end = time_match.group(2)

            day_text = entry[:time_match.start()].strip()

            schedule[day_text] = {
                "open": start,
                "close": end
            }

            continue

        if re.search(r"\b(am|pm)\b", entry, re.IGNORECASE):
            ambiguous = True
            continue

        ambiguous = True

    if remarks:
        if not re.search(
            r"\b(mon|tue|wed|thu|fri|sat|sun)\b",
            remarks,
            re.IGNORECASE
        ):
            ambiguous = True

    if ambiguous:
        status = "AMBIGUOUS"
        confidence = "MEDIUM"
        reason = (
            "Operating-hours text contains a pattern "
            "requiring additional interpretation."
        )

    elif remarks_found:
        status = "PARSED_WITH_REMARKS"
        confidence = "MEDIUM"
        reason = (
            "Base schedule parsed, but additional remarks "
            "may modify the schedule."
        )

    elif schedule:
        status = "PARSED"
        confidence = "HIGH"
        reason = "Operating-hours pattern successfully parsed."

    else:
        status = "UNPARSED"
        confidence = "LOW"
        reason = "Operating-hours pattern could not be reliably parsed."

    return {
        "status": status,
        "confidence": confidence,
        "schedule": schedule,
        "reason": reason
    }


def main():

    print("Loading dataset...")

    aed = gpd.read_file(DATA_PATH)

    print(f"Records loaded: {len(aed)}")

    results = []

    for value in aed["OPERATING_HOURS"]:
        results.append(parse_operating_hours(value))

    aed["OH_STATUS"] = [
        r["status"] for r in results
    ]

    aed["OH_CONFIDENCE"] = [
        r["confidence"] for r in results
    ]

    aed["OH_REASON"] = [
        r["reason"] for r in results
    ]

    print("\n=== OPERATING HOURS ANALYSIS ===")

    print("\nStatus distribution:")
    print(aed["OH_STATUS"].value_counts(dropna=False))

    print("\nConfidence distribution:")
    print(aed["OH_CONFIDENCE"].value_counts(dropna=False))

    print("\nSample results:")

    for i, result in enumerate(results[:10]):
        print(f"\nRecord {i + 1}")
        print(json.dumps(result, indent=2))

    print("\nPhase 2 operating-hours analysis completed.")


if __name__ == "__main__":
    main()
