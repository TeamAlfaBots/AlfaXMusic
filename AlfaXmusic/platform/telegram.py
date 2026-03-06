#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from typing import Optional, Dict

from pyrogram.types import Message

from AlfaXmusic.utils.logger import LOGGER

class TelegramPlatform:
    """Telegram audio platform handler"""
    
    def __init__(self):
        self.logger = LOGGER("Telegram")
    
    def is_telegram_audio(self, message: Message) -> bool:
        """Check if message contains audio"""
        return bool(
            message.audio or 
            message.voice or 
            message.video_note or
            (message.document and message.document.mime_type and 
             'audio' in message.document.mime_type)
        )
    
    async def extract_audio_info(self, message: Message) -> Optional[Dict]:
        """Extract audio information from message"""
        try:
            audio = message.audio or message.voice or message.video_note or message.document
            
            if not audio:
                return None
            
            # Get file info
            file_id = audio.file_id
            file_size = getattr(audio, 'file_size', 0)
            duration = getattr(audio, 'duration', 0)
            
            # Get metadata
            title = getattr(audio, 'title', None) or getattr(audio, 'file_name', 'Unknown')
            performer = getattr(audio, 'performer', 'Unknown')
            
            # Get thumbnail
            thumb = getattr(audio, 'thumb', None)
            thumbnail = thumb.file_id if thumb else None
            
            return {
                'title': title,
                'artist': performer,
                'duration': duration,
                'file_id': file_id,
                'file_size': file_size,
                'thumbnail': thumbnail,
                'message_id': message.message_id,
                'chat_id': message.chat.id,
                'platform': 'telegram'
            }
            
        except Exception as e:
            self.logger.error(f"Error extracting audio info: {e}")
            return None
    
    async def get_audio_file(self, client, file_id: str) -> Optional[str]:
        """Download audio file and return path"""
        try:
            file_path = await client.download_media(file_id)
            return file_path
        except Exception as e:
            self.logger.error(f"Error downloading audio: {e}")
            return None

# Global instance
telegram = TelegramPlatform()
