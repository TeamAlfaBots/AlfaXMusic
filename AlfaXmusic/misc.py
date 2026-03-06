# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import asyncio
from typing import List, Set

from AlfaXmusic.core.mongo import AlfaMongo
from config import Config

# Sudo users set
sudo_users: Set[int] = set()

async def load_sudoers():
    """Load sudo users from database and config"""
    global sudo_users
    
    # Add owner
    sudo_users.add(Config.OWNER_ID)
    
    # Load from database
    mongo = AlfaMongo()
    sudo_data = await mongo.get_sudo_users()
    
    for user_id in sudo_data:
        sudo_users.add(user_id)

async def add_sudo(user_id: int) -> bool:
    """Add a user to sudo list"""
    global sudo_users
    
    if user_id in sudo_users:
        return False
    
    sudo_users.add(user_id)
    mongo = AlfaMongo()
    await mongo.add_sudo_user(user_id)
    return True

async def remove_sudo(user_id: int) -> bool:
    """Remove a user from sudo list"""
    global sudo_users
    
    if user_id == Config.OWNER_ID:
        return False  # Can't remove owner
    
    if user_id not in sudo_users:
        return False
    
    sudo_users.discard(user_id)
    mongo = AlfaMongo()
    await mongo.remove_sudo_user(user_id)
    return True

def is_sudo(user_id: int) -> bool:
    """Check if user is sudo"""
    return user_id in sudo_users

async def restart_bot():
    """Restart the bot"""
    import os
    import sys
    
    os.execl(sys.executable, sys.executable, "-m", "AlfaXmusic")

async def update_bot():
    """Update bot from git repository"""
    import subprocess
    
    try:
        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.returncode == 0, result.stdout
    except Exception as e:
        return False, str(e)
