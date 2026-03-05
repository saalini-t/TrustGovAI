from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.language_detector import detect_language
from app.services.rag_service import generate_rag_answer
from app.services.hallucination_detector import detect_hallucination
from app.services.correction_engine import correct_answer

router = APIRouter()

@router.post("/")
def chat(request: ChatRequest):

    text = request.message

    language = detect_language(text)

    answer, context, sources = generate_rag_answer(text)

    hallucinated, confidence = detect_hallucination(answer, context)

    if hallucinated:
        answer = correct_answer(text, context)

    return {
        "language": language,
        "answer": answer,
        "confidence_score": confidence,
        "verified": not hallucinated,
        "source": context,
        "sources": sources
    }