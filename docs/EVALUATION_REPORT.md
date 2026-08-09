# AED Guardian AI — Evaluation Report

## Lane

Lane 3 — Registry and readiness

## Evaluation Objective

The evaluation measures whether the prototype can:

1. Identify registry-quality concerns.
2. Parse common operating-hours patterns.
3. Surface potential duplicate records for human review.
4. Handle uncertainty without forcing unsupported binary decisions.
5. Provide an explainable and reproducible review workflow.

---

# 1. Operating-Hours Evaluation

## Test Design

A scripted evaluation set containing 10 representative operating-hours cases
was used.

The cases include:

- 24-hour schedule
- Standard weekday schedule
- Weekend closed
- Schedule with remarks
- Missing value
- Empty value
- Null value
- Unusual text
- AM/PM format
- Mixed schedule

## Results

| Metric | Result |
|---|---:|
| Total cases | 10 |
| Correct | 10 |
| Incorrect | 0 |
| Accuracy | 100% |

All 10 scripted cases were classified according to their expected labels.

### Classification results

- `PARSED`: correctly identified for standard and mixed schedules.
- `PARSED_WITH_REMARKS`: correctly identified when additional remarks were present.
- `MISSING`: correctly identified for missing, empty, and null values.
- `AMBIGUOUS`: correctly identified for unusual or difficult-to-interpret formats.

### Interpretation

The prototype achieved 100% accuracy on this scripted evaluation set.

This result demonstrates correct behavior on the defined test cases. It is NOT
claimed as independently validated real-world operating-hours extraction
accuracy for the complete AED registry.

---

# 2. Duplicate Candidate Human Review

## Test Design

The duplicate detection component generated 100 candidate record pairs.

Every candidate pair was presented to a human reviewer.

The reviewer could select:

- `DUPLICATE`
- `NOT_DUPLICATE`
- `UNCERTAIN`

## Results

| Metric | Result |
|---|---:|
| Total candidate pairs | 100 |
| Reviewed pairs | 100 |
| Unreviewed pairs | 0 |
| DUPLICATE | 24 |
| NOT_DUPLICATE | 62 |
| UNCERTAIN | 14 |
| Abstention rate | 14% |

## Review Coverage

All candidate pairs were reviewed:

`100 / 100 = 100% review coverage`

No candidate pair remained unreviewed.

## Uncertainty Handling

14 cases were marked `UNCERTAIN`.

This is intentional.

The system does not force a binary decision when the available registry
evidence is insufficient.

This is particularly important for records that share coordinates but have
different indoor descriptions or floor levels.

---

# 3. Duplicate Review Interpretation

The human-review labels are treated as review outcomes rather than an
independent ground-truth dataset.

Therefore this report does NOT claim:

- Duplicate precision
- Duplicate recall
- Duplicate F1

from the 100 reviewed pairs alone.

Independent ground truth would be required to make those claims valid.

The review demonstrates:

- Candidate generation
- Explainability
- Human review coverage
- Explicit uncertainty handling
- Auditability

---

# 4. Baseline

## Baseline Method

The baseline is:

**Deterministic validation rules with unranked human review.**

The baseline uses transparent rules to surface possible data-quality concerns
without automatically asserting that a record is faulty.

## Prototype Contribution

The prototype adds:

- Structured candidate generation
- Detection-rule labels
- Confidence levels
- Human-readable reasons
- Human-in-the-loop decisions
- Explicit `UNCERTAIN` handling
- Review-result persistence

---

# 5. Primary and Secondary Metrics

## Primary Metric

**Human review coverage**

Result:

`100%`

All generated candidate pairs were reviewed.

## Effectiveness Metric

**Scripted operating-hours classification accuracy**

Result:

`100% (10/10)`

## Safety/Error Metric

**Duplicate-review abstention rate**

Result:

`14%`

The system allowed reviewers to abstain when evidence was insufficient.

## Usability/Workflow Metric

**Review completion coverage**

Result:

`100% (100/100 candidate pairs reviewed)`

---

# 6. Failure and Uncertainty Cases

Observed or expected difficult cases include:

1. Multiple records with identical coordinates.
2. Different indoor floor descriptions at identical coordinates.
3. Different indoor service-area descriptions at identical coordinates.
4. Missing operating-hours values.
5. Unusual operating-hours wording.
6. AM/PM or non-standard schedule formats.
7. Historical registry information that cannot establish current availability.

These cases are intentionally surfaced rather than converted into unsupported
claims.

---

# 7. Safety Interpretation

The dataset is historical.

The evaluation does NOT demonstrate:

- Current AED availability
- Current AED accessibility
- Current AED readiness
- Battery status
- Pad expiry
- Inspection status
- Maintenance status

The prototype must therefore be presented as a registry-quality decision-support
tool rather than a live AED readiness system.

---

# 8. Evaluation Limitations

The evaluation has several limitations:

- The operating-hours evaluation contains only 10 scripted cases.
- The duplicate review contains human-review outcomes rather than independent
  ground truth.
- Real-world registry corrections have not been independently verified.
- The historical dataset does not provide live device status.
- Duplicate and anomaly performance should be re-evaluated against an
  independently labeled held-out dataset if such data becomes available.

The prototype therefore reports the results as evaluation evidence and does not
overstate them as real-world validated performance.

---

# 9. Overall Evaluation Status

**PHASE 2 EVALUATION COMPLETE**

The prototype demonstrates a complete Lane 3 decision-support workflow:

`Registry → Detection → Explanation → Confidence → Human Review → Evaluation`

The system successfully completed:

- Operating-hours scripted evaluation
- Duplicate candidate generation
- 100/100 human review
- Uncertainty handling
- Baseline definition
- Safety-boundary documentation

---

Generated: August 2026
