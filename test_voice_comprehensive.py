#!/usr/bin/env python
"""
Comprehensive voice pipeline tests
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
VOICE_ENDPOINT = f"{BASE_URL}/voice/"

# Test MP4 file
mp4_file = r"c:\Users\shalu\Downloads\test_audio_1.mp4"

if not Path(mp4_file).exists():
    print(f"❌ Test audio file not found: {mp4_file}")
    exit(1)

print("=" * 80)
print("COMPREHENSIVE VOICE PIPELINE TESTS")
print("=" * 80)

tests_passed = 0
tests_total = 1

print(f"\n🎤 TEST 1: Audio Transcription and RAG Response")
print("-" * 80)

with open(mp4_file, 'rb') as f:
    files = {'file': f}
    try:
        start = time.time()
        response = requests.post(VOICE_ENDPOINT, files=files, timeout=60)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify response structure
            required_fields = ['transcribed_text', 'language', 'answer', 'confidence', 'verified', 'source', 'sources']
            all_fields_present = all(field in data for field in required_fields)
            
            if all_fields_present:
                print(f"✅ Response structure valid")
                print(f"⏱️  Response time: {elapsed:.2f}s")
                print(f"\n📝 Transcription: {data['transcribed_text']}")
                print(f"🗣️  Language: {data['language']}")
                print(f"📚 Answer: {data['answer'][:150]}...")
                print(f"🎯 Confidence: {data['confidence']:.4f}")
                print(f"✔️  Verified: {data['verified']}")
                print(f"📖 Sources retrieved: {len(data['sources'])} chunks")
                
                # Check if transcription is meaningful
                if len(data['transcribed_text']) > 5 and 'error' not in data['transcribed_text'].lower():
                    print(f"✅ Transcription successful")
                    tests_passed += 1
                else:
                    print(f"❌ Transcription failed or unclear")
            else:
                print(f"❌ Missing fields in response: {[f for f in required_fields if f not in data]}")
        else:
            print(f"❌ API returned status {response.status_code}")
            print(f"Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print(f"RESULTS: {tests_passed}/{tests_total} tests passed")
print("=" * 80)

if tests_passed == tests_total:
    print("✅ All voice pipeline tests passed!")
else:
    print("❌ Some tests failed")
