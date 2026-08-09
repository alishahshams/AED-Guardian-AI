# AED Guardian AI — Data Manifest

## Dataset

- Dataset name: Public Access AEDs
- Frozen input file: `data/PublicAccessAEDs.geojson`
- Publisher: Singapore Civil Defence Force (SCDF)
- Source platform: data.gov.sg
- Dataset type: Historical public AED registry snapshot
- Dataset date: February 2020
- Retrieval/use date: August 2026
- Live data: No
- Live device-health information: Not provided

## Purpose

The dataset is used to develop and evaluate a registry-quality decision-support
prototype for Lane 3 — Registry and readiness.

The prototype identifies records that may require correction, clarification,
or human field verification.

## Fields Used

The prototype may use the following published fields:

- OBJECTID
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

Fields such as `INC_CRC` and `FMEL_UPD_D` are not assigned operational meaning
without an authoritative data dictionary.

## Transformations

The prototype performs registry-quality processing including:

1. Loading the frozen GeoJSON dataset.
2. Reading AED identity, address, indoor-location, coordinate, and
   operating-hours fields.
3. Classifying operating-hours text into structured review categories.
4. Generating candidate duplicate pairs using deterministic matching rules.
5. Assigning explainable detection rules and confidence levels.
6. Sending candidate cases to a human review queue.
7. Recording human decisions as DUPLICATE, NOT_DUPLICATE, or UNCERTAIN.

No live registry service is used during the judged workflow.

## Duplicate Review Data

Generated review artifacts include:

- `phase2/duplicate_candidates.json`
- `phase2/duplicate_review_queue.json`
- `phase2/duplicate_review_report.csv`
- `phase2/final_duplicate_review_report.json`

The final human review covered 100 candidate pairs.

Results:

- DUPLICATE: 24
- NOT_DUPLICATE: 62
- UNCERTAIN: 14
- UNREVIEWED: 0
- Abstention rate: 14%

## Operating-Hours Evaluation

The scripted evaluation contains 10 test cases.

- Correct: 10
- Incorrect: 0
- Scripted accuracy: 100%

This is a scripted test-case result and must not be interpreted as
real-world validated national registry performance.

## Reproducibility

The frozen registry input is stored locally at:

`data/PublicAccessAEDs.geojson`

Important generated Phase 2 artifacts are stored under:

`phase2/`

Documentation is stored under:

`docs/`

The prototype should be evaluated using the frozen dataset rather than a
live API so that judged results remain reproducible.

## Licensing and Source Verification

Source: data.gov.sg / Singapore Civil Defence Force public AED dataset.

The exact source URL and licence wording should be verified against the
event-provided dataset/source page before final submission.

## Important Data Limitations

The supplied dataset does NOT establish:

- Current AED presence
- Current AED accessibility
- Current AED operational readiness
- Battery state
- Pad expiry
- Inspection status
- Maintenance history
- Temporary closures
- Live access restrictions
- Emergency incidents
- Responder locations

Therefore, the prototype must not claim that an AED is currently available,
working, accessible, inspected, or ready for use based only on this dataset.

## Data Integrity Boundary

The system treats the supplied dataset as a historical registry snapshot.
A data-quality flag is a concern requiring review, not proof of a real-world
fault.

Generated: August 2026

## Verified Source Information

- Official source URL: https://data.gov.sg/datasets/d_4e6b82c58a8a832f6f1fee5dfa6d47ea/view
- Dataset ID: d_4e6b82c58a8a832f6f1fee5dfa6d47ea
- Publisher: Singapore Civil Defence Force (SCDF)
- Dataset data date: February 2020
- Official licence: Free forever for personal or commercial use, under the Open Data Licence.
- Frozen local file: data/PublicAccessAEDs.geojson
- SHA-256: E2EF793FFD0FD2DBE99FFDCFB21B38154C81FD0685D1F0FCC5B75A6D57205C02

The SHA-256 checksum identifies the exact frozen input used for the judged workflow.
No live API data is used during the judged demonstration.
