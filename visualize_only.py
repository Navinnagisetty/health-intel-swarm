import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
# We switch to the standard 1.5 Flash model which has higher limits
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# --- THE VISUALIZER AGENT ---
visualizer = Agent(
    role='Chief Data Visualization Officer',
    goal='Create compelling charts from summary data.',
    backstory='You are a master of Matplotlib and Seaborn. You turn boring CSVs into beautiful .png images.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# --- THE TASK ---
visualization_task = Task(
    description="""
    I have a file named 'top_providers.csv' containing 'Provider_ID' and 'Billed_Amount'.
    1. Read this file.
    2. Create a Bar Chart using Python (Seaborn/Matplotlib).
       - X-Axis: Provider_ID
       - Y-Axis: Billed_Amount
       - Title: 'Top 5 Providers by Revenue'
       - Color: 'skyblue'
    3. Save the chart as an image file named 'provider_revenue.png'.
    4. Print "Chart Saved Successfully" when done.
    """,
    expected_output="Confirmation that provider_revenue.png has been saved.",
    agent=visualizer
)

# --- RUN THE CREW ---
crew = Crew(agents=[visualizer], tasks=[visualization_task])

print("\n🤖 Generating Chart using gemini-1.5-flash...\n")
result = crew.kickoff()
print(f"\n✅ RESULT: {result}")