#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import asyncio
import yaml
from pathlib import Path

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.call import AlfaCall
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.platform.youtube import youtube
from AlfaXmusic.platform.spotify import spotify
from AlfaXmusic.utils.decorators import admin_only, authorized_chat
from AlfaXmusic.utils.logger import LOGGER
from AlfaXmusic.utils.thumbnails import generate_thumbnail

logger = LOGGER("PlayCmd")
bot = AlfaBot()
call = AlfaCall()
mongo = AlfaMongo()

# Playlist mapping
PLAYLIST_MAP = {
    "90shits": "90sHits",
    "arijit singh sad": "arijitsingh",
    "arijit singh love": "arijitsinghLove",
    "punjabi hits": "PunjabiHits",
    "bhojpuri hits": "bhojpurihits",
    "sad": "sad",
    "romantic": "romatic",
    "dance": "dance",
}

def load_playlist(playlist_name: str) -> list:
    """Load playlist from YAML file"""
    try:
        # Normalize playlist name
        playlist_key = playlist_name.lower().replace(" ", "")
        
        # Map to filename
        filename = PLAYLIST_MAP.get(playlist_key)
        if not filename:
            return None
        
        # Load YAML file
        playlist_path = Path(__file__).parent.parent.parent / "assets" / f"{filename}.yml"
        
        if not playlist_path.exists():
            return None
        
        with open(playlist_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data.get('songs', [])
            
    except Exception as e:
        logger.error(f"Error loading playlist: {e}")
        return None

async def process_song_request(query: str, user_id: int, user_name: str) -> dict:
    """Process a song request and return song data"""
    
    # Check if it's a YouTube URL
    if youtube.is_youtube_url(query):
        video_id = youtube.extract_video_id(query)
        if video_id:
            song = await youtube.get_video_info(video_id)
            if song:
                song['requested_by'] = user_name
                song['requested_by_id'] = user_id
                return song
    
    # Check if it's a Spotify URL
    if spotify.is_spotify_url(query):
        spot_type, spot_id = spotify.extract_spotify_id(query)
        if spot_type == 'track':
            song = await spotify.get_track(spot_id)
            if song:
                song['requested_by'] = user_name
                song['requested_by_id'] = user_id
                return song
    
    # Search YouTube
    search_results = await youtube.search(query, limit=1)
    if search_results:
        video = search_results[0]
        song = await youtube.get_video_info(video['id'])
        if song:
            song['requested_by'] = user_name
            song['requested_by_id'] = user_id
            return song
    
    return None

@bot.on_message(filters.command("play"))
@authorized_chat
async def play_command(client, message: Message):
    """Handle /play command"""
    
    # Check if command has arguments
    if len(message.command) < 2:
        await message.reply_text(
            "🎵 **Usage:**\n"
            "`/play <song name>` - Search and play\n"
            "`/play <YouTube URL>` - Play from URL\n"
            "`/play <playlist name>` - Play playlist\n\n"
            "**Available Playlists:**\n"
            "• 90sHits\n"
            "• Arijit Singh Sad\n"
            "• Arijit Singh Love\n"
            "• Punjabi Hits\n"
            "• Bhojpuri Hits\n"
            "• Sad\n"
            "• Romantic\n"
            "• Dance"
        )
        return
    
    # Get query
    query = " ".join(message.command[1:])
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.mention
    
    # Check if it's a playlist request
    playlist_songs = load_playlist(query)
    
    if playlist_songs:
        # Playlist mode
        status_msg = await message.reply_text(
            f"📂 **Loading Playlist:** `{query}`\n"
            f"🎵 **Songs:** {len(playlist_songs)}\n"
            f"⏳ Please wait..."
        )
        
        # Process first song
        first_song = await process_song_request(playlist_songs[0], user_id, user_name)
        
        if not first_song:
            await status_msg.edit_text("❌ Failed to load playlist. Try again.")
            return
        
        # Play first song
        await call.play(chat_id, first_song)
        
        # Queue remaining songs
        remaining = playlist_songs[1:]
        for song_name in remaining:
            song = await process_song_request(song_name, user_id, user_name)
            if song:
                await call.add_to_queue(chat_id, song)
        
        await status_msg.edit_text(
            f"✅ **Playlist Loaded:** `{query}`\n"
            f"🎵 **Total Songs:** {len(playlist_songs)}\n"
            f"▶️ Now playing first song..."
        )
        
        # Increment stats
        await mongo.increment_stat("playlists_played")
        return
    
    # Single song mode
    status_msg = await message.reply_text("🔍 **Searching...** Please wait.")
    
    # Process song request
    song = await process_song_request(query, user_id, user_name)
    
    if not song:
        await status_msg.edit_text("❌ **Song not found.** Try a different query.")
        return
    
    # Check if already playing
    if call.is_playing(chat_id):
        # Add to queue
        position = await call.add_to_queue(chat_id, song)
        
        # Generate thumbnail
        thumb = await generate_thumbnail(song)
        
        # Send queue message
        duration = song.get('duration', 0)
        if isinstance(duration, int):
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"
        else:
            duration_str = str(duration)
        
        caption = (
            f"🎵 **Added to Queue**\n\n"
            f"**Title:** {song.get('title', 'Unknown')}\n"
            f"**Artist:** {song.get('artist', 'Unknown')}\n"
            f"**Duration:** {duration_str}\n"
            f"**Position:** #{position}\n"
            f"**Requested by:** {user_name}"
        )
        
        await status_msg.delete()
        
        if thumb:
            await message.reply_photo(photo=thumb, caption=caption)
        else:
            await message.reply_text(caption)
            
    else:
        # Play directly
        await status_msg.edit_text("🎵 **Loading...** Please wait.")
        
        success = await call.play(chat_id, song)
        
        if not success:
            await status_msg.edit_text("❌ **Failed to play.** Try again.")
            return
        
        await status_msg.delete()
    
    # Increment stats
    await mongo.increment_stat("songs_played")

@bot.on_callback_query(filters.regex(r"^play\|"))
async def play_callback(client, callback_query):
    """Handle play callback"""
    await callback_query.answer("Use /play command to play music!")
