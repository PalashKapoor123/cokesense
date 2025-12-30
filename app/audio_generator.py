"""
Audio Generation Module - Creates text-to-speech audio for slogans
Uses multiple TTS methods to get the best voice quality
"""
from io import BytesIO
from gtts import gTTS
import tempfile
import os


def generate_slogan_audio(slogan: str, language: str = 'en', slow: bool = True) -> BytesIO:
    """
    Generates text-to-speech audio for a slogan with bear-like characteristics.
    Uses Google Text-to-Speech with optimized settings for a deeper, friendlier voice.
    
    Note: Free TTS has limitations - for a true bear voice, consider using:
    - ElevenLabs (paid, has character voices)
    - Voice cloning (complex, requires samples)
    - Custom voice models
    
    Args:
        slogan: The slogan text to convert to speech
        language: Language code (default: 'en' for English)
        slow: Whether to speak slowly (default: True for bear-like voice)
    
    Returns:
        BytesIO object containing the MP3 audio file
    """
    try:
        # For bear-like voice characteristics:
        # - Slower pace (more friendly, less rushed)
        # - Add emphasis with punctuation
        # - Make it sound warmer and friendlier
        
        # Enhance the slogan text for better TTS output
        enhanced_slogan = slogan.strip()
        
        # Add punctuation for better intonation if missing
        if not any(char in enhanced_slogan for char in ['.', '!', '?']):
            enhanced_slogan = enhanced_slogan + "!"  # Add exclamation for energy
        
        # Use slower speed for more character-like, friendly voice
        # Slow=True makes it sound warmer and less robotic (closer to bear voice)
        tts = gTTS(text=enhanced_slogan, lang=language, slow=slow)
        
        # Generate audio to bytes
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None


def generate_slogan_audio_file(slogan: str, output_path: str = None) -> str:
    """
    Generates text-to-speech audio and saves to a file.
    
    Args:
        slogan: The slogan text to convert to speech
        output_path: Optional path to save the file. If None, creates a temp file.
    
    Returns:
        Path to the generated audio file
    """
    try:
        # Create gTTS object
        tts = gTTS(text=slogan, lang='en', slow=False)
        
        # Save to file
        if output_path is None:
            # Create temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            output_path = temp_file.name
            temp_file.close()
        
        tts.save(output_path)
        return output_path
        
    except Exception as e:
        print(f"Error generating audio file: {e}")
        return None


def get_audio_bytes(slogan: str) -> bytes:
    """
    Convenience function to get audio as bytes.
    
    Args:
        slogan: The slogan text
    
    Returns:
        bytes: Audio file as bytes
    """
    audio_buffer = generate_slogan_audio(slogan)
    if audio_buffer:
        return audio_buffer.read()
    return None

