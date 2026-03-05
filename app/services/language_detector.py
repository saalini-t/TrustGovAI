"""
Language Detection Service
Detects language and identifies mixed languages (Tanglish, Hinglish, etc.)
"""

from langdetect import detect, DetectorFactory
import re

# Make langdetect deterministic
DetectorFactory.seed = 0

# Common words in Indian languages written in English (transliteration)
TAMIL_MARKERS = ['enna', 'epdi', 'yenna', 'panna', 'vaanga', 'ponga', 'iruku', 'illa', 'thaan', 'romba', 'nalla', 'kudukum', 'varum', 'aana', 'aagum', 'pannunga', 'sollunga', 'paaru', 'veedu', 'panam', 'velai', 'oru', 'indha', 'antha', 'enga', 'unga', 'naan', 'nee', 'avanga', 'ivanga', 'kidaikum', 'venum', 'achu', 'irukku', 'illai', 'scheme', 'apply', 'eligibility']
HINDI_MARKERS = ['kya', 'kaise', 'kahan', 'kaun', 'kyun', 'hai', 'hain', 'tha', 'thi', 'kar', 'karo', 'karna', 'milta', 'milega', 'dena', 'lena', 'aur', 'lekin', 'mein', 'paisa', 'kaam', 'ghar', 'zaruri', 'chahiye', 'hoga', 'hoti', 'kab', 'kitna', 'batao', 'bolo', 'yojana', 'sarkari', 'labh']
TELUGU_MARKERS = ['enti', 'ela', 'cheppandi', 'ivvandi', 'undi', 'ledu', 'kavali', 'cheyali', 'vastundi', 'emiti', 'evaru', 'ekkada']

def detect_language(text):
    """
    Detect language with support for mixed languages.
    Returns language code: 'en', 'hi', 'ta', 'te', etc.
    """
    try:
        text_lower = text.lower()
        words = text_lower.split()
        
        # Check for Tamil markers (Tanglish) - check first as it's common
        tamil_count = sum(1 for marker in TAMIL_MARKERS if marker in text_lower)
        
        # Check for Hindi markers (Hinglish)
        hindi_count = sum(1 for marker in HINDI_MARKERS if marker in text_lower)
        
        # Check for Telugu markers
        telugu_count = sum(1 for marker in TELUGU_MARKERS if marker in text_lower)
        
        # Prioritize based on marker count
        if tamil_count >= 1:
            print(f"🔍 Detected Tamil markers: {tamil_count}")
            return 'ta'
        
        if hindi_count >= 1:
            print(f"🔍 Detected Hindi markers: {hindi_count}")
            return 'hi'
        
        if telugu_count >= 1:
            print(f"🔍 Detected Telugu markers: {telugu_count}")
            return 'te'
        
        # Use langdetect for pure languages
        detected = detect(text)
        
        # Map common misdetections
        if detected in ['tl', 'id', 'ms', 'de', 'nl', 'af']:
            # These are often misdetections of Indian languages
            if tamil_count > 0:
                return 'ta'
            elif hindi_count > 0:
                return 'hi'
            # Default to English if can't determine
            return 'en'
        
        return detected
        
    except Exception as e:
        print(f"⚠️ Language detection error: {e}")
        return "en"


def get_language_name(lang_code):
    """Get human-readable language name"""
    names = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil', 
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'bn': 'Bengali',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'pa': 'Punjabi',
    }
    return names.get(lang_code, lang_code.upper())