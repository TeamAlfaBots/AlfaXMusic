#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from functools import wraps
from typing import Callable

from pyrogram.types import Message, CallbackQuery
from pyrogram.enums import ChatMemberStatus

from config import Config
from AlfaXmusic.misc import is_sudo
from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("Decorators")

def admin_only(func: Callable) -> Callable:
    """Decorator to allow only admins/owner/sudo"""
    @wraps(func)
    async def decorator(client, message: Message, *args, **kwargs):
        if not message.from_user:
            return
        
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # Check if owner or sudo
        if user_id == Config.OWNER_ID or is_sudo(user_id):
            return await func(client, message, *args, **kwargs)
        
        # Check if chat is private
        if message.chat.type == "private":
            return await message.reply("⚠️ This command is only for admins.")
        
        # Check admin status in group
        try:
            member = await message.chat.get_member(user_id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await func(client, message, *args, **kwargs)
            else:
                return await message.reply("⚠️ This command is only for admins.")
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            return await message.reply("⚠️ Could not verify admin status.")
    
    return decorator

def sudo_only(func: Callable) -> Callable:
    """Decorator to allow only owner and sudo users"""
    @wraps(func)
    async def decorator(client, message: Message, *args, **kwargs):
        if not message.from_user:
            return
        
        user_id = message.from_user.id
        
        if user_id == Config.OWNER_ID or is_sudo(user_id):
            return await func(client, message, *args, **kwargs)
        else:
            return await message.reply("⚠️ This command is only for sudo users.")
    
    return decorator

def owner_only(func: Callable) -> Callable:
    """Decorator to allow only owner"""
    @wraps(func)
    async def decorator(client, message: Message, *args, **kwargs):
        if not message.from_user:
            return
        
        user_id = message.from_user.id
        
        if user_id == Config.OWNER_ID:
            return await func(client, message, *args, **kwargs)
        else:
            return await message.reply("⚠️ This command is only for the bot owner.")
    
    return decorator

def authorized_chat(func: Callable) -> Callable:
    """Decorator to check if chat is authorized"""
    @wraps(func)
    async def decorator(client, message: Message, *args, **kwargs):
        if not message.chat:
            return
        
        # Allow private chats
        if message.chat.type == "private":
            return await func(client, message, *args, **kwargs)
        
        # Check if chat is in database (served)
        from AlfaXmusic.core.mongo import AlfaMongo
        mongo = AlfaMongo()
        
        chat = await mongo.get_chat(message.chat.id)
        if not chat:
            # Add chat to database
            await mongo.add_chat(
                message.chat.id,
                message.chat.title,
                message.chat.type
            )
        
        return await func(client, message, *args, **kwargs)
    
    return decorator

def callback_admin_only(func: Callable) -> Callable:
    """Decorator for callback queries - admin only"""
    @wraps(func)
    async def decorator(client, callback_query: CallbackQuery, *args, **kwargs):
        if not callback_query.from_user:
            return
        
        user_id = callback_query.from_user.id
        
        # Check if owner or sudo
        if user_id == Config.OWNER_ID or is_sudo(user_id):
            return await func(client, callback_query, *args, **kwargs)
        
        # Check admin status in chat
        try:
            member = await callback_query.message.chat.get_member(user_id)
            if member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                return await func(client, callback_query, *args, **kwargs)
            else:
                return await callback_query.answer("⚠️ Admin only!", show_alert=True)
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            return await callback_query.answer("⚠️ Could not verify!", show_alert=True)
    
    return decorator
