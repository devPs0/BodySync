import os
import google.generativeai as genai

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    api_key = 'AIzaSyC_o683zWGVRcixvelJXeOwZR17V43YJSk'  # from .env file

genai.configure(api_key=api_key)

print("🔍 Listing available Gemini models...")
print("=" * 50)

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   Display Name: {model.display_name}")
            print(f"   Description: {model.description}")
            print()
    
    print("=" * 50)
    print("🧪 Testing with most likely model names...")
    
    # Test common model names
    test_names = [
        'gemini-1.5-flash-latest',
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'models/gemini-1.5-flash-latest',
        'models/gemini-1.5-flash'
    ]
    
    for name in test_names:
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content("Hello")
            print(f"✅ WORKING: {name}")
            print(f"   Response: {response.text.strip()[:50]}...")
            break
        except Exception as e:
            print(f"❌ FAILED: {name} - {str(e)[:100]}...")
            
except Exception as e:
    print(f"❌ Error listing models: {e}")
    print("This might be an API key issue.")