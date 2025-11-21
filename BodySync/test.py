# Simple test script for the Gym Planner
print("Gym Planner Test")
print("================")

# Test basic functionality
try:
    from app import app
    print("✅ Flask app imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Flask app: {e}")

try:
    from gemini_handler import generate_workout_plan
    print("✅ Gemini handler imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Gemini handler: {e}")

# Test basic workout plan generation (without API)
try:
    plan = generate_workout_plan("Weight Loss", "Beginner", 3, 1, "basic")
    print(f"✅ Generated workout plan with {len(plan)} days")
    for i, day in enumerate(plan):
        print(f"   Day {i+1}: {day.get('workout', day.get('task', 'No workout'))}")
except Exception as e:
    print(f"❌ Failed to generate workout plan: {e}")

print("\nTest completed!")