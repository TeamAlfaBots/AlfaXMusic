#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.utils.decorators import admin_only
from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("AuthCmd")
bot = AlfaBot()

# In-memory authorized users per chat (chat_id: set of user_ids)
authorized_users = {}

def is_authorized(chat_id: int, user_id: int) -> bool:
    """Check if user is authorized in chat"""
    if chat_id not in authorized_users:
        return False
    return user_id in authorized_users[chat_id]

async def get_target_user(message: Message) -> int:
    """Extract target user ID from message"""
    # Check reply
    if message.reply_to_message and message.reply_to_message.from_user:
        return message.reply_to_message.from_user.id
    
    # Check command argument
    if len(message.command) > 1:
        arg = message.command[1]
        
        # Username
        if arg.startswith("@"):
            try:
                user = await bot.get_users(arg)
                return user.id
            except:
                return None
        
        # User ID
        if arg.isdigit():
            return int(arg)
    
    return None

@bot.on_message(filters.command("auth"))
@admin_only
async def auth_command(client, message: Message):
    """Handle /auth command - authorize user"""
    chat_id = message.chat.id
    
    # Get target user
    user_id = await get_target_user(message)
    
    if not user_id:
        await message.reply_text(
            "⚠️ **Usage:**\n"
            "`/auth` (reply to user)\n"
            "`/auth @username`\n"
            "`/auth user_id`"
        )
        return
    
    # Initialize chat auth set
    if chat_id not in authorized_users:
        authorized_users[chat_id] = set()
    
    # Check if already authorized
    if user_id in authorized_users[chat_id]:
        await message.reply_text("✅ User is already authorized.")
        return
    
    # Add to authorized
    authorized_users[chat_id].add(user_id)
    
    try:
        user = await bot.get_users(user_id)
        await message.reply_text(f"✅ **Authorized:** {user.mention}")
    except:
        await message.reply_text(f"✅ **Authorized:** `{user_id}`")

@bot.on_message(filters.command("unauth"))
@admin_only
async def unauth_command(client, message: Message):
    """Handle /unauth command - unauthorize user"""
    chat_id = message.chat.id
    
    # Get target user
    user_id = await get_target_user(message)
    
    if not user_id:
        await message.reply_text(
            "⚠️ **Usage:**\n"
            "`/unauth` (reply to user)\n"
            "`/unauth @username`\n"
            "`/unauth user_id`"
        )
        return
    
    # Check if chat has authorized users
    if chat_id not in authorized_users or user_id not in authorized_users[chat_id]:
        await message.reply_text("❌ User is not authorized.")
        return
    
    # Remove from authorized
    authorized_users[chat_id].discard(user_id)
    
    try:
        user = await bot.get_users(user_id)
        await message.reply_text(f"❌ **Unauthorized:** {user.mention}")
    except:
        await message.reply_text(f"❌ **Unauthorized:** `{user_id}`")

@bot.on_message(filters.command("authusers"))
async def authusers_command(client, message: Message):
    """Handle /authusers command - list authorized users"""
    chat_id = message.chat.id
    
    if chat_id not in authorized_users or not authorized_users[chat_id]:
        await message.reply_text("📭 **No authorized users in this chat.**")
        return
    
    text = "👥 **Authorized Users:**\n\n"
    
    for i, user_id in enumerate(authorized_users[chat_id], 1):
        try:
            user = await bot.get_users(user_id)
            text += f"{i}. {user.mention} (`{user_id}`)\n"
        except:
            text += f"{i}. `{user_id}`\n"
    
    await message.reply_text(text)
