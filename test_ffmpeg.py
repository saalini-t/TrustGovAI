#!/usr/bin/env python
import imageio_ffmpeg

print("imageio_ffmpeg imported successfully")
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
print(f"FFmpeg executable: {ffmpeg_exe}")

# Test with moviepy
try:
    from moviepy.editor import VideoFileClip
    print("moviepy imported successfully")
    
    # Try to open the test MP4
    import os
    mp4_path = r"c:\Users\shalu\Downloads\test_audio_1.mp4"
    if os.path.exists(mp4_path):
        print(f"Opening {mp4_path}...")
        video = VideoFileClip(mp4_path)
        print(f"Video duration: {video.duration}s")
        print(f"Video fps: {video.fps}")
        print(f"Has audio: {video.audio is not None}")
        if video.audio:
            print(f"Audio duration: {video.audio.duration}s")
            print(f"Audio fps: {video.audio.fps}")
        video.close()
        print("Video closed successfully")
    else:
        print(f"MP4 file not found at {mp4_path}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
