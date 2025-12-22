import os, sys, io
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM, Process
from crewai_tools import SerperDevTool
from elevenlabs.client import ElevenLabs
from datetime import datetime
os.environ['NO_PROXY'] = '*'

# Step 1: Fix Windows Emoji Crashes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
load_dotenv()

# THE FIX: Updated Gemini Initialization
# Using "gemini/gemini-1.5-flash" is the standard for the LiteLLM bridge
gemini_llm = LLM(
    model="gemini/gemini-flash-latest",
    api_key=os.getenv("GEMINI_API_KEY")
)
print("Step 1: Environment & Gemini LLM Loaded")

# Step 2: Set Tools & Keys
search_tool = SerperDevTool()
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# Step 3: Setup Agents (Using the same Gemini brain)
researcher = Agent(
    role='News Scout', 
    goal='Find the headline of 1 major AI news story from today.', 
    tools=[search_tool], 
    backstory='A pro journalist. You always provide search queries in a clear dictionary format.',
    llm=gemini_llm,
    allow_delegation=False, # This stops agents from talking too much to each other
    verbose=True
)

writer = Agent(
    role='Writer', 
    goal='Turn a headline into a catchy 5-word podcast greeting.', 
    backstory='A casual podcaster who sounds human, not like a robot.',
    llm=gemini_llm,
    verbose=True
)

editor = Agent(
    role='Chief Editor',
    goal='Ensure the final script is under 30 characters.',
    backstory='A master of brevity who cuts out every unnecessary word.',
    llm=gemini_llm,
    verbose=True
)

# Step 4: Define the Pipeline Tasks
task1 = Task(
    description="Find the single biggest AI headline today.", 
    agent=researcher, 
    expected_output="A short AI news headline."
)

task2 = Task(
    description="Convert the news headline into a friendly 5-word intro.", 
    agent=writer, 
    expected_output="A 5-word podcast greeting."
)

task3 = Task(
    description="Review the script. It MUST be under 30 characters. Example: 'AI news is here. Enjoy!'", 
    agent=editor, 
    expected_output="A final script under 30 characters."
)

# THE FIX: Added max_rpm=2 to prevent the 429 Rate Limit error
my_podcast_crew = Crew(
    agents=[researcher, writer, editor],
    tasks=[task1, task2, task3],
    max_rpm=1, 
    process=Process.sequential,
    verbose=True
)
print("Step 2: Agents & Speed Governor Ready")

# Step 5: Run the Process
print("Step 3: Starting AI Research...")
podcast_output = my_podcast_crew.kickoff()
final_script = str(podcast_output)
print(f"Final Script for Voice: {final_script}")

# Step 6: Generate Audio
print("Starting Voice Synthesis...")
try:
    client = ElevenLabs(api_key=os.getenv("ELEVEN_API_KEY"))
    audio_stream = client.text_to_speech.convert(
        text=final_script,
        voice_id=os.getenv("VOICE_ID"),
        model_id="eleven_multilingual_v2"
    )
    
    # Consolidate the audio data
    audio_bytes = b"".join(list(audio_stream))
    
    with open("final_episode.mp3", "wb") as f:
        f.write(audio_bytes)
    print(f"SUCCESS! MP3 generated. Size: {len(audio_bytes)} bytes")

except Exception as e:
    print(f"VOICE ERROR: {e}")

# Step 7: Data Logging
try:
    with open("production_log.txt", "a", encoding='utf-8') as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"\n--- Episode Created: {timestamp} ---\n")
        log_file.write(f"Final Script: {final_script}\n")
        log_file.write("-" * 40 + "\n")
    print("Step 5: Log Updated.")
except Exception as e:
    print(f"Error saving log: {e}")

# Step 8: Update "Cyber-Glass" Dashboard
print("Step 6: Updating Web Dashboard...")
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Podcast Studio</title>
    <style>
        :root {{
            --primary: #00f2fe; --secondary: #4facfe; --bg: #0a0b10;
        }}
        body {{ 
            font-family: 'Inter', sans-serif; background: var(--bg); color: white; 
            display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0;
        }}
        .glass-panel {{
            background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px;
            padding: 40px; width: 90%; max-width: 500px; text-align: center;
        }}
        .script-box {{
            background: rgba(0,0,0,0.3); padding: 15px; border-radius: 12px;
            font-style: italic; color: #cbd5e1; margin: 20px 0; border-left: 4px solid var(--primary);
        }}
        audio {{ width: 100%; filter: invert(100%) hue-rotate(180deg) brightness(1.5); }}
        .bar {{ width: 4px; background: var(--primary); border-radius: 2px; transition: height 0.2s; }}
        .visualizer {{ display: flex; justify-content: center; align-items: flex-end; height: 40px; gap: 3px; }}
    </style>
</head>
<body>
    <div class="glass-panel">
        <p style="color: var(--secondary); font-size: 12px; letter-spacing: 2px;">● SYSTEM LIVE</p>
        <h1>AI Studio</h1>
        <div class="script-box">"{final_script}"</div>
        <audio id="audioPlayer" controls>
            <source src="final_episode.mp3?t={datetime.now().timestamp()}" type="audio/mpeg">
        </audio>
        <div class="visualizer" id="visualizer"></div>
    </div>
    <script>
        const visualizer = document.getElementById('visualizer');
        for (let i = 0; i < 20; i++) {{
            const bar = document.createElement('div');
            bar.className = 'bar';
            bar.style.height = '10%';
            visualizer.appendChild(bar);
        }}
        const player = document.getElementById('audioPlayer');
        player.onplay = () => {{
            setInterval(() => {{
                document.querySelectorAll('.bar').forEach(bar => {{
                    bar.style.height = Math.random() * 100 + '%';
                }});
            }}, 150);
        }};
    </script>
</body>
</html>
"""
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
print("Step 8: Dashboard Live! Check index.html.")