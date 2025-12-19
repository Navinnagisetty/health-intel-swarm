import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import CodeInterpreterTool

# --- 1. CONFIGURATION ---
# We use the key and model that successfully worked for you
os.environ["GOOGLE_API_KEY"] = "os.getenv("GOOGLE_API_KEY")"
MY_MODEL_NAME = "gemini-flash-latest"

# 2. Setup Brain
llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)

# 3. Setup Tool (The "Hands" of the Agent)
# unsafe_mode=True allows it to read/write files on your C: drive
code_tool = CodeInterpreterTool(unsafe_mode=True)

# 4. Define the Agent (The "Janitor")
data_engineer = Agent(
    role='Senior Data Engineer',
    goal='Clean and preprocess datasets using Python Pandas.',
    backstory='You are an expert data engineer. Your job is to detect dirty data (nulls, wrong types) and fix it programmatically.',
    llm=llm,
    tools=[code_tool],
    allow_code_execution=False, # We use the custom tool instead
    verbose=True
)

# 5. Define the Task (The "Work Order")
cleaning_task = Task(
    description="""
    I have a file named 'messy_sales_data.csv' in the current directory.
    Perform the following steps using Python code:
    1. Load the CSV file into a Pandas DataFrame.
    2. Check the 'Sales' column. It has string values "MISSING". Convert these to NaN, then fill them with the median value of the valid sales.
    3. Check the 'Product' column. Drop any rows where the Product is empty or null.
    4. Save the cleaned data to a new file named 'cleaned_sales_data.csv'.
    """,
    expected_output="A confirmation message saying the file has been saved, along with the first 5 rows of the clean dataframe.",
    agent=data_engineer
)

# 6. Run the Swarm
crew = Crew(agents=[data_engineer], tasks=[cleaning_task])

print("\n🤖 Data Engineer is starting work on messy_sales_data.csv...\n")
result = crew.kickoff()
print(f"\n✅ FINAL REPORT:\n{result}")