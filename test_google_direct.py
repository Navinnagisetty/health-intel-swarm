from langchain_google_genai import ChatGoogleGenerativeAI

# PASTE YOUR NEW KEY INSIDE THE QUOTES BELOW
# Example: my_key = "AIzaSyD..."
my_key = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo" 

print(f"Testing Key: {my_key[:5]}...")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=my_key
    )
    result = llm.invoke("Say 'Hello Navin' if this works.")
    print(f"\n✅ SUCCESS: {result.content}")
except Exception as e:
    print(f"\n❌ FAILED: {e}")