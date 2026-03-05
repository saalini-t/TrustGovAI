"""
Test Voice Pipeline - Audio Upload to API
"""
import requests
import os
import time

print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                    VOICE PIPELINE TEST                                    ║
╚════════════════════════════════════════════════════════════════════════════╝
""")

API_URL = "http://localhost:8000/voice/"

# Wait for server to start
print("⏳ Waiting for server to start...")
time.sleep(3)

# Check if server is running
try:
    response = requests.get("http://localhost:8000/docs", timeout=5)
    if response.status_code == 200:
        print("✅ Server is running\n")
    else:
        print("❌ Server not responding properly\n")
except:
    print("❌ Server not ready yet\n")

# Look for audio files in common locations
audio_extensions = ['.mp4', '.mp3', '.wav', '.m4a', '.flac', '.ogg']
found_files = []

search_paths = [
    r"c:\Saalu_Data\Ling_verse",
    r"c:\Saalu_Data\Ling_verse\trustgov_backend",
    r"c:\Users\shalu\Downloads",
    r"c:\Users\shalu\Desktop",
    r".",
]

print("🔍 Searching for audio files...\n")

for path in search_paths:
    if os.path.exists(path):
        for file in os.listdir(path):
            if any(file.lower().endswith(ext) for ext in audio_extensions):
                full_path = os.path.join(path, file)
                found_files.append(full_path)
                print(f"  Found: {full_path}")

if found_files:
    print(f"\n✅ Found {len(found_files)} audio file(s)\n")
    
    # Test with first found file
    audio_file = found_files[0]
    print(f"📤 Testing with: {audio_file}")
    print(f"   File size: {os.path.getsize(audio_file) / 1024:.2f} KB\n")
    
    try:
        with open(audio_file, 'rb') as f:
            files = {'file': f}
            print("📨 Sending audio to API...")
            response = requests.post(API_URL, files=files, timeout=120)
            
        print(f"✅ Status Code: {response.status_code}\n")
        
        if response.status_code == 200:
            data = response.json()
            print("📋 Response:")
            print(f"  • Transcribed: {data.get('transcribed_text', 'N/A')}")
            print(f"  • Language: {data.get('language', 'N/A')}")
            print(f"  • Answer: {data.get('answer', 'N/A')[:150]}...")
            print(f"  • Confidence: {data.get('confidence', 'N/A'):.2f}")
            print(f"  • Verified: {data.get('verified', 'N/A')}")
            
            print("\n✅ VOICE PIPELINE TEST PASSED!")
        else:
            print(f"❌ Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
else:
    print("⚠️  No audio files found\n")
    print("📝 Instructions to test:")
    print("   1. Place your MP4/MP3 audio file in the current directory")
    print("   2. Run this script again")
    print("   3. Or use curl:")
    print(f"      curl -X POST http://localhost:8000/voice/voice \\")
    print(f"           -F 'file=@your_audio_file.mp4'")
    print("\n   For manual testing:")
    print(f"   • Go to: http://localhost:8000/docs")
    print(f"   • Find the POST /voice/voice endpoint")
    print(f"   • Click Try it out")
    print(f"   • Upload your audio file")
