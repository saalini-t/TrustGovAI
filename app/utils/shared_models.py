"""Shared embedding model to avoid loading multiple times"""
from sentence_transformers import SentenceTransformer

_shared_model = None

def get_embedding_model():
    """Get shared embedding model (singleton)"""
    global _shared_model
    if _shared_model is None:
        print("🔄 Loading embedding model (one-time)...")
        _shared_model = SentenceTransformer("all-MiniLM-L6-v2")
        print("✅ Embedding model loaded!")
    return _shared_model
