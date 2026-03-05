import faiss
import pickle
import numpy as np
import os

from sentence_transformers import SentenceTransformer

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_PATH = os.path.join(BASE_DIR, "vector.index")
CHUNKS_PATH = os.path.join(BASE_DIR, "chunks.pkl")
METADATA_PATH = os.path.join(BASE_DIR, "metadata.pkl")

# Lazy load model
_model = None
_index = None
_chunks = None
_metadata = None

def _load_resources():
    global _model, _index, _chunks, _metadata
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
        _index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            _chunks = pickle.load(f)
        with open(METADATA_PATH, "rb") as f:
            _metadata = pickle.load(f)

def retrieve_documents(query, k=3):
    _load_resources()
    
    query_vector = _model.encode([query])
    distances, indices = _index.search(np.array(query_vector), k)
    
    results = []
    for i in indices[0]:
        results.append({
            "text": _chunks[i],
            "source": _metadata[i]
        })
    
    return results


def search_documents(query, k=2):
    """Legacy function for backward compatibility"""
    docs = retrieve_documents(query, k)
    return [d["text"] for d in docs]