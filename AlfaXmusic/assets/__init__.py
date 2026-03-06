# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

from pathlib import Path

ASSETS_DIR = Path(__file__).parent

# Font paths
FONT_PATH = ASSETS_DIR / "font.ttf"
FONT2_PATH = ASSETS_DIR / "font2.ttf"

# Default thumbnail
DEFAULT_THUMB = ASSETS_DIR / "default_thumb.jpg"

# Silence audio for joining calls
SILENCE_AUDIO = ASSETS_DIR / "silence.mp3"
