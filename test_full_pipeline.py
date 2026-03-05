"""Test 6: Full Chat Pipeline"""
import requests
import json

print("[TEST 6] Full Chat Pipeline")
print("-" * 60)

try:
    response = requests.post(
        "http://localhost:8000/chat/",
        json={"message": "How much money does PM Kisan provide?"},
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nResponse:")
        print(json.dumps(data, indent=2))
        
        # Check response structure
        required_fields = ["language", "answer", "confidence_score", "verified"]
        missing_fields = [f for f in required_fields if f not in data]
        
        if not missing_fields:
            print("\n✅ TEST PASSED: Full chat pipeline working")
            print(f"   - Language detected: {data['language']}")
            print(f"   - Confidence score: {data['confidence_score']:.2f}")
            print(f"   - Verified: {data['verified']}")
        else:
            print(f"\n⚠️  Missing fields: {missing_fields}")
    else:
        print(f"❌ API returned error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ TEST FAILED: {str(e)}")
