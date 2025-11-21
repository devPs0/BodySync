#!/usr/bin/env python3
"""Test the workout generation function directly"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from gemini_handler import generate_workout_plan

print("🧪 Testing workout generation function...")
print("=" * 50)

try:
    result = generate_workout_plan("Weight Loss", "Beginner", 3, 1, "Basic")
    print("✅ Function executed successfully!")
    print(f"Result type: {type(result)}")
    print(f"Result: {result}")
    
    if isinstance(result, list) and len(result) > 0:
        print("✅ Generated workout plan structure looks good!")
        for i, day in enumerate(result, 1):
            print(f"  Day {i}: {day.get('workout', 'No workout')}")
    else:
        print("❌ Result structure unexpected")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 50)