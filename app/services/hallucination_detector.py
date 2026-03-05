from app.utils.shared_models import get_embedding_model
import numpy as np

def detect_hallucination(answer, context):
    """Simple cosine similarity-based hallucination detection"""
    model = get_embedding_model()
    
    emb1 = model.encode([answer])
    emb2 = model.encode([context])
    
    # Cosine similarity
    similarity = np.dot(emb1[0], emb2[0]) / (np.linalg.norm(emb1[0]) * np.linalg.norm(emb2[0]))
    confidence = float(similarity)
    
    # If similarity is low, likely hallucination
    if confidence < 0.65:
        return True, confidence
    
    return False, confidence