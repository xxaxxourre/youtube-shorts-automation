#!/usr/bin/env python3
"""
Automated YouTube Channel Creation

This script automates the creation of YouTube channels using Selenium.
It requires a Google account with YouTube access.

IMPORTANT: You must complete the OAuth2 flow manually (bot detection prevention)
but the script handles all the repetitive steps.
"""

import os
import json
import time
import argparse
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def create_channels_selenium():
    """Create YouTube channels using Selenium automation."""
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
    except ImportError:
        print("❌ Selenium not installed. Install with:")
        print("   pip install selenium webdriver-manager")
        return False

    # Channel configuration
    channels_to_create = [
        {
            "name": "Science Facts Daily",
            "handle": "@sciencefactsdaily",
            "description": "Daily fascinating science and space facts"
        },
        {
            "name": "Daily Motivation",
            "handle": "@dailymotivation",
            "description": "Daily motivation and personal growth inspiration"
        },
        {
            "name": "Life Hacks Pro",
            "handle": "@lifehackspro",
            "description": "Practical life hacks and productivity tips"
        },
        {
            "name": "History Facts",
            "handle": "@historyfacts",
            "description": "Fascinating historical facts and events"
        },
        {
            "name": "Finance Tips Daily",
            "handle": "@financetipsdaily",
            "description": "Money management and financial tips"
        }
    ]

    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        driver = webdriver.Chrome(options=chrome_options)

        # Navigate to YouTube Studio
        print("🔐 Opening YouTube Studio...")
        driver.get("https://studio.youtube.com/")

        # User must authenticate manually
        print("\n📱 Please log in with your Google account in the browser")
        print("   (Waiting for 60 seconds...)")
        time.sleep(60)

        # Check if logged in
        if "studio.youtube.com" not in driver.current_url:
            print("❌ Authentication failed")
            return False

        print("✓ Authentication successful\n")

        # Create each channel
        for i, channel in enumerate(channels_to_create, 1):
            print(f"[{i}/{len(channels_to_create)}] Creating channel: {channel['name']}")

            try:
                # Navigate to create channel
                driver.get("https://studio.youtube.com/")
                time.sleep(2)

                # Look for the "Create a channel" button
                # Note: YouTube's UI changes frequently, adjust selectors if needed
                try:
                    create_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Create')]")
                    create_btn.click()
                except:
                    print(f"⚠️  Could not find 'Create' button for channel {i}")
                    print("   Manual creation may be needed. YouTube UI may have changed.")
                    continue

                time.sleep(2)

                # Fill in channel name
                try:
                    name_input = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "input-box"))
                    )
                    name_input.clear()
                    name_input.send_keys(channel['name'])
                except:
                    print(f"⚠️  Could not enter channel name for {channel['name']}")
                    continue

                time.sleep(1)

                # Click create button
                try:
                    create_confirm = driver.find_element(By.XPATH, "//*[contains(text(), 'Create channel')]")
                    create_confirm.click()
                    time.sleep(5)
                    print(f"✓ Channel '{channel['name']}' created")
                except:
                    print(f"⚠️  Could not confirm channel creation for {channel['name']}")

            except Exception as e:
                print(f"⚠️  Error creating channel {channel['name']}: {str(e)}")
                continue

        print("\n" + "="*60)
        print("✅ Channel creation complete!")
        print("="*60)
        print("\nNext steps:")
        print("1. Go to YouTube Settings for each channel")
        print("2. Add collaborator: youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com")
        print("3. Grant them Editor access")
        print("\nAfter setup, run:")
        print("  python -m src.main science_facts motivation_daily life_hacks history_facts finance_tips")

        return True

    except Exception as e:
        print(f"❌ Error during channel creation: {e}")
        return False
    finally:
        if driver:
            driver.quit()

def create_channels_manual_guide():
    """Provide manual guide for channel creation."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║         YouTube Channel Creation - Quick Guide               ║
╚══════════════════════════════════════════════════════════════╝

📋 Create these 5 channels:

1. Science Facts Daily
   - Handle: @sciencefactsdaily
   - Description: Daily fascinating science and space facts

2. Daily Motivation
   - Handle: @dailymotivation
   - Description: Daily motivation and personal growth inspiration

3. Life Hacks Pro
   - Handle: @lifehackspro
   - Description: Practical life hacks and productivity tips

4. History Facts
   - Handle: @historyfacts
   - Description: Fascinating historical facts and events

5. Finance Tips Daily
   - Handle: @financetipsdaily
   - Description: Money management and financial tips

🔗 Steps for each channel:

1. Go to https://studio.youtube.com/
2. Click "+" icon → "Create a channel"
3. Enter channel name and description
4. Customize basic settings (profile picture, banner)
5. Go to Settings → Permissions → Manage permissions
6. Add collaborator:
   Email: youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com
   Role: Editor

⏱️  Total time: ~15 minutes for all 5 channels

After creation, run:
  python -m src.main science_facts motivation_daily life_hacks history_facts finance_tips

""")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Automated YouTube Channel Creation"
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Attempt automated creation with Selenium"
    )
    parser.add_argument(
        "--guide",
        action="store_true",
        default=True,
        help="Show manual creation guide (default)"
    )

    args = parser.parse_args()

    if args.auto:
        print("🤖 Attempting automated channel creation with Selenium...")
        success = create_channels_selenium()
        if not success:
            print("\n⚠️  Falling back to manual guide...")
            create_channels_manual_guide()
    else:
        create_channels_manual_guide()
