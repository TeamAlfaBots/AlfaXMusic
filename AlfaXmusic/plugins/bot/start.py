#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.utils.decorators import authorized_chat
from AlfaXmusic.utils.logger import LOGGER
from AlfaXmusic.misc import sudo_users
from config import Config

logger = LOGGER("StartCmd")

# Initialize bot instance
bot = AlfaBot()
mongo = AlfaMongo()

def get_start_buttons() -> InlineKeyboardMarkup:
    """Generate start message buttons"""
    buttons = []
    
    row1 = []
    if hasattr(Config, 'SUPPORT_URL') and Config.SUPPORT_URL:
        row1.append(InlineKeyboardButton("🆘 Support", url=Config.SUPPORT_URL))
    if hasattr(Config, 'UPDATES_URL') and Config.UPDATES_URL:
        row1.append(InlineKeyboardButton("📢 Updates", url=Config.UPDATES_URL))
    if row1:
        buttons.append(row1)
    
    row2 = []
    if hasattr(Config, 'REPO_URL') and Config.REPO_URL:
        row2.append(InlineKeyboardButton("📂 Repo", url=Config.REPO_URL))
    if hasattr(Config, 'DEV_URL') and Config.DEV_URL:
        row2.append(InlineKeyboardButton("👨‍💻 Developer", url=Config.DEV_URL))
    if row2:
        buttons.append(row2)
    
    row3 = []
    if hasattr(Config, 'PRIVACY_URL') and Config.PRIVACY_URL:
        row3.append(InlineKeyboardButton("🔒 Privacy Policy", url=Config.PRIVACY_URL))
    if hasattr(Config, 'QUESTIONS_URL') and Config.QUESTIONS_URL:
        row3.append(InlineKeyboardButton("❓ Any Question", url=Config.QUESTIONS_URL))
    if row3:
        buttons.append(row3)
    
    row4 = []
    if hasattr(Config, 'ADD_GROUP_URL') and Config.ADD_GROUP_URL:
        row4.append(InlineKeyboardButton("➕ Add to Group", url=Config.ADD_GROUP_URL))
    row4.append(InlineKeyboardButton("❓ Help & Commands", callback_data="help"))
    if row4:
        buttons.append(row4)
    
    return InlineKeyboardMarkup(buttons)

@bot.on_message(filters.command("start") & filters.private)
@authorized_chat
async def start_command(client, message: Message):
    """Handle /start command"""
    
    # Add user to database
    await mongo.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
    
    # Get bot info
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    
    # Welcome text
    welcome_text = (
        f"👋 **Hey {message.from_user.mention},**\n\n"
        f"🎵 **I am {bot_name},**\n"
        f"Your smart Telegram streaming player!\n\n"
        f"✨ **Features:**\n"
        f"• Stream music from YouTube & Spotify\n"
        f"• Queue management & playlist support\n"
        f"• Admin controls & loop/shuffle\n"
        f"• High-quality audio streaming\n\n"
        f"🚀 **Get Started:**\n"
        f"Add me to your group and use /play\n\n"
        f"📌 **Powered by Alfa Bots**"
    )
    
    # Send with image if available
    start_img = getattr(Config, 'START_IMG_URL', None)
    
    try:
        if start_img:
            await message.reply_photo(
                photo=start_img,
                caption=welcome_text,
                reply_markup=get_start_buttons()
            )
        else:
            await message.reply_text(
                welcome_text,
                reply_markup=get_start_buttons()
            )
    except Exception as e:
        logger.error(f"Error sending start message: {e}")
        await message.reply_text(
            welcome_text,
            reply_markup=get_start_buttons()
        )

@bot.on_message(filters.command("start") & filters.group)
@authorized_chat
async def start_group_command(client, message: Message):
    """Handle /start command in groups"""
    
    # Add chat to database
    await mongo.add_chat(
        chat_id=message.chat.id,
        title=message.chat.title,
        chat_type=message.chat.type
    )
    
    await message.reply_text(
        f"👋 **Hello {message.chat.title}!**\n\n"
        f"🎵 I'm ready to play music!\n"
        f"Use /play to start streaming.\n\n"
        f"📌 **Powered by Alfa Bots**"
    )

@bot.on_callback_query(filters.regex("^start$"))
async def start_callback(client, callback_query: CallbackQuery):
    """Handle start callback"""
    
    bot_info = await client.get_me()
    bot_name = bot_info.first_name
    
    welcome_text = (
        f"👋 **Hey {callback_query.from_user.mention},**\n\n"
        f"🎵 **I am {bot_name},**\n"
        f"Your smart Telegram streaming player!\n\n"
        f"✨ **Features:**\n"
        f"• Stream music from YouTube & Spotify\n"
        f"• Queue management & playlist support\n"
        f"• Admin controls & loop/shuffle\n"
        f"• High-quality audio streaming\n\n"
        f"🚀 **Get Started:**\n"
        f"Add me to your group and use /play\n\n"
        f"📌 **Powered by Alfa Bots**"
    )
    
    await callback_query.message.edit_text(
        welcome_text,
        reply_markup=get_start_buttons()
    )
