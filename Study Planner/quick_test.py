import requests
import json

# Quick test
s = requests.Session()
s.post('http://127.0.0.1:5000/login', data={'username':'dev','password':'devps0123'})

# Test workout page
workouts_resp = s.get('http://127.0.0.1:5000/my_workouts')
print(f"My Workouts: {workouts_resp.status_code}")

# Test progress API  
progress_resp = s.get('http://127.0.0.1:5000/get_progress')
print(f"Progress API: {progress_resp.status_code}")

# Test mark complete
mark_resp = s.post('http://127.0.0.1:5000/mark_complete', 
                  json={'workout_index': 0, 'day_index': 5, 'completed': True})
print(f"Mark Complete: {mark_resp.status_code}")

print("Done!")