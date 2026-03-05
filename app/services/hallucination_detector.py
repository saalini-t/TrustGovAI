from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def detect_hallucination(answer, context):
    """Simple cosine similarity-based hallucination detection"""
    _load_model()
    
    emb1 = _model.encode([answer])
    emb2 = _model.encode([context])
    
    # Cosine similarity
    similarity = np.dot(emb1[0], emb2[0]) / (np.linalg.norm(emb1[0]) * np.linalg.norm(emb2[0]))
    confidence = float(similarity)
    
    # If similarity is low, likely hallucination
    if confidence < 0.65:
        return True, confidence
    
    return False, confidence