import os
import sys
import subprocess
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import FileReadTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo"
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
read_tool = FileReadTool(file_path='final_top_providers.csv')

# --- AGENT ---
coder = Agent(
    role='Python Scripter',
    goal='Write a standalone Python script to generate a chart.',
    backstory='You are a python expert. You do not execute code. You write .py files for the user to run.',
    llm=llm,
    tools=[read_tool],
    verbose=True,
    allow_code_execution=False 
)

# --- TASK ---
task_write_code = Task(
    description="""
    1. Read 'final_top_providers.csv'.
    2. Write a Python script named 'my_chart_script.py'.
    3. The script must:
       - Import pandas and matplotlib.pyplot.
       - Read 'final_top_providers.csv'.
       - Create a Bar Chart (Provider_ID vs Billed_Amount).
       - Save the chart as 'final_chart.png'.
       - Print "SUCCESS: final_chart.png saved."
    4. OUTPUT: Return ONLY the python script code. No markdown.
    """,
    expected_output="The python code string.",
    agent=coder
)

# --- RUN THE CREW ---
crew = Crew(agents=[coder], tasks=[task_write_code], verbose=True)

print("\n🤖 Agent is writing the code...\n")
result = crew.kickoff()

# --- THE MANUAL EXECUTION ---
print("\n📝 Saving Agent's code to 'my_chart_script.py'...")

# Clean up the output (remove markdown backticks if the agent added them)
cleaned_code = str(result).replace("```python", "").replace("```", "")

with open("my_chart_script.py", "w", encoding="utf-8") as f:
    f.write(cleaned_code)

print("🚀 Executing the script inside the VENV...")

# CRITICAL FIX: Use sys.executable to ensure we use the VENV python
try:
    subprocess.run([sys.executable, "my_chart_script.py"], check=True)
    print("\n✅ DONE! Check your folder for 'final_chart.png'")
except Exception as e:
    print(f"❌ Error running the generated script: {e}")