#!/usr/bin/env python3
"""
Gemini API Key Setup Script for Gym Planner
===========================================

This script helps you set up your new Gemini API key for the Gym Planner application.
"""

import os
import sys
import json
from gemini_config import update_gemini_api_key, get_gemini_status

def main():
    print("🏋️ Gym Planner - Gemini API Setup")
    print("=" * 40)
    
    # Show current status
    status = get_gemini_status()
    print(f"Current Status:")
    print(f"  API Key: {status['api_key_preview']}")
    print(f"  Model: {status['model_name']}")
    print(f"  Available: {'✅ Yes' if status['available'] else '❌ No'}")
    print()
    
    if not status['available']:
        print("⚠️  Gemini API is not currently available.")
        print("   This could be due to:")
        print("   1. Missing API key")
        print("   2. Invalid API key")
        print("   3. google-generativeai package not installed")
        print()
    
    # Get new API key
    print("To get a new Gemini API key:")
    print("1. Go to https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated key")
    print()
    
    new_key = input("Enter your new Gemini API key (or press Enter to skip): ").strip()
    
    if new_key:
        print(f"\n🔄 Updating API key...")
        try:
            update_gemini_api_key(new_key)
            
            # Check new status
            new_status = get_gemini_status()
            if new_status['available']:
                print("✅ API key updated successfully!")
                print("✅ Gemini API is now available for workout generation.")
            else:
                print("❌ API key updated but Gemini API is still not available.")
                print("   Please check if the key is valid.")
                
        except Exception as e:
            print(f"❌ Failed to update API key: {e}")
    else:
        print("⏭️  Skipping API key update.")
    
    print("\n📝 Alternative Setup Methods:")
    print("1. Set environment variable: GEMINI_API_KEY=your_key_here")
    print("2. Edit the gemini_config.json file directly")
    print("3. Run this script again")
    
    print(f"\n🚀 To start the Gym Planner:")
    print("   python app.py")
    print("\n   The app will be available at: http://127.0.0.1:5000")

if __name__ == "__main__":
    main()