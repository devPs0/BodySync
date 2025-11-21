import requests
import json

print("🧪 Testing Workout Generation...")
print("=" * 40)

session = requests.Session()

# Step 1: Login
print("1. Logging in...")
login_data = {
    'username': 'dev',
    'password': 'devps0123'
}

try:
    login_response = session.post("http://127.0.0.1:5000/login", data=login_data)
    if login_response.status_code == 302:
        print("✅ Login successful")
    else:
        print(f"❌ Login failed: {login_response.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Login error: {e}")
    exit(1)

# Step 2: Generate workout
print("2. Generating workout...")
workout_data = {
    'goal': 'Weight Loss',
    'experience': 'Beginner',
    'equipment': 'Basic',
    'schedule': '3 days per week'
}

try:
    workout_response = session.post("http://127.0.0.1:5000/generate_workout", data=workout_data)
    
    if workout_response.status_code == 200:
        print("✅ Request successful (200)")
        
        # Check if there's an error message in the response
        if "Error generating workout" in workout_response.text:
            print("❌ Error in workout generation")
            # Extract error message
            error_start = workout_response.text.find("Error generating workout")
            error_section = workout_response.text[error_start:error_start+200]
            print(f"Error details: {error_section}")
        elif "workout" in workout_response.text.lower() and "plan" in workout_response.text.lower():
            print("✅ Workout generated successfully!")
            print("Response contains workout content")
        else:
            print("⚠️  Response received but unclear if workout was generated")
            print(f"Response length: {len(workout_response.text)} characters")
            
    else:
        print(f"❌ Request failed: {workout_response.status_code}")
        
except Exception as e:
    print(f"❌ Workout generation error: {e}")

print("\n" + "=" * 40)