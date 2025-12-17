from elevenlabs.client import ElevenLabs
from elevenlabs import play

# 1. Initialize the Client (The Toolbox)
client = ElevenLabs(
  api_key="sk_3c14e2bd9abe7b683a01b9f9b6c77ba104bd256dd5420414" # Put your key inside the quotes
)

# 2. Use the "convert" tool instead of "generate"
audio = client.text_to_speech.convert(
    text="Hello! The assembly line is fixed and working.",
    voice_id="ReR9IDlPZjMjNqMDIRSR",
    model_id="eleven_multilingual_v2"
)