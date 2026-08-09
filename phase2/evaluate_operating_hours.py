import json
from operating_hours import parse_operating_hours


TEST_CASES = [
    {
        "name": "24 hour schedule",
        "input": "Mon - Sun 00:00-23:59;",
        "expected_status": "PARSED",
    },
    {
        "name": "Standard weekday schedule",
        "input": "Mon - Fri 09:00-18:00;",
        "expected_status": "PARSED",
    },
    {
        "name": "Weekend closed",
        "input": "Mon - Sat 07:00-23:00; Sun Closed;",
        "expected_status": "PARSED",
    },
    {
        "name": "Schedule with remarks",
        "input": (
            "Mon - Sun 08:00-23:59; "
            "Remarks: Fri: Closes at 2:00 AM, Sat: Closes at 2:00 AM;"
        ),
        "expected_status": "PARSED_WITH_REMARKS",
    },
    {
        "name": "Missing value",
        "input": None,
        "expected_status": "MISSING",
    },
    {
        "name": "Empty value",
        "input": "",
        "expected_status": "MISSING",
    },
    {
        "name": "Null value",
        "input": "null",
        "expected_status": "MISSING",
    },
    {
        "name": "Unusual text",
        "input": "Open whenever required",
        "expected_status": "AMBIGUOUS",
    },
    {
        "name": "AM PM format",
        "input": "Monday 9 AM - 5 PM",
        "expected_status": "AMBIGUOUS",
    },
    {
        "name": "Mixed schedule",
        "input": "Mon - Fri 07:45-18:00; Sat 07:45-14:00; Sun Closed;",
        "expected_status": "PARSED",
    },
]


def main():

    print("=== PHASE 2 OPERATING-HOURS EVALUATION ===\n")

    correct = 0
    results = []

    for case in TEST_CASES:

        result = parse_operating_hours(case["input"])

        predicted = result["status"]
        expected = case["expected_status"]

        is_correct = predicted == expected

        if is_correct:
            correct += 1

        results.append({
            "name": case["name"],
            "expected": expected,
            "predicted": predicted,
            "correct": is_correct,
            "confidence": result["confidence"],
            "reason": result["reason"],
        })

        print(f"Test: {case['name']}")
        print(f"Expected : {expected}")
        print(f"Predicted: {predicted}")
        print(f"Result   : {'PASS' if is_correct else 'FAIL'}")
        print()

    total = len(TEST_CASES)
    accuracy = correct / total

    print("===================================")
    print(f"Total test cases : {total}")
    print(f"Correct          : {correct}")
    print(f"Incorrect        : {total - correct}")
    print(f"Accuracy         : {accuracy:.3f}")
    print("===================================")

    output = {
        "total_cases": total,
        "correct": correct,
        "incorrect": total - correct,
        "accuracy": accuracy,
        "results": results,
    }

    with open(
        "phase2/phase2_operating_hours_evaluation.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(output, f, indent=2)

    print(
        "\nEvaluation saved to "
        "phase2/phase2_operating_hours_evaluation.json"
    )


if __name__ == "__main__":
    main()
