# Gemini API Configuration for Gym Planner
# This file contains the Gemini API configuration
import os
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

class GeminiConfig:
    """Configuration class for Gemini API"""
    
    def __init__(self):
        # Try to load from environment first, then from config file
        self.api_key = self._get_api_key()
        self.model_name = os.getenv('GEMINI_MODEL', 'models/gemini-2.5-flash')
        self.model = None
        self.genai = None
        
        self._initialize_gemini()
    
    def _get_api_key(self):
        """Get API key from multiple sources"""
        # 1. Try environment variable
        env_key = os.getenv('GEMINI_API_KEY')
        if env_key:
            return env_key
            
        # 2. Try config file
        config_file = os.path.join(os.path.dirname(__file__), 'gemini_config.json')
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('api_key')
            except Exception:
                pass
        
        # 3. Return None if not found
        return None
    
    def _initialize_gemini(self):
        """Initialize Gemini API client"""
        try:
            import google.generativeai as genai
            self.genai = genai
            
            if self.api_key:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
                print(f"✅ Gemini API initialized successfully with model: {self.model_name}")
            else:
                print("⚠️  No Gemini API key found. Using fallback responses.")
                
        except ImportError:
            print("⚠️  google-generativeai package not installed. Using fallback responses.")
        except Exception as e:
            print(f"⚠️  Failed to initialize Gemini API: {e}")
    
    def update_api_key(self, new_api_key):
        """Update the API key and reinitialize"""
        self.api_key = new_api_key
        
        # Save to config file
        config_file = os.path.join(os.path.dirname(__file__), 'gemini_config.json')
        config = {
            'api_key': new_api_key,
            'model_name': self.model_name,
            'updated_at': str(os.times())
        }
        
        try:
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            print(f"✅ API key saved to {config_file}")
        except Exception as e:
            print(f"❌ Failed to save API key: {e}")
        
        # Reinitialize
        self._initialize_gemini()
    
    def is_available(self):
        """Check if Gemini API is available"""
        return self.model is not None
    
    def get_status(self):
        """Get current configuration status"""
        status = {
            'api_key_set': bool(self.api_key),
            'api_key_preview': f"{self.api_key[:10]}..." if self.api_key else "Not set",
            'model_name': self.model_name,
            'available': self.is_available()
        }
        return status

# Global instance
gemini_config = GeminiConfig()

def get_gemini_client():
    """Get the configured Gemini model"""
    return gemini_config.model

def update_gemini_api_key(new_key):
    """Update the Gemini API key"""
    gemini_config.update_api_key(new_key)

def get_gemini_status():
    """Get Gemini configuration status"""
    return gemini_config.get_status()