import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import time

print("🔧 COMPREHENSIVE WORKOUT TEST")
print("=" * 50)

# Create session with retries
session = requests.Session()
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
)
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("http://", adapter)

base_url = "http://127.0.0.1:5000"

# Test 1: Check if server is up
print("1. Testing server availability...")
try:
    response = session.get(f"{base_url}/login", timeout=10)
    if response.status_code == 200:
        print("✅ Server is responding")
    else:
        print(f"⚠️  Server returned {response.status_code}")
except Exception as e:
    print(f"❌ Server not responding: {e}")
    exit(1)

# Test 2: Login with correct credentials
print("\n2. Testing login...")
login_data = {
    'username': 'dev',
    'password': 'devps0123'
}

try:
    login_response = session.post(f"{base_url}/login", data=login_data, timeout=10)
    print(f"Login response status: {login_response.status_code}")
    
    if login_response.status_code == 302:
        print("✅ Login successful - redirected")
    elif "Invalid credentials" in login_response.text:
        print("❌ Invalid credentials")
        exit(1)
    elif login_response.status_code == 200:
        if "Welcome" in login_response.text or "Generate" in login_response.text:
            print("✅ Login successful - already on main page")
        else:
            print("⚠️  Login returned 200 but unclear if successful")
            print("Checking for login form...")
            if "login" in login_response.text.lower() and "password" in login_response.text.lower():
                print("❌ Still showing login form - login failed")
                exit(1)
    else:
        print(f"❌ Unexpected login response: {login_response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Login error: {e}")
    exit(1)

# Test 3: Generate workout
print("\n3. Testing workout generation...")
workout_data = {
    'goal': 'Weight Loss',
    'experience': 'Beginner',
    'equipment': 'Basic',
    'schedule': '3 days per week'
}

try:
    print("Sending workout generation request...")
    workout_response = session.post(f"{base_url}/generate_workout", data=workout_data, timeout=30)
    
    print(f"Workout response status: {workout_response.status_code}")
    
    if workout_response.status_code == 200:
        response_text = workout_response.text
        
        # Check for error messages
        if "Error generating workout" in response_text:
            print("❌ Error in workout generation")
            error_start = response_text.find("Error generating workout")
            error_section = response_text[error_start:error_start+300]
            print(f"Error: {error_section}")
        
        # Check for successful generation
        elif "workout-day" in response_text or ("workout" in response_text.lower() and "exercise" in response_text.lower()):
            print("✅ Workout generated successfully!")
            print("Found workout content in response")
            
            # Look for specific workout elements
            if "Day 1" in response_text:
                print("✅ Multi-day workout plan detected")
            if "exercise" in response_text.lower():
                print("✅ Exercise details included")
                
        else:
            print("⚠️  Response received but no clear workout content")
            print(f"Response length: {len(response_text)} characters")
            
            # Show a snippet of the response
            snippet = response_text[:500].replace('\n', ' ')
            print(f"Response snippet: {snippet}...")
            
    else:
        print(f"❌ Workout generation failed: {workout_response.status_code}")
        
except Exception as e:
    print(f"❌ Workout generation error: {e}")

print("\n" + "=" * 50)
print("🏁 Test complete!")

# Give some final instructions
print("\n📋 INSTRUCTIONS:")
print("1. Open your browser and go to: http://127.0.0.1:5000")
print("2. Login with username: dev, password: devps0123")
print("3. Fill out the workout form and click 'Generate Workout'")
print("4. If it doesn't work, check the server terminal for error messages")