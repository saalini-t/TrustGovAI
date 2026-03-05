import os
import pickle
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_PATH = "data/schemes_docs"

# Load embedding model
model = SentenceTransformer("intfloat/multilingual-e5-base")

documents = []
metadata = []

# Load documents
for file in os.listdir(DATA_PATH):

    path = os.path.join(DATA_PATH, file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

        documents.append(text)
        metadata.append(file)


# ---------- Chunking ----------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = []
chunk_meta = []

for i, doc in enumerate(documents):

    splits = text_splitter.split_text(doc)

    for chunk in splits:
        chunks.append(chunk)
        chunk_meta.append(metadata[i])


print("Total chunks:", len(chunks))


# ---------- Embeddings ----------
embeddings = model.encode(chunks)


# ---------- FAISS Index ----------
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))


# ---------- Save Index ----------
faiss.write_index(index, "vector.index")

with open("chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

with open("metadata.pkl", "wb") as f:
    pickle.dump(chunk_meta, f)

print("Vector database created successfully.")