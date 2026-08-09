import json
from datetime import datetime

output_file = "phase2/lane3_method_card.json"

method_card = {
    "title": "AED Guardian AI - Lane 3 Method Card",
    "generated_at": datetime.now().isoformat(),

    "lane": "Registry and readiness",

    "intended_user": {
        "primary": "Human AED registry/data-quality reviewer",
        "decision": "Identify records that may require correction, clarification, or field verification."
    },

    "problem": {
        "description": "The prototype helps reviewers identify possible registry-quality concerns in a historical AED dataset.",
        "data_quality_concerns": [
            "Possible duplicate AED records",
            "Inconsistent or missing operating-hours information",
            "Records requiring human field verification"
        ]
    },

    "system_architecture": [
        {
            "stage": 1,
            "name": "Registry input",
            "description": "Load the frozen AED GeoJSON registry snapshot."
        },
        {
            "stage": 2,
            "name": "Operating-hours analysis",
            "description": "Classify operating-hours text as parsed, parsed with remarks, missing, or ambiguous."
        },
        {
            "stage": 3,
            "name": "Duplicate candidate detection",
            "description": "Generate candidate record pairs using registry fields and deterministic matching rules."
        },
        {
            "stage": 4,
            "name": "Explainable flagging",
            "description": "Attach a detection rule, confidence level, and human-readable reason to each candidate."
        },
        {
            "stage": 5,
            "name": "Human-in-the-loop review",
            "description": "Present candidate pairs to a reviewer who chooses DUPLICATE, NOT_DUPLICATE, or UNCERTAIN."
        },
        {
            "stage": 6,
            "name": "Evaluation",
            "description": "Measure review coverage, abstention, and scripted operating-hours classification performance."
        }
    ],

    "input_features": [
        "AED_ID",
        "OPERATING_HOURS",
        "HOUSE_NUMBER",
        "ROAD_NAME",
        "BUILDING_NAME",
        "UNIT_NUMBER",
        "POSTAL_CODE",
        "AED_LOCATION_DESCRIPTION",
        "AED_LOCATION_FLOOR_LEVEL",
        "LATITUDE",
        "LONGITUDE",
        "XVAL",
        "YVAL"
    ],

    "duplicate_detection": {
        "approach": "Deterministic candidate generation with explainable matching rules",
        "example_rule": "EXACT_COORDINATES",
        "rule_description": "Records with identical latitude and longitude but different AED IDs are surfaced for human review.",
        "important_note": "Identical coordinates alone do not prove that two AED records are duplicates because multiple AEDs may legitimately exist at different floors or indoor locations."
    },

    "operating_hours": {
        "approach": "Structured rule-based parsing and classification",
        "classes": [
            "PARSED",
            "PARSED_WITH_REMARKS",
            "MISSING",
            "AMBIGUOUS"
        ],
        "confidence_levels": [
            "HIGH",
            "MEDIUM",
            "LOW"
        ],
        "human_review_trigger": "Ambiguous or missing operating-hours information can be surfaced for additional review."
    },

    "confidence_handling": {
        "HIGH": "Strong deterministic evidence supports the flag, but the flag remains a data-quality concern rather than proof of a real-world fault.",
        "MEDIUM": "Evidence is suggestive but requires interpretation or reviewer confirmation.",
        "LOW": "Information is missing or insufficient for a reliable automated conclusion."
    },

    "human_approval_points": [
        "Reviewer determines whether a duplicate candidate is actually a duplicate.",
        "Reviewer may select UNCERTAIN when available registry fields do not support a confident binary decision.",
        "Human decisions are recorded for evaluation and auditability."
    ],

    "assumptions": [
        "The supplied dataset is treated as a historical registry snapshot.",
        "Operating-hours text is treated as registry information rather than proof of current access.",
        "Identical coordinates can represent different indoor AED placements.",
        "Missing or ambiguous fields should not be converted into unsupported real-world claims."
    ],

    "limitations": [
        "The prototype does not establish current AED availability.",
        "The prototype does not establish AED operational readiness.",
        "The prototype does not detect battery depletion or pad expiry.",
        "The prototype does not verify inspections or maintenance.",
        "The prototype does not use live emergency or responder data.",
        "Duplicate precision, recall and F1 require independently established ground truth for valid reporting."
    ],

    "safety_boundary": {
        "planning_and_simulation_only": True,
        "emergency_use": False,
        "live_incident_integration": False,
        "current_device_readiness_claims": False,
        "statement": "A registry record is not proof that an AED is currently present, accessible, working, inspected, or ready for use."
    },

    "reproducibility": {
        "code_location": "phase2/",
        "review_interface": "phase2/review_app.py",
        "evaluation_report": "phase2/lane3_baseline_evaluation_report.json",
        "duplicate_review_report": "phase2/final_duplicate_review_report.json"
    }
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(method_card, f, indent=2)

print("=" * 60)
print("LANE 3 METHOD CARD")
print("=" * 60)
print(f"Saved to: {output_file}")
print()
print("Architecture documented")
print("Input features documented")
print("Duplicate detection documented")
print("Operating-hours method documented")
print("Confidence handling documented")
print("Human approval points documented")
print("Assumptions and limitations documented")
print("Safety boundary documented")
print()
print("Status: METHOD CARD COMPLETE")
