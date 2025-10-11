import requests
import json

def test_workout_selector():
    print("🔧 TESTING WORKOUT SELECTOR FIX")
    print("=" * 40)
    
    try:
        s = requests.Session()
        
        # Login
        login_resp = s.post('http://127.0.0.1:5000/login', 
                           data={'username':'dev','password':'devps0123'})
        print(f"1. Login: {login_resp.status_code}")
        
        # Test progress page
        progress_resp = s.get('http://127.0.0.1:5000/progress_fitness')
        print(f"2. Progress page: {progress_resp.status_code}")
        
        # Test progress API (should return workout goals)
        api_resp = s.get('http://127.0.0.1:5000/get_progress')
        if api_resp.status_code == 200:
            data = api_resp.json()
            print(f"3. Progress API success: {data.get('success')}")
            print(f"   Available workouts: {list(data.get('workout_data', {}).keys())}")
            print(f"   Total workouts: {data.get('total_workouts')}")
        else:
            print(f"3. Progress API failed: {api_resp.status_code}")
        
        # Test my_workouts page (source of workout data)
        workouts_resp = s.get('http://127.0.0.1:5000/my_workouts')
        if workouts_resp.status_code == 200:
            content = workouts_resp.text
            print(f"4. My Workouts page: {workouts_resp.status_code}")
            print(f"   Contains workouts data: {'const workouts =' in content}")
            print(f"   Page length: {len(content)} chars")
        else:
            print(f"4. My Workouts failed: {workouts_resp.status_code}")
        
        print("\\n✅ Test completed - check progress page!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_workout_selector()