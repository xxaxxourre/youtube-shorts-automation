# YouTube Shorts Automation System 🚀

A fully autonomous, multi-channel YouTube Shorts generator powered by AI. Create, edit, and upload 2-5 videos per day per channel without lifting a finger.

## ⚡ Quick Start

### 1. Setup

```bash
# Clone/download this repo
cd youtube-shorts-automation

# Install dependencies
pip install -r requirements.txt

# Copy .env template and add your API keys
cp .env.example .env
```

### 2. Get API Keys (All Free Tier)

#### Google Gemini API
1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Copy to `GEMINI_API_KEY` in `.env`

#### Pexels API
1. Go to [Pexels API](https://www.pexels.com/api/)
2. Sign up and get API key
3. Copy to `PEXELS_API_KEY` in `.env`

#### YouTube API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable YouTube Data API v3
4. Create a service account (APIs & Services > Credentials > Create Credentials > Service Account)
5. Download JSON key and save to `config/youtube_credentials.json`
6. Update paths in `config/channels.yaml`

### 3. Configure Channels

Edit `config/channels.yaml` to customize:
- Niche topics
- Keywords for each channel
- Video search queries
- YouTube credentials path

### 4. Run Locally

```bash
# Generate scripts
python -m src.main generate

# Create videos
python -m src.main create

# Upload to YouTube
python -m src.main upload

# Or run all at once
python -m src.main

# View dashboard
python dashboard.py
# Open http://localhost:5000
```

## 🤖 How It Works

### Pipeline Architecture

1. **Generate** (Content Generator)
   - Calls Gemini API with niche-specific prompts
   - Generates scripts, titles, descriptions, tags
   - Stores in SQLite database

2. **Create** (Video Creator)
   - Converts script to speech (text-to-speech)
   - Downloads stock footage from Pexels
   - Composes video with FFmpeg (text overlay + audio + footage)
   - Adds captions automatically

3. **Upload** (YouTube Uploader)
   - Uploads video to YouTube via API
   - Optimizes metadata (title, description, tags)
   - Tracks upload in database
   - Returns YouTube Shorts link

### Automation with GitHub Actions

GitHub Actions runs the pipeline automatically on a schedule:

- **Generate**: Every 6 hours → creates 3 scripts per channel
- **Create**: 30 min after generate → creates videos
- **Upload**: 1 hour after create → uploads to YouTube

**Result**: 2-3 fully automated videos per channel per day

### Dashboard

View live metrics at `http://localhost:5000`:
- Scripts generated per channel
- Videos created
- Uploads to YouTube
- 24h activity
- Completion rate
- Recent uploads with links

## 📊 Multi-Channel Setup

Default channels (5 niches):

1. **Science Facts** - Space, physics, biology (16x growth potential)
2. **Motivation Daily** - Inspiration, self-improvement (high engagement)
3. **Life Hacks** - Productivity, time-saving tips (high CPM)
4. **History Facts** - Lesser-known historical events (evergreen)
5. **Finance Tips** - Money management, investing (highest CPM $4.50)

Each channel:
- Independent YouTube account
- Custom prompts and keywords
- Separate credentials
- Tracks own metrics

Add more channels by copying the format in `config/channels.yaml`

## 🔧 Customization

### Change Video Duration
In `src/video_creator.py`, line 45:
```python
duration=30.0  # Change to desired seconds
```

### Change Upload Frequency
In `.github/workflows/generate.yml`:
```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  # Try: '0 */3 * * *' for every 3 hours
  # Try: '0 * * * *' for every hour
```

### Use Different TTS Voice
In `src/video_creator.py`:
```python
generate_audio(script_text, str(audio_path), method="edge-tts")
# Options: "pyttsx3" (default) or "edge-tts" (Microsoft voices)
```

### Customize Stock Footage
In `config/channels.yaml`:
```yaml
pexels_search_query: "space universe"  # Change search terms
```

## 📁 Project Structure

```
youtube-shorts-automation/
├── src/
│   ├── main.py              # Orchestrator
│   ├── generator.py         # Content generation
│   ├── video_creator.py     # Video composition
│   ├── youtube_uploader.py  # YouTube upload
│   ├── database.py          # SQLite manager
│   └── utils/
│       ├── api_clients.py   # Gemini, Pexels, YouTube APIs
│       ├── tts.py           # Text-to-speech
│       └── ffmpeg_handler.py # Video editing
├── config/
│   └── channels.yaml        # Channel configuration
├── .github/workflows/       # GitHub Actions CI/CD
├── templates/
│   └── dashboard.html       # Web dashboard
├── dashboard.py             # Flask server
├── data/
│   ├── generated_scripts.db # SQLite database
│   ├── videos/              # Output videos
│   ├── audio/               # Generated audio
│   └── footage/             # Downloaded stock footage
└── requirements.txt         # Python dependencies
```

## 💰 Monetization Timeline

- **Week 1-2**: Upload 15-30 videos
- **Week 3-4**: Start getting views and engagement data
- **Month 1-2**: Reach 1,000 subscribers
- **Month 2-3**: Hit 4,000 watch hours → YouTube Partner Program eligible
- **Month 3+**: Enable monetization → Start earning AdSense revenue

**Expected CPM by niche:**
- Finance: $4-5 (highest)
- Life Hacks: $4-6
- Science: $3-5
- Motivation: $3-5
- History: $2-4

## 🐛 Troubleshooting

### "FFmpeg not found"
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows (with Chocolatey)
choco install ffmpeg
```

### "No footage found"
- Check Pexels API key in `.env`
- Verify API key has access
- Try different search query in `channels.yaml`

### "Script generation failed"
- Verify Gemini API key in `.env`
- Check API rate limit (15/min free tier)
- Increase delay between requests

### YouTube upload fails
- Verify service account has YouTube Data API enabled
- Check credentials JSON path is correct
- Ensure service account has proper IAM permissions

## 📈 Performance Tips

1. **Optimize Video Length**: 20-25 seconds has best retention
2. **Strong Hook**: First 2 seconds are critical
3. **Quality Over Quantity**: 2 great videos > 5 mediocre videos
4. **Consistent Schedule**: Daily uploads outperform sporadic
5. **A/B Test**: Try different titles/thumbnails per niche

## 🚀 Next Steps

1. ✅ Set up API keys
2. ✅ Configure channels
3. ✅ Run local pipeline first (test with 1 video)
4. ✅ View dashboard to confirm videos created
5. ✅ Create YouTube test channel (upload 1 private video)
6. ✅ Set up GitHub Actions for automation
7. ✅ Scale to 3-5 channels
8. ✅ Monitor metrics weekly
9. ✅ Reach 1k subs + 4k watch hours
10. ✅ Enable monetization → Profit!

## 📞 Support

- Check logs in `data/logs/` 
- Review database with `sqlite3 data/generated_scripts.db`
- Run dashboard to see real-time status
- Check GitHub Actions runs for automation logs

## 📄 License

MIT - Use freely for personal use

---

**Built with ❤️ for creators**
