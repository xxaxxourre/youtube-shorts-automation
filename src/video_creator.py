import os
from pathlib import Path
from src.utils.api_clients import PexelsClient
from src.utils.tts import generate_audio
from src.utils.ffmpeg_handler import create_text_overlay_video
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
