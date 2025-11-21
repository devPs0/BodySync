#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from gemini_handler import generate_workout_plan

print("🧪 Testing Gemini Handler Directly...")
print("=" * 50)

try:
    print("Generating workout plan...")
    result = generate_workout_plan("Weight Loss", "Beginner", 7, 1, "Basic")
    
    print(f"✅ Function returned: {type(result)}")
    
    if isinstance(result, list):
        print(f"✅ Got list with {len(result)} items")
        for i, item in enumerate(result[:3]):  # Show first 3 items
            print(f"  Day {i+1}: {item}")
    elif isinstance(result, str):
        print(f"✅ Got string: {result[:200]}...")
    else:
        print(f"⚠️  Unexpected type: {result}")
        
    print("\n" + "=" * 50)
    print("🎉 Gemini handler is working!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()