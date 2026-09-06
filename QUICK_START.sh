#!/bin/bash
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     YouTube Shorts Automation - Quick Start Setup          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "\n${YELLOW}This is the ONLY time you need to do manual setup.${NC}"
echo "After this, your system runs 24/7 with zero manual work.\n"

# Step 1: GitHub Authentication
echo -e "${BLUE}[Step 1/3] GitHub Authentication${NC}"
echo "─────────────────────────────────────────────────────────────"
echo ""

if ! gh auth status > /dev/null 2>&1; then
    echo "📱 Opening GitHub login in your browser..."
    echo "   (You'll be asked to authenticate once)"
    echo ""
    echo "Instructions:"
    echo "1. A browser window will open"
    echo "2. Authorize GitHub CLI access"
    echo "3. Come back to this terminal"
    echo ""
    read -p "Press ENTER to continue..."

    gh auth login || {
        echo -e "${RED}❌ GitHub authentication failed${NC}"
        echo "Run this again when you're ready: gh auth login"
        exit 1
    }
fi

echo -e "${GREEN}✓ GitHub authenticated${NC}\n"

# Step 2: Repository & Secrets Setup
echo -e "${BLUE}[Step 2/3] Creating GitHub Repository & Configuring Secrets${NC}"
echo "─────────────────────────────────────────────────────────────"
echo ""
echo "This will:"
echo "  • Create your GitHub repository"
echo "  • Push all code"
echo "  • Configure GitHub Actions secrets"
echo "  • Test system credentials"
echo ""
echo "Running setup..."
echo ""

bash setup_automation.sh || {
    echo -e "${RED}❌ Setup failed${NC}"
    exit 1
}

echo -e "${GREEN}✓ GitHub & CI/CD configured${NC}\n"

# Step 3: YouTube Channel Creation
echo -e "${BLUE}[Step 3/3] YouTube Channel Creation${NC}"
echo "─────────────────────────────────────────────────────────────"
echo ""
echo "Two options:"
echo ""
echo "  [A] Automated with Selenium (~80% automated)"
echo "      • Script handles most steps automatically"
echo "      • You complete 1 OAuth2 login"
echo "      • Time: ~5 minutes total"
echo ""
echo "  [B] Manual guide (fastest & most reliable)"
echo "      • Step-by-step instructions provided"
echo "      • Time: ~15 minutes for all 5 channels"
echo ""
read -p "Choose [A/B]: " choice

case $choice in
    [Aa])
        echo ""
        echo "🤖 Running automated channel creation..."
        python3 create_channels.py --auto
        ;;
    [Bb])
        echo ""
        echo "📋 Showing manual guide..."
        python3 create_channels.py --guide
        ;;
    *)
        echo "Invalid choice. Showing manual guide..."
        python3 create_channels.py --guide
        ;;
esac

echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "═════════════════════════════════════════════════════════════"
echo ""
echo -e "${YELLOW}NEXT STEP: Add Service Account to YouTube Channels${NC}"
echo ""
echo "For each channel you created:"
echo "  1. Go to https://studio.youtube.com/"
echo "  2. Select the channel"
echo "  3. Settings → Permissions → Manage permissions"
echo "  4. Add collaborator:"
echo "     Email: youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com"
echo "     Role: Editor"
echo ""
echo "Once added, your system starts automatically:"
echo ""
echo -e "${BLUE}GitHub Actions Daily Schedule:${NC}"
echo "  • 12:00 AM UTC - Generate scripts"
echo "  • 6:00 AM UTC  - Create videos"
echo "  • 12:00 PM UTC - Upload to YouTube"
echo ""
echo "That's 10-15 new YouTube Shorts per day, fully automated."
echo ""
echo "═════════════════════════════════════════════════════════════"
echo ""
echo -e "${YELLOW}Optional: Monitor your progress${NC}"
echo ""
echo "  View GitHub workflows:"
echo "    gh workflow view"
echo "    gh run list"
echo ""
echo "  Local dashboard:"
echo "    python dashboard.py"
echo "    (visit http://localhost:5000)"
echo ""
echo "  Manual test:"
echo "    python -m src.main science_facts"
echo ""
echo -e "${GREEN}You're all set! 🚀${NC}"
