import requests

try:
    response = requests.get("http://127.0.0.1:5000/generate_workout", allow_redirects=False)
    print(f"Status: {response.status_code}")
    if response.status_code == 302:
        print(f"Redirects to: {response.headers.get('Location', 'Unknown')}")
        print("✅ Route works - redirects as expected")
    elif response.status_code == 404:
        print("❌ Route not found - 404 error")
    else:
        print(f"Unexpected status: {response.status_code}")
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"Error: {e}")