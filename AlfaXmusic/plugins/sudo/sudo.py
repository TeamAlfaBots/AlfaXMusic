#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import filters
from pyrogram.types import Message

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.utils.decorators import owner_only
from AlfaXmusic.utils.logger import LOGGER
from AlfaXmusic.misc import add_sudo, remove_sudo, sudo_users

logger = LOGGER("SudoCmd")
bot = AlfaBot()

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

@bot.on_message(filters.command("sudo"))
@owner_only
async def sudo_command(client, message: Message):
    """Handle /sudo command - add sudo user"""
    
    user_id = await get_target_user(message)
    
    if not user_id:
        await message.reply_text(
            "⚠️ **Usage:**\n"
            "`/sudo` (reply to user)\n"
            "`/sudo @username`\n"
            "`/sudo user_id`"
        )
        return
    
    success = await add_sudo(user_id)
    
    if success:
        try:
            user = await bot.get_users(user_id)
            await message.reply_text(f"✅ **Added to sudo:** {user.mention}")
        except:
            await message.reply_text(f"✅ **Added to sudo:** `{user_id}`")
    else:
        await message.reply_text("⚠️ User is already a sudo user.")

@bot.on_message(filters.command("rmsudo"))
@owner_only
async def rmsudo_command(client, message: Message):
    """Handle /rmsudo command - remove sudo user"""
    
    user_id = await get_target_user(message)
    
    if not user_id:
        await message.reply_text(
            "⚠️ **Usage:**\n"
            "`/rmsudo` (reply to user)\n"
            "`/rmsudo @username`\n"
            "`/rmsudo user_id`"
        )
        return
    
    success = await remove_sudo(user_id)
    
    if success:
        try:
            user = await bot.get_users(user_id)
            await message.reply_text(f"❌ **Removed from sudo:** {user.mention}")
        except:
            await message.reply_text(f"❌ **Removed from sudo:** `{user_id}`")
    else:
        await message.reply_text("⚠️ User is not a sudo user or cannot be removed.")

@bot.on_message(filters.command("sudolist"))
@owner_only
async def sudolist_command(client, message: Message):
    """Handle /sudolist command - list sudo users"""
    
    if not sudo_users:
        await message.reply_text("📭 **No sudo users.**")
        return
    
    text = "👑 **Sudo Users:**\n\n"
    
    for i, user_id in enumerate(sudo_users, 1):
        try:
            user = await bot.get_users(user_id)
            text += f"{i}. {user.mention} (`{user_id}`)\n"
        except:
            text += f"{i}. `{user_id}`\n"
    
    await message.reply_text(text)
