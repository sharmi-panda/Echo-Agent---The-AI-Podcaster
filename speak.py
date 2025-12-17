import os
from elevenlabs.client import ElevenLabs

# 1. Initialize the "Voice Box"
client = ElevenLabs(
  api_key="sk_3c14e2bd9abe7b683a01b9f9b6c77ba104bd256dd5420414" 
)

# 2. Tell the robot what to say and which voice to use
audio = client.text_to_speech.convert(
    text="Hey there! I am now a digital podcaster. My assembly line is working!",
    voice_id="ReR9IDlPZjMjNqMDIRSR",
    model_id="eleven_multilingual_v2", # This model sounds the most human
    output_format="mp3_44100_128"
)

# 3. Save the voice to a file you can listen to
with open("my_first_podcast.mp3", "wb") as f:
    for chunk in audio:
        if chunk:
            f.write(chunk)

print("Success! Your audio file is saved as 'my_first_podcast.mp3'")