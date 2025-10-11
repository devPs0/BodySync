#!/usr/bin/env python3
import requests
import json
import re

def test_all_functionality():
    print("🔧 COMPREHENSIVE FUNCTIONALITY TEST")
    print("=" * 50)
    
    try:
        s = requests.Session()
        
        # Login
        login_resp = s.post('http://127.0.0.1:5000/login', 
                           data={'username':'dev','password':'devps0123'})
        print(f"1. Login: {login_resp.status_code}")
        
        if login_resp.status_code not in [200, 302]:
            print("❌ Login failed, stopping tests")
            return
        
        # Test My Workouts page (view workout issue)
        print("\n🔍 TESTING VIEW WORKOUT ISSUE")
        workouts_resp = s.get('http://127.0.0.1:5000/my_workouts')
        print(f"2. My Workouts page: {workouts_resp.status_code}")
        
        if workouts_resp.status_code == 200:
            content = workouts_resp.text
            print(f"   ✅ Contains workout data: {'const workouts =' in content}")
            print(f"   ✅ Has viewWorkout function: {'function viewWorkout(' in content}")
            print(f"   ✅ Has modal elements: {'workoutModal' in content}")
            
            # Check if JavaScript data is properly formatted
            js_match = re.search(r'const workouts = (.*?);', content, re.DOTALL)
            if js_match:
                try:
                    data = js_match.group(1)
                    workouts_data = json.loads(data)
                    print(f"   ✅ JavaScript data valid: {len(workouts_data)} workouts")
                except:
                    print("   ❌ JavaScript data invalid")
            else:
                print("   ❌ No workouts data found")
        
        # Test Progress APIs
        print("\n🔍 TESTING PROGRESS FUNCTIONALITY")
        progress_resp = s.get('http://127.0.0.1:5000/get_progress')
        print(f"3. Progress API: {progress_resp.status_code}")
        if progress_resp.status_code == 200:
            data = progress_resp.json()
            print(f"   ✅ Total workouts: {data.get('total_workouts')}")
            print(f"   ✅ Completed days: {data.get('completed_days')}")
        
        # Test Streak Achievements API
        streak_resp = s.get('http://127.0.0.1:5000/api/streak_achievements')
        print(f"4. Streak API: {streak_resp.status_code}")
        if streak_resp.status_code == 200:
            streak_data = streak_resp.json()
            print(f"   ✅ Badge: {streak_data.get('badge')}")
            print(f"   ✅ Progress: {streak_data.get('progress')}")
        
        # Test Progress Fitness page
        progress_page_resp = s.get('http://127.0.0.1:5000/progress_fitness')
        print(f"5. Progress Fitness page: {progress_page_resp.status_code}")
        
        # Test Mark Complete functionality
        print("\n🔍 TESTING PROGRESS MARKING")
        mark_resp = s.post('http://127.0.0.1:5000/mark_complete', 
                          json={'workout_index': 0, 'day_index': 4, 'completed': True})
        print(f"6. Mark Complete API: {mark_resp.status_code}")
        
        # Check if progress updated
        final_resp = s.get('http://127.0.0.1:5000/get_progress')
        if final_resp.status_code == 200:
            final_data = final_resp.json()
            print(f"7. Updated completed days: {final_data.get('completed_days')}")
        
        print("\n🎉 ALL TESTS COMPLETED!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_all_functionality()