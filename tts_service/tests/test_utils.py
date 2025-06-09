# Modified test_utils.py
from app.utils import segment_sentences
from app.core import generate_audio
from unittest.mock import patch, MagicMock
import pytest
from pydub import AudioSegment
import os

def test_sentence_segmentation():
    sample = "This is sentence one. This is sentence two."
    sentences = segment_sentences(sample)
    assert isinstance(sentences, list)
    assert len(sentences) == 2
    assert sentences[0] == "This is sentence one."
    assert sentences[1] == "This is sentence two."


# Mock the extract_text_from_pdf and segment_sentences functions to focus on testing generate_audio
@pytest.fixture
def mock_pdf_processing():
    with patch('app.core.extract_text_from_pdf') as mock_text:
        with patch('app.core.segment_sentences') as mock_segment:
            # Mock the text extraction to return a predefined text
            mock_text.return_value = "This is sentence one. This is sentence two."
            
            # Mock the sentence segmentation
            mock_segment.return_value = ["This is sentence one.", "This is sentence two."]
            yield mock_text, mock_segment

# Test case for generate_audio function
def test_generate_audio(mock_pdf_processing):
    mock_text, mock_segment = mock_pdf_processing

    # Patch the TTS instance and the audio export function
    with patch('app.core.TTS') as mock_tts:
        mock_tts_instance = MagicMock()
        mock_tts.return_value = mock_tts_instance
        mock_tts_instance.tts_to_file = MagicMock()
        
        # Mock file system operations
        with patch('os.path.exists', return_value=True), \
             patch('os.path.getsize', return_value=1000), \
             patch('os.makedirs'):
            
            # Create a proper mock for AudioSegment with necessary attributes
            mock_audio = MagicMock()
            mock_audio.channels = 2
            mock_audio.frame_rate = 44100
            mock_audio.sample_width = 2
            # Make the + operator work with our mock
            mock_audio.__add__.return_value = mock_audio
            
            # Mock AudioSegment methods
            with patch('pydub.AudioSegment.from_wav', return_value=mock_audio), \
                 patch('pydub.AudioSegment.silent', return_value=mock_audio), \
                 patch.object(mock_audio, 'export'):
                
                # Call the function to test
                pdf_path = "C:/Users/mali/Desktop/NLP/NLP_Project/NLP_Project/RichDadPoorDad.pdf"
                audio_path = generate_audio(pdf_path, page_range=(1, 2))

                # Assertions to verify the behavior
                mock_text.assert_called_once_with(pdf_path, page_range=(1, 2))  # Ensure text extraction was called
                mock_segment.assert_called_once()  # Ensure segmentation was called
                assert mock_audio.export.call_count == 1  # Ensure audio export was called
                assert audio_path is not None  # Check if a path was returned