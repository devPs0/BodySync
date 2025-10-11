# gemini_test_gen.py
import os
from gemini_config import get_gemini_client

# Get the configured Gemini model
model = get_gemini_client()

def generate_fitness_assessment(goal, level, num_questions):
    if not model:
        # Fallback fitness assessment questions
        assessments = []
        for i in range(num_questions):
            assessments.append(f"How would you measure progress for {goal}? (Assessment {i+1})")
        return assessments
        
    prompt = f"""
    Generate {num_questions} fitness assessment questions for someone working on "{goal}".
    The fitness level should be {level}.
    Focus on form, technique, progress tracking, and safety.
    Return numbered questions only, no explanations or answers.
    """

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Simple line-based split for numbered questions
    assessments = [line.strip("0123456789. ") for line in text.split("\n") if line.strip()]
    return assessments[:num_questions]

# 🔽 Add this block to test from command line
if __name__ == "__main__":
    goal = "Weight Loss"
    level = "Beginner"
    num = 5
    print("\n--- Sample Fitness Assessment Output ---\n")
    for assessment in generate_fitness_assessment(goal, level, num):
        print("Assessment:", assessment)
