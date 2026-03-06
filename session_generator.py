#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

"""
Session String Generator for AlfaXMusic

This script generates a session string for the userbot.
Run this before starting the bot for the first time.
"""

import asyncio
import os

from pyrogram import Client

print("======================================")
print("  AlfaXMusic - Session Generator")
print("  Powered by Alfa Bots")
print("======================================")
print()

# Get credentials
API_ID = input("Enter your API_ID: ").strip()
API_HASH = input("Enter your API_HASH: ").strip()

if not API_ID or not API_HASH:
    print("❌ API_ID and API_HASH are required!")
    exit(1)

async def generate_session():
    """Generate session string"""
    
    print("\n📱 Starting session generation...")
    print("Please enter your phone number with country code (e.g., +1234567890)")
    
    async with Client(
        name="AlfaSession",
        api_id=int(API_ID),
        api_hash=API_HASH,
        in_memory=True
    ) as app:
        
        session_string = await app.export_session_string()
        
        print("\n" + "="*50)
        print("✅ Session String Generated Successfully!")
        print("="*50)
        print()
        print("Your Session String:")
        print("-"*50)
        print(session_string)
        print("-"*50)
        print()
        print("⚠️  IMPORTANT: Keep this string secret!")
        print("Add it to your .env file as SESSION_STRING")
        print()
        print("Example:")
        print(f"SESSION_STRING={session_string}")
        print()

if __name__ == "__main__":
    asyncio.run(generate_session())
