import time
import requests

# Wait for server to be fully ready
time.sleep(1)

try:
    # Test the generate_workout route on port 5001
    response = requests.get("http://127.0.0.1:5001/generate_workout", allow_redirects=False, timeout=5)
    print(f"✅ Status: {response.status_code}")
    
    if response.status_code == 302:
        location = response.headers.get('Location', 'Unknown')
        print(f"✅ Redirects to: {location}")
        print("SUCCESS: Route works correctly!")
    elif response.status_code == 404:
        print("❌ 404 Error - Route not found")
    else:
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:100]}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Connection error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")