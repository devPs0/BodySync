import requests
import json

# Test the complete login flow
session = requests.Session()

print("🔧 Testing complete login flow...")
print("=" * 40)

# Step 1: Test login page access
try:
    login_page = session.get("http://127.0.0.1:5000/login")
    print(f"✅ Login page accessible: {login_page.status_code}")
except Exception as e:
    print(f"❌ Cannot access login page: {e}")
    exit(1)

# Step 2: Try to login with existing user
print("\n🔑 Testing login with existing user...")
login_data = {
    'username': 'dev',
    'password': 'devps0123'
}

try:
    login_response = session.post("http://127.0.0.1:5000/login", data=login_data)
    print(f"Login response status: {login_response.status_code}")
    
    if login_response.status_code == 200 and "Invalid credentials" in login_response.text:
        print("❌ Login failed - Invalid credentials")
    elif login_response.status_code == 302:
        print("✅ Login successful - redirected to home")
    else:
        print(f"Login response: {login_response.status_code}")
except Exception as e:
    print(f"❌ Login failed: {e}")
    exit(1)

# Step 3: Now try to access generate_workout
print("\n🏋️ Testing generate_workout access after login...")
try:
    workout_page = session.get("http://127.0.0.1:5000/generate_workout", allow_redirects=False)
    print(f"Generate workout page status: {workout_page.status_code}")
    
    if workout_page.status_code == 302:
        location = workout_page.headers.get('Location', 'Unknown')
        print(f"✅ Redirects to: {location}")
        if location == '/':
            print("✅ SUCCESS: Route works correctly (redirects to home as expected)")
        else:
            print(f"⚠️  Redirects to {location} instead of home")
    elif workout_page.status_code == 404:
        print("❌ Still getting 404 - route not found")
    else:
        print(f"Status: {workout_page.status_code}")
        
except Exception as e:
    print(f"❌ Error accessing generate_workout: {e}")

print("\n" + "=" * 40)
print("If you're still getting errors, the issue might be:")
print("1. Flask server not running properly")
print("2. Multiple Flask instances running")
print("3. Port conflicts")
print("4. Browser cache issues")