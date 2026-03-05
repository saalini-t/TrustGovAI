#!/usr/bin/env python
import os
import sys
import tempfile

# Debug: Print environment
print("DEBUG: Current working directory:", os.getcwd())
print("DEBUG: sys.path:", sys.path[:3])

# Setup ffmpeg in PATH
try:
    import imageio_ffmpeg
    ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
    current_path = os.environ.get('PATH', '')
    os.environ['PATH'] = f"{ffmpeg_dir};{current_path}"
    print(f"DEBUG: Added ffmpeg to PATH: {ffmpeg_dir}")
except Exception as e:
    print(f"ERROR: Could not setup ffmpeg: {e}")

# Test importing modules
print("DEBUG: Importing whisper...")
try:
    import whisper
    print("DEBUG: whisper imported successfully")
except Exception as e:
    print(f"ERROR: Could not import whisper: {e}")

# Create a simple WAV file from MP4
import subprocess
mp4_file = r"c:\Users\shalu\Downloads\test_audio_1.mp4"
wav_file = "debug_test.wav"

print(f"\nDEBUG: Converting MP4 to WAV...")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
cmd = [
    ffmpeg_exe,
    "-i", mp4_file,
    "-acodec", "pcm_s16le",
    "-ar", "16000",
    "-ac", "1",
    "-y",
    wav_file
]

result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
print(f"DEBUG: ffmpeg return code: {result.returncode}")
print(f"DEBUG: ffmpeg stderr: {result.stderr[:200] if result.stderr else '(empty)'}")

if os.path.exists(wav_file):
    print(f"DEBUG: WAV file created: {os.path.getsize(wav_file)} bytes")
    
    print("\nDEBUG: Loading Whisper model...")
    model = whisper.load_model("base")
    
    # Use absolute path
    wav_path = os.path.abspath(wav_file)
    print(f"DEBUG: Absolute WAV path: {wav_path}")
    print(f"DEBUG: WAV exists: {os.path.exists(wav_path)}")
    
    print("\nDEBUG: Transcribing...")
    try:
        result = model.transcribe(wav_path, language="en", verbose=False)
        print(f"SUCCESS: Transcription completed")
        print(f"Text: {result['text'][:200]}")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    # Cleanup
    try:
        os.remove(wav_file)
    except:
        pass
else:
    print("ERROR: WAV file not created")
