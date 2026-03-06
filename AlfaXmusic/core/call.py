#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import asyncio
from typing import Optional, Dict, List, Callable
from datetime import datetime

from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types import Update, AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from pyrogram.raw.base import InputPeer
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import Config
from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.utils.logger import LOGGER
from AlfaXmusic.utils.thumbnails import generate_thumbnail

class AlfaCall:
    """PyTgCalls handler for voice chat streaming"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.call: Optional[PyTgCalls] = None
        self.bot: Optional[AlfaBot] = None
        self.mongo: Optional[AlfaMongo] = None
        self.logger = LOGGER("AlfaCall")
        
        # Active chats data
        self.active_chats: Dict[int, Dict] = {}
        self.queues: Dict[int, List[Dict]] = {}
        self.loop_status: Dict[int, bool] = {}
        self.shuffle_status: Dict[int, bool] = {}
        self.current_song: Dict[int, Dict] = {}
        
        self._initialized = True
    
    async def start(self):
        """Initialize PyTgCalls"""
        try:
            # Initialize bot instance
            self.bot = AlfaBot()
            self.mongo = AlfaMongo()
            
            # Initialize PyTgCalls with bot
            self.call = PyTgCalls(self.bot)
            
            # Register event handlers
            self.call.on_stream_end()(self._on_stream_end)
            self.call.on_kicked()(self._on_kicked)
            self.call.on_closed_voice_chat()(self._on_closed_voice_chat)
            self.call.on_left()(self._on_left)
            
            await self.call.start()
            self.logger.info("PyTgCalls started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start PyTgCalls: {e}")
            raise
    
    async def stop(self):
        """Stop PyTgCalls"""
        if self.call:
            await self.call.stop()
            self.logger.info("PyTgCalls stopped")
    
    async def _on_stream_end(self, client: PyTgCalls, update: Update):
        """Handle stream end event"""
        chat_id = update.chat_id
        
        self.logger.info(f"Stream ended in chat {chat_id}")
        
        # Check if loop is enabled
        if self.loop_status.get(chat_id, False) and self.current_song.get(chat_id):
            # Replay current song
            song = self.current_song[chat_id]
            await self.play(chat_id, song)
            return
        
        # Play next song in queue
        await self.play_next(chat_id)
    
    async def _on_kicked(self, client: PyTgCalls, chat_id: int):
        """Handle bot kicked from chat"""
        self.logger.warning(f"Bot kicked from chat {chat_id}")
        await self._cleanup_chat(chat_id)
    
    async def _on_closed_voice_chat(self, client: PyTgCalls, chat_id: int):
        """Handle voice chat closed"""
        self.logger.info(f"Voice chat closed in chat {chat_id}")
        await self._cleanup_chat(chat_id)
    
    async def _on_left(self, client: PyTgCalls, chat_id: int):
        """Handle bot left chat"""
        self.logger.info(f"Bot left chat {chat_id}")
        await self._cleanup_chat(chat_id)
    
    async def _cleanup_chat(self, chat_id: int):
        """Clean up chat data"""
        self.active_chats.pop(chat_id, None)
        self.queues.pop(chat_id, None)
        self.loop_status.pop(chat_id, None)
        self.shuffle_status.pop(chat_id, None)
        self.current_song.pop(chat_id, None)
        
        # Clear from database
        await self.mongo.clear_queue(chat_id)
    
    async def join_call(self, chat_id: int) -> bool:
        """Join a voice chat"""
        try:
            # Check if already in call
            if chat_id in self.active_chats:
                return True
            
            # Join the call
            await self.call.join_group_call(
                chat_id,
                AudioPiped(
                    "assets/silence.mp3",  # Silent audio to join
                ),
                stream_type=StreamType().pulse_stream,
            )
            
            self.active_chats[chat_id] = {
                "joined_at": datetime.utcnow(),
                "is_playing": False
            }
            
            self.logger.info(f"Joined voice chat in {chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to join voice chat: {e}")
            return False
    
    async def leave_call(self, chat_id: int) -> bool:
        """Leave a voice chat"""
        try:
            await self.call.leave_group_call(chat_id)
            await self._cleanup_chat(chat_id)
            
            self.logger.info(f"Left voice chat in {chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to leave voice chat: {e}")
            return False
    
    async def play(self, chat_id: int, song: Dict) -> bool:
        """Play a song in voice chat"""
        try:
            # Join call if not already
            if chat_id not in self.active_chats:
                success = await self.join_call(chat_id)
                if not success:
                    return False
            
            # Get audio URL
            audio_url = song.get("audio_url") or song.get("url")
            if not audio_url:
                self.logger.error("No audio URL provided")
                return False
            
            # Change stream
            await self.call.change_stream(
                chat_id,
                AudioPiped(audio_url)
            )
            
            # Update current song
            self.current_song[chat_id] = song
            self.active_chats[chat_id]["is_playing"] = True
            
            # Log to database
            await self.mongo.add_play_history(chat_id, song)
            await self.mongo.increment_stat("songs_played")
            
            # Send now playing message
            await self._send_now_playing(chat_id, song)
            
            self.logger.info(f"Playing: {song.get('title', 'Unknown')} in {chat_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to play song: {e}")
            return False
    
    async def play_next(self, chat_id: int) -> bool:
        """Play next song in queue"""
        queue = self.queues.get(chat_id, [])
        
        if not queue:
            # No more songs
            self.active_chats[chat_id]["is_playing"] = False
            self.current_song.pop(chat_id, None)
            return False
        
        # Get next song
        next_song = queue.pop(0)
        self.queues[chat_id] = queue
        
        # Update database queue
        await self.mongo.set_queue(chat_id, queue)
        
        # Play the song
        return await self.play(chat_id, next_song)
    
    async def add_to_queue(self, chat_id: int, song: Dict) -> int:
        """Add song to queue, returns queue position"""
        if chat_id not in self.queues:
            self.queues[chat_id] = []
        
        self.queues[chat_id].append(song)
        
        # Update database
        await self.mongo.set_queue(chat_id, self.queues[chat_id])
        
        return len(self.queues[chat_id])
    
    async def get_queue(self, chat_id: int) -> List[Dict]:
        """Get queue for a chat"""
        return self.queues.get(chat_id, [])
    
    async def clear_queue(self, chat_id: int):
        """Clear queue for a chat"""
        self.queues[chat_id] = []
        await self.mongo.clear_queue(chat_id)
    
    async def skip(self, chat_id: int) -> bool:
        """Skip current song"""
        try:
            await self.call.change_stream(chat_id, AudioPiped("assets/silence.mp3"))
            return await self.play_next(chat_id)
        except Exception as e:
            self.logger.error(f"Failed to skip: {e}")
            return False
    
    async def pause(self, chat_id: int) -> bool:
        """Pause playback"""
        try:
            await self.call.pause_stream(chat_id)
            self.active_chats[chat_id]["is_playing"] = False
            return True
        except Exception as e:
            self.logger.error(f"Failed to pause: {e}")
            return False
    
    async def resume(self, chat_id: int) -> bool:
        """Resume playback"""
        try:
            await self.call.resume_stream(chat_id)
            self.active_chats[chat_id]["is_playing"] = True
            return True
        except Exception as e:
            self.logger.error(f"Failed to resume: {e}")
            return False
    
    async def set_volume(self, chat_id: int, volume: int) -> bool:
        """Set volume (0-200)"""
        try:
            await self.call.change_volume_call(chat_id, volume)
            return True
        except Exception as e:
            self.logger.error(f"Failed to set volume: {e}")
            return False
    
    def toggle_loop(self, chat_id: int) -> bool:
        """Toggle loop mode"""
        current = self.loop_status.get(chat_id, False)
        self.loop_status[chat_id] = not current
        return self.loop_status[chat_id]
    
    def toggle_shuffle(self, chat_id: int) -> bool:
        """Toggle shuffle mode"""
        current = self.shuffle_status.get(chat_id, False)
        self.shuffle_status[chat_id] = not current
        return self.shuffle_status[chat_id]
    
    def is_playing(self, chat_id: int) -> bool:
        """Check if playing in chat"""
        return self.active_chats.get(chat_id, {}).get("is_playing", False)
    
    def get_current_song(self, chat_id: int) -> Optional[Dict]:
        """Get current playing song"""
        return self.current_song.get(chat_id)
    
    async def _send_now_playing(self, chat_id: int, song: Dict):
        """Send now playing message"""
        try:
            # Generate thumbnail
            thumb_path = await generate_thumbnail(song)
            
            # Create buttons
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⏸️ Pause", callback_data=f"pause|{chat_id}"),
                    InlineKeyboardButton("⏭️ Skip", callback_data=f"skip|{chat_id}"),
                    InlineKeyboardButton("🔁 Loop", callback_data=f"loop|{chat_id}"),
                ],
                [
                    InlineKeyboardButton("📋 Queue", callback_data=f"queue|{chat_id}"),
                    InlineKeyboardButton("⏹️ Stop", callback_data=f"stop|{chat_id}"),
                ]
            ])
            
            # Send message
            duration = song.get('duration', 'Unknown')
            if isinstance(duration, int):
                minutes = duration // 60
                seconds = duration % 60
                duration = f"{minutes}:{seconds:02d}"
            
            caption = (
                f"🎵 **Now Playing**\n\n"
                f"**Title:** {song.get('title', 'Unknown')}\n"
                f"**Artist:** {song.get('artist', 'Unknown')}\n"
                f"**Duration:** {duration}\n"
                f"**Requested by:** {song.get('requested_by', 'Unknown')}"
            )
            
            if thumb_path:
                await self.bot.send_photo(
                    chat_id=chat_id,
                    photo=thumb_path,
                    caption=caption,
                    reply_markup=buttons
                )
            else:
                await self.bot.send_message(
                    chat_id=chat_id,
                    text=caption,
                    reply_markup=buttons
                )
                
        except Exception as e:
            self.logger.error(f"Failed to send now playing: {e}")
