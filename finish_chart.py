import os
import time
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
# We stick to the model that works, just running it slower (one agent)
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
code_tool = CodeInterpreterTool(unsafe_mode=True)

# --- THE VISUALIZER ---
visualizer = Agent(
    role='Strict Visualization Officer',
    goal='Generate image files using Python code.',
    backstory='You are a code-first agent. You create charts from CSVs.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# --- THE TASK ---
visualization_task = Task(
    description="""
    I have a file named 'final_top_providers.csv' in the CURRENT directory.
    
    1. Read the CSV using Pandas.
    2. Define X as the first column (Provider ID) and Y as the second column (Money).
       HINT: Use `df.iloc[:, 0]` and `df.iloc[:, 1]` to be safe against column name typos.
    3. Create a Bar Chart.
    4. Save it as 'final_report_chart.png'.
    5. Verify the file exists on disk using `os.path.abspath`.
    """,
    expected_output="The verification message containing the absolute path of the png file.",
    agent=visualizer
)

# --- RUN THE CREW ---
crew = Crew(agents=[visualizer], tasks=[visualization_task], verbose=True)

print("\n🤖 Resuming Pipeline: Visualizer Only...\n")
result = crew.kickoff()
print(f"\n✅ FINAL RESULT:\n{result}")