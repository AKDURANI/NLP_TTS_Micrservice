import os

# Constants and paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_PATH = os.path.join(BASE_DIR, "assets", "RichDadPoorDad.pdf")
SPEAKER_WAV_PATH = os.path.join(BASE_DIR, "assets", "speaker.wav")
TEMP_AUDIO_DIR = os.path.join(BASE_DIR, "audio_outputs")
FINAL_AUDIO_PATH = os.path.join(BASE_DIR, "final_narration.mp3")

# Ensure output directory exists
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
