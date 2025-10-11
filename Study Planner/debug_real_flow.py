import requests
import time

print("🔍 TESTING REAL USER INTERACTION...")
print("=" * 50)

session = requests.Session()

# Step 1: Get login page
print("1. Getting login page...")
login_page = session.get("http://127.0.0.1:5000/login")
print(f"Login page status: {login_page.status_code}")

# Step 2: Login
print("2. Logging in...")
login_data = {
    'username': 'dev',
    'password': 'devps0123'
}
login_response = session.post("http://127.0.0.1:5000/login", data=login_data, allow_redirects=True)
print(f"Login response status: {login_response.status_code}")
print(f"Final URL after login: {login_response.url}")

# Check if we're on the main page
if "Generate Your Workout Plan" in login_response.text or "workout" in login_response.text.lower():
    print("✅ Successfully reached main page")
else:
    print("❌ Not on main page - login may have failed")
    print("Response contains:", login_response.text[:200])

# Step 3: Generate workout
print("\n3. Submitting workout form...")
workout_data = {
    'goal': 'Weight Loss',
    'experience': 'Beginner',
    'equipment': 'Basic',
    'schedule': '3 days per week'
}

workout_response = session.post("http://127.0.0.1:5000/generate_workout", data=workout_data, allow_redirects=True)
print(f"Workout response status: {workout_response.status_code}")
print(f"Response length: {len(workout_response.text)} characters")

# Check what's in the response
response_text = workout_response.text

# Look for error messages
if "Error generating workout" in response_text:
    print("❌ ERROR FOUND IN RESPONSE:")
    error_start = response_text.find("Error generating workout")
    error_end = error_start + 500
    print(response_text[error_start:error_end])

# Look for workout content
if "workout-day" in response_text:
    print("✅ Found workout-day divs - workout generated!")
elif "Day 1" in response_text or "Day 2" in response_text:
    print("✅ Found day references - workout generated!")
elif "exercise" in response_text.lower():
    print("✅ Found exercise content - workout generated!")
else:
    print("❌ NO WORKOUT CONTENT FOUND")
    print("Response snippet:")
    # Find the main content area
    if "<main" in response_text:
        main_start = response_text.find("<main")
        main_end = response_text.find("</main>", main_start) + 7
        main_content = response_text[main_start:main_end]
        print(main_content[:1000])
    else:
        print(response_text[:1000])

print("\n" + "=" * 50)