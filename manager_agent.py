import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# --- AGENTS ---

# 1. The Analyst 
analyst = Agent(
    role='Lead Healthcare Analyst',
    goal='Extract top trends and SAVE them to CSV.',
    backstory='You are a code-first analyst. You do not speak until you have saved a CSV file.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# 2. The Visualizer (STRICT MODE)
visualizer = Agent(
    role='Strict Visualization Officer',
    goal='Generate image files using Python code. You never just "say" you did it.',
    backstory='You are a code-first agent. You do not speak until you have successfully executed Python code to save a .png file.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# 3. The Manager
manager = Agent(
    role='Project Manager',
    goal='Ensure files are actually created on disk.',
    backstory='You are a skeptic. You do not believe work is done until you see the file path.',
    llm=llm,
    verbose=True,
    allow_delegation=True 
)

# --- TASKS ---

# Task 1: Analyze
task_analyze = Task(
    description="""
    CRITICAL: You MUST use the 'Code Interpreter' tool.
    1. Read 'outpatient.csv' (use parse_dates=['Service_Date']).
    2. Group by 'Provider_ID' and sum 'Billed_Amount'.
    3. Sort descending and keep TOP 5.
    4. Save to 'final_top_providers.csv'.
    5. Print the absolute path of the saved file using python: print(os.path.abspath('final_top_providers.csv'))
    """,
    expected_output="Confirmation that the CSV was saved, including its file path.",
    agent=analyst
)

# Task 2: Visualize
task_visualize = Task(
    description="""
    CRITICAL: You MUST use the 'Code Interpreter' tool. Do not just answer.
    1. Read 'final_top_providers.csv'.
    2. Create a Bar Chart of Provider vs Billed Amount.
    3. Save it as 'final_report_chart.png'.
    4. AFTER saving, use Python to check if the file exists:
       `if os.path.exists('final_report_chart.png'): print("VERIFIED: File found at", os.path.abspath('final_report_chart.png'))`
    """,
    expected_output="The verification message containing the absolute path of the png file.",
    agent=visualizer,
    context=[task_analyze] 
)

# --- CREW ---
crew = Crew(
    agents=[analyst, visualizer],
    tasks=[task_analyze, task_visualize],
    process=Process.sequential,
    verbose=True
)

print("\n🤖 Manager is running the Hardened Pipeline...\n")
result = crew.kickoff()
print(f"\n✅ FINAL REPORT:\n{result}")