#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.call import AlfaCall
from AlfaXmusic.utils.decorators import admin_only
from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("QueueCmd")
bot = AlfaBot()
call = AlfaCall()

@bot.on_message(filters.command("queue"))
async def queue_command(client, message: Message):
    """Handle /queue command"""
    chat_id = message.chat.id
    
    # Get current song
    current = call.get_current_song(chat_id)
    queue = await call.get_queue(chat_id)
    
    if not current and not queue:
        await message.reply_text("📭 **Queue is empty.**\nUse /play to add songs.")
        return
    
    # Build queue text
    text = "📋 **Music Queue**\n\n"
    
    # Current song
    if current:
        duration = current.get('duration', 0)
        if isinstance(duration, int):
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"
        else:
            duration_str = str(duration)
        
        text += (
            f"🎵 **Now Playing:**\n"
            f"├ **Title:** {current.get('title', 'Unknown')}\n"
            f"├ **Artist:** {current.get('artist', 'Unknown')}\n"
            f"├ **Duration:** {duration_str}\n"
            f"└ **Requested by:** {current.get('requested_by', 'Unknown')}\n\n"
        )
    
    # Queue
    if queue:
        text += f"📑 **Up Next ({len(queue)} songs):**\n\n"
        
        for i, song in enumerate(queue[:10], 1):  # Show first 10
            title = song.get('title', 'Unknown')[:30]
            if len(song.get('title', '')) > 30:
                title += "..."
            
            duration = song.get('duration', 0)
            if isinstance(duration, int):
                minutes = duration // 60
                seconds = duration % 60
                duration_str = f"{minutes}:{seconds:02d}"
            else:
                duration_str = str(duration)
            
            text += f"{i}. **{title}** ({duration_str})\n"
        
        if len(queue) > 10:
            text += f"\n... and {len(queue) - 10} more songs"
    else:
        text += "📭 **No songs in queue.**"
    
    # Create buttons
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏭️ Skip", callback_data=f"skip|{chat_id}"),
            InlineKeyboardButton("🗑️ Clear", callback_data=f"clearqueue|{chat_id}"),
        ],
        [
            InlineKeyboardButton("🔀 Shuffle", callback_data=f"shuffle|{chat_id}"),
            InlineKeyboardButton("🔁 Loop", callback_data=f"loop|{chat_id}"),
        ]
    ])
    
    await message.reply_text(text, reply_markup=buttons)

@bot.on_message(filters.command("skip"))
@admin_only
async def skip_command(client, message: Message):
    """Handle /skip command"""
    chat_id = message.chat.id
    
    if not call.is_playing(chat_id):
        await message.reply_text("❌ **Nothing is playing.**")
        return
    
    await message.reply_text("⏭️ **Skipping...**")
    await call.skip(chat_id)

@bot.on_message(filters.command("stop"))
@admin_only
async def stop_command(client, message: Message):
    """Handle /stop command"""
    chat_id = message.chat.id
    
    if not call.is_playing(chat_id):
        await message.reply_text("❌ **Nothing is playing.**")
        return
    
    await call.leave_call(chat_id)
    await message.reply_text("⏹️ **Playback stopped.**")

@bot.on_message(filters.command("pause"))
@admin_only
async def pause_command(client, message: Message):
    """Handle /pause command"""
    chat_id = message.chat.id
    
    if not call.is_playing(chat_id):
        await message.reply_text("❌ **Nothing is playing.**")
        return
    
    success = await call.pause(chat_id)
    if success:
        await message.reply_text("⏸️ **Paused.**")
    else:
        await message.reply_text("❌ **Failed to pause.**")

@bot.on_message(filters.command("resume"))
@admin_only
async def resume_command(client, message: Message):
    """Handle /resume command"""
    chat_id = message.chat.id
    
    success = await call.resume(chat_id)
    if success:
        await message.reply_text("▶️ **Resumed.**")
    else:
        await message.reply_text("❌ **Failed to resume.**")

@bot.on_message(filters.command("loop"))
@admin_only
async def loop_command(client, message: Message):
    """Handle /loop command"""
    chat_id = message.chat.id
    
    status = call.toggle_loop(chat_id)
    
    if status:
        await message.reply_text("🔁 **Loop enabled.**")
    else:
        await message.reply_text("🔁 **Loop disabled.**")

@bot.on_message(filters.command("shuffle"))
@admin_only
async def shuffle_command(client, message: Message):
    """Handle /shuffle command"""
    chat_id = message.chat.id
    
    status = call.toggle_shuffle(chat_id)
    
    if status:
        await message.reply_text("🔀 **Shuffle enabled.**")
    else:
        await message.reply_text("🔀 **Shuffle disabled.**")

@bot.on_callback_query(filters.regex(r"^skip\|"))
async def skip_callback(client, callback_query: CallbackQuery):
    """Handle skip callback"""
    chat_id = int(callback_query.data.split("|")[1])
    
    if not call.is_playing(chat_id):
        await callback_query.answer("Nothing is playing!", show_alert=True)
        return
    
    await callback_query.answer("Skipping...")
    await call.skip(chat_id)
    await callback_query.message.edit_text("⏭️ **Skipped.**")

@bot.on_callback_query(filters.regex(r"^pause\|"))
async def pause_callback(client, callback_query: CallbackQuery):
    """Handle pause callback"""
    chat_id = int(callback_query.data.split("|")[1])
    
    success = await call.pause(chat_id)
    if success:
        await callback_query.answer("Paused!")
        await callback_query.message.edit_text("⏸️ **Paused.**")
    else:
        await callback_query.answer("Failed to pause!", show_alert=True)

@bot.on_callback_query(filters.regex(r"^resume\|"))
async def resume_callback(client, callback_query: CallbackQuery):
    """Handle resume callback"""
    chat_id = int(callback_query.data.split("|")[1])
    
    success = await call.resume(chat_id)
    if success:
        await callback_query.answer("Resumed!")
        await callback_query.message.edit_text("▶️ **Resumed.**")
    else:
        await callback_query.answer("Failed to resume!", show_alert=True)

@bot.on_callback_query(filters.regex(r"^loop\|"))
async def loop_callback(client, callback_query: CallbackQuery):
    """Handle loop callback"""
    chat_id = int(callback_query.data.split("|")[1])
    
    status = call.toggle_loop(chat_id)
    
    if status:
        await callback_query.answer("Loop enabled!")
        await callback_query.message.edit_text("🔁 **Loop enabled.**")
    else:
        await callback_query.answer("Loop disabled!")
        await callback_query.message.edit_text("🔁 **Loop disabled.**")

@bot.on_callback_query(filters.regex(r"^clearqueue\|"))
async def clearqueue_callback(client, callback_query: CallbackQuery):
    """Handle clear queue callback"""
    chat_id = int(callback_query.data.split("|")[1])
    
    await call.clear_queue(chat_id)
    await callback_query.answer("Queue cleared!")
    await callback_query.message.edit_text("🗑️ **Queue cleared.**")

@bot.on_callback_query(filters.regex(r"^stop\|"))
async def stop_callback(client, callback_query: CallbackQuery):
    """Handle stop callback"""
    chat_id = int(callback_query.data.split("|")[1])
    
    await call.leave_call(chat_id)
    await callback_query.answer("Stopped!")
    await callback_query.message.edit_text("⏹️ **Playback stopped.**")
