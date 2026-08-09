# AED Guardian AI — Method Card

## Lane

Lane 3 — Registry and readiness

## Intended User

Human AED registry and data-quality reviewer.

## Decision Supported

The prototype helps a reviewer identify AED registry records that may require:

- Correction
- Clarification
- Field verification
- Duplicate investigation
- Operating-hours review

The system provides decision support only. Final decisions remain with a human reviewer.

## Problem Definition

The supplied AED registry is a historical snapshot. Registry records may contain
possible duplicates, ambiguous operating-hours text, missing information, or
conflicting/unclear location information.

The prototype identifies such cases and explains why they were flagged.

A flag represents a data-quality concern. It does not prove a real-world fault.

---

# System Architecture

## Stage 1 — Dataset Input

The frozen GeoJSON dataset is loaded from:

`data/PublicAccessAEDs.geojson`

The judged workflow does not depend on a live registry API.

## Stage 2 — Registry Field Processing

Relevant fields include:

- AED_ID
- OPERATING_HOURS
- HOUSE_NUMBER
- ROAD_NAME
- BUILDING_NAME
- UNIT_NUMBER
- POSTAL_CODE
- AED_LOCATION_DESCRIPTION
- AED_LOCATION_FLOOR_LEVEL
- LATITUDE
- LONGITUDE
- XVAL
- YVAL

Internal fields whose meaning is not documented by an authoritative data
dictionary are not assigned unsupported operational meaning.

## Stage 3 — Operating-Hours Analysis

Operating-hours text is processed using deterministic parsing and validation
rules.

The system can classify values as:

- `PARSED`
- `PARSED_WITH_REMARKS`
- `MISSING`
- `AMBIGUOUS`

Confidence levels:

- HIGH
- MEDIUM
- LOW

Examples:

- Standard schedules can be parsed with HIGH confidence.
- Schedules containing additional remarks may receive MEDIUM confidence.
- Missing values receive LOW confidence.
- Unusual or difficult-to-interpret text can be marked AMBIGUOUS.

Ambiguous cases can be surfaced for human review.

## Stage 4 — Duplicate Candidate Detection

Candidate pairs are generated using deterministic, explainable rules.

One important rule is:

`EXACT_COORDINATES`

This rule identifies records with identical latitude and longitude but different
AED IDs.

Example:

Two records may share the same coordinates while describing different indoor
locations such as different floors or service areas.

Therefore:

**Identical coordinates do not automatically mean duplicate.**

The system sends such candidates to human review rather than automatically
deleting or merging records.

## Stage 5 — Confidence and Explanation

Each flag includes:

- Detection rule
- Confidence level
- Human-readable reason
- Relevant record fields

Confidence is interpreted as follows:

### HIGH

Strong deterministic evidence exists for the flag, but human verification may
still be required.

### MEDIUM

The evidence is suggestive but requires interpretation.

### LOW

Information is missing or insufficient for a reliable automated conclusion.

Confidence does not represent proof of a real-world device fault.

## Stage 6 — Human-in-the-Loop Review

The reviewer receives candidate pairs through the review interface.

Available decisions:

- `DUPLICATE`
- `NOT_DUPLICATE`
- `UNCERTAIN`

The `UNCERTAIN` option prevents the system from forcing a binary decision when
available evidence is insufficient.

Human decisions are retained as review records for evaluation.

---

# Human Approval Points

Human approval is required for duplicate candidate decisions.

The reviewer determines whether:

1. Two records represent the same registry entry.
2. Two records are legitimate separate AED placements.
3. Available evidence is insufficient, resulting in `UNCERTAIN`.

The system does not automatically remove records based on duplicate detection.

---

# Evaluation

## Operating-Hours Evaluation

Scripted test cases:

- Total: 10
- Correct: 10
- Incorrect: 0
- Accuracy: 100%

This is a scripted evaluation and not independently validated real-world
performance.

## Duplicate Human Review

Candidate pairs:

- Total: 100
- Reviewed: 100
- DUPLICATE: 24
- NOT_DUPLICATE: 62
- UNCERTAIN: 14
- UNREVIEWED: 0
- Abstention rate: 14%

The duplicate review labels are human-review outcomes and are not treated as
independent ground truth. Therefore precision, recall, and F1 are not claimed
from these labels alone.

---

# Baseline

Baseline approach:

**Deterministic validation rules plus unranked human review.**

The baseline is transparent and reproducible.

The prototype improves the review workflow by:

- Generating candidate cases
- Providing explainable reasons
- Assigning confidence
- Providing structured human decisions
- Recording uncertainty explicitly

---

# Assumptions

1. The supplied dataset is a historical registry snapshot.
2. Coordinates represent registry-record locations and may not uniquely identify
   an individual AED.
3. Multiple AED records may legitimately exist at different floors or indoor
   locations.
4. Operating-hours text describes registry information and is not proof of
   current access.
5. Missing information should not be converted into unsupported claims.
6. Human reviewers remain responsible for final registry decisions.

---

# Known Failure Modes

The system may require human review when:

- Multiple AEDs legitimately share coordinates.
- Indoor locations differ while coordinates remain identical.
- Operating-hours text contains unusual wording.
- Operating-hours values are missing.
- Address fields are incomplete.
- Registry information is insufficient to distinguish two records.
- Historical information does not establish current real-world status.

---

# Safety Boundary

The prototype does NOT claim to detect:

- Depleted batteries
- Expired pads
- Failed inspections
- Maintenance failures
- Physical AED removal
- Current device readiness
- Current accessibility

The system does not use:

- Live emergency incidents
- Responder dispatch
- Patient records
- Private responder information
- Live SCDF emergency integrations

The prototype is for planning, registry-quality analysis, and simulation only.

A registry-quality flag is not proof that an AED is currently unavailable or
faulty.

---

# Reproducibility

Frozen dataset:

`data/PublicAccessAEDs.geojson`

Important implementation directory:

`phase2/`

Review interface:

`phase2/review_app.py`

Evaluation report:

`phase2/lane3_baseline_evaluation_report.json`

Duplicate review report:

`phase2/final_duplicate_review_report.json`

Data manifest:

`docs/DATA_MANIFEST.md`

---

# Summary

AED Guardian AI uses explainable registry-quality rules, operating-hours
validation, duplicate candidate detection, confidence scoring, and
human-in-the-loop review to help maintain a cleaner AED registry.

The prototype deliberately distinguishes:

**Data-quality concern ≠ confirmed real-world fault**

and

**Historical registry record ≠ current AED readiness.**

Generated: August 2026
