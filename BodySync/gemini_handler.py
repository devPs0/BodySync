import os
import json
from gemini_config import get_gemini_client

def generate_workout_plan(goal, level, days, hours, equipment="basic"):
    # Get the configured Gemini model fresh each time
    model = get_gemini_client()
    prompt = f"""Create a {days}-day workout plan for {goal} ({level} level) with {equipment} equipment.

Return ONLY a valid JSON array. No explanation, no markdown, no extra text.

Format:
[
  {{"workout": "Day 1 description", "exercises": "• Exercise 1: 3x10\\n• Exercise 2: 3x12"}},
  {{"workout": "Day 2 description", "exercises": "• Exercise 3: 3x8\\n• Exercise 4: 3x15"}},
  {{"workout": "Day 3 description", "exercises": "• Exercise 5: 3x10\\n• Exercise 6: 3x12"}}
]

Create exactly {days} workout objects. Return only the JSON array."""

    # If model not available, return a simple deterministic plan
    if not model:
        plan = []
        workout_types = ["Upper body", "Lower body", "Cardio", "Core", "Full body", "Rest/Stretch", "HIIT"]
        for i in range(days):
            workout_type = workout_types[i % len(workout_types)]
            plan.append({
                "workout": f"{workout_type} workout - Day {i+1}",
                "exercises": f"• Exercise 1: 3 sets of 10-15\\n• Exercise 2: 3 sets of 8-12\\n• Stretch: 5-10 minutes",
                "completed": False
            })
        return plan

    response = model.generate_content(prompt)
    try:
        json_str = response.text.strip()
        print(f"Raw Gemini response: {json_str[:200]}...")  # Debug output
        
        # Remove markdown if accidentally returned
        if json_str.startswith("```"):
            parts = json_str.split("```")
            # try to find JSON-like part
            for part in parts:
                if part.strip().startswith("["):
                    json_str = part.strip()
                    break
        
        if not json_str or json_str == "":
            raise ValueError("Empty response from Gemini")
            
        plan = json.loads(json_str)
        # ensure completed flag
        for day in plan:
            day.setdefault('completed', False)
        return plan
    except Exception as e:
        print(f"Error parsing Gemini response: {e}")
        print(f"Raw response was: '{response.text if response else 'None'}'")  # More debug info
        # Fallback
        plan = []
        workout_types = ["Upper body", "Lower body", "Cardio", "Core", "Full body", "Rest/Stretch", "HIIT"]
        for i in range(days):
            workout_type = workout_types[i % len(workout_types)]
            plan.append({
                "workout": f"{workout_type} workout - Day {i+1}",
                "exercises": f"• Exercise 1: 3 sets of 10-15\\n• Exercise 2: 3 sets of 8-12\\n• Stretch: 5-10 minutes",
                "completed": False
            })
        return plan

def generate_exercise_tips(workout):
    prompt = f"""
You are a fitness expert. Create a compact bullet-point exercise guide for the following workout:
"{workout}"

Output format:
- Use plain text bullet points (•)
- Include form tips and safety notes
- No explanation or introduction.
- Only return the exercise tips as a plain string.
"""

    # Get the configured Gemini model fresh each time
    model = get_gemini_client()
    
    if not model:
        return "• Focus on proper form\n• Control your breathing\n• Start with lighter weights\n• Rest between sets"
    response = model.generate_content(prompt)
    return response.text.strip()


