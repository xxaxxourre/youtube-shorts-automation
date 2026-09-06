import json
import os
from src.utils.api_clients import YouTubeClient
from src.database import get_pending_videos, add_upload, update_video_status

def upload_videos(channel: str, config: dict, num_videos: int = 2) -> int:
    credentials_path = config.get("youtube_credentials_path")

    if not credentials_path or not os.path.exists(credentials_path):
        print(f"YouTube credentials not found for {channel} at {credentials_path}")
        return 0

    youtube_client = YouTubeClient(credentials_path)
    videos_uploaded = 0

    pending = get_pending_videos(channel, limit=num_videos)

    for video_id, video_path, title, description, tags_json in pending:
        if not os.path.exists(video_path):
            print(f"Video file not found: {video_path}")
            update_video_status(video_id, "file_not_found")
            continue

        tags = json.loads(tags_json) if tags_json else []

        full_description = f"""{description}

---
This video was automatically generated using AI.
#shorts #{channel}
"""

        result = youtube_client.upload_video(
            file_path=video_path,
            title=title,
            description=full_description,
            tags=tags,
            category_id="28"
        )

        if result.get("success"):
            youtube_id = result.get("video_id")
            youtube_url = result.get("url")
            add_upload(channel, video_id, youtube_id, youtube_url)
            print(f"Uploaded video to YouTube: {youtube_url}")
            update_video_status(video_id, "uploaded")
            videos_uploaded += 1
        else:
            print(f"Failed to upload video {video_id}: {result.get('error')}")
            update_video_status(video_id, "upload_failed")

    return videos_uploaded
