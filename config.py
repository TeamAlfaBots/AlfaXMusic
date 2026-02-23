#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import os
from typing import Optional

class Config:
    """Configuration class for AlfaXMusic Bot"""
    
    # ==================== REQUIRED ====================
    
    # Telegram API credentials
    API_ID: int = int(os.getenv("API_ID", 0))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017/AlfaXMusic")
    
    # Owner ID
    OWNER_ID: int = int(os.getenv("OWNER_ID", 0))
    
    # ==================== OPTIONAL ====================
    
    # Userbot Session (optional but recommended)
    SESSION_STRING: Optional[str] = os.getenv("SESSION_STRING", None)
    
    # Spotify API (optional)
    SPOTIFY_CLIENT_ID: Optional[str] = os.getenv("SPOTIFY_CLIENT_ID", None)
    SPOTIFY_CLIENT_SECRET: Optional[str] = os.getenv("SPOTIFY_CLIENT_SECRET", None)
    
    # ==================== IMAGES ====================
    
    # Start image URL
    START_IMG_URL: Optional[str] = os.getenv("START_IMG_URL", None)
    
    # Ping image URL
    PING_IMG_URL: Optional[str] = os.getenv("PING_IMG_URL", None)
    
    # ==================== BUTTONS ====================
    
    # Support URL
    SUPPORT_URL: Optional[str] = os.getenv("SUPPORT_URL", None)
    
    # Updates URL
    UPDATES_URL: Optional[str] = os.getenv("UPDATES_URL", None)
    
    # Repository URL
    REPO_URL: Optional[str] = os.getenv("REPO_URL", None)
    
    # Developer URL
    DEV_URL: Optional[str] = os.getenv("DEV_URL", None)
    
    # Privacy Policy URL
    PRIVACY_URL: Optional[str] = os.getenv("PRIVACY_URL", None)
    
    # Add to Group URL
    ADD_GROUP_URL: Optional[str] = os.getenv("ADD_GROUP_URL", None)
    
    # Questions URL
    QUESTIONS_URL: Optional[str] = os.getenv("QUESTIONS_URL", None)
    
    # ==================== SETTINGS ====================
    
    # Default language
    DEFAULT_LANG: str = os.getenv("DEFAULT_LANG", "en")
    
    # Max queue size
    MAX_QUEUE_SIZE: int = int(os.getenv("MAX_QUEUE_SIZE", 200))
    
    # Max playlist songs
    MAX_PLAYLIST_SONGS: int = int(os.getenv("MAX_PLAYLIST_SONGS", 100))
    
    # Maintenance mode
    MAINTENANCE_MODE: bool = os.getenv("MAINTENANCE_MODE", "False").lower() == "true"
    
    # ==================== VALIDATION ====================
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        required_vars = [
            ("API_ID", cls.API_ID),
            ("API_HASH", cls.API_HASH),
            ("BOT_TOKEN", cls.BOT_TOKEN),
            ("MONGO_URI", cls.MONGO_URI),
            ("OWNER_ID", cls.OWNER_ID),
        ]
        
        missing = []
        for name, value in required_vars:
            if not value:
                missing.append(name)
        
        if missing:
            print(f"❌ Missing required environment variables: {', '.join(missing)}")
            return False
        
        return True

# Create config instance
config = Config()
