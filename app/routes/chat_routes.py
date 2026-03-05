from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.language_detector import detect_language
from app.services.rag_service import generate_rag_answer
from app.services.hallucination_detector import detect_hallucination
from app.services.correction_engine import correct_answer
from app.services.translation_service import translate_to_english, translate_from_english

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest):

    text = request.message

    # Step 1: Detect the language of the input
    language = detect_language(text)
    print(f"🔍 Detected language: {language}")

    # Step 2: Translate query to English if needed (for retrieval)
    query_in_english = translate_to_english(text, language)

    # Step 3: Get answer from RAG (using English query)
    answer, context, sources = generate_rag_answer(query_in_english)

    # Step 4: Check for hallucination
    hallucinated, confidence = detect_hallucination(answer, context)

    if hallucinated:
        answer = correct_answer(query_in_english, context)

    # Step 5: Translate answer back to user's language
    if language != 'en':
        answer = translate_from_english(answer, language)

    return {
        "language": language,
        "answer": answer,
        "confidence_score": confidence,
        "verified": not hallucinated,
        "source": context,
        "sources": sources
    }