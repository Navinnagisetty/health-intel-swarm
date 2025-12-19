import os
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import FileReadTool

# --- CONFIGURATION ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyAzB-1NhrNN2jGWWzWbGUGtBXrUnRgJ7zo"
MY_MODEL_NAME = "gemini-flash-latest"

llm = ChatGoogleGenerativeAI(model=MY_MODEL_NAME)
file_tool = FileReadTool(file_path='suspicious_providers.csv')

# --- THE AGENT ---
investigator = Agent(
    role='Senior Fraud Investigator',
    goal='Summarize suspicious billing patterns for executive review.',
    backstory='You are a compliance officer. You analyze outliers and write clear, urgent warnings.',
    llm=llm,
    tools=[file_tool],
    verbose=True,
    allow_code_execution=False
)

# --- THE TASK ---
report_task = Task(
    description="""
    1. Read 'suspicious_providers.csv'.
    2. Identify the Provider with the highest Z-Score.
    3. Write a short, formal email to the CEO.
       - Subject: URGENT: Anomaly Detected - Provider [ID]
       - Body: Explain that this provider's average bill is significantly higher than the global average. Mention their Z-Score and Total Revenue.
       - Recommendation: Suggest an immediate audit.
    """,
    expected_output="A formal email draft.",
    agent=investigator
)

# --- RUN THE CREW ---
crew = Crew(agents=[investigator], tasks=[report_task], verbose=True)

print("\n🤖 Investigator is reviewing the evidence...\n")
result = crew.kickoff()
print(f"\n✅ FINAL EMAIL DRAFT:\n{result}")