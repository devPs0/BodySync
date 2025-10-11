import requests

base_url = "http://127.0.0.1:5000"

# Test login page
try:
    response = requests.get(f"{base_url}/login")
    print(f"Login page status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Login page works")
    else:
        print("❌ Login page failed")
except Exception as e:
    print(f"❌ Error accessing login page: {e}")

# Test register page
try:
    response = requests.get(f"{base_url}/register")
    print(f"Register page status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Register page works")
    else:
        print("❌ Register page failed")
except Exception as e:
    print(f"❌ Error accessing register page: {e}")

# Test main page (should redirect to login)
try:
    response = requests.get(f"{base_url}/", allow_redirects=False)
    print(f"Main page status: {response.status_code}")
    if response.status_code == 302:
        print("✅ Main page redirects (as expected)")
        print(f"Redirect location: {response.headers.get('Location', 'Not specified')}")
    else:
        print("❌ Main page didn't redirect")
except Exception as e:
    print(f"❌ Error accessing main page: {e}")

# Test generate_workout page (should redirect to login)
try:
    response = requests.get(f"{base_url}/generate_workout", allow_redirects=False)
    print(f"Generate workout page status: {response.status_code}")
    if response.status_code == 302:
        print("✅ Generate workout page redirects (as expected)")
        print(f"Redirect location: {response.headers.get('Location', 'Not specified')}")
    else:
        print("❌ Generate workout page didn't redirect")
except Exception as e:
    print(f"❌ Error accessing generate workout page: {e}")