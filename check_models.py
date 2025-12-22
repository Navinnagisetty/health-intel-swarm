import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Load the Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key not found in .env")
else:
    print(f"✅ Key found: {api_key[:5]}...")
    
    # 2. Configure Google AI
    genai.configure(api_key=api_key)

    # 3. List Available Models
    print("\n🔍 Asking Google for available models...")
    try:
        models = genai.list_models()
        found = False
        for m in models:
            if 'generateContent' in m.supported_generation_methods:
                print(f"   • {m.name}")
                found = True
        
        if not found:
            print("❌ No chat models found. Your key might have restrictions.")
            
    except Exception as e:
        print(f"❌ Error connecting to Google: {e}")