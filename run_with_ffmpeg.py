#!/usr/bin/env python
import os
import sys

# Add imageio-ffmpeg to PATH so Whisper can find it
import imageio_ffmpeg
ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
print(f"Adding to PATH: {ffmpeg_dir}")

# Add to beginning of PATH
current_path = os.environ.get('PATH', '')
new_path = f"{ffmpeg_dir};{current_path}"
os.environ['PATH'] = new_path

# Verify ffmpeg is in PATH
import subprocess
try:
    result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
    if result.returncode == 0:
        print("✅ ffmpeg is now in PATH and accessible")
    else:
        print("❌ ffmpeg returned non-zero exit code")
except Exception as e:
    print(f"❌ Error accessing ffmpeg: {e}")

# Now import and run the main app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from app.main import app
    import uvicorn
    
    print("\n🚀 Starting TrustGov Backend Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
