# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

__version__ = "1.0.0"
__author__ = "Alfa Bots"
__license__ = "MIT"
__title__ = "AlfaXMusic"

from .core.bot import AlfaBot
from .core.call import AlfaCall
from .core.mongo import AlfaMongo
from .core.userbot import AlfaUserbot

__all__ = ["AlfaBot", "AlfaCall", "AlfaMongo", "AlfaUserbot"]
