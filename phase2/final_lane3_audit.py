import os
import json

print("=" * 70)
print("AED GUARDIAN AI — LANE 3 FINAL COMPLIANCE AUDIT")
print("=" * 70)

checks = {
    "Frozen AED dataset": "data/PublicAccessAEDs.geojson",
    "Review application": "phase2/review_app.py",
    "Duplicate detection": "phase2/duplicate_detection.py",
    "Duplicate review queue": "phase2/duplicate_review_queue.py",
    "Final duplicate report": "phase2/final_duplicate_review_report.json",
    "Operating-hours evaluation": "phase2/phase2_operating_hours_evaluation.json",
    "Baseline evaluation report": "phase2/lane3_baseline_evaluation_report.json",
    "Method Card JSON": "phase2/lane3_method_card.json",
    "Data Manifest": "docs/DATA_MANIFEST.md",
    "Method Card documentation": "docs/METHOD_CARD.md",
    "Evaluation Report": "docs/EVALUATION_REPORT.md",
    "Safety Compliance": "docs/SAFETY_COMPLIANCE.md"
}

passed = 0
missing = 0

print("\nFILE CHECKS")
print("-" * 70)

for name, path in checks.items():
    exists = os.path.exists(path)

    if exists:
        size = os.path.getsize(path)
        print(f"[PASS] {name}: {path} ({size} bytes)")
        passed += 1
    else:
        print(f"[MISSING] {name}: {path}")
        missing += 1

print("\nCONTENT CHECKS")
print("-" * 70)

# Final duplicate report
report_path = "phase2/final_duplicate_review_report.json"

if os.path.exists(report_path):
    with open(report_path, encoding="utf-8") as f:
        report = json.load(f)

    print(f"[INFO] Duplicate pairs reviewed : {report.get('reviewed_pairs')}")
    print(f"[INFO] DUPLICATE               : {report.get('labels', {}).get('DUPLICATE')}")
    print(f"[INFO] NOT_DUPLICATE           : {report.get('labels', {}).get('NOT_DUPLICATE')}")
    print(f"[INFO] UNCERTAIN               : {report.get('labels', {}).get('UNCERTAIN')}")
    print(f"[INFO] UNREVIEWED              : {report.get('unreviewed_pairs')}")
    print(f"[INFO] Abstention rate         : {report.get('abstention_rate')}")

    if (
        report.get("reviewed_pairs") == 100
        and report.get("unreviewed_pairs") == 0
    ):
        print("[PASS] 100/100 candidate pairs reviewed")
    else:
        print("[WARNING] Duplicate review is not fully complete")

# Operating-hours evaluation
hours_path = "phase2/phase2_operating_hours_evaluation.json"

if os.path.exists(hours_path):
    with open(hours_path, encoding="utf-8") as f:
        hours = json.load(f)

    print(f"\n[INFO] Operating-hours test cases : {hours.get('total_cases')}")
    print(f"[INFO] Correct                  : {hours.get('correct')}")
    print(f"[INFO] Incorrect                : {hours.get('incorrect')}")
    print(f"[INFO] Accuracy                 : {hours.get('accuracy')}")

    if (
        hours.get("total_cases") == 10
        and hours.get("correct") == 10
        and hours.get("incorrect") == 0
    ):
        print("[PASS] 10/10 scripted operating-hours cases correct")
    else:
        print("[WARNING] Operating-hours evaluation differs from expected result")

# Documentation content check
docs = {
    "DATA_MANIFEST.md": "docs/DATA_MANIFEST.md",
    "METHOD_CARD.md": "docs/METHOD_CARD.md",
    "EVALUATION_REPORT.md": "docs/EVALUATION_REPORT.md",
    "SAFETY_COMPLIANCE.md": "docs/SAFETY_COMPLIANCE.md"
}

for name, path in docs.items():
    if os.path.exists(path) and os.path.getsize(path) > 0:
        print(f"[PASS] {name} contains documentation")
    else:
        print(f"[FAIL] {name} is missing or empty")

print("\n" + "=" * 70)
print("AUDIT SUMMARY")
print("=" * 70)

print(f"Existing required files : {passed}/{len(checks)}")
print(f"Missing required files  : {missing}")

if missing == 0:
    print("\nSTATUS: CORE LANE 3 PACKAGE PRESENT")
else:
    print("\nSTATUS: ACTION REQUIRED")

print("\nIMPORTANT:")
print("File presence does not by itself prove every hackathon requirement.")
print("Final submission should also verify the actual UI safety notice,")
print("source URL/licence details, frozen-data checksum, and reproducibility.")
