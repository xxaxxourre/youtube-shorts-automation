import os
import yaml
import sys
from pathlib import Path
from src.database import init_db
from src.generator import generate_content
from src.video_creator import create_videos
from src.youtube_uploader import upload_videos

def load_config(config_path: str = "config/channels.yaml") -> dict:
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_pipeline(channels: list = None, stages: list = None):
    init_db()

    if stages is None:
        stages = ["generate", "create", "upload"]

    if channels is None:
        config = load_config()
        channels = config.get("channels", {}).keys()

    for channel in channels:
        config = load_config()
        channel_config = config.get("channels", {}).get(channel)

        if not channel_config:
            print(f"Channel {channel} not found in config")
            continue

        print(f"\n{'='*60}")
        print(f"Processing channel: {channel}")
        print(f"{'='*60}")

        if "generate" in stages:
            print(f"\n[GENERATE] Generating content for {channel}...")
            num_generated = generate_content(
                channel=channel,
                config=channel_config,
                num_videos=channel_config.get("videos_per_run", 2)
            )
            print(f"✓ Generated {num_generated} scripts")

        if "create" in stages:
            print(f"\n[CREATE] Creating videos for {channel}...")
            num_created = create_videos(
                channel=channel,
                config=channel_config,
                num_videos=channel_config.get("videos_per_run", 2)
            )
            print(f"✓ Created {num_created} videos")

        if "upload" in stages:
            print(f"\n[UPLOAD] Uploading videos for {channel}...")
            num_uploaded = upload_videos(
                channel=channel,
                config=channel_config,
                num_videos=channel_config.get("videos_per_run", 2)
            )
            print(f"✓ Uploaded {num_uploaded} videos")

if __name__ == "__main__":
    channels_arg = sys.argv[1:] if len(sys.argv) > 1 else None
    run_pipeline(channels=channels_arg)
