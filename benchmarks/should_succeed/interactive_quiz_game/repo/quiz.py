"""Interactive quiz game with scoring."""

questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
        "correct": "C"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["A) 3", "B) 4", "C) 5", "D) 6"],
        "correct": "B"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
        "correct": "B"
    },
    {
        "question": "What is the largest ocean?",
        "options": ["A) Atlantic", "B) Indian", "C) Arctic", "D) Pacific"],
        "correct": "D"
    },
    {
        "question": "What is the square root of 16?",
        "options": ["A) 2", "B) 4", "C) 6", "D) 8"],
        "correct": "B"
    }
]

def display_question(question_data, question_num):
    """Display a question and its options."""
    print(f"\nQuestion {question_num}: {question_data['question']}")
    for option in question_data['options']:
        print(f"  {option}")

def get_user_answer():
    """Get and validate user's answer."""
    while True:
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        if answer in ['A', 'B', 'C', 'D']:
            return answer
        print("Invalid input. Please enter A, B, C, or D.")

def check_answer(user_answer, correct_answer):
    """Check if the user's answer is correct."""
    return user_answer == correct_answer

def calculate_score(correct_count, total_questions):
    """Calculate the final score percentage."""
    if total_questions == 0:
        return 0.0
    return (correct_count / total_questions) * 100

def main():
    """Main quiz game loop."""
    print("=" * 50)
    print("Welcome to the Interactive Quiz Game!")
    print("=" * 50)
    
    correct_count = 0
    total_questions = len(questions)
    
    for i, question_data in enumerate(questions, 1):
        display_question(question_data, i)
        user_answer = get_user_answer()
        
        if check_answer(user_answer, question_data['correct']):
            print("\u2713 Correct!")
            correct_count += 1
        else:
            print(f"\u2717 Incorrect. The correct answer is {question_data['correct']}.")
    
    print("\n" + "=" * 50)
    print("Quiz Complete!")
    print("=" * 50)
    
    score = calculate_score(correct_count, total_questions)
    print(f"Your score: {correct_count}/{total_questions} ({score:.1f}%)")
    
    if score >= 80:
        print("Excellent work!")
    elif score >= 60:
        print("Good job!")
    else:
        print("Keep practicing!")

if __name__ == "__main__":
    main()
