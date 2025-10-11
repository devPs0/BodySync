import requests

print("💾 Saving actual workout response to file...")

session = requests.Session()

# Login
login_data = {'username': 'dev', 'password': 'devps0123'}
session.post("http://127.0.0.1:5000/login", data=login_data)

# Generate workout
workout_data = {
    'goal': 'Weight Loss',
    'experience': 'Beginner',
    'equipment': 'Basic',
    'schedule': '3 days per week'
}

response = session.post("http://127.0.0.1:5000/generate_workout", data=workout_data)

# Save response to file
with open("workout_response.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"✅ Saved response ({len(response.text)} chars) to workout_response.html")
print("🔍 Open workout_response.html in your browser to see the actual output")

# Also extract just the workout content
if "workout-day" in response.text:
    start = response.text.find('<div class="workout-plan">')
    end = response.text.find('</div>', start + 100) + 6
    if start > -1:
        workout_content = response.text[start:end]
        print("\n📋 WORKOUT CONTENT FOUND:")
        print(workout_content[:1000])
        print("..." if len(workout_content) > 1000 else "")
else:
    print("❌ No workout-day content found")