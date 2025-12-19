import google.genai.models
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# PASTE YOUR WORKING KEY HERE
my_key = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo"

print("🔍 Asking Google for available models...")

try:
    # We will try a different, older model name that usually works for everyone
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",  # <--- TRYING "gemini-pro" INSTEAD
        google_api_key=my_key
    )
    result = llm.invoke("Say 'Hello Navin' if gemini-pro works.")
    print(f"\n✅ SUCCESS with 'gemini-pro': {result.content}")
    
except Exception as e:
    print(f"\n❌ 'gemini-pro' failed too: {e}")