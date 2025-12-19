import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- 1. FORCE THE KEY INTO THE SYSTEM ---
# This is the "Nuclear Option". It sets the key globally for this script.
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"

# --- 2. CONFIGURATION ---
MY_MODEL_NAME = "gemini-flash-latest"

# 3. Configure Brain
# We don't even need to pass the key here anymore, the system has it.
gemini_llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)

# 4. Setup the "Unsafe" Code Tool (Bypasses Docker)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# 5. Define Agent
coder = Agent(
    role='Junior Python Dev',
    goal='Write and execute a simple python script.',
    backstory='You are a helpful assistant.',
    llm=gemini_llm,
    allow_code_execution=False, 
    tools=[code_tool],
    verbose=True
)

# 6. Define Task
task = Task(
    description="Calculate the square root of 256 using Python code and print the result.",
    expected_output="The number 16.",
    agent=coder
)

# 7. Run Crew
crew = Crew(agents=[coder], tasks=[task])
print(f"\n🤖 Testing Agent with {MY_MODEL_NAME}...\n")
result = crew.kickoff()
print(f"\n✅ FINAL RESULT: {result}")