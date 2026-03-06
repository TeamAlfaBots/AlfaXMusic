#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("HelpCmd")
bot = AlfaBot()

HELP_TEXT = """
🎵 **AlfaXMusic - Help Menu** 🎵

**📌 Basic Commands:**
/start - Start the bot
/help - Show this help menu
/ping - Check bot latency

**🎶 Music Commands:**
/play <song name/url> - Play music
/song <song name> - Download song

**📋 Queue Commands:**
/queue - Show current queue
/skip - Skip current song
/stop - Stop playback
/pause - Pause playback
/resume - Resume playback

**🔁 Playback Controls:**
/loop - Toggle loop mode
/shuffle - Toggle shuffle mode
/volume <1-200> - Set volume

**👤 Admin Commands:**
/auth - Authorize user
/unauth - Unauthorize user
/authusers - List authorized users

**⚙️ Settings:**
/language - Change language
/settings - Bot settings

**👑 Owner Commands:**
/broadcast - Broadcast message
/stats - Show bot statistics
/sudo - Manage sudo users

**📌 Powered by Alfa Bots**
"""

ADMIN_HELP = """
**👑 Admin Commands:**

/auth <user> - Authorize user to use bot
/unauth <user> - Unauthorize user
/authusers - List all authorized users

/mute - Mute the voice chat
/unmute - Unmute the voice chat

**📌 Powered by Alfa Bots**
"""

OWNER_HELP = """
**🔰 Owner Commands:**

/broadcast - Reply to any message to broadcast
/sudo <user> - Add user to sudo
/rmsudo <user> - Remove user from sudo
/sudolist - List all sudo users

/stats - Show bot statistics
/logs - Get bot logs
/maintenance - Toggle maintenance mode

/restart - Restart the bot
/update - Update from git

**📌 Powered by Alfa Bots**
"""

def get_help_buttons() -> InlineKeyboardMarkup:
    """Generate help menu buttons"""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🎵 Basic", callback_data="help_basic"),
            InlineKeyboardButton("🎶 Music", callback_data="help_music"),
        ],
        [
            InlineKeyboardButton("📋 Queue", callback_data="help_queue"),
            InlineKeyboardButton("👤 Admin", callback_data="help_admin"),
        ],
        [
            InlineKeyboardButton("👑 Owner", callback_data="help_owner"),
            InlineKeyboardButton("🔙 Back", callback_data="start"),
        ]
    ])

@bot.on_message(filters.command("help"))
async def help_command(client, message: Message):
    """Handle /help command"""
    await message.reply_text(
        HELP_TEXT,
        reply_markup=get_help_buttons()
    )

@bot.on_callback_query(filters.regex("^help$"))
async def help_callback(client, callback_query: CallbackQuery):
    """Handle help callback"""
    await callback_query.message.edit_text(
        HELP_TEXT,
        reply_markup=get_help_buttons()
    )

@bot.on_callback_query(filters.regex("^help_basic$"))
async def help_basic_callback(client, callback_query: CallbackQuery):
    """Handle basic help callback"""
    text = """
**📌 Basic Commands:**

/start - Start the bot and get welcome message
/help - Show this help menu with all commands
/ping - Check bot latency and response time

**Usage:**
• Use /start in private to see bot info
• Use /start in group to initialize bot
• Use /ping to check if bot is online

**📌 Powered by Alfa Bots**
"""
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
    )

@bot.on_callback_query(filters.regex("^help_music$"))
async def help_music_callback(client, callback_query: CallbackQuery):
    """Handle music help callback"""
    text = """
**🎶 Music Commands:**

/play <song name> - Play a song from YouTube
/play <YouTube URL> - Play from direct URL
/play <Spotify URL> - Play from Spotify

**Playlist Commands:**
/play 90sHits - Play 90s hits playlist
/play Arijit Singh Sad - Play sad songs
/play Arijit Singh Love - Play love songs
/play Punjabi Hits - Play Punjabi hits
/play Bhojpuri Hits - Play Bhojpuri hits
/play Sad - Play sad songs
/play Romantic - Play romantic songs
/play Dance - Play dance songs

/song <name> - Download song as audio file

**📌 Powered by Alfa Bots**
"""
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
    )

@bot.on_callback_query(filters.regex("^help_queue$"))
async def help_queue_callback(client, callback_query: CallbackQuery):
    """Handle queue help callback"""
    text = """
**📋 Queue Commands:**

/queue - Show current queue list
/skip - Skip to next song in queue
/stop - Stop playback and clear queue
/pause - Pause current playback
/resume - Resume paused playback

**🔁 Playback Controls:**
/loop - Toggle loop mode (repeat current)
/shuffle - Toggle shuffle mode (random order)
/volume <1-200> - Adjust volume level

**📌 Powered by Alfa Bots**
"""
    await callback_query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
    )

@bot.on_callback_query(filters.regex("^help_admin$"))
async def help_admin_callback(client, callback_query: CallbackQuery):
    """Handle admin help callback"""
    await callback_query.message.edit_text(
        ADMIN_HELP,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
    )

@bot.on_callback_query(filters.regex("^help_owner$"))
async def help_owner_callback(client, callback_query: CallbackQuery):
    """Handle owner help callback"""
    await callback_query.message.edit_text(
        OWNER_HELP,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="help")]
        ])
    )
