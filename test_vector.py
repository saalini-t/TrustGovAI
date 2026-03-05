"""Test 1: Vector Store Retrieval"""
from app.utils.vector_store import retrieve_documents

query = "What is PM Kisan scheme?"

print("[TEST 1] Vector Store Retrieval")
print(f"Query: {query}")
print("-" * 60)

docs = retrieve_documents(query, k=2)

print(f"Retrieved {len(docs)} documents:\n")
for i, doc in enumerate(docs):
    print(f"{i+1}. Text: {doc['text'][:100]}...")
    print(f"   Source: {doc['source']}\n")

if docs and 'text' in docs[0]:
    print("✅ TEST PASSED: Retrieval returned documents")
else:
    print("❌ TEST FAILED: No documents retrieved")
