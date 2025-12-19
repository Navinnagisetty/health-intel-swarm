import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

if key is None:
    print("❌ ERROR: No key found. Python cannot see 'GOOGLE_API_KEY' in .env")
elif key.startswith("AIza"):
    print(f"✅ Key Found: {key[:8]}... (Looks correct)")
else:
    print(f"⚠️ Key Found, but it looks wrong: {key[:5]}...")