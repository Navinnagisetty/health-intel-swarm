import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo"
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# --- AGENT 1: THE ANALYST ---
analyst = Agent(
    role='Lead Healthcare Analyst',
    goal='Extract top trends from large datasets.',
    backstory='You are an expert at summarizing millions of rows into concise insights.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# --- AGENT 2: THE VISUALIZER ---
visualizer = Agent(
    role='Chief Data Visualization Officer',
    goal='Create compelling charts from summary data.',
    backstory='You are a master of Matplotlib and Seaborn. You turn boring CSVs into beautiful .png images.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# --- TASK 1: CRUNCH THE NUMBERS ---
# This task reads the BIG file and saves a SMALL summary file.
analysis_task = Task(
    description="""
    1. Read 'outpatient.csv' (use parse_dates=['Service_Date']).
    2. Group by 'Provider_ID' and sum the 'Billed_Amount'.
    3. Sort descending and keep only the TOP 5 Providers.
    4. Save this dataframe to a file named 'top_providers.csv'. 
    5. The file must have columns: 'Provider_ID' and 'Billed_Amount'.
    """,
    expected_output="Confirmation that top_providers.csv has been saved.",
    agent=analyst
)

# --- TASK 2: DRAW THE PICTURE ---
# This task reads the SMALL summary file and creates an image.
visualization_task = Task(
    description="""
    1. Read the file 'top_providers.csv'.
    2. Create a Bar Chart using Python (Matplotlib/Seaborn).
       - X-Axis: Provider_ID
       - Y-Axis: Billed_Amount
       - Title: 'Top 5 Providers by Revenue'
       - Color: 'skyblue'
    3. Save the chart as an image file named 'provider_revenue.png'.
    """,
    expected_output="Confirmation that provider_revenue.png has been saved.",
    agent=visualizer,
    context=[analysis_task] # This tells Agent 2 to wait for Agent 1
)

# --- RUN THE CREW ---
crew = Crew(agents=[analyst, visualizer], tasks=[analysis_task, visualization_task])

print("\n🤖 The Visual Swarm is starting...\n")
result = crew.kickoff()
print(f"\n✅ FINAL RESULT:\n{result}")