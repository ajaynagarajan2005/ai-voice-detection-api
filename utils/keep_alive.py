"""
Keep-Alive Service for Hugging Face Spaces
Pings the API every 24 hours to prevent sleep
"""
import requests
import time
import os
from datetime import datetime

# Your Hugging Face Space URL (update after deployment)
API_URL = "https://tamizh019-ai-voice-detection.hf.space/health"

# Ping interval (24 hours in seconds)
PING_INTERVAL = 24 * 60 * 60  # 86400 seconds

def ping_api():
    """Send a simple health check request to keep the API alive"""
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            print(f"✅ [{datetime.now()}] API is alive!")
            return True
        else:
            print(f"⚠️ [{datetime.now()}] API returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ [{datetime.now()}] Failed to ping API: {str(e)}")
        return False

def main():
    print(f"🚀 Keep-Alive Service Started")
    print(f"📍 Target: {API_URL}")
    print(f"⏰ Ping interval: Every 24 hours\n")
    
    while True:
        ping_api()
        print(f"💤 Sleeping for 24 hours...\n")
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()
