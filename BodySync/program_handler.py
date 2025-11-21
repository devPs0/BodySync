import json
import os

WORKOUT_FILE = 'saved_workouts.json'

def load_workouts():
    if not os.path.exists(WORKOUT_FILE):
        return {}
    with open(WORKOUT_FILE, 'r') as f:
        return json.load(f)

def save_all_workouts(workouts):
    with open(WORKOUT_FILE, 'w') as f:
        json.dump(workouts, f, indent=2)

def save_workout(workout):
    workouts = load_workouts()
    workouts[workout['goal']] = workout
    save_all_workouts(workouts)

def update_day_status(goal, day, status):
    workouts = load_workouts()
    if goal in workouts and day < len(workouts[goal]["plan"]):
        workouts[goal]["plan"][day]["completed"] = status
        save_all_workouts(workouts)

def save_exercise_tips(goal, workout, tips_text):
    workouts = load_workouts()
    if goal in workouts:
        for day in workouts[goal]["plan"]:
            if day.get("workout") == workout or day.get("task") == workout:
                day["exercises"] = tips_text
                save_all_workouts(workouts)
                break
