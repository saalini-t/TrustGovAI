"""Test 3: Embeddings"""
from sentence_transformers import SentenceTransformer

print("[TEST 3] Embeddings")
print("-" * 60)

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded: all-MiniLM-L6-v2")

emb = model.encode(["PM Kisan scheme"])
embedding_dim = len(emb[0])

print(f"Embedding dimension: {embedding_dim}")

if embedding_dim == 384:
    print(f"✅ TEST PASSED: Correct embedding dimension (384)")
else:
    print(f"⚠️  Different dimension: {embedding_dim}")
    print(f"   (Expected 384 for all-MiniLM-L6-v2)")
