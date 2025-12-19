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

# 3. Define the Inspector
inspector = Agent(
    role='Big Data Analyst',
    goal='Analyze large datasets efficiently.',
    backstory='You are an expert at handling large CSV files. You know how to check data structure without crashing memory.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False,
    verbose=True
)

# 4. Define the Task
# We added 'low_memory=False' instruction for the agent
inspection_task = Task(
    description="""
    I have a large file named 'outpatient.csv'.
    Write and execute Python code to:
    1. Load the file into a Pandas DataFrame. (Hint: Use pd.read_csv('outpatient.csv', low_memory=False))
    2. Print the Total Number of Rows and Columns.
    3. Print the List of Column Names.
    4. Check for any missing values (nulls) and print the count per column.
    5. Print the memory usage of the dataframe (df.info(memory_usage='deep')).
    """,
    expected_output="A summary report of the dataset structure and memory usage.",
    agent=inspector
)

# 5. Run the Crew
crew = Crew(agents=[inspector], tasks=[inspection_task])

print("\n🤖 Inspector is analyzing the 300MB 'outpatient.csv' file...\n")
result = crew.kickoff()
print(f"\n✅ BIG DATA REPORT:\n{result}")