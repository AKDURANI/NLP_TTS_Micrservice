import os
from pydub import AudioSegment
from TTS.api import TTS
from app.config import TEMP_AUDIO_DIR, FINAL_AUDIO_PATH, SPEAKER_WAV_PATH
from app.utils import extract_text_from_pdf, segment_sentences
import torch.serialization
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Initialize TTS model with safe_globals context
with torch.serialization.safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs]):
    tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

def generate_audio(pdf_path, page_range=None):
    """
    Generate audio from PDF text
    
    Args:
        pdf_path: Path to the PDF file
        page_range: Tuple of (start_page, end_page) - Optional
        
    Returns:
        Path to the generated audio file
    """
    # Extract text from PDF for the given page range
    if page_range:
        # Make sure to pass page_range as a named parameter
        text = extract_text_from_pdf(pdf_path, page_range=page_range)
    else:
        text = extract_text_from_pdf(pdf_path)
    
    # Segment the extracted text into individual sentences
    sentences = segment_sentences(text)
    
    # Create the output directory if it doesn't exist
    os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
    
    # Initialize an empty AudioSegment for combining audio
    combined_audio = None
    
    # Flag to track if any valid audio was generated
    valid_audio_generated = False
    
    # Iterate over sentences and generate audio for each
    for idx, sentence in enumerate(sentences):
        try:
            audio_path = os.path.join(TEMP_AUDIO_DIR, f"line_{idx+1}.wav")
            
            # Generate speech for the sentence and save to temporary file
            tts.tts_to_file(
                text=sentence,
                file_path=audio_path,
                speaker_wav=SPEAKER_WAV_PATH,
                language="en"
            )
            
            # Check if the audio file was generated successfully
            if os.path.exists(audio_path) and os.path.getsize(audio_path) > 0:
                # Load the generated audio
                audio_seg = AudioSegment.from_wav(audio_path)
                
                # Initialize combined_audio if this is the first valid segment
                if combined_audio is None:
                    combined_audio = audio_seg
                else:
                    # Append the audio segment and add some silence between sentences
                    combined_audio = combined_audio + AudioSegment.silent(duration=400) + audio_seg
                
                valid_audio_generated = True
                print(f" > Text splitted to sentences.\n['{sentence}']")
            else:
                print(f"⚠️ Audio file for sentence {idx+1} not found or empty.")
        except Exception as e:
            print(f"⚠️ Skipping sentence {idx+1} due to error: {e}")
    
    # Export the combined audio to the final audio file path
    if valid_audio_generated and combined_audio is not None:
        combined_audio.export(FINAL_AUDIO_PATH, format="mp3")
        print(f"✅ Audio file saved as {FINAL_AUDIO_PATH}")
    else:
        print("❌ No valid audio generated.")
    
    return FINAL_AUDIO_PATH