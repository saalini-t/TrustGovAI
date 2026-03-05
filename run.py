import os
import sys

# Add imageio-ffmpeg to PATH so Whisper can find it
try:
    import imageio_ffmpeg
    ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    current_path = os.environ.get('PATH', '')
    os.environ['PATH'] = f"{ffmpeg_dir};{current_path}"
    print(f"✅ Added ffmpeg to PATH: {ffmpeg_dir}")
except Exception as e:
    print(f"⚠️  Could not add ffmpeg to PATH: {e}")

from app.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
