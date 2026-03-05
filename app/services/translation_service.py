"""
Multilingual Translation Service
Supports: Tamil, Hindi, Telugu, Kannada, Malayalam, Bengali, Marathi, Gujarati
Also handles mixed languages like Tanglish (Tamil+English) and Hinglish (Hindi+English)
"""

from deep_translator import GoogleTranslator
import re

# Language code mapping
LANGUAGE_CODES = {
    'en': 'english',
    'hi': 'hindi',
    'ta': 'tamil',
    'te': 'telugu',
    'kn': 'kannada',
    'ml': 'malayalam',
    'bn': 'bengali',
    'mr': 'marathi',
    'gu': 'gujarati',
    'pa': 'punjabi'
}

# Reverse mapping
LANGUAGE_NAMES_TO_CODES = {v: k for k, v in LANGUAGE_CODES.items()}


def translate_to_english(text, source_lang):
    """Translate text from any supported language to English"""
    
    # If already English or unknown, return as is
    if source_lang == 'en' or source_lang not in LANGUAGE_CODES:
        return text
    
    try:
        translator = GoogleTranslator(source=source_lang, target='en')
        translated = translator.translate(text)
        print(f"🌐 Translated from {LANGUAGE_CODES.get(source_lang, source_lang)}: '{text}' → '{translated}'")
        return translated
    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return text


def translate_from_english(text, target_lang):
    """Translate text from English to target language"""
    
    # If target is English or unknown, return as is
    if target_lang == 'en' or target_lang not in LANGUAGE_CODES:
        return text
    
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        translated = translator.translate(text)
        print(f"🌐 Translated to {LANGUAGE_CODES.get(target_lang, target_lang)}: '{text[:50]}...' → '{translated[:50]}...'")
        return translated
    except Exception as e:
        print(f"⚠️ Translation error: {e}")
        return text


def is_mixed_language(text, detected_lang):
    """Check if text is mixed language (Tanglish, Hinglish, etc.)"""
    
    # Count English words
    english_pattern = re.compile(r'\b[a-zA-Z]+\b')
    english_words = english_pattern.findall(text)
    
    # Count total words
    total_words = len(text.split())
    
    if total_words == 0:
        return False
    
    english_ratio = len(english_words) / total_words
    
    # If 20-80% English words, it's likely mixed language
    return 0.2 < english_ratio < 0.8


def get_response_language(detected_lang, is_mixed):
    """Determine what language to respond in"""
    
    if is_mixed:
        # For mixed languages, respond in the detected base language
        # This gives a more natural feel
        return detected_lang
    
    return detected_lang