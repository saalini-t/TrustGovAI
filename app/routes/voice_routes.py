from fastapi import APIRouter, UploadFile, File
from app.services.speech_service import speech_to_text
from app.services.language_detector import detect_language
from app.services.rag_service import generate_rag_answer
from app.services.hallucination_detector import detect_hallucination
from app.services.correction_engine import correct_answer
from app.services.translation_service import translate_to_english, translate_from_english

router = APIRouter()

@router.post("/")
async def voice_query(file: UploadFile = File(...)):
    """
    Voice query endpoint:
    1. Accepts audio file (wav, mp3, m4a, mp4)
    2. Transcribes using Whisper
    3. Detects language
    4. Translates to English for retrieval
    5. Generates RAG answer
    6. Translates response back to user's language
    7. Returns transcribed text + answer
    """
    
    audio_path = "temp_audio.wav"
    
    with open(audio_path, "wb") as f:
        f.write(await file.read())
    
    # Transcribe audio
    text = speech_to_text(audio_path)
    
    # Detect language
    language = detect_language(text)
    print(f"🔍 Detected language: {language}")
    
    # Translate to English for retrieval
    query_in_english = translate_to_english(text, language)
    
    # Generate answer with RAG
    answer, context, sources = generate_rag_answer(query_in_english)
    
    # Check for hallucination
    hallucinated, confidence = detect_hallucination(answer, context)
    
    if hallucinated:
        answer = correct_answer(query_in_english, context)
    
    # Translate answer back to user's language
    if language != 'en':
        answer = translate_from_english(answer, language)
    
    return {
        "transcribed_text": text,
        "language": language,
        "answer": answer,
        "confidence": confidence,
        "verified": not hallucinated,
        "source": context,
        "sources": sources
    }