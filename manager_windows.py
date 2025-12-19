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

analyst = Agent(
    role='Lead Healthcare Analyst',
    goal='Extract top trends and SAVE them to the CURRENT DIRECTORY.',
    backstory='You are a code-first analyst. You NEVER use "/mnt/data". You always check the current folder path first.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

visualizer = Agent(
    role='Strict Visualization Officer',
    goal='Generate image files in the CURRENT DIRECTORY.',
    backstory='You are a code-first agent. You NEVER use "/mnt/data". You save files locally.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# --- TASKS ---

# Task 1: Analyze with EXPLICIT PATH instructions
task_analyze = Task(
    description="""
    CRITICAL: Do NOT use '/mnt/data'. Use the current working directory.
    
    1. Run this Python code FIRST to get the current path: `import os; print(os.getcwd())`
    2. Read 'outpatient.csv' (use parse_dates=['Service_Date']).
    3. Group by 'Provider_ID', sum 'Billed_Amount', sort descending, keep Top 5.
    4. Save to 'final_top_providers.csv' in the CURRENT directory.
    5. Verify file exists using `os.path.exists('final_top_providers.csv')`.
    """,
    expected_output="Confirmation that the CSV exists in the current folder.",
    agent=analyst
)

# Task 2: Visualize with EXPLICIT PATH instructions
task_visualize = Task(
    description="""
    CRITICAL: Do NOT use '/mnt/data'. Use the current working directory.
    
    1. Read 'final_top_providers.csv' from the CURRENT directory.
    2. Create a Bar Chart of Provider vs Billed Amount.
    3. Save it as 'final_report_chart.png' in the CURRENT directory.
    4. AFTER saving, run this Python check:
       `import os; print(f"VERIFIED IMAGE AT: {os.path.abspath('final_report_chart.png')}")`
    """,
    expected_output="The verification message containing the absolute path.",
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

print("\n🤖 Manager is running the Windows-Compatible Pipeline...\n")
result = crew.kickoff()
print(f"\n✅ FINAL REPORT:\n{result}")