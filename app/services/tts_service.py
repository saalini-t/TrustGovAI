"""
Text-to-Speech Service
Converts text responses to audio in multiple languages
"""

from gtts import gTTS
import os
import uuid
import tempfile

# Language code mapping for gTTS
GTTS_LANGUAGE_CODES = {
    'en': 'en',
    'hi': 'hi',
    'ta': 'ta',
    'te': 'te',
    'kn': 'kn',
    'ml': 'ml',
    'bn': 'bn',
    'mr': 'mr',
    'gu': 'gu',
    'pa': 'pa'
}

# Directory to store temporary audio files
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "audio_cache")

# Create audio directory if it doesn't exist
os.makedirs(AUDIO_DIR, exist_ok=True)


def text_to_speech(text: str, language: str = 'en') -> str:
    """
    Convert text to speech and return the audio file path.
    
    Args:
        text: The text to convert to speech
        language: Language code (en, hi, ta, te, etc.)
    
    Returns:
        Path to the generated audio file
    """
    try:
        # Map to gTTS language code
        gtts_lang = GTTS_LANGUAGE_CODES.get(language, 'en')
        
        # Generate unique filename
        filename = f"tts_{uuid.uuid4().hex[:8]}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        # Create TTS
        print(f"🔊 Generating speech in {gtts_lang}: '{text[:50]}...'")
        tts = gTTS(text=text, lang=gtts_lang, slow=False)
        tts.save(filepath)
        
        print(f"✅ Audio saved: {filepath}")
        return filepath
        
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return None


def cleanup_old_audio_files(max_age_seconds: int = 3600):
    """Clean up audio files older than max_age_seconds"""
    import time
    
    try:
        current_time = time.time()
        for filename in os.listdir(AUDIO_DIR):
            filepath = os.path.join(AUDIO_DIR, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    print(f"🗑️ Cleaned up old audio: {filename}")
    except Exception as e:
        print(f"⚠️ Cleanup error: {e}")
