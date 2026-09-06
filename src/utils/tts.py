import os
import subprocess
from pathlib import Path

TTS_OUTPUT_DIR = Path("data/audio")
TTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def generate_audio_pyttsx3(text: str, output_path: str, rate: int = 150) -> bool:
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 1.0)
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return True
    except Exception as e:
        print(f"Error generating audio with pyttsx3: {e}")
        return False

def generate_audio_edge_tts(text: str, output_path: str, voice: str = "en-US-AriaNeural") -> bool:
    try:
        cmd = [
            "edge-tts",
            "--text", text,
            "--voice", voice,
            "--write-media", output_path
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        print(f"Error generating audio with edge-tts: {e}")
        print("Install edge-tts: pip install edge-tts")
        return False

def generate_audio(text: str, output_path: str, method: str = "pyttsx3") -> bool:
    if method == "edge-tts":
        return generate_audio_edge_tts(text, output_path)
    else:
        return generate_audio_pyttsx3(text, output_path)

def get_audio_duration(audio_path: str) -> float:
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_file(audio_path)
        return len(audio) / 1000.0
    except Exception as e:
        print(f"Error getting audio duration: {e}")
        return 0.0
