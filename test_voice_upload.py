"""Test voice API with mp4 upload"""
import requests
import json
import sys

print("=" * 80)
print("TESTING VOICE ENDPOINT WITH MP4 AUDIO")
print("=" * 80)

audio_file = r"c:\Users\shalu\Downloads\test_audio_1.mp4"

print(f"\n📁 Audio File: {audio_file}")
print(f"📤 Uploading to: http://localhost:8000/voice/\n")

try:
    with open(audio_file, 'rb') as f:
        files = {'file': f}
        print("⏳ Processing (this may take 20-40 seconds)...\n")
        
        response = requests.post(
            'http://localhost:8000/voice/',
            files=files,
            timeout=300
        )
    
    print(f"✅ Response Status: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        print("📊 RESPONSE DATA:")
        print("-" * 80)
        print(json.dumps(data, indent=2))
        print("-" * 80)
        
        print("\n✅ VOICE PIPELINE TEST SUCCESSFUL!")
        print(f"   • Transcribed: {data.get('transcribed_text', 'N/A')}")
        print(f"   • Language: {data.get('language', 'N/A')}")
        print(f"   • Answer: {data.get('answer', 'N/A')[:100]}...")
        print(f"   • Confidence: {data.get('confidence', 'N/A'):.2f}")
        print(f"   • Verified: {data.get('verified', 'N/A')}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except FileNotFoundError:
    print(f"❌ Audio file not found: {audio_file}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
