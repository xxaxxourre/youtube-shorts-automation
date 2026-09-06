#!/bin/bash
set -e

echo "🚀 YouTube Shorts Automation - Full Setup Script"
echo "=================================================="

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Check GitHub authentication
echo -e "\n${BLUE}[1/5] Checking GitHub authentication...${NC}"
if ! gh auth status > /dev/null 2>&1; then
    echo -e "${RED}❌ Not authenticated with GitHub${NC}"
    echo "Run: gh auth login"
    exit 1
fi
echo -e "${GREEN}✓ GitHub authenticated${NC}"

# 2. Create GitHub repository
echo -e "\n${BLUE}[2/5] Creating GitHub repository...${NC}"
REPO_URL="https://github.com/xxaxxourre/youtube-shorts-automation"

if gh repo view xxaxxourre/youtube-shorts-automation > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Repository already exists${NC}"
else
    echo "Creating new repository..."
    gh repo create youtube-shorts-automation \
        --public \
        --source=. \
        --remote=origin \
        --push \
        --description "AI-powered YouTube Shorts automation system"
    echo -e "${GREEN}✓ Repository created and pushed${NC}"
fi

# 3. Set up GitHub secrets
echo -e "\n${BLUE}[3/5] Configuring GitHub Actions secrets...${NC}"

# Load environment variables
set -a
source .env
set +a

# Extract the service account JSON (being careful with special characters)
SERVICE_ACCOUNT=$(cat config/youtube_credentials.json | jq -c .)

gh secret set GEMINI_API_KEY --body "$GEMINI_API_KEY"
gh secret set PEXELS_API_KEY --body "$PEXELS_API_KEY"
gh secret set GOOGLE_APPLICATION_CREDENTIALS --body "$SERVICE_ACCOUNT"

echo -e "${GREEN}✓ Secrets configured${NC}"

# 4. Enable GitHub Actions
echo -e "\n${BLUE}[4/5] Enabling GitHub Actions...${NC}"
echo "ℹ️  GitHub Actions are automatically enabled for public repositories"
echo -e "${GREEN}✓ GitHub Actions ready${NC}"

# 5. Test credentials
echo -e "\n${BLUE}[5/5] Testing system credentials...${NC}"
python3 << 'PYTHON_TEST'
import os
from dotenv import load_dotenv
load_dotenv()

print(f"✓ Gemini API Key configured: {os.getenv('GEMINI_API_KEY')[:20]}...")
print(f"✓ Pexels API Key configured: {os.getenv('PEXELS_API_KEY')[:20]}...")
print(f"✓ YouTube credentials: {os.path.exists('config/youtube_credentials.json')}")
PYTHON_TEST

echo -e "\n${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Create YouTube channels (see create_channels.py)"
echo "2. Add service account as collaborator to each channel:"
echo "   youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com"
echo ""
echo "Run the full pipeline with:"
echo "  python -m src.main science_facts motivation_daily life_hacks history_facts finance_tips"
