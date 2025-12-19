import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# 1. Define the Analyst
big_data_analyst = Agent(
    role='Lead Healthcare Analyst',
    goal='Process 1M+ row datasets efficiently to find financial trends.',
    backstory='You are specialized in "Payment Integrity". You look for large gaps between what Providers bill and what they get paid.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# 2. Define the Task
# We instruct the agent to use 'parse_dates' for speed and clean in-memory.
analysis_task = Task(
    description="""
    I have a 1-million row file named 'outpatient.csv'.
    Write and execute Python code to:
    
    1. LOAD: Read the CSV. Use `parse_dates=['Service_Date']` to load dates faster.
    2. CLEAN: Fill missing 'Modifier' values with the string "None".
    3. ENGINEER: Create a new column 'Write_Off' = 'Billed_Amount' - 'Paid_Amount'.
    4. ANALYZE: Group by 'Provider_ID'. Calculate the SUM of 'Billed_Amount', 'Paid_Amount', and 'Write_Off'.
    5. RANK: Sort the results by 'Billed_Amount' descending (highest first) and take the top 5.
    6. REPORT: Print a neat table of these Top 5 Providers showing their Total Billed, Total Paid, and Collection Rate (Paid / Billed * 100).
    """,
    expected_output="A table of the Top 5 Providers by Billed Amount with their collection rates.",
    agent=big_data_analyst
)

# 3. Run the Crew
crew = Crew(agents=[big_data_analyst], tasks=[analysis_task])

print("\n🤖 Crunching 1 Million Rows... (This may take 30-60 seconds)...\n")
result = crew.kickoff()
print(f"\n✅ PROFITABILITY REPORT:\n{result}")