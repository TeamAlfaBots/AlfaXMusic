#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import asyncio
import importlib
import os
import sys
from pathlib import Path

from pyrogram import idle

from AlfaXmusic.core.bot import AlfaBot
from AlfaXmusic.core.call import AlfaCall
from AlfaXmusic.core.mongo import AlfaMongo
from AlfaXmusic.core.userbot import AlfaUserbot
from AlfaXmusic.logging import setup_logging
from AlfaXmusic.misc import sudo_users, load_sudoers
from AlfaXmusic.utils.logger import LOGGER
from config import Config

# Setup logging
setup_logging()
logger = LOGGER("AlfaXMusic")

# Initialize core components
bot = AlfaBot()
call = AlfaCall()
mongo = AlfaMongo()
userbot = AlfaUserbot()

async def load_plugins():
    """Load all plugins from plugins directory"""
    plugins_dir = Path(__file__).parent / "plugins"
    
    plugin_categories = ["admin", "bot", "misc", "play", "sudo", "tools"]
    
    for category in plugin_categories:
        category_path = plugins_dir / category
        if not category_path.exists():
            continue
            
        for file in sorted(category_path.glob("*.py")):
            if file.name.startswith("_"):
                continue
                
            module_name = f"AlfaXmusic.plugins.{category}.{file.stem}"
            try:
                importlib.import_module(module_name)
                logger.info(f"Loaded plugin: {module_name}")
            except Exception as e:
                logger.error(f"Failed to load {module_name}: {e}")

async def load_platforms():
    """Load all platform modules"""
    platforms_dir = Path(__file__).parent / "platform"
    
    for file in sorted(platforms_dir.glob("*.py")):
        if file.name.startswith("_"):
            continue
            
        module_name = f"AlfaXmusic.platform.{file.stem}"
        try:
            importlib.import_module(module_name)
            logger.info(f"Loaded platform: {module_name}")
        except Exception as e:
            logger.error(f"Failed to load {module_name}: {e}")

async def init_bot():
    """Initialize bot and all components"""
    logger.info("Starting AlfaXMusic Bot...")
    
    # Initialize MongoDB
    await mongo.connect()
    logger.info("MongoDB connected successfully")
    
    # Load sudo users
    await load_sudoers()
    
    # Start userbot
    await userbot.start()
    logger.info("Userbot started successfully")
    
    # Start bot
    await bot.start()
    logger.info(f"Bot started as @{bot.username}")
    
    # Initialize PyTgCalls
    await call.start()
    logger.info("PyTgCalls initialized successfully")
    
    # Load platforms
    await load_platforms()
    
    # Load plugins
    await load_plugins()
    
    logger.info("AlfaXMusic Bot started successfully!")

async def main():
    """Main entry point"""
    try:
        await init_bot()
        await idle()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot crashed: {e}")
    finally:
        await shutdown()

async def shutdown():
    """Cleanup and shutdown"""
    logger.info("Shutting down AlfaXMusic Bot...")
    
    try:
        await call.stop()
        logger.info("PyTgCalls stopped")
    except:
        pass
    
    try:
        await userbot.stop()
        logger.info("Userbot stopped")
    except:
        pass
    
    try:
        await bot.stop()
        logger.info("Bot stopped")
    except:
        pass
    
    try:
        await mongo.close()
        logger.info("MongoDB connection closed")
    except:
        pass
    
    logger.info("AlfaXMusic Bot shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
