import json
import math
import re
from difflib import SequenceMatcher

import geopandas as gpd


DATA_PATH = "data/PublicAccessAEDs.geojson"
OUTPUT_PATH = "phase2/duplicate_candidates.json"


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize(value):
    if value is None:
        return ""

    text = str(value).strip().lower()

    if text in {"nan", "none", "null"}:
        return ""

    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = " ".join(text.split())

    return text


def similarity(value1, value2):
    a = normalize(value1)
    b = normalize(value2)

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    return SequenceMatcher(None, a, b).ratio()


def same_nonempty(value1, value2):
    a = normalize(value1)
    b = normalize(value2)

    return bool(a and b and a == b)


# =========================================================
# HOUSE NUMBER EXTRACTION
# =========================================================

def extract_house_number(value):
    text = normalize(value)

    if not text:
        return ""

    match = re.search(r"\b\d+[a-z]?\b", text)

    if match:
        return match.group(0)

    return ""


# =========================================================
# DISTANCE
# =========================================================

def distance_meters(lat1, lon1, lat2, lon2):

    try:
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

    except (TypeError, ValueError):
        return None

    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        return None

    if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        return None

    earth_radius = 6371000

    p1 = math.radians(lat1)
    p2 = math.radians(lat2)

    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)

    a = (
        math.sin(dp / 2) ** 2
        + math.cos(p1)
        * math.cos(p2)
        * math.sin(dl / 2) ** 2
    )

    return 2 * earth_radius * math.asin(math.sqrt(a))


# =========================================================
# BUILD RECORD REPRESENTATION
# =========================================================

def build_record(index, row):

    return {
        "index": int(index),

        "aed_id": normalize(
            row.get("AED_ID")
        ),

        "building": normalize(
            row.get("BUILDING_NAME")
        ),

        "road": normalize(
            row.get("ROAD_NAME")
        ),

        "postal": normalize(
            row.get("POSTAL_CODE")
        ),

        "house_number": extract_house_number(
            row.get("HOUSE_NUMBER")
        ),

        "location": normalize(
            row.get("AED_LOCATION_DESCRIPTION")
        ),

        "floor": normalize(
            row.get("AED_LOCATION_FLOOR_LEVEL")
        ),

        "unit": normalize(
            row.get("UNIT_NUMBER")
        ),

        "lat": row.get("LATITUDE"),

        "lon": row.get("LONGITUDE"),
    }


# =========================================================
# EVIDENCE ANALYSIS
# =========================================================

def analyze_pair(r1, r2):

    evidence = []
    reasons = []

    # -----------------------------------------------------
    # AED ID
    # -----------------------------------------------------

    same_aed_id = (
        r1["aed_id"]
        and r2["aed_id"]
        and r1["aed_id"] == r2["aed_id"]
    )

    different_aed_id = (
        r1["aed_id"]
        and r2["aed_id"]
        and r1["aed_id"] != r2["aed_id"]
    )

    if same_aed_id:

        evidence.append({
            "type": "EXACT_AED_ID",
            "strength": "VERY_STRONG"
        })

        reasons.append(
            "The records contain the same AED ID."
        )

    elif different_aed_id:

        evidence.append({
            "type": "DIFFERENT_AED_ID",
            "strength": "NEGATIVE"
        })

        reasons.append(
            "The records have different AED IDs."
        )


    # -----------------------------------------------------
    # COORDINATES
    # -----------------------------------------------------

    distance = distance_meters(
        r1["lat"],
        r1["lon"],
        r2["lat"],
        r2["lon"]
    )

    if distance is not None:

        if distance <= 1:

            evidence.append({
                "type": "EXACT_COORDINATES",
                "strength": "VERY_STRONG",
                "distance_meters": round(
                    distance,
                    2
                )
            })

            reasons.append(
                "Records have identical or near-identical coordinates."
            )

        elif distance <= 5:

            evidence.append({
                "type": "VERY_CLOSE_COORDINATES",
                "strength": "STRONG",
                "distance_meters": round(
                    distance,
                    2
                )
            })

            reasons.append(
                "Records are located within 5 meters."
            )

        elif distance <= 20:

            evidence.append({
                "type": "CLOSE_COORDINATES",
                "strength": "WEAK",
                "distance_meters": round(
                    distance,
                    2
                )
            })

            reasons.append(
                "Records are located within 20 meters."
            )

        else:

            evidence.append({
                "type": "DISTANT_COORDINATES",
                "strength": "NEGATIVE",
                "distance_meters": round(
                    distance,
                    2
                )
            })

            reasons.append(
                "The coordinates indicate different physical locations."
            )


    # -----------------------------------------------------
    # POSTAL CODE
    # -----------------------------------------------------

    if same_nonempty(
        r1["postal"],
        r2["postal"]
    ):

        evidence.append({
            "type": "POSTAL_CODE_MATCH",
            "strength": "WEAK"
        })

        reasons.append(
            "The records have the same postal code."
        )


    # -----------------------------------------------------
    # BUILDING
    # -----------------------------------------------------

    building_similarity = similarity(
        r1["building"],
        r2["building"]
    )

    same_building = (
        building_similarity == 1.0
    )

    if same_building:

        evidence.append({
            "type": "EXACT_BUILDING_MATCH",
            "strength": "WEAK"
        })

        reasons.append(
            "The building names match exactly."
        )

    elif building_similarity >= 0.85:

        evidence.append({
            "type": "BUILDING_NAME_SIMILARITY",
            "strength": "WEAK",
            "similarity": round(
                building_similarity,
                3
            )
        })

        reasons.append(
            "The building names are highly similar."
        )


    # -----------------------------------------------------
    # ROAD
    # -----------------------------------------------------

    road_similarity = similarity(
        r1["road"],
        r2["road"]
    )

    if road_similarity == 1.0:

        evidence.append({
            "type": "EXACT_ROAD_MATCH",
            "strength": "WEAK"
        })

        reasons.append(
            "The road names match exactly."
        )

    elif road_similarity >= 0.85:

        evidence.append({
            "type": "ROAD_NAME_SIMILARITY",
            "strength": "WEAK",
            "similarity": round(
                road_similarity,
                3
            )
        })

        reasons.append(
            "The road names are highly similar."
        )


    # -----------------------------------------------------
    # HOUSE NUMBER
    # -----------------------------------------------------

    if (
        r1["house_number"]
        and r2["house_number"]
        and r1["house_number"]
        == r2["house_number"]
    ):

        evidence.append({
            "type": "HOUSE_NUMBER_MATCH",
            "strength": "MODERATE"
        })

        reasons.append(
            "The house numbers match."
        )


    # -----------------------------------------------------
    # LOCATION DESCRIPTION
    # -----------------------------------------------------

    location_similarity = similarity(
        r1["location"],
        r2["location"]
    )

    same_location = (
        location_similarity >= 0.90
    )

    if location_similarity == 1.0:

        evidence.append({
            "type": "EXACT_LOCATION_MATCH",
            "strength": "STRONG"
        })

        reasons.append(
            "The location descriptions match exactly."
        )

    elif location_similarity >= 0.90:

        evidence.append({
            "type": "LOCATION_SIMILARITY",
            "strength": "MODERATE",
            "similarity": round(
                location_similarity,
                3
            )
        })

        reasons.append(
            "The location descriptions are highly similar."
        )


    # -----------------------------------------------------
    # FLOOR
    # -----------------------------------------------------

    same_floor = same_nonempty(
        r1["floor"],
        r2["floor"]
    )

    if same_floor:

        evidence.append({
            "type": "FLOOR_MATCH",
            "strength": "WEAK"
        })

        reasons.append(
            "The floor information matches."
        )


    # -----------------------------------------------------
    # UNIT
    # -----------------------------------------------------

    if same_nonempty(
        r1["unit"],
        r2["unit"]
    ):

        evidence.append({
            "type": "UNIT_MATCH",
            "strength": "MODERATE"
        })

        reasons.append(
            "The unit information matches."
        )


    # =====================================================
    # DUPLICATE DECISION LOGIC
    # =====================================================

    # -----------------------------------------------------
    # CASE 1:
    # EXACT SAME AED ID
    # -----------------------------------------------------

    if same_aed_id:

        score = 1.0
        confidence = "HIGH"
        decision = "DUPLICATE"


    # -----------------------------------------------------
    # CASE 2:
    # DIFFERENT IDs + SAME/NEAR COORDINATES
    # + SAME LOCATION
    # -----------------------------------------------------

    elif (
        different_aed_id
        and distance is not None
        and distance <= 1
        and same_location
    ):

        score = 0.95
        confidence = "HIGH"
        decision = "POSSIBLE_DUPLICATE"


    # -----------------------------------------------------
    # CASE 3:
    # DIFFERENT IDs + VERY CLOSE COORDINATES
    # + SAME BUILDING
    # -----------------------------------------------------

    elif (
        different_aed_id
        and distance is not None
        and distance <= 1
        and same_building
    ):

        score = 0.75
        confidence = "HIGH"
        decision = "POSSIBLE_DUPLICATE"


    # -----------------------------------------------------
    # CASE 4:
    # DIFFERENT IDs + WITHIN 5 METERS
    # + SAME LOCATION
    # -----------------------------------------------------

    elif (
        different_aed_id
        and distance is not None
        and distance <= 5
        and same_location
    ):

        score = 0.80
        confidence = "HIGH"
        decision = "POSSIBLE_DUPLICATE"


    # -----------------------------------------------------
    # CASE 5:
    # SAME LOCATION + WITHIN 20 METERS
    # -----------------------------------------------------

    elif (
        different_aed_id
        and distance is not None
        and distance <= 20
        and same_location
    ):

        score = 0.55
        confidence = "MEDIUM"
        decision = "POSSIBLE_DUPLICATE"


    # -----------------------------------------------------
    # CASE 6:
    # DIFFERENT IDs + DIFFERENT LOCATIONS
    # -----------------------------------------------------

    else:

        score = 0.0
        confidence = "LOW"
        decision = "NOT_DUPLICATE"


    # =====================================================
    # CANDIDATE DECISION
    # =====================================================

    meaningful = (
        same_aed_id
        or (
            different_aed_id
            and distance is not None
            and distance <= 5
            and same_location
        )
        or (
            different_aed_id
            and distance is not None
            and distance <= 1
            and same_building
        )
    )


    if not meaningful:

        return None


    # -----------------------------------------------------
    # FINAL REASON
    # -----------------------------------------------------

    if decision == "NOT_DUPLICATE":

        reason = (
            "The records have different AED IDs and "
            "represent different physical locations. "
            "Shared building, road, or postal code "
            "is not sufficient evidence of duplication."
        )

    elif reasons:

        reason = " ".join(reasons)

    else:

        reason = (
            "Records share strong physical or registry "
            "evidence that warrants review."
        )


    # =====================================================
    # RETURN ANALYSIS
    # =====================================================

    return {

        "distance_meters": (
            round(distance, 2)
            if distance is not None
            else None
        ),

        "score": round(
            score,
            3
        ),

        "confidence": confidence,

        "decision": decision,

        "evidence": evidence,

        "reason": reason,
    }


# =========================================================
# MAIN
# =========================================================

def main():

    print(
        "Loading AED dataset..."
    )

    aed = gpd.read_file(
        DATA_PATH
    )

    print(
        f"Records loaded: {len(aed)}"
    )


    # =====================================================
    # BUILD RECORDS
    # =====================================================

    records = []

    for index, row in aed.iterrows():

        records.append(
            build_record(
                index,
                row
            )
        )


    candidates = []


    # =====================================================
    # CANDIDATE BLOCKING
    # =====================================================

    blocks = {}


    for record in records:

        keys = set()


        if record["postal"]:

            keys.add(
                "postal:" +
                record["postal"]
            )


        if record["building"]:

            keys.add(
                "building:" +
                record["building"]
            )


        if record["road"]:

            keys.add(
                "road:" +
                record["road"]
            )


        if record["house_number"]:

            keys.add(
                "house:" +
                record["house_number"]
            )


        if record["aed_id"]:

            keys.add(
                "aedid:" +
                record["aed_id"]
            )


        for key in keys:

            blocks.setdefault(
                key,
                []
            ).append(
                record
            )


    # =====================================================
    # GENERATE BLOCKED PAIRS
    # =====================================================

    candidate_pairs = set()


    for block_records in blocks.values():

        if len(block_records) < 2:
            continue


        for i in range(
            len(block_records)
        ):

            for j in range(
                i + 1,
                len(block_records)
            ):

                idx1 = (
                    block_records[i]["index"]
                )

                idx2 = (
                    block_records[j]["index"]
                )


                if idx1 == idx2:
                    continue


                pair = tuple(
                    sorted(
                        [
                            idx1,
                            idx2
                        ]
                    )
                )


                candidate_pairs.add(
                    pair
                )


    # =====================================================
    # GEOGRAPHICALLY CLOSE RECORDS
    # =====================================================

    for i in range(
        len(records)
    ):

        r1 = records[i]


        for j in range(
            i + 1,
            len(records)
        ):

            r2 = records[j]


            distance = distance_meters(
                r1["lat"],
                r1["lon"],
                r2["lat"],
                r2["lon"]
            )


            if (
                distance is not None
                and distance <= 20
            ):

                candidate_pairs.add(
                    tuple(
                        sorted(
                            [
                                r1["index"],
                                r2["index"]
                            ]
                        )
                    )
                )


    print(
        f"Candidate pairs after blocking: "
        f"{len(candidate_pairs)}"
    )


    # =====================================================
    # ANALYZE PAIRS
    # =====================================================

    for idx1, idx2 in sorted(
        candidate_pairs
    ):

        r1 = records[idx1]
        r2 = records[idx2]


        analysis = analyze_pair(
            r1,
            r2
        )


        if analysis is None:
            continue


        candidates.append({

            "record_1": idx1,

            "record_2": idx2,

            "AED_ID_1": r1["aed_id"],

            "AED_ID_2": r2["aed_id"],

            "rule": (
                "MULTI_ATTRIBUTE_ENTITY_RESOLUTION"
            ),

            "decision": analysis[
                "decision"
            ],

            "confidence": analysis[
                "confidence"
            ],

            "score": analysis[
                "score"
            ],

            "evidence": analysis[
                "evidence"
            ],

            "distance_meters": analysis[
                "distance_meters"
            ],

            "reason": analysis[
                "reason"
            ],
        })


    # =====================================================
    # SORT
    # =====================================================

    candidates.sort(
        key=lambda x: (
            -x["score"],
            x["record_1"],
            x["record_2"]
        )
    )


    # =====================================================
    # OUTPUT
    # =====================================================

    output = {

        "purpose": (
            "Rule-based entity-resolution screening "
            "for possible duplicate AED registry records."
        ),

        "important_boundary": (
            "Candidate pairs are not automatically confirmed "
            "duplicates. Strong evidence is required and "
            "human review may be required."
        ),

        "decision_rules": [

            "Same AED ID = DUPLICATE",

            "Different AED IDs with near-identical "
            "coordinates and same location = POSSIBLE_DUPLICATE",

            "Different AED IDs within 5 meters and "
            "same location = POSSIBLE_DUPLICATE",

            "Same building, road, or postal code alone "
            "does NOT indicate a duplicate",

            "Different coordinates and different "
            "locations = NOT_DUPLICATE"
        ],

        "rules": [

            "EXACT_AED_ID",

            "EXACT_COORDINATES",

            "VERY_CLOSE_COORDINATES",

            "CLOSE_COORDINATES",

            "POSTAL_CODE_MATCH",

            "BUILDING_NAME_SIMILARITY",

            "ROAD_NAME_SIMILARITY",

            "HOUSE_NUMBER_MATCH",

            "LOCATION_SIMILARITY",

            "FLOOR_MATCH",

            "UNIT_MATCH",

            "MULTI_ATTRIBUTE_ENTITY_RESOLUTION"
        ],

        "candidate_pair_count": len(
            candidates
        ),

        "candidate_pairs": candidates
    }


    # =====================================================
    # SAVE
    # =====================================================

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


    # =====================================================
    # SUMMARY
    # =====================================================

    print(
        "\n=== AED GUARDIAN AI ==="
    )

    print(
        "=== ADVANCED DUPLICATE / ENTITY RESOLUTION ==="
    )


    print(
        f"Candidate duplicate pairs: "
        f"{len(candidates)}"
    )


    # =====================================================
    # DECISION DISTRIBUTION
    # =====================================================

    decision_counts = {}


    for candidate in candidates:

        decision = candidate[
            "decision"
        ]


        decision_counts[
            decision
        ] = decision_counts.get(
            decision,
            0
        ) + 1


    print(
        "\nDecision distribution:"
    )


    for decision, count in (
        decision_counts.items()
    ):

        print(
            f"{decision}: {count}"
        )


    # =====================================================
    # CONFIDENCE DISTRIBUTION
    # =====================================================

    confidence_counts = {}


    for candidate in candidates:

        confidence = candidate[
            "confidence"
        ]


        confidence_counts[
            confidence
        ] = confidence_counts.get(
            confidence,
            0
        ) + 1


    print(
        "\nConfidence distribution:"
    )


    for confidence, count in (
        confidence_counts.items()
    ):

        print(
            f"{confidence}: {count}"
        )


    # =====================================================
    # EVIDENCE DISTRIBUTION
    # =====================================================

    evidence_counts = {}


    for candidate in candidates:

        for evidence in candidate[
            "evidence"
        ]:

            evidence_type = evidence[
                "type"
            ]


            evidence_counts[
                evidence_type
            ] = evidence_counts.get(
                evidence_type,
                0
            ) + 1


    print(
        "\nEvidence distribution:"
    )


    for evidence_type, count in (
        evidence_counts.items()
    ):

        print(
            f"{evidence_type}: {count}"
        )


    print(
        f"\nResults saved to: "
        f"{OUTPUT_PATH}"
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    main()