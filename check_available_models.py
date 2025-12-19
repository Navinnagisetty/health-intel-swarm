import google.generativeai as genai
import os

# PASTE YOUR WORKING KEY HERE (ending in J7zo)
KEY = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo"

genai.configure(api_key=KEY)

print("🔍 Scanning for available models...")

try:
    # List all models available to your key
    models = genai.list_models()
    found_any = False
    
    print("\n--- AVAILABLE MODELS ---")
    for m in models:
        # We only care about models that can generate content (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            found_any = True
            
    if not found_any:
        print("❌ No chat models found. You might need to enable the API in Google Cloud Console.")
        
except Exception as e:
    print(f"❌ Error listing models: {e}")