import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

DATA_PATH = "data/schemes_docs"

# Initialize model
model = SentenceTransformer("all-MiniLM-L6-v2")

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

# Chunk documents into smaller pieces for better retrieval
chunk_size = 300  # characters per chunk
overlap = 50  # character overlap between chunks

for doc_idx, doc in enumerate(documents):
    # Split into chunks with overlap
    for i in range(0, len(doc), chunk_size - overlap):
        chunk = doc[i:i + chunk_size]
        if len(chunk.strip()) > 0:
            chunks.append(chunk)
            metadata.append({
                "doc_index": doc_idx,
                "chunk_index": len(chunks) - 1,
                "start": i,
                "length": len(chunk)
            })

# Create embeddings for all chunks
embeddings = model.encode(chunks)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

# Save files
faiss.write_index(index, "vector.index")

with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

with open("metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print(f"Total chunks: {len(chunks)}")
print("Vector database created successfully.")
print("\nFiles created:")
print("✓ vector.index")
print("✓ chunks.pkl")
print("✓ metadata.pkl")