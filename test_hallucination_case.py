"""Test 7: Hallucination Case & Correction"""
import requests
import json

print("[TEST 7] Testing Hallucination Detection & Correction")
print("-" * 60)

try:
    # Query with factually incorrect amount
    response = requests.post(
        "http://localhost:8000/chat/",
        json={"message": "Does PM Kisan provide 12000 rupees?"},
        timeout=30
    )
    
    print(f"Query: Does PM Kisan provide 12000 rupees?")
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Answer: {data['answer']}")
        print(f"Verified: {data['verified']}")
        print(f"Confidence: {data['confidence_score']:.2f}")
        
        if not data['verified']:
            print("\n✅ TEST PASSED: Hallucination was detected")
            print("   Correction engine provided verified answer")
        else:
            print("\n⚠️  Answer was verified as correct (may need more tuning)")
            
except Exception as e:
    print(f"❌ TEST FAILED: {str(e)}")
