from crewai import Agent, Task, Crew
import os
import sys
import io

# Force stdout to use UTF-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Replace the text inside the quotes with your actual OpenAI API Key
os.environ["GEMINI_API_KEY"] = "AIzaSyB6699DasFyp6p3Uj3wNnrMvuL96e7Mh2A"

# --- 1. Define the Researcher Agent ---
researcher = Agent(
  role='Tech News Researcher',
  goal='Find the 3 most exciting news stories about AI this week.',
  backstory='You are an expert journalist who knows how to find the "wow" factor.',
  verbose=True # This lets you see the agent "thinking" in the terminal
)

# --- 2. Define the Scriptwriter Agent ---
writer = Agent(
  role='Podcast Scriptwriter',
  goal='Write a 2-minute podcast script in a casual, friendly tone.',
  backstory='You are a famous podcaster. You use phrases like "Yo, what is up!" and "Check this out."',
  verbose=True
)

# --- 3. Give them Tasks ---
task1 = Task(
    description="Search for AI news and find the 'wow' factor.",
    expected_output="A bulleted list of the top 5 most significant AI news stories from the past 24 hours.",
    agent=researcher
)
task2 = Task(
    description="Write a script based on the news. Focus on making it engaging and use catchy hooks.",
    expected_output="A full podcast script in markdown format, including an introduction, three main news segments, and a closing.",
    agent=writer
)

# --- 4. Put them to work together (The Crew) ---
my_podcast_crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=False  # This hides the emojis and logs that are causing the crash

)

result = my_podcast_crew.kickoff()
print(result)