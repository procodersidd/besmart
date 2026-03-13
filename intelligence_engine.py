import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from langchain_google_genai import ChatGoogleGenerativeAI
from cloud_tool import save_to_cloud # IMPORTING YOUR SEPARATE FILE

# --- AUTHENTICATION ---
os.environ["GOOGLE_API_KEY"] = "AIzaSyAX008Hp4lj26WUB-FuxDfkwJ6XICJizpk"

os.environ["SERPER_API_KEY"] = "533f59ef8613a6d7733b31fafe39310d47a44fc0" # Add your Serper key here

os.environ["SUPABASE_URL"] = "https://wlayjqoaofcwkzavctfh.supabase.co"

os.environ["SUPABASE_KEY"] = "sb_publishable_lQx5zbupUfHw6zBqhFMZFQ_JzQheqTe"

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5)
search_tool = SerperDevTool()

# --- THE ELITE AGENTS ---
historian = Agent(
    role='Lead Historian',
    goal='Find deep historical parallels and patterns.',
    backstory='A scholar who avoids surface-level news to find the "long-view" of history.',
    tools=[search_tool],
    llm=llm
)

critic = Agent(
    role='Logic Auditor',
    goal='Challenge assumptions and find flaws in the historical analysis.',
    backstory='A master of red-teaming who ensures the report isn\'t biased or lazy.',
    llm=llm
)

philosopher = Agent(
    role='Intelligence Architect',
    goal='Synthesize findings into a Future Manifest and save to the cloud.',
    backstory='A visionary writer who bridges the gap between past facts and future possibilities.',
    tools=[save_to_cloud],
    llm=llm,
    verbose=True
)

# --- THE ORCHESTRATED WORKFLOW ---
def run_perfected_analysis(topic):
    task1 = Task(
        description=f"Research the historical roots of '{topic}'. List 2 parallels with dates.",
        agent=historian,
        expected_output="A documented historical context report."
    )
    
    task2 = Task(
        description="Audit the historical report for logic gaps. Provide a 'Devil's Advocate' view.",
        agent=critic,
        context=[task1],
        expected_output="A critical feedback memo."
    )
    
    task3 = Task(
        description=(
            f"1. Write the final 700-word Intelligence Manifest for '{topic}'.\n"
            f"2. Use the DatabaseWriter tool to archive the final version to the cloud."
        ),
        agent=philosopher,
        context=[task1, task2],
        expected_output="Confirmation of cloud storage and the final text."
    )

    crew = Crew(
        agents=[historian, critic, philosopher],
        tasks=[task1, task2, task3],
        process=Process.sequential,
        memory=True # This enables the "Long Term Memory" feature
    )
    
    return crew.kickoff()

if __name__ == "__main__":
    query = input("\n🏛️ [INQUIRY] Enter topic for deep analysis: ")
    result = run_perfected_analysis(query)
    print(f"\nRESULT:\n{result}")