# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from .youtube import YouTubePlatform
from .spotify import SpotifyPlatform
from .telegram import TelegramPlatform

__all__ = ["YouTubePlatform", "SpotifyPlatform", "TelegramPlatform"]
