import time
import requests

# Wait for server to be fully ready
time.sleep(2)

try:
    # Test the generate_workout route
    response = requests.get("http://127.0.0.1:5000/generate_workout", allow_redirects=False, timeout=5)
    print(f"✅ Status: {response.status_code}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', 'Unknown')
        print(f"✅ Redirects to: {location}")
        print("SUCCESS: Route works correctly!")
    elif response.status_code == 404:
        print("❌ 404 Error - Route not found")
        # Try to access other routes to compare
        print("\nTesting other routes:")
        login_resp = requests.get("http://127.0.0.1:5000/login", timeout=5)
        print(f"Login page: {login_resp.status_code}")
        home_resp = requests.get("http://127.0.0.1:5000/", allow_redirects=False, timeout=5)
        print(f"Home page: {home_resp.status_code}")
    else:
        print(f"Unexpected status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Connection error: {e}")
    print("Make sure Flask server is running on http://127.0.0.1:5000")
except Exception as e:
    print(f"❌ Error: {e}")