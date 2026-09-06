import subprocess
from pathlib import Path
from typing import List

VIDEO_OUTPUT_DIR = Path("data/videos")
VIDEO_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def compose_video(audio_path: str, footage_path: str, output_path: str,
                  title_text: str = None, duration: float = None) -> bool:
    try:
        cmd = [
            "ffmpeg",
            "-i", footage_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "-2",
            "-pix_fmt", "yuv420p",
        ]

        if duration:
            cmd.extend(["-t", str(duration)])

        if title_text:
            cmd.extend([
                "-vf",
                f"scale=1080:1920,drawtext=text='{title_text}':x=540-tw/2:y=100:fontsize=50:fontcolor=white:fontfile=/System/Library/Fonts/Arial.ttf"
            ])

        cmd.extend([
            "-y",
            output_path
        ])

        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error composing video: {e}")
        return False

def add_captions(video_path: str, caption_text: str, output_path: str) -> bool:
    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vf",
            f"drawtext=text='{caption_text}':x=w/2-tw/2:y=h-100:fontsize=40:fontcolor=white:fontfile=/System/Library/Fonts/Arial.ttf:box=1:boxcolor=black@0.5:boxborderw=5",
            "-c:a", "copy",
            "-y",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error adding captions: {e}")
        return False

def create_text_overlay_video(footage_path: str, audio_path: str, title: str,
                             subtitle: str, output_path: str, duration: float = 25.0) -> bool:
    try:
        vf = f"scale=1080:1920"

        if title:
            title_esc = title.replace("'", "'\\''")
            vf += f",drawtext=text='{title_esc}':x=540-tw/2:y=400:fontsize=50:fontcolor=white:fontfile=/System/Library/Fonts/Arial.ttf:box=1:boxcolor=black@0.7:boxborderw=10"

        if subtitle:
            subtitle_esc = subtitle.replace("'", "'\\''")
            vf += f",drawtext=text='{subtitle_esc}':x=540-tw/2:y=1000:fontsize=40:fontcolor=yellow:fontfile=/System/Library/Fonts/Arial.ttf:box=1:boxcolor=black@0.7:boxborderw=10"

        cmd = [
            "ffmpeg",
            "-i", footage_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "-2",
            "-pix_fmt", "yuv420p",
            "-t", str(duration),
            "-vf", vf,
            "-y",
            output_path
        ]

        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error creating text overlay video: {e}")
        return False

def merge_audio_video(video_path: str, audio_path: str, output_path: str) -> bool:
    try:
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-y",
            output_path
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Error merging audio and video: {e}")
        return False
