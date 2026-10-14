# Echo Agent: The AI Podcaster

Echo Agent is a multi-agent [CrewAI](https://www.crewai.com/) pipeline that finds today's top AI news headline, turns it into a short podcast greeting, and speaks it aloud with ElevenLabs.

## Objective

I built this project to show that one person can produce a podcast clip without recording audio or doing the research by hand. The goal is a "digital twin" host that can research a topic, write a script, and speak it.

## Problem Statement

- **Creative burnout:** It is hard to come up with new ideas every day.
- **Complexity:** Setting up a studio, recording, and editing takes a lot of time.
- **Consistency:** Many podcasters quit because they cannot keep up with the schedule.

## Solution

Echo Agent is an agentic system: instead of one program following a list of commands, a small crew of agents each does one job and passes its result to the next.

## How It Works

The crew runs in sequence:

| Agent | Role | Output |
| --- | --- | --- |
| News Scout | Searches the web (Serper.dev) for the biggest AI news story of the day | One AI news headline |
| Writer | Turns the headline into a friendly podcast greeting | A 5-word greeting |
| Chief Editor | Checks that the final script is under 30 characters | The final script |

After the crew finishes, the script is sent to ElevenLabs, which speaks it using the voice set in `VOICE_ID`.

**Pipeline:**

1. The News Scout finds today's top AI headline.
2. The Writer turns the headline into a short greeting.
3. The Chief Editor trims the script to under 30 characters.
4. ElevenLabs converts the script to speech and saves `final_episode.mp3`.
5. The script and a timestamp are appended to `production_log.txt`.
6. `index.html` is regenerated as a web dashboard with the script and an audio player.

## Tech Stack

- **Python:** the language of the whole project
- **CrewAI:** orchestrates the agents and tasks
- **Google Gemini** (`gemini-flash-latest`, through CrewAI's `LLM` class): provides the language model
- **Serper.dev:** gives the News Scout live web search
- **ElevenLabs API:** text-to-speech (`eleven_multilingual_v2` model)
- **python-dotenv:** loads API keys from a `.env` file

## Setup

### Prerequisites

- Python 3
- API keys for [Google Gemini](https://aistudio.google.com/), [Serper.dev](https://serper.dev/), and [ElevenLabs](https://elevenlabs.io/)
- An ElevenLabs voice ID

### Installation

1. Clone the repository and open the folder:

   ```bash
   git clone https://github.com/sharmi-panda/Echo-Agent---The-AI-Podcaster.git
   cd Echo-Agent---The-AI-Podcaster
   ```

2. Install the dependencies:

   ```bash
   pip install crewai crewai-tools elevenlabs python-dotenv
   ```

3. Create a file named `.env` in the project folder and add your keys:

   ```text
   GEMINI_API_KEY=your_gemini_key
   SERPER_API_KEY=your_serper_key
   ELEVEN_API_KEY=your_elevenlabs_key
   VOICE_ID=your_elevenlabs_voice_id
   ```

   Never commit the `.env` file. Add it to `.gitignore`.

## Usage

Run the main script:

```bash
python final_podcast.py
```

The terminal prints each step as it runs. When it finishes, you will find:

- `final_episode.mp3`: the generated audio
- `production_log.txt`: a log of every script and when it was created
- `index.html`: open it in a browser to see the script and play the audio

## Troubleshooting

- **Rate limit error (429):** The crew is limited to one request per minute (`max_rpm=1`) to avoid this. Wait a minute and run the script again.
- **"VOICE ERROR" in the terminal:** Check that `ELEVEN_API_KEY` and `VOICE_ID` in your `.env` file are correct.

## Current Scope

The script currently produces a short greeting of under 30 characters. Longer, full-length episodes are a future goal.

## Future Goals

- Add "guest agents" for simulated interviews
- Post to social media automatically
- Generate background music that matches the mood of the script
