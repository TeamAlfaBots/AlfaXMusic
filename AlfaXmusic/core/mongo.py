#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from typing import List, Dict, Optional, Any
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING

from config import Config
from AlfaXmusic.utils.logger import LOGGER

class AlfaMongo:
    """MongoDB handler for AlfaXMusic"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        self.logger = LOGGER("AlfaMongo")
        self._initialized = True
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(
                Config.MONGO_URI,
                serverSelectionTimeoutMS=5000
            )
            
            # Get database
            self.db = self.client["AlfaXMusic"]
            
            # Create collections and indexes
            await self._setup_collections()
            
            # Test connection
            await self.client.admin.command('ping')
            self.logger.info("MongoDB connected successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def _setup_collections(self):
        """Setup collections and indexes"""
        # Users collection
        await self.db.users.create_index("user_id", unique=True)
        
        # Chats collection
        await self.db.chats.create_index("chat_id", unique=True)
        
        # Playlists collection
        await self.db.playlists.create_index("chat_id")
        await self.db.playlists.create_index([("played_at", DESCENDING)])
        
        # Stats collection
        await self.db.stats.create_index("type", unique=True)
        
        # Sudo users collection
        await self.db.sudo_users.create_index("user_id", unique=True)
        
        # Settings collection
        await self.db.settings.create_index("chat_id", unique=True)
        
        # Queue collection
        await self.db.queue.create_index("chat_id", unique=True)
    
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")
    
    # ==================== USER METHODS ====================
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add or update user"""
        await self.db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "username": username,
                    "first_name": first_name,
                    "last_seen": datetime.utcnow()
                },
                "$setOnInsert": {
                    "user_id": user_id,
                    "joined_at": datetime.utcnow()
                }
            },
            upsert=True
        )
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        return await self.db.users.find_one({"user_id": user_id})
    
    async def get_all_users(self) -> List[Dict]:
        """Get all users"""
        return await self.db.users.find().to_list(length=None)
    
    async def get_users_count(self) -> int:
        """Get total users count"""
        return await self.db.users.count_documents({})
    
    # ==================== CHAT METHODS ====================
    
    async def add_chat(self, chat_id: int, title: str = None, chat_type: str = None):
        """Add or update chat"""
        await self.db.chats.update_one(
            {"chat_id": chat_id},
            {
                "$set": {
                    "title": title,
                    "type": chat_type,
                    "last_active": datetime.utcnow()
                },
                "$setOnInsert": {
                    "chat_id": chat_id,
                    "added_at": datetime.utcnow()
                }
            },
            upsert=True
        )
    
    async def get_chat(self, chat_id: int) -> Optional[Dict]:
        """Get chat by ID"""
        return await self.db.chats.find_one({"chat_id": chat_id})
    
    async def get_all_chats(self) -> List[Dict]:
        """Get all chats"""
        return await self.db.chats.find().to_list(length=None)
    
    async def get_chats_count(self) -> int:
        """Get total chats count"""
        return await self.db.chats.count_documents({})
    
    # ==================== PLAYLIST HISTORY ====================
    
    async def add_play_history(self, chat_id: int, song: Dict):
        """Add song to play history"""
        await self.db.playlists.insert_one({
            "chat_id": chat_id,
            "song": song,
            "played_at": datetime.utcnow()
        })
    
    async def get_chat_history(self, chat_id: int, limit: int = 50) -> List[Dict]:
        """Get chat's play history"""
        cursor = self.db.playlists.find(
            {"chat_id": chat_id}
        ).sort("played_at", DESCENDING).limit(limit)
        return await cursor.to_list(length=limit)
    
    # ==================== STATS METHODS ====================
    
    async def increment_stat(self, stat_type: str, value: int = 1):
        """Increment a stat counter"""
        await self.db.stats.update_one(
            {"type": stat_type},
            {
                "$inc": {"count": value},
                "$set": {"updated_at": datetime.utcnow()},
                "$setOnInsert": {"created_at": datetime.utcnow()}
            },
            upsert=True
        )
    
    async def get_stat(self, stat_type: str) -> int:
        """Get stat value"""
        doc = await self.db.stats.find_one({"type": stat_type})
        return doc.get("count", 0) if doc else 0
    
    async def get_all_stats(self) -> Dict[str, int]:
        """Get all stats"""
        cursor = self.db.stats.find()
        stats = {}
        async for doc in cursor:
            stats[doc.get("type", "unknown")] = doc.get("count", 0)
        return stats
    
    # ==================== SUDO USERS ====================
    
    async def add_sudo_user(self, user_id: int):
        """Add sudo user"""
        await self.db.sudo_users.update_one(
            {"user_id": user_id},
            {"$set": {"user_id": user_id, "added_at": datetime.utcnow()}},
            upsert=True
        )
    
    async def remove_sudo_user(self, user_id: int):
        """Remove sudo user"""
        await self.db.sudo_users.delete_one({"user_id": user_id})
    
    async def get_sudo_users(self) -> List[int]:
        """Get all sudo user IDs"""
        cursor = self.db.sudo_users.find()
        users = await cursor.to_list(length=None)
        return [u["user_id"] for u in users]
    
    # ==================== SETTINGS ====================
    
    async def get_chat_settings(self, chat_id: int) -> Dict:
        """Get chat settings"""
        settings = await self.db.settings.find_one({"chat_id": chat_id})
        if not settings:
            default_settings = {
                "chat_id": chat_id,
                "language": "en",
                "volume": 100,
                "loop": False,
                "shuffle": False,
                "auto_play": False
            }
            await self.db.settings.insert_one(default_settings)
            return default_settings
        return settings
    
    async def update_chat_setting(self, chat_id: int, key: str, value: Any):
        """Update a chat setting"""
        await self.db.settings.update_one(
            {"chat_id": chat_id},
            {"$set": {key: value}},
            upsert=True
        )
    
    # ==================== QUEUE METHODS ====================
    
    async def get_queue(self, chat_id: int) -> List[Dict]:
        """Get chat's music queue"""
        doc = await self.db.queue.find_one({"chat_id": chat_id})
        return doc.get("queue", []) if doc else []
    
    async def set_queue(self, chat_id: int, queue: List[Dict]):
        """Set chat's music queue"""
        await self.db.queue.update_one(
            {"chat_id": chat_id},
            {"$set": {"queue": queue, "updated_at": datetime.utcnow()}},
            upsert=True
        )
    
    async def clear_queue(self, chat_id: int):
        """Clear chat's music queue"""
        await self.db.queue.delete_one({"chat_id": chat_id})
    
    # ==================== BROADCAST ====================
    
    async def log_broadcast(self, total: int, success: int, failed: int):
        """Log broadcast statistics"""
        await self.db.broadcasts.insert_one({
            "total": total,
            "success": success,
            "failed": failed,
            "timestamp": datetime.utcnow()
        })
