import json
from src.utils.api_clients import GeminiClient
from src.database import add_script

def generate_content(channel: str, config: dict, num_videos: int = 2) -> int:
    client = GeminiClient()
    niche = config.get("niche")
    prompt_template = config.get("prompt_template")
    keywords = config.get("keywords", [])

    scripts_generated = 0

    for i in range(num_videos):
        keyword = keywords[i % len(keywords)] if keywords else niche

        full_prompt = f"""{prompt_template}

Topic/Keyword: {keyword}

Generate a short, engaging script for a YouTube Short (15-30 seconds when read at normal speed).
Format the response as JSON with these fields:
- "script": The exact voiceover text (2-3 sentences max)
- "title": YouTube video title (under 100 chars)
- "description": YouTube description (under 5000 chars, include relevant info)
- "tags": List of 5-8 relevant hashtags
"""

        script_content = client.generate_script(full_prompt)

        if not script_content:
            print(f"Failed to generate script for {channel} - {keyword}")
            continue

        try:
            parsed = json.loads(script_content)
            script_id = add_script(
                channel=channel,
                niche=niche,
                script=parsed.get("script", ""),
                title=parsed.get("title", ""),
                description=parsed.get("description", ""),
                tags=parsed.get("tags", [])
            )
            print(f"Generated script {script_id} for {channel}: {parsed.get('title', 'N/A')}")
            scripts_generated += 1
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response for {channel}")
            continue

    return scripts_generated
