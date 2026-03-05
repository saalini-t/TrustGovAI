"""Test 4: RAG Retrieval Function"""
from app.services.rag_service import generate_rag_answer

print("[TEST 4] RAG Retrieval Function")
print("-" * 60)

try:
    answer, context, sources = generate_rag_answer("How much money does PM Kisan give?")
    
    print(f"Answer: {answer[:150]}...")
    print(f"\nContext (first 200 chars): {context[:200]}...")
    print(f"\nNumber of sources: {len(sources)}")
    
    if "6000" in answer or "rupees" in answer.lower():
        print("\n✅ TEST PASSED: Answer contains relevant information")
    else:
        print("\n⚠️  Answer might not be optimal")
        
except Exception as e:
    print(f"❌ TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
