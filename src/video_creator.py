import os
import re
from pathlib import Path
from src.utils.api_clients import PexelsClient
from src.utils.tts import generate_audio
from src.utils.ffmpeg_handler import create_text_overlay_video, create_caption_overlay
from src.database import get_pending_scripts, update_script_status, add_video, update_video_status

FOOTAGE_CACHE = Path("data/footage")
FOOTAGE_CACHE.mkdir(parents=True, exist_ok=True)

def create_videos(channel: str, config: dict, num_videos: int = 2) -> int:
    pexels_client = PexelsClient()
    videos_created = 0

    pending = get_pending_scripts(channel, limit=num_videos)

    for script_id, script_text, title, description, tags_json in pending:
        search_query = config.get("pexels_search_query", "nature")

        footage_files = pexels_client.search_videos(search_query, per_page=1)

        if not footage_files:
            print(f"No footage found for {channel}")
            update_script_status(script_id, "no_footage")
            continue

        footage_url = footage_files[0]['video_files'][0]['link']
        footage_path = FOOTAGE_CACHE / f"{script_id}_{search_query}.mp4"

        if not footage_path.exists():
            if not pexels_client.download_video(footage_url, str(footage_path)):
                print(f"Failed to download footage for script {script_id}")
                update_script_status(script_id, "download_failed")
                continue

        audio_path = FOOTAGE_CACHE / f"{script_id}_audio.wav"
        if not generate_audio(script_text, str(audio_path), method="pyttsx3"):
            print(f"Failed to generate audio for script {script_id}")
            update_script_status(script_id, "audio_failed")
            continue

        video_path = Path("data/videos") / f"{channel}_{script_id}.mp4"
        video_path.parent.mkdir(parents=True, exist_ok=True)

        if not create_text_overlay_video(
            str(footage_path),
            str(audio_path),
            title=title,
            subtitle="",
            output_path=str(video_path),
            duration=25.0
        ):
            print(f"Failed to create video for script {script_id}")
            update_script_status(script_id, "video_creation_failed")
            continue

        video_id = add_video(channel, script_id, str(video_path))
        print(f"Created video {video_id} for channel {channel}")

        update_script_status(script_id, "video_created")
        videos_created += 1

    return videos_created

def create_reddit_story_video(channel: str, config: dict, num_videos: int = 1) -> int:
    """Create Reddit story videos with Minecraft parkour overlay and captions."""
    pexels_client = PexelsClient()
    videos_created = 0

    pending = get_pending_scripts(channel, limit=num_videos)

    for script_id, script_text, title, description, tags_json in pending:
        try:
            # Search for Minecraft footage
            search_query = config.get("minecraft_settings", {}).get("footage_types", ["parkour_gameplay"])[0]
            minecraft_videos = pexels_client.search_videos(f"minecraft {search_query}", per_page=3)

            if not minecraft_videos:
                # Fallback to generic gameplay
                minecraft_videos = pexels_client.search_videos("minecraft gameplay", per_page=1)

            if not minecraft_videos:
                print(f"No Minecraft footage found for {script_id}")
                update_script_status(script_id, "no_footage")
                continue

            # Pick a random video from results for variety
            footage_url = minecraft_videos[0]['video_files'][0]['link']
            footage_path = FOOTAGE_CACHE / f"{script_id}_minecraft.mp4"

            if not footage_path.exists():
                if not pexels_client.download_video(footage_url, str(footage_path)):
                    print(f"Failed to download Minecraft footage")
                    update_script_status(script_id, "download_failed")
                    continue

            # Generate TTS with storyteller voice
            audio_path = FOOTAGE_CACHE / f"{script_id}_story_audio.wav"
            if not generate_audio(script_text, str(audio_path), method="pyttsx3"):
                print(f"Failed to generate audio for Reddit story")
                update_script_status(script_id, "audio_failed")
                continue

            # Create captions by breaking story into segments
            caption_texts = _break_into_captions(script_text, max_length=50)

            # Create video with Minecraft overlay
            video_path = Path("data/videos") / f"{channel}_{script_id}_reddit.mp4"
            video_path.parent.mkdir(parents=True, exist_ok=True)

            # Create base video with captions
            if not create_caption_overlay(
                str(footage_path),
                str(audio_path),
                captions=caption_texts,
                output_path=str(video_path),
                style="minecraft",  # Yellow/black Minecraft-style captions
                duration=30.0
            ):
                print(f"Failed to create Reddit story video")
                update_script_status(script_id, "video_creation_failed")
                continue

            video_id = add_video(channel, script_id, str(video_path))
            print(f"Created Reddit story video {video_id}")

            update_script_status(script_id, "video_created")
            videos_created += 1

        except Exception as e:
            print(f"Error creating Reddit story video: {e}")
            update_script_status(script_id, "creation_error")
            continue

    return videos_created

def _break_into_captions(text: str, max_length: int = 50) -> list:
    """Break story text into caption segments."""
    # Split by sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)
    captions = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) < max_length:
            current += " " + sentence
        else:
            if current:
                captions.append(current.strip())
            current = sentence

    if current:
        captions.append(current.strip())

    return captions
