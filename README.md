# 🛡️ AED Guardian AI

## Lane 3 — Registry Quality & Human-in-the-Loop Decision Support

AED Guardian AI is an explainable registry-quality decision-support prototype designed to identify **possible data-quality concerns in AED registry records** and prioritize them for human review.

The prototype focuses on:

* Possible duplicate AED records
* Shared coordinates between different AED IDs
* Ambiguous or incomplete operating-hours information
* Explainable detection rules
* Confidence-based prioritization
* Human-in-the-loop review
* Reproducible evaluation using a frozen dataset

> **⚠️ SAFETY BOUNDARY**
>
> AED Guardian AI is a **planning, simulation, research, and registry-quality prototype.**
>
> **NOT FOR EMERGENCY USE.**
>
> It does not determine whether an AED is currently available, accessible, operational, inspected, maintained, or ready for emergency use.
>
> A data-quality flag is a concern requiring review, **not proof of a real-world fault.**

---

# 1. Lane 3 Objective

Lane 3 focuses on **Registry and Readiness** from a registry-quality and human-review perspective.

The system is designed to help identify records that may require:

* Correction
* Clarification
* Duplicate verification
* Operating-hours verification
* Human field verification

The system does **not** automatically modify the source registry.

---

# 2. Dataset

## Public Access AEDs

**Dataset name:** Public Access AEDs

**Publisher:** Singapore Civil Defence Force (SCDF)

**Source platform:** data.gov.sg

**Dataset ID:** `d_4e6b82c58a8a832f6f1fee5dfa6d47ea`

**Dataset date:** February 2020

**Dataset type:** Historical public AED registry snapshot

**Frozen local file:**

```text
data/PublicAccessAEDs.geojson
```

**Records:** 9,644

**Live data:** No

**Live device-health information:** Not provided

### Official Source

Official dataset page:

https://data.gov.sg/datasets/d_4e6b82c58a8a832f6f1fee5dfa6d47ea/view

### Licence

The dataset is provided under the **Open Data Licence**, with the source page stating that it is free forever for personal or commercial use.

The exact licence wording should be retained according to the event-provided dataset/source page used for submission.

---

# 3. Frozen Dataset Integrity

The judged workflow uses the locally frozen dataset rather than live API data.

### SHA-256

```text
E2EF793FFD0FD2DBE99FFDCFB21B38154C81FD0685D1F0FCC5B75A6D57205C02
```

The checksum identifies the exact frozen input used by the judged workflow.

### Verification

Run:

```powershell
Get-FileHash .\data\PublicAccessAEDs.geojson -Algorithm SHA256
```

Expected SHA-256:

```text
E2EF793FFD0FD2DBE99FFDCFB21B38154C81FD0685D1F0FCC5B75A6D57205C02
```

No live API data is used during the judged demonstration.

---

# 4. Important Data Limitations

The supplied dataset does **not** establish:

* Current AED presence
* Current AED accessibility
* Current AED operational readiness
* Battery state
* Pad expiry
* Inspection status
* Maintenance history
* Temporary closures
* Live access restrictions
* Emergency incidents
* Responder locations

Therefore, AED Guardian AI must not claim that an AED is currently available, working, accessible, inspected, or ready for use based only on this dataset.

The dataset is treated strictly as a **historical registry snapshot**.

---

# 5. Data Integrity Boundary

The system treats the supplied dataset as a historical registry snapshot.

A data-quality flag is a **concern requiring review**, not proof of a real-world fault.

The prototype therefore distinguishes between:

```text
Registry-quality concern
        ↓
Candidate case
        ↓
Human review
        ↓
Human decision
```

The system does not convert a data-quality signal into a claim about the physical AED.

---

# 6. Registry-Quality Processing

The prototype uses deterministic and explainable processing.

The workflow includes:

1. Loading the frozen GeoJSON dataset.
2. Reading AED identity, address, location, coordinate, and operating-hours fields.
3. Classifying operating-hours text into structured review categories.
4. Generating candidate duplicate pairs.
5. Applying explainable duplicate-detection rules.
6. Assigning confidence levels.
7. Creating a human review queue.
8. Recording human decisions.
9. Generating evaluation and audit artifacts.

No live registry service is required during the judged workflow.

---

# 7. Fields Used

The prototype may use the following published fields:

```text
OBJECTID
AED_ID
OPERATING_HOURS
HOUSE_NUMBER
ROAD_NAME
BUILDING_NAME
UNIT_NUMBER
POSTAL_CODE
AED_LOCATION_DESCRIPTION
AED_LOCATION_FLOOR_LEVEL
LATITUDE
LONGITUDE
XVAL
YVAL
```

Fields such as `INC_CRC` and `FMEL_UPD_D` are not assigned operational meaning without an authoritative data dictionary.

---

# 8. Duplicate Detection

The duplicate workflow generates candidate pairs using deterministic registry-quality rules.

Examples include:

```text
EXACT_COORDINATES
```

and other explainable matching conditions.

A candidate pair is **not automatically considered a duplicate**.

Every candidate case is sent to human review.

### Human Review Labels

```text
DUPLICATE
NOT_DUPLICATE
UNCERTAIN
```

---

# 9. Human Review Results

The final duplicate review sample contains:

```text
Candidate pairs reviewed : 100

DUPLICATE                : 24
NOT_DUPLICATE            : 62
UNCERTAIN                : 14
UNREVIEWED               : 0
```

### Review Coverage

```text
100 / 100 candidate pairs reviewed
```

### Abstention Rate

```text
14%
```

The `UNCERTAIN` category represents cases where the available registry evidence was insufficient for a confident human decision.

This is an intentional human-review outcome rather than an error condition.

---

# 10. Operating-Hours Evaluation

The prototype includes a scripted evaluation of operating-hours classification.

```text
Test cases : 10
Correct    : 10
Incorrect  : 0
Accuracy   : 100%
```

This result represents performance on the defined scripted test cases.

It must **not** be interpreted as real-world validated national registry performance.

---

# 11. Human-in-the-Loop Review Interface

The project includes a local browser-based review application.

Start the application with:

```powershell
python .\phase2\review_app.py
```

The application runs at:

```text
http://localhost:8000
```

The interface presents:

* AED Record 1
* AED Record 2
* AED IDs
* Building information
* Road information
* Postal codes
* Location descriptions
* Coordinates
* Detection rule
* Confidence
* Reason for review
* Human review actions

### Review Actions

The reviewer can classify a candidate pair as:

```text
DUPLICATE
NOT DUPLICATE
UNCERTAIN
```

The interface clearly states:

```text
Planning / simulation only.
Candidate pairs are NOT confirmed duplicates.
Do not infer current AED availability, accessibility, or operational readiness.
```

---

# 12. Safety Notice

The review application displays the following safety boundary:

```text
WARNING: Prototype for planning and simulation only - NOT FOR EMERGENCY USE.

In an emergency in Singapore, call 995 immediately and follow SCDF instructions.
Use official SCDF/myResponder channels.
Do not delay emergency action to use this prototype.
```

The application also reinforces that candidate duplicate records are not confirmed duplicates and that registry information must not be interpreted as current AED readiness.

---

# 13. Evaluation Artifacts

The project contains the following important evaluation artifacts:

```text
phase2/final_duplicate_review_report.json
phase2/phase2_operating_hours_evaluation.json
phase2/lane3_baseline_evaluation_report.json
phase2/lane3_method_card.json
```

Documentation:

```text
docs/DATA_MANIFEST.md
docs/METHOD_CARD.md
docs/EVALUATION_REPORT.md
docs/SAFETY_COMPLIANCE.md
```

---

# 14. Final Compliance Audit

The Lane 3 audit verifies the required project package.

### Required Files

```text
Existing required files : 12/12
Missing required files  : 0
```

### Duplicate Review

```text
Candidate pairs reviewed : 100
DUPLICATE                : 24
NOT_DUPLICATE            : 62
UNCERTAIN                : 14
UNREVIEWED               : 0
Abstention rate          : 0.14
```

### Operating-Hours Evaluation

```text
Test cases : 10
Correct    : 10
Incorrect  : 0
Accuracy   : 1.0
```

### Audit Status

```text
STATUS: CORE LANE 3 PACKAGE PRESENT
```

---

# 15. Reproducibility

The judged workflow is based on a frozen dataset.

The important reproducibility components are:

```text
Frozen input:
data/PublicAccessAEDs.geojson

Duplicate review queue:
phase2/duplicate_review_queue.json

Review application:
phase2/review_app.py

Documentation:
docs/
```

### Dataset Hash

```text
E2EF793FFD0FD2DBE99FFDCFB21B38154C81FD0685D1F0FCC5B75A6D57205C02
```

### Audit Command

From the project root:

```powershell
python .\phase2\final_lane3_audit.py
```

The audit should confirm:

```text
Existing required files : 12/12
Missing required files  : 0
100/100 candidate pairs reviewed
10/10 scripted operating-hours cases correct
```

---

# 16. Project Structure

```text
AED-Guardian-AI/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── PublicAccessAEDs.geojson
│
├── docs/
│   ├── DATA_MANIFEST.md
│   ├── METHOD_CARD.md
│   ├── EVALUATION_REPORT.md
│   └── SAFETY_COMPLIANCE.md
│
└── phase2/
    ├── review_app.py
    ├── duplicate_detection.py
    ├── duplicate_review_queue.py
    ├── duplicate_review_queue.json
    ├── final_duplicate_review_report.json
    ├── phase2_operating_hours_evaluation.json
    ├── lane3_baseline_evaluation_report.json
    ├── lane3_method_card.json
    └── final_lane3_audit.py
```

---

# 17. What AED Guardian AI Does

AED Guardian AI provides:

* Registry-quality analysis
* Explainable duplicate detection
* Operating-hours classification
* Candidate prioritization
* Human review workflow
* Confidence information
* Review evidence
* Reproducible evaluation
* Safety-aware decision support

---

# 18. What AED Guardian AI Does NOT Do

AED Guardian AI does **not**:

* Confirm that an AED physically exists today
* Confirm that an AED is accessible
* Confirm that an AED is operational
* Check battery condition
* Check pad expiry
* Verify maintenance
* Verify inspection status
* Provide emergency dispatch
* Locate emergency responders
* Replace official SCDF systems
* Provide individualized medical advice
* Automatically modify the original registry

---

# 19. Final Safety Statement

AED Guardian AI is a **registry-quality and human-review prototype**.

Its outputs are intended to identify records that may deserve further investigation.

They are **not emergency instructions and not proof of real-world AED status**.

For real emergencies in Singapore, users should rely on official emergency services and official SCDF channels rather than this prototype.

---

# 20. Final Project Status

```text
AED Guardian AI
Lane 3 — Registry Quality & Human-in-the-Loop Decision Support

Required files       : 12/12
Missing files        : 0

Duplicate reviews    : 100/100
Duplicate            : 24
Not duplicate        : 62
Uncertain            : 14

Operating-hours      : 10/10 correct

Frozen dataset       : Verified
SHA-256              : Verified
Safety notice        : Present
Human review         : Present
Reproducibility      : Documented

CORE LANE 3 PACKAGE PRESENT
```

**Generated: August 2026**
