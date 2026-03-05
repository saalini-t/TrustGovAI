import os
import sys
import subprocess
import numpy as np
import imageio_ffmpeg

# ============  CRITICAL: Patch subprocess BEFORE importing Whisper ============
#  Whisper's audio.py will inherit the patched subprocess.run at import time

_original_subprocess_run = subprocess.run
_ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

def _patched_subprocess_run(args, *pargs, **kwargs):
    """Intercept subprocess calls to replace 'ffmpeg' with full path"""
    # If first arg is a list and first element is 'ffmpeg', replace it
    if isinstance(args, list) and len(args) > 0 and args[0] == "ffmpeg":
        args = list(args)  # Make copy
        args[0] = _ffmpeg_exe
        print(f"🔧 Patched ffmpeg call: using {_ffmpeg_exe}")
    return _original_subprocess_run(args, *pargs, **kwargs)

# Global patch before importing whisper
subprocess.run = _patched_subprocess_run

# NOW import whisper - it will use our patched subprocess.run
import whisper

# ===============================================================================

_model = None

def _load_model():
    global _model
    if _model is None:
        print("Loading Whisper model...")
        print(f"ffmpeg executable available: {os.path.exists(_ffmpeg_exe)}")
        _model = whisper.load_model("base")
    return _model

def _convert_mp4_to_wav(input_path, output_path="temp_audio.wav"):
    """Convert MP4 to WAV using imageio-ffmpeg"""
    try:
        print(f"Converting {input_path} to WAV using ffmpeg...")
        cmd = [
            _ffmpeg_exe,
            "-i", input_path,
            "-vn",  # No video
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",
            output_path
        ]
        result = _original_subprocess_run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode == 0 and os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Successfully converted to {output_path} ({file_size} bytes)")
            return output_path
        else:
            print(f"❌ ffmpeg failed: {result.stderr[:200]}")
            return None
    except Exception as e:
        print(f"❌ ffmpeg conversion error: {e}")
        return None

def speech_to_text(audio_path):
    """Convert speech to text using Whisper"""
    model = _load_model()
    
    temp_wav_file = None
    try:
        # If not WAV, convert to WAV first
        if not audio_path.lower().endswith('.wav'):
            print(f"Input is {os.path.splitext(audio_path)[1]} format, converting to WAV...")
            temp_wav_file = "temp_audio_" + os.urandom(4).hex() + ".wav"
            converted_path = _convert_mp4_to_wav(audio_path, temp_wav_file)
            if converted_path:
                audio_path = converted_path
            else:
                return "Error: Could not convert audio format"
        
        print(f"🎤 Transcribing {audio_path}...")
        result = model.transcribe(audio_path, language="en", verbose=False)
        text = result["text"].strip()
        print(f"✅ Transcription complete: {len(text)} characters")
        return text if text else "Unable to transcribe audio"
            
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        import traceback
        traceback.print_exc()
        return f"Transcription error: {str(e)}"
    finally:
        # Clean up temp file
        if temp_wav_file and os.path.exists(temp_wav_file):
            try:
                os.remove(temp_wav_file)
                print(f"Cleaned up temp file: {temp_wav_file}")
            except:
                pass