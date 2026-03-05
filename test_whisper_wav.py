#!/usr/bin/env python
import whisper
import os

# Try to load a WAV file directly with Whisper
wav_file = "test_output.wav"

if not os.path.exists(wav_file):
    print(f"WAV file not found: {wav_file}")
    print("Creating WAV file from MP4...")
    
    import subprocess
    import imageio_ffmpeg
    
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    mp4_file = r"c:\Users\shalu\Downloads\test_audio_1.mp4"
    
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
    print(f"FFmpeg return code: {result.returncode}")

if os.path.exists(wav_file):
    print(f"WAV file size: {os.path.getsize(wav_file)} bytes")
    
    print("\nLoading Whisper model (may take time)...")
    model = whisper.load_model("base")
    
    print(f"Transcribing {wav_file}...")
    try:
        result = model.transcribe(wav_file, language="en", verbose=False)
        print(f"\nTranscription:")
        print(result['text'])
    except Exception as e:
        print(f"Error during transcription: {e}")
        import traceback
        traceback.print_exc()
else:
    print("Could not create WAV file")
