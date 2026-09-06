# Full YouTube Shorts Automation - Setup Instructions

This document provides the complete automation workflow to get the system fully operational with **zero manual work** after initial setup.

## 🎯 Goal: Full Autonomy

- ✅ Code on GitHub with CI/CD
- ✅ Automated video generation, creation, and upload
- ✅ Scheduled runs via GitHub Actions
- ✅ Zero manual intervention required

---

## ⚡ Quick Start (2 steps)

### Step 1: GitHub Authentication (One-time, 2 minutes)

```bash
# This is the ONLY manual step required
gh auth login

# Choose: GitHub.com → HTTPS → Authenticate via web browser
# This will generate a token that allows Claude Code to manage your repository
```

### Step 2: Run Full Automation

```bash
cd ~/Desktop/youtube-shorts-automation

# This will:
# 1. Create GitHub repository
# 2. Push all code
# 3. Configure secrets
# 4. Set up GitHub Actions
bash setup_automation.sh
```

---

## 📋 What Gets Automated

### ✅ Already Done
- [x] Environment setup (.env with API keys)
- [x] Python dependencies configured
- [x] Database schema created
- [x] Content generator (Gemini API)
- [x] Video creation (FFmpeg + stock footage)
- [x] YouTube uploader (OAuth2)
- [x] GitHub Actions workflows (.github/workflows/)

### ✅ Automated in setup_automation.sh
- [x] GitHub repository creation
- [x] Code push to GitHub
- [x] GitHub Actions secrets configuration
- [x] System credentials test

### ⏳ Remaining: YouTube Channel Creation

The only thing that cannot be fully automated (YouTube API limitation):
- Manual creation of 5 YouTube channels
- Adding service account as collaborator

**Two options provided:**

1. **Automated with Selenium** (80% automated)
   ```bash
   python create_channels.py --auto
   ```
   - You complete OAuth2 once (bot detection)
   - Script handles all repetitive steps

2. **Manual Quick Guide** (15 min for all 5)
   ```bash
   python create_channels.py --guide
   ```
   - Step-by-step instructions
   - Estimated 3 minutes per channel

---

## 🚀 Full Automation Workflow

### Phase 1: GitHub Setup (NOW)

```bash
# Check GitHub auth
gh auth login

# Run automated setup
bash setup_automation.sh
# This does: repo creation → code push → secrets config
```

### Phase 2: YouTube Channel Setup (5-15 min)

```bash
# Create YouTube channels (choose one):

# Option A: Selenium automation (80% automated)
python create_channels.py --auto

# Option B: Manual guide (fastest, 15 min)
python create_channels.py --guide
```

**Important:** After creating channels, add the service account as collaborator:
- Go to each channel Settings → Permissions → Manage permissions
- Add: `youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com`
- Role: Editor

### Phase 3: CI/CD Automation (AUTOMATIC)

Once channels are set up:

```bash
# Test locally
python -m src.main science_facts

# Or push a commit to trigger GitHub Actions
git add .
git commit -m "Trigger GitHub Actions"
git push
```

**GitHub Actions will now:**
- Generate 10+ scripts daily (all 5 channels)
- Create videos automatically
- Upload to YouTube
- Run 24/7 without intervention

---

## 📊 GitHub Actions Workflows

The system includes 3 automated workflows:

### 1. `generate.yml` - Daily content generation
- Runs daily at 12:00 AM UTC
- Generates 2-3 scripts per channel
- Stores in database
- **Fully automated**

### 2. `create.yml` - Video creation
- Runs daily at 06:00 AM UTC
- Creates videos from generated scripts
- Uses FFmpeg + TTS + stock footage
- **Fully automated**

### 3. `upload.yml` - YouTube upload
- Runs daily at 12:00 PM UTC
- Uploads created videos to channels
- Publishes immediately
- **Fully automated**

All workflows run in parallel across your 5 channels.

---

## 🔐 Secrets Configured

The `setup_automation.sh` script configures these GitHub secrets:

- `GEMINI_API_KEY` - Content generation
- `PEXELS_API_KEY` - Stock footage
- `GOOGLE_APPLICATION_CREDENTIALS` - YouTube upload

These are automatically injected into GitHub Actions environment.

---

## 📈 Expected Output

Once fully set up:

```
Daily Output (per channel):
├─ 2-3 generated scripts
├─ 2-3 videos created
└─ 2-3 videos uploaded to YouTube

Total per day: 10-15 videos across 5 channels
```

---

## 🆘 Troubleshooting

### "gh: command not found"
```bash
brew install gh
```

### "Not authenticated with GitHub"
```bash
gh auth login
# Follow browser prompts
```

### "Repository already exists"
The script checks and skips if repo exists. Safe to re-run.

### "YouTube channel creation fails"
- Selenium might not work with latest YouTube UI changes
- Use manual guide instead: `python create_channels.py --guide`
- Takes only 15 minutes for all 5 channels

### "Collaborator won't load in YouTube"
- Service account email: `youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com`
- Make sure you're in channel Settings → Permissions
- Grant "Editor" role (not Viewer)
- Wait 5 minutes for access to propagate

---

## ✨ Key Differences from Manual Setup

| Task | Manual | Automated |
|------|--------|-----------|
| Repository creation | 5 min | 30 sec |
| Code push | 3 min | Auto |
| Secrets setup | 15 min | Auto |
| Channel creation | 15 min | 15 min (or 5 with Selenium) |
| Workflow setup | 10 min | Auto |
| **Total time** | **~45 min** | **~20 min** |

---

## 📝 Next Steps After Full Automation

Once everything is running:

1. **Monitor dashboard** (optional):
   ```bash
   python dashboard.py
   # Visit http://localhost:5000
   ```

2. **Check GitHub Actions** (optional):
   ```bash
   gh workflow view
   gh run list
   ```

3. **Verify YouTube uploads** (optional):
   - Go to each channel's YouTube Studio
   - Shorts should appear automatically

4. **Scale up** (optional):
   - Modify `config/channels.yaml` to add more niches
   - GitHub Actions will automatically generate for new channels

---

## 🎓 How It Works

```
┌─────────────────────────────────────────────────┐
│          GitHub Actions (24/7)                  │
├─────────────────────────────────────────────────┤
│                                                 │
│  Every day, 3 workflows run:                   │
│  1. Generate scripts (Gemini API)              │
│  2. Create videos (FFmpeg + TTS)               │
│  3. Upload to YouTube (OAuth2)                 │
│                                                 │
│  All automated, zero human intervention        │
│                                                 │
└─────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────┐
│   YouTube Channels (5 operating)                │
├─────────────────────────────────────────────────┤
│  • Science Facts Daily                          │
│  • Daily Motivation                             │
│  • Life Hacks Pro                               │
│  • History Facts                                │
│  • Finance Tips Daily                           │
│                                                 │
│  Each channel: 2-3 new Shorts daily            │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

**Questions?** Check the main README or run:
```bash
python -c "from src.main import run_pipeline; help(run_pipeline)"
```
