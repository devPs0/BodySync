import os
from gemini_config import get_gemini_client

# Get the configured Gemini model
model = get_gemini_client()

def generate_enhanced_workout_output(goal, day_workout, level, days, hours):
    if not model:
        return f"""
<div>
    <h3>Today's Workout: {day_workout}</h3>
    <ul>
        <li><strong>Warm-up:</strong> 5-10 minutes light cardio and dynamic stretching</li>
        <li><strong>Main workout:</strong> Focus on proper form and controlled movements</li>
        <li><strong>Cool-down:</strong> 5-10 minutes stretching and breathing exercises</li>
        <li><strong>Safety:</strong> Listen to your body and stay hydrated</li>
    </ul>
</div>
"""
        
    prompt = f"""
You are a fitness coach. Take the following workout and format it into professional, clean HTML. Avoid markdown, triple backticks, or raw tags. Return only clean, embeddable HTML (not markdown blocks).

Use this layout:
- Use simple `<div>`s and `<ul>` for structure.
- Include 4 sections: **Warm-up**, **Main Workout**, **Cool-down**, **Safety Tips**.
- Explain them clearly with specific guidance.

Workout to format: {day_workout}
Fitness level: {level}
Goal: {goal}

The tone should be motivating, clear, and safety-focused.
    """

    response = model.generate_content(prompt)
    
    # Clean known unwanted wrappers if any still appear
    cleaned = response.text.replace("```html", "").replace("```", "").strip()
    return cleaned
