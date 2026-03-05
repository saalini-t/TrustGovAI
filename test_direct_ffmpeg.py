#!/usr/bin/env python
import os
import sys
import subprocess

# Test ffmpeg from imageio-ffmpeg
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print(f"FFmpeg executable: {ffmpeg_exe}")
print(f"Exists: {os.path.exists(ffmpeg_exe)}")

mp4_file = r"c:\Users\shalu\Downloads\test_audio_1.mp4"
output_wav = "test_output.wav"

print(f"\nMP4 input: {mp4_file}")
print(f"Exists: {os.path.exists(mp4_file)}")

print(f"\nRunning ffmpeg command...")
cmd = [
    ffmpeg_exe,
    "-i", mp4_file,
    "-acodec", "pcm_s16le",
    "-ar", "16000",
    "-ac", "1",
    "-y",
    output_wav
]

print("Command:", " ".join(cmd))
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

print(f"\nReturn code: {result.returncode}")
print(f"Stdout: {result.stdout[:500] if result.stdout else '(empty)'}")
print(f"Stderr: {result.stderr[:500] if result.stderr else '(empty)'}")

if os.path.exists(output_wav):
    size = os.path.getsize(output_wav)
    print(f"\n✅ Output WAV created: {size} bytes")
    
    # Try to load it with whisper
    try:
        import whisper
        print("\nLoading Whisper model...")
        model = whisper.load_model("base")
        print("Transcribing...")
        transcription = model.transcribe(output_wav, language="en", verbose=False)
        print(f"Transcription: {transcription['text'][:200]}")
    except Exception as e:
        print(f"Error with Whisper: {e}")
        
    # Clean up
    os.remove(output_wav)
else:
    print(f"\n❌ Output WAV not created")
