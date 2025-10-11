import os
import google.generativeai as genai

# Test the exact model we're going to use
api_key = 'AIzaSyC_o683zWGVRcixvelJXeOwZR17V43YJSk'
genai.configure(api_key=api_key)

print("🧪 Testing models/gemini-2.5-flash...")
print("=" * 40)

try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content("Generate a simple 3-day workout plan for weight loss. Keep it short.")
    print("✅ SUCCESS! Model is working")
    print(f"Response: {response.text[:200]}...")
    print("=" * 40)
    print("🎉 Workout generation should work now!")
except Exception as e:
    print(f"❌ ERROR: {e}")
    
    # Try alternative model
    print("\n🔄 Trying models/gemini-2.0-flash...")
    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        response = model.generate_content("Generate a simple workout plan.")
        print("✅ Alternative model works!")
        print("📝 Update .env to use: models/gemini-2.0-flash")
    except Exception as e2:
        print(f"❌ Alternative also failed: {e2}")