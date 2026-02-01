"""Test script to verify the quiz game scoring works correctly."""

import sys

def test_score_calculation():
    """Test that score calculation works correctly for various scenarios."""
    import quiz
    test_cases = [
        {
            "name": "All correct answers",
            "correct_count": 5,
            "total_questions": 5,
            "expected_score": 100.0
        },
        {
            "name": "Half correct answers",
            "correct_count": 2,
            "total_questions": 4,
            "expected_score": 50.0
        },
        {
            "name": "One correct out of five",
            "correct_count": 1,
            "total_questions": 5,
            "expected_score": 20.0
        },
        {
            "name": "No correct answers",
            "correct_count": 0,
            "total_questions": 5,
            "expected_score": 0.0
        },
        {
            "name": "Three correct out of five",
            "correct_count": 3,
            "total_questions": 5,
            "expected_score": 60.0
        },
        {
            "name": "Four correct out of five",
            "correct_count": 4,
            "total_questions": 5,
            "expected_score": 80.0
        }
    ]
    all_passed = True
    for test_case in test_cases:
        score = quiz.calculate_score(
            test_case["correct_count"],
            test_case["total_questions"]
        )
        if abs(score - test_case["expected_score"]) > 0.01:
            print(f"FAIL: {test_case['name']} - Expected {test_case['expected_score']}%, got {score}%")
            all_passed = False
    if all_passed:
        print("score_accuracy: 1.0")
        return 1.0
    else:
        print("score_accuracy: 0.0")
        return 0.0

def test_answer_checking():
    """Test that answer checking logic works correctly."""
    import quiz
    test_cases = [
        {"user": "A", "correct": "A", "expected": True},
        {"user": "B", "correct": "A", "expected": False},
        {"user": "C", "correct": "C", "expected": True},
        {"user": "D", "correct": "B", "expected": False},
    ]
    all_passed = True
    for test_case in test_cases:
        result = quiz.check_answer(test_case["user"], test_case["correct"])
        if result != test_case["expected"]:
            print(f"FAIL: Answer check - User: {test_case['user']}, Correct: {test_case['correct']}, Expected: {test_case['expected']}, Got: {result}")
            all_passed = False
    return all_passed

if __name__ == "__main__":
    score_test = test_score_calculation()
    answer_test = test_answer_checking()
    if score_test == 1.0 and answer_test:
        sys.exit(0)
    else:
        sys.exit(1)