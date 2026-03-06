#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import asyncio
from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import (
    FloodWait, 
    UserIsBlocked, 
    PeerIdInvalid, 
    InputUserDeactivated,
    ChatWriteForbidden
)

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.utils.decorators import owner_only
from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("Broadcast")
bot = AlfaBot()
mongo = AlfaMongo()

@bot.on_message(filters.command("broadcast") & filters.reply)
@owner_only
async def broadcast_command(client, message: Message):
    """Handle /broadcast command - broadcast replied message"""
    
    # Get the message to broadcast
    broadcast_msg = message.reply_to_message
    
    if not broadcast_msg:
        await message.reply_text(
            "⚠️ **Usage:**\n"
            "Reply to a message with `/broadcast`\n\n"
            "Supports: Text, Photo, Video, Audio, Document"
        )
        return
    
    # Get broadcast targets
    users = await mongo.get_all_users()
    chats = await mongo.get_all_chats()
    
    total_targets = len(users) + len(chats)
    
    if total_targets == 0:
        await message.reply_text("📭 **No users or chats to broadcast to.**")
        return
    
    # Send initial status
    status_msg = await message.reply_text(
        f"📢 **Broadcast Started**\n\n"
        f"👥 Users: `{len(users)}`\n"
        f"💬 Groups: `{len(chats)}`\n"
        f"📊 Total: `{total_targets}`\n\n"
        f"⏳ Broadcasting..."
    )
    
    # Broadcast stats
    success_count = 0
    failed_count = 0
    blocked_count = 0
    deleted_count = 0
    
    start_time = datetime.utcnow()
    
    # Broadcast to users
    for user in users:
        user_id = user.get('user_id')
        
        if not user_id:
            continue
        
        try:
            if broadcast_msg.text:
                await bot.send_message(user_id, broadcast_msg.text)
            elif broadcast_msg.photo:
                await bot.send_photo(
                    user_id, 
                    broadcast_msg.photo.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.video:
                await bot.send_video(
                    user_id,
                    broadcast_msg.video.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.audio:
                await bot.send_audio(
                    user_id,
                    broadcast_msg.audio.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.document:
                await bot.send_document(
                    user_id,
                    broadcast_msg.document.file_id,
                    caption=broadcast_msg.caption
                )
            else:
                await broadcast_msg.copy(user_id)
            
            success_count += 1
            
        except FloodWait as e:
            await asyncio.sleep(e.value)
            success_count += 1
            
        except UserIsBlocked:
            blocked_count += 1
            failed_count += 1
            
        except (PeerIdInvalid, InputUserDeactivated):
            deleted_count += 1
            failed_count += 1
            
        except Exception as e:
            logger.error(f"Broadcast failed for user {user_id}: {e}")
            failed_count += 1
        
        # Small delay to avoid flood
        await asyncio.sleep(0.1)
        
        # Update status every 50 users
        if (success_count + failed_count) % 50 == 0:
            try:
                await status_msg.edit_text(
                    f"📢 **Broadcast in Progress**\n\n"
                    f"✅ Success: `{success_count}`\n"
                    f"❌ Failed: `{failed_count}`\n"
                    f"🚫 Blocked: `{blocked_count}`\n"
                    f"🗑️ Deleted: `{deleted_count}`\n\n"
                    f"⏳ Broadcasting to groups..."
                )
            except:
                pass
    
    # Broadcast to chats
    for chat in chats:
        chat_id = chat.get('chat_id')
        
        if not chat_id:
            continue
        
        try:
            if broadcast_msg.text:
                await bot.send_message(chat_id, broadcast_msg.text)
            elif broadcast_msg.photo:
                await bot.send_photo(
                    chat_id,
                    broadcast_msg.photo.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.video:
                await bot.send_video(
                    chat_id,
                    broadcast_msg.video.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.audio:
                await bot.send_audio(
                    chat_id,
                    broadcast_msg.audio.file_id,
                    caption=broadcast_msg.caption
                )
            elif broadcast_msg.document:
                await bot.send_document(
                    chat_id,
                    broadcast_msg.document.file_id,
                    caption=broadcast_msg.caption
                )
            else:
                await broadcast_msg.copy(chat_id)
            
            success_count += 1
            
        except FloodWait as e:
            await asyncio.sleep(e.value)
            success_count += 1
            
        except ChatWriteForbidden:
            failed_count += 1
            
        except Exception as e:
            logger.error(f"Broadcast failed for chat {chat_id}: {e}")
            failed_count += 1
        
        # Small delay
        await asyncio.sleep(0.1)
    
    # Calculate duration
    end_time = datetime.utcnow()
    duration = (end_time - start_time).total_seconds()
    
    # Log broadcast
    await mongo.log_broadcast(total_targets, success_count, failed_count)
    
    # Final status
    await status_msg.edit_text(
        f"✅ **Broadcast Complete**\n\n"
        f"📊 **Statistics:**\n"
        f"├ Total Targets: `{total_targets}`\n"
        f"├ ✅ Success: `{success_count}`\n"
        f"├ ❌ Failed: `{failed_count}`\n"
        f"├ 🚫 Blocked: `{blocked_count}`\n"
        f"├ 🗑️ Deleted: `{deleted_count}`\n"
        f"└ ⏱️ Duration: `{duration:.2f}s`\n\n"
        f"📌 **Powered by Alfa Bots**"
    )
    
    logger.info(f"Broadcast completed: {success_count}/{total_targets} successful")

@bot.on_message(filters.command("broadcast") & ~filters.reply)
@owner_only
async def broadcast_help(client, message: Message):
    """Handle /broadcast without reply"""
    await message.reply_text(
        "⚠️ **Usage:**\n"
        "Reply to a message with `/broadcast`\n\n"
        "**Supported message types:**\n"
        "• Text\n"
        "• Photo\n"
        "• Video\n"
        "• Audio\n"
        "• Document\n\n"
        "The message will be broadcasted to:\n"
        "• All users who started the bot\n"
        "• All groups where bot is added"
    )
