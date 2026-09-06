import os
import google.generativeai as genai
import requests
from typing import List, Dict

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    def generate_script(self, prompt: str, max_tokens: int = 300) -> str:
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.7,
                )
            )
            return response.text
        except Exception as e:
            print(f"Error generating script: {e}")
            return None

class PexelsClient:
    BASE_URL = "https://api.pexels.com/v1"

    def __init__(self):
        self.headers = {"Authorization": PEXELS_API_KEY}

    def search_videos(self, query: str, per_page: int = 5) -> List[Dict]:
        try:
            url = f"{self.BASE_URL}/videos/search"
            params = {"query": query, "per_page": per_page}
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            videos = response.json().get("videos", [])
            return videos
        except Exception as e:
            print(f"Error searching videos: {e}")
            return []

    def download_video(self, video_url: str, output_path: str) -> bool:
        try:
            response = requests.get(video_url, stream=True)
            response.raise_for_status()
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"Error downloading video: {e}")
            return False

class YouTubeClient:
    def __init__(self, credentials_path: str):
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build

        self.credentials = Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/youtube.upload"]
        )
        self.youtube = build("youtube", "v3", credentials=self.credentials)

    def upload_video(self, file_path: str, title: str, description: str,
                     tags: List[str], category_id: str = "28") -> Dict:
        try:
            request = self.youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "title": title,
                        "description": description,
                        "tags": tags,
                        "categoryId": category_id,
                        "defaultLanguage": "en",
                        "defaultAudioLanguage": "en",
                    },
                    "status": {
                        "privacyStatus": "public",
                        "madeForKids": False,
                    }
                },
                media_body=file_path
            )

            response = request.execute()
            return {
                "success": True,
                "video_id": response.get("id"),
                "url": f"https://youtube.com/shorts/{response.get('id')}"
            }
        except Exception as e:
            print(f"Error uploading video: {e}")
            return {"success": False, "error": str(e)}
