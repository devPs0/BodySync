#!/usr/bin/env python3
"""
Quick test to verify Gemini API is working with correct model name
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
    
    # Configure the API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No GEMINI_API_KEY found in environment")
        exit(1)
    
    genai.configure(api_key=api_key)
    
    # Test different model names
    model_names_to_test = [
        'gemini-1.5-flash',
        'gemini-1.5-pro',
        'gemini-pro',
        'models/gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    print("🧪 Testing Gemini model names...")
    print("=" * 40)
    
    for model_name in model_names_to_test:
        try:
            print(f"Testing: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'Hello from Gemini!' in 3 words.")
            print(f"✅ SUCCESS: {model_name}")
            print(f"   Response: {response.text.strip()}")
            print(f"   Using this model: {model_name}")
            break
        except Exception as e:
            print(f"❌ FAILED: {model_name} - {str(e)}")
    
    print("\n" + "=" * 40)
    print("✅ Test complete!")
    
except ImportError:
    print("❌ google-generativeai not installed")
    print("Install with: pip install google-generativeai")
except Exception as e:
    print(f"❌ Error: {e}")