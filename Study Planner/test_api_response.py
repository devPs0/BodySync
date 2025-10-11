#!/usr/bin/env python3

import requests
import json

# Test the get_progress API to see what it returns
def test_get_progress():
    """Test the /get_progress endpoint directly"""
    
    # First login to get a session
    session = requests.Session()
    
    # Login
    login_data = {
        'username': 'dev',
        'password': 'dev'  # assuming this is the password based on common patterns
    }
    
    print("🔍 Attempting to login...")
    login_response = session.post('http://127.0.0.1:5000/login', data=login_data)
    print(f"Login status: {login_response.status_code}")
    
    if login_response.status_code == 200:
        # Now test the get_progress API
        print("\n🔍 Testing /get_progress endpoint...")
        progress_response = session.get('http://127.0.0.1:5000/get_progress')
        print(f"Progress status: {progress_response.status_code}")
        
        if progress_response.status_code == 200:
            try:
                data = progress_response.json()
                print("\n📊 Full API Response:")
                print(json.dumps(data, indent=2))
                
                print(f"\n✅ Success: {data.get('success')}")
                print(f"✅ Has 'workouts' key: {'workouts' in data}")
                print(f"✅ Workouts type: {type(data.get('workouts'))}")
                print(f"✅ Workouts length: {len(data.get('workouts', []))}")
                
                if 'workouts' in data and len(data['workouts']) > 0:
                    print("\n🏋️ First workout:")
                    print(json.dumps(data['workouts'][0], indent=2))
                    
            except Exception as e:
                print(f"❌ Error parsing JSON: {e}")
                print(f"Raw response: {progress_response.text}")
        else:
            print(f"❌ Failed to get progress: {progress_response.text}")
    else:
        print(f"❌ Login failed: {login_response.text}")

if __name__ == "__main__":
    test_get_progress()