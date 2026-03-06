#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import time
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.core.call import AlfaCall
from AlfaXmusic.utils.logger import LOGGER
from config import Config

logger = LOGGER("PingCmd")
bot = AlfaBot()
mongo = AlfaMongo()
call = AlfaCall()

@bot.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    """Handle /ping command"""
    
    start_time = time.time()
    
    # Send initial message
    ping_msg = await message.reply_text("🏓 **Pong!**")
    
    # Calculate response time
    end_time = time.time()
    response_time = round((end_time - start_time) * 1000, 2)
    
    # Get system info
    uptime = datetime.utcnow() - datetime.utcnow()  # Placeholder
    
    # Get stats
    users_count = await mongo.get_users_count()
    chats_count = await mongo.get_chats_count()
    
    # Build response
    ping_text = (
        f"🏓 **Pong!**\n\n"
        f"⚡ **Response Time:** `{response_time} ms`\n"
        f"👥 **Users:** `{users_count}`\n"
        f"💬 **Chats:** `{chats_count}`\n"
        f"🎵 **Active Calls:** `{len(call.active_chats)}`\n\n"
        f"📌 **Powered by Alfa Bots**"
    )
    
    # Send with image if available
    ping_img = getattr(Config, 'PING_IMG_URL', None)
    
    try:
        if ping_img:
            await ping_msg.delete()
            await message.reply_photo(
                photo=ping_img,
                caption=ping_text
            )
        else:
            await ping_msg.edit_text(ping_text)
    except Exception as e:
        logger.error(f"Error sending ping: {e}")
        await ping_msg.edit_text(ping_text)

@bot.on_message(filters.command("status"))
async def status_command(client, message: Message):
    """Handle /status command"""
    
    # Get all stats
    stats = await mongo.get_all_stats()
    
    status_text = (
        f"📊 **Bot Status**\n\n"
        f"🎵 **Songs Played:** `{stats.get('songs_played', 0)}`\n"
        f"📂 **Playlists Played:** `{stats.get('playlists_played', 0)}`\n"
        f"👥 **Total Users:** `{await mongo.get_users_count()}`\n"
        f"💬 **Total Chats:** `{await mongo.get_chats_count()}`\n"
        f"🎵 **Active Calls:** `{len(call.active_chats)}`\n\n"
        f"📌 **Powered by Alfa Bots**"
    )
    
    await message.reply_text(status_text)
