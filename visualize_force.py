import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# --- THE VISUALIZER AGENT ---
visualizer = Agent(
    role='Strict Visualization Officer',
    goal='You MUST generate image files using Python code. You never just "say" you did it.',
    backstory='You are a code-first agent. You do not speak until you have successfully executed Python code to save a file.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# --- THE TASK ---
visualization_task = Task(
    description="""
    I have a file named 'top_providers.csv'.
    
    CRITICAL INSTRUCTION: You MUST use the 'Code Interpreter' tool. Do not just answer me.
    
    1. Write Python code to read 'top_providers.csv'.
    2. Create a Bar Chart of Provider_ID vs Billed_Amount.
    3. Save it as 'provider_revenue.png'.
    4. AFTER saving, use Python to check if 'provider_revenue.png' exists on disk.
    5. Only if the file exists, return the message: "VERIFIED: Image saved to disk."
    """,
    expected_output="The string 'VERIFIED: Image saved to disk.'",
    agent=visualizer
)

# --- RUN THE CREW ---
crew = Crew(agents=[visualizer], tasks=[visualization_task])

print("\n🤖 Force-Generating Chart...\n")
result = crew.kickoff()
print(f"\n✅ RESULT: {result}")