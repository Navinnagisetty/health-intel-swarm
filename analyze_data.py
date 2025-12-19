import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
MY_MODEL_NAME = "gemini-flash-latest"

# 1. Setup Brain
llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)

# 2. Setup Tool
code_tool = CodeInterpreterTool(unsafe_mode=True)

# 3. Define the Analyst Agent
analyst = Agent(
    role='Senior Financial Analyst',
    goal='Derive insights from healthcare financial data.',
    backstory='You are an expert at finding cost drivers in medical datasets. You summarize complex numbers into clear actionable tables.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# 4. Define the Analysis Task
analysis_task = Task(
    description="""
    I have a file named 'clean_beneficiary_2024.csv'.
    Write and execute Python code to:
    1. Load the file.
    2. Group the data by 'Age_Group'.
    3. Calculate the SUM of 'Total_Claims_Paid' for each group.
    4. Calculate the AVERAGE (Mean) 'Total_Claims_Paid' for each group.
    5. Print a text-based summary table sorted by the highest Total Cost.
    6. Answer the question: "Which age group is the most expensive?"
    """,
    expected_output="A summary table of costs by age group and a final text answer.",
    agent=analyst
)

# 5. Run the Crew
crew = Crew(agents=[analyst], tasks=[analysis_task])

print("\n🤖 Analyst is crunching the numbers...\n")
result = crew.kickoff()
print(f"\n✅ FINANCIAL REPORT:\n{result}")