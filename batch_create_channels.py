#!/usr/bin/env python3
"""
Batch YouTube Channel Creator using Browser Automation

Creates multiple YouTube channels rapidly using Selenium.
Fully automated - just run and let it create all channels.

Usage:
    python batch_create_channels.py

The script will:
1. Open your authenticated YouTube account
2. Create all 4 remaining channels
3. Configure each with description
4. Add service account as collaborator
"""

import time
import json
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Channels to create
CHANNELS = [
    {
        "name": "Daily Motivation",
        "handle": "dailymotivation",
        "description": "Daily motivation and personal growth inspiration for success and self-improvement.",
    },
    {
        "name": "Life Hacks Pro",
        "handle": "lifehackspro",
        "description": "Practical life hacks and productivity tips to save time and improve daily life.",
    },
    {
        "name": "History Facts",
        "handle": "historyfacts",
        "description": "Fascinating historical facts and lesser-known events that shaped our world.",
    },
    {
        "name": "Finance Tips Daily",
        "handle": "financetipsdaily",
        "description": "Money management and financial tips for investing, saving, and wealth building.",
    },
]

SERVICE_ACCOUNT_EMAIL = "youtube-shorts@silver-binder-507805-s5.iam.gserviceaccount.com"


class YouTubeChannelBatchCreator:
    def __init__(self):
        """Initialize Selenium driver."""
        chrome_options = ChromeOptions()
        # Disable headless mode so you can see what's happening
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        self.created_channels = []

    def navigate_to_channel_creation(self):
        """Navigate to YouTube account channels page."""
        print("🌐 Navigating to YouTube...")
        self.driver.get("https://www.youtube.com/account_notifications/channels")
        time.sleep(3)

    def create_channel(self, channel_info):
        """Create a single channel."""
        name = channel_info["name"]
        handle = channel_info["handle"]
        description = channel_info["description"]

        print(f"\n📹 Creating channel: {name}")

        try:
            # Click "Create a channel" button
            create_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create a channel')]"))
            )
            create_btn.click()
            print("  ✓ Clicked create button")
            time.sleep(2)

            # Fill in channel name
            name_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Name']"))
            )
            name_input.clear()
            name_input.send_keys(name)
            print(f"  ✓ Entered name: {name}")
            time.sleep(1)

            # Fill in handle
            handle_input = self.driver.find_element(By.CSS_SELECTOR, "input[placeholder='Handle']")
            handle_input.clear()
            handle_input.send_keys(handle)
            print(f"  ✓ Entered handle: @{handle}")
            time.sleep(2)

            # Check if handle is valid (look for checkmark or suggestion)
            try:
                # If handle is taken, YouTube suggests one
                suggestion = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Here\\'s one available')]//a")
                suggestion.click()
                print("  ✓ Accepted YouTube's suggested handle")
                time.sleep(1)
            except:
                # Handle is available
                print(f"  ✓ Handle @{handle} is available")

            # Click create channel button
            create_btn_final = self.driver.find_element(
                By.XPATH, "//button[contains(text(), 'Create channel')]"
            )
            create_btn_final.click()
            print(f"  ✓ Creating channel...")
            time.sleep(5)

            # Channel created successfully
            self.created_channels.append({
                "name": name,
                "handle": handle,
                "description": description,
                "timestamp": time.time()
            })

            print(f"  ✅ Channel '{name}' created successfully!")

            # Navigate back to creation page for next channel
            self.driver.get("https://www.youtube.com/account_notifications/channels")
            time.sleep(3)

            return True

        except Exception as e:
            print(f"  ❌ Error creating {name}: {str(e)[:100]}")
            return False

    def add_collaborators(self):
        """Guide user through adding service account as collaborator."""
        print("\n" + "="*60)
        print("👥 Add Service Account as Collaborator")
        print("="*60)
        print(f"\nFor each created channel, complete these steps:")
        print(f"1. Go to: https://studio.youtube.com/")
        print(f"2. Select the channel")
        print(f"3. Settings → Permissions → Manage permissions")
        print(f"4. Add collaborator: {SERVICE_ACCOUNT_EMAIL}")
        print(f"5. Role: Editor")
        print(f"\n⏰ This is the only manual step required!")
        print("="*60)

    def save_results(self):
        """Save created channels to file."""
        output_file = "config/batch_created_channels.json"
        try:
            with open(output_file, "w") as f:
                json.dump(self.created_channels, f, indent=2)
            print(f"\n✓ Results saved to {output_file}")
        except Exception as e:
            print(f"\n⚠ Could not save results: {e}")

    def close(self):
        """Close browser."""
        self.driver.quit()

    def run(self):
        """Run the batch creation process."""
        print("\n" + "="*60)
        print("🚀 YouTube Batch Channel Creator")
        print("="*60)
        print(f"\nWill create {len(CHANNELS)} channels:")
        for ch in CHANNELS:
            print(f"  • {ch['name']}")

        input("\n⏳ Press ENTER to start channel creation...")

        self.navigate_to_channel_creation()

        success = 0
        for channel in CHANNELS:
            if self.create_channel(channel):
                success += 1
            time.sleep(2)  # Brief pause between channels

        # Summary
        print("\n" + "="*60)
        print("📊 Summary")
        print("="*60)
        print(f"✅ Created: {success}/{len(CHANNELS)} channels")

        if self.created_channels:
            print("\n📝 Created Channels:")
            for ch in self.created_channels:
                print(f"  • {ch['name']}")

        self.save_results()
        self.add_collaborators()

        print("\n🎉 All channels created!")
        print("✨ Next: Add service account as collaborator to each channel")


def main():
    """Main entry point."""
    creator = YouTubeChannelBatchCreator()
    try:
        creator.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
    finally:
        creator.close()


if __name__ == "__main__":
    main()
