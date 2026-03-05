import faiss
import pickle
import numpy as np
import os
import glob

from app.utils.shared_models import get_embedding_model

# Get the project root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INDEX_PATH = os.path.join(BASE_DIR, "vector.index")
CHUNKS_PATH = os.path.join(BASE_DIR, "chunks.pkl")
METADATA_PATH = os.path.join(BASE_DIR, "metadata.pkl")
DOCS_DIR = os.path.join(BASE_DIR, "data", "schemes_docs")

# Lazy load resources
_index = None
_chunks = None
_metadata = None
_doc_files = None  # List of document filenames

def _load_resources():
    global _index, _chunks, _metadata, _doc_files
    if _index is None:
        print("🔄 Loading vector index...")
        _index = faiss.read_index(INDEX_PATH)
        with open(CHUNKS_PATH, "rb") as f:
            _chunks = pickle.load(f)
        with open(METADATA_PATH, "rb") as f:
            _metadata = pickle.load(f)
        
        # Load list of document files (sorted to match doc_index)
        _doc_files = sorted(glob.glob(os.path.join(DOCS_DIR, "*.txt")))
        print(f"✅ Vector index loaded! ({len(_chunks)} chunks, {len(_doc_files)} docs)")

def _get_source_name(metadata_item):
    """Convert metadata to human-readable source name"""
    global _doc_files
    
    # If metadata is already a string, return it
    if isinstance(metadata_item, str):
        return metadata_item
    
    # If metadata is a dict with doc_index, map to filename
    if isinstance(metadata_item, dict) and 'doc_index' in metadata_item:
        doc_index = metadata_item['doc_index']
        if _doc_files and 0 <= doc_index < len(_doc_files):
            # Return just the filename without path
            return os.path.basename(_doc_files[doc_index])
        return f"Document {doc_index + 1}"
    
    # Fallback
    return str(metadata_item)

def retrieve_documents(query, k=3):
    _load_resources()
    model = get_embedding_model()
    
    query_vector = model.encode([query])
    distances, indices = _index.search(np.array(query_vector), k)
    
    results = []
    for i in indices[0]:
        source_name = _get_source_name(_metadata[i])
        results.append({
            "text": _chunks[i],
            "source": source_name
        })
    
    return results


def search_documents(query, k=2):
    """Legacy function for backward compatibility"""
    docs = retrieve_documents(query, k)
    return [d["text"] for d in docs]