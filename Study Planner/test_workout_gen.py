import requests
import json

# Test workout generation after login
print("🧪 Testing Workout Generation...")
print("=" * 40)

session = requests.Session()

# Login first
login_data = {
    'username': 'dev',
    'password': 'devps0123'
}

print("1. Logging in...")
login_response = session.post("http://127.0.0.1:5000/login", data=login_data)
if login_response.status_code == 302:
    print("✅ Login successful")
else:
    print("❌ Login failed")
    exit(1)

# Test workout generation
print("2. Generating workout...")
workout_data = {
    'goal': 'Weight Loss',
    'experience': 'Beginner', 
    'equipment': 'Basic',
    'schedule': '3 days per week'
}

workout_response = session.post("http://127.0.0.1:5000/generate_workout", data=workout_data)

if workout_response.status_code == 200:
    print("✅ Workout generation request successful")
    if "Error generating workout" in workout_response.text:
        print("❌ But there was an error in generation")
    elif "workout" in workout_response.text.lower():
        print("✅ Workout generated successfully!")
    else:
        print("⚠️  Response received but no workout content found")
else:
    print(f"❌ Workout generation failed with status: {workout_response.status_code}")

print("\n" + "=" * 40)