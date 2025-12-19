import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo"
MY_MODEL_NAME = "gemini-flash-latest"

# 1. Setup Brain
llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)

# 2. Setup Tool
code_tool = CodeInterpreterTool(unsafe_mode=True)

# 3. Define the Engineer Agent
engineer = Agent(
    role='Healthcare Data Engineer',
    goal='Clean and enrich healthcare datasets.',
    backstory='You specialize in preparing medical claims data for analysis. You are strict about data types.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# 4. Define the Task
# We give specific instructions based on your Inspector Report
cleaning_task = Task(
    description="""
    I have a file named 'beneficiary_2024.csv'. 
    Write and execute Python code to perform these cleaning steps:
    
    1. Load the CSV file.
    2. CLEANING: The 'Total_Claims_Paid' column has missing values. Fill all missing (NaN) values with 0.0.
    3. FORMATTING: Convert the 'Enrollment_Date' column to a proper Datetime object.
    4. ENGINEERING: Create a new column named 'Age_Group'. 
       - If Age < 65, label as 'Under 65'.
       - If Age is 65-75, label as '65-75'.
       - If Age > 75, label as 'Over 75'.
    5. SAVE: Save the result to 'clean_beneficiary_2024.csv'.
    6. VERIFY: Print the first 5 rows of the new file to prove the 'Age_Group' column exists.
    """,
    expected_output="A confirmation that the file was saved, and a printout of the first 5 rows.",
    agent=engineer
)

# 5. Run the Crew
crew = Crew(agents=[engineer], tasks=[cleaning_task])

print("\n🤖 Engineer is cleaning 'beneficiary_2024.csv'...\n")
result = crew.kickoff()
print(f"\n✅ ENGINEERING REPORT:\n{result}")