#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from AlfaXmusic.utils.logger import LOGGER

class AlfaBot(Client):
    """Main bot client for AlfaXMusic"""
    
    def __init__(self):
        super().__init__(
            name="AlfaXMusic",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            in_memory=True,
            workers=100,
            max_concurrent_transmissions=10,
        )
        self.username = None
        self.logger = LOGGER("AlfaBot")
    
    async def start(self):
        """Start the bot client"""
        await super().start()
        
        # Get bot info
        me = await self.get_me()
        self.username = me.username
        self.name = me.first_name
        
        self.logger.info(f"Bot started: @{self.username}")
        
        # Send startup message to owner
        try:
            await self.send_message(
                chat_id=Config.OWNER_ID,
                text=f"🚀 **AlfaXMusic Bot Started!**\n\n"
                     f"🤖 Bot: @{self.username}\n"
                     f"👤 Owner: {Config.OWNER_ID}\n"
                     f"✅ Status: Online"
            )
        except Exception as e:
            self.logger.warning(f"Could not send startup message to owner: {e}")
    
    async def stop(self):
        """Stop the bot client"""
        self.logger.info("Stopping bot...")
        await super().stop()
    
    async def send_message_to_owner(self, text: str):
        """Send message to bot owner"""
        try:
            await self.send_message(
                chat_id=Config.OWNER_ID,
                text=text
            )
        except Exception as e:
            self.logger.error(f"Failed to send message to owner: {e}")
    
    async def get_bot_info(self) -> dict:
        """Get bot information"""
        me = await self.get_me()
        return {
            "id": me.id,
            "username": me.username,
            "name": me.first_name,
            "is_bot": me.is_bot,
        }
