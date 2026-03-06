#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import filters
from pyrogram.types import Message

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.core.call import AlfaCall
from AlfaXmusic.utils.decorators import sudo_only
from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("StatsCmd")
bot = AlfaBot()
mongo = AlfaMongo()
call = AlfaCall()

@bot.on_message(filters.command("stats"))
@sudo_only
async def stats_command(client, message: Message):
    """Handle /stats command - show detailed statistics"""
    
    # Get all stats
    all_stats = await mongo.get_all_stats()
    
    # Get counts
    users_count = await mongo.get_users_count()
    chats_count = await mongo.get_chats_count()
    
    # Build stats text
    stats_text = (
        f"📊 **AlfaXMusic Statistics**\n"
        f"{'=' * 30}\n\n"
        f"👥 **Users:** `{users_count}`\n"
        f"💬 **Groups:** `{chats_count}`\n"
        f"🎵 **Active Calls:** `{len(call.active_chats)}`\n\n"
        f"📈 **Activity Stats:**\n"
    )
    
    for stat_type, count in all_stats.items():
        stats_text += f"  • {stat_type}: `{count}`\n"
    
    stats_text += f"\n📌 **Powered by Alfa Bots**"
    
    await message.reply_text(stats_text)

@bot.on_message(filters.command("activevc"))
@sudo_only
async def activevc_command(client, message: Message):
    """Handle /activevc command - show active voice chats"""
    
    active_chats = call.active_chats
    
    if not active_chats:
        await message.reply_text("📭 **No active voice chats.**")
        return
    
    text = f"🎵 **Active Voice Chats ({len(active_chats)})**\n\n"
    
    for chat_id, data in active_chats.items():
        current = call.get_current_song(chat_id)
        song_title = current.get('title', 'Unknown') if current else 'None'
        is_playing = "▶️" if data.get('is_playing') else "⏸️"
        
        text += f"{is_playing} `{chat_id}` - {song_title[:30]}...\n"
    
    await message.reply_text(text)
