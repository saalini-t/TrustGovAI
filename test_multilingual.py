"""Test 8: Multilingual Query"""
import requests
import json

print("[TEST 8] Multilingual Query Support")
print("-" * 60)

queries = [
    ("English", "How much money does PM Kisan provide?"),
    ("Hindi", "PM Kisan ne kitna paisa diya?"),
    ("Tanglish", "PM Kisan ku evlo money kudupanga?"),
]

for lang, query in queries:
    try:
        print(f"\n{lang} Query: {query}")
        
        response = requests.post(
            "http://localhost:8000/chat/",
            json={"message": query},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Status: ✓")
            print(f"  Detected Language: {data['language']}")
            print(f"  Answer: {data['answer'][:80]}...")
        else:
            print(f"  Status: Error {response.status_code}")
            
    except Exception as e:
        print(f"  Error: {str(e)}")

print("\n✅ TEST COMPLETE: Multilingual support tested")
