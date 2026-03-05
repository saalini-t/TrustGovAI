"""Test 2: Document Chunking"""
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

DATA_PATH = "data/schemes_docs"
print("[TEST 2] Document Chunking")
print("-" * 60)

documents = []
chunks = []
metadata = []

# Load all documents
for file in os.listdir(DATA_PATH):
    file_path = os.path.join(DATA_PATH, file)
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(text)

print(f"Documents loaded: {len(documents)}")

# Chunk documents
chunk_size = 300
overlap = 50

for doc_idx, doc in enumerate(documents):
    for i in range(0, len(doc), chunk_size - overlap):
        chunk = doc[i:i + chunk_size]
        if len(chunk.strip()) > 0:
            chunks.append(chunk)

print(f"Total chunks created: {len(chunks)}")

if len(chunks) > len(documents):
    print(f"✅ TEST PASSED: Chunking increased documents from {len(documents)} to {len(chunks)}")
else:
    print(f"❌ TEST FAILED: Expected more chunks than documents")
