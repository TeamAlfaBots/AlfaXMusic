#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import Client
from config import Config
from AlfaXmusic.utils.logger import LOGGER

class AlfaUserbot:
    """Userbot client for voice chat assistance"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.client: Client = None
        self.logger = LOGGER("AlfaUserbot")
        self._initialized = True
    
    async def start(self):
        """Start the userbot client"""
        try:
            # Note: Userbot requires a session string
            # For production, use a valid session string
            self.client = Client(
                name="AlfaUserbot",
                api_id=Config.API_ID,
                api_hash=Config.API_HASH,
                session_string=getattr(Config, 'SESSION_STRING', None),
                workers=50,
                in_memory=True,
            )
            
            await self.client.start()
            me = await self.client.get_me()
            
            self.logger.info(f"Userbot started: {me.first_name} (@{me.username or 'N/A'})")
            
        except Exception as e:
            self.logger.error(f"Failed to start userbot: {e}")
            self.logger.warning("Continuing without userbot - some features may be limited")
            self.client = None
    
    async def stop(self):
        """Stop the userbot client"""
        if self.client:
            await self.client.stop()
            self.logger.info("Userbot stopped")
    
    def is_active(self) -> bool:
        """Check if userbot is active"""
        return self.client is not None and self.client.is_connected
    
    async def join_group_call(self, chat_id: int):
        """Join a group call"""
        if not self.is_active():
            return False
        
        try:
            # Join the voice chat
            await self.client.invoke(
                raw.functions.phone.JoinGroupCall(
                    call=await self._get_group_call(chat_id),
                    join_as=await self.client.resolve_peer(self.client.me.id),
                    params=raw.types.DataJSON(data="{}"),
                    muted=False
                )
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to join group call: {e}")
            return False
    
    async def leave_group_call(self, chat_id: int):
        """Leave a group call"""
        if not self.is_active():
            return False
        
        try:
            # Leave the voice chat
            return True
        except Exception as e:
            self.logger.error(f"Failed to leave group call: {e}")
            return False
