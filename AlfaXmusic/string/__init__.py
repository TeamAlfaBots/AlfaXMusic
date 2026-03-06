# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import yaml
from pathlib import Path
from typing import Dict, Optional

from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("Language")

# Default language
DEFAULT_LANG = "en"

# Cache for loaded languages
_lang_cache: Dict[str, Dict] = {}

def get_lang_file_path(lang_code: str) -> Path:
    """Get path to language file"""
    return Path(__file__).parent / "langs" / f"{lang_code.capitalize()}.yml"

def load_language(lang_code: str) -> Dict:
    """Load language file"""
    global _lang_cache
    
    lang_code = lang_code.lower()
    
    # Return from cache if available
    if lang_code in _lang_cache:
        return _lang_cache[lang_code]
    
    # Try to load language file
    lang_path = get_lang_file_path(lang_code)
    
    if not lang_path.exists():
        logger.warning(f"Language file not found: {lang_path}, falling back to English")
        lang_path = get_lang_file_path(DEFAULT_LANG)
    
    try:
        with open(lang_path, 'r', encoding='utf-8') as f:
            lang_data = yaml.safe_load(f)
            _lang_cache[lang_code] = lang_data
            return lang_data
    except Exception as e:
        logger.error(f"Error loading language file: {e}")
        return {}

def get_string(key: str, lang_code: str = DEFAULT_LANG) -> str:
    """Get a string by key from language file"""
    lang_data = load_language(lang_code)
    
    # Try to get the string
    value = lang_data.get(key)
    
    if value is None:
        # Fall back to English
        if lang_code != DEFAULT_LANG:
            lang_data = load_language(DEFAULT_LANG)
            value = lang_data.get(key)
        
        # If still not found, return the key
        if value is None:
            return key
    
    return value

def get_string_formatted(key: str, lang_code: str = DEFAULT_LANG, **kwargs) -> str:
    """Get a formatted string by key from language file"""
    text = get_string(key, lang_code)
    
    try:
        return text.format(**kwargs)
    except Exception as e:
        logger.error(f"Error formatting string: {e}")
        return text

class Language:
    """Language helper class"""
    
    def __init__(self, lang_code: str = DEFAULT_LANG):
        self.lang_code = lang_code.lower()
        self.data = load_language(lang_code)
    
    def get(self, key: str, default: str = None) -> str:
        """Get string by key"""
        return self.data.get(key, default or key)
    
    def format(self, key: str, **kwargs) -> str:
        """Get formatted string by key"""
        text = self.get(key)
        try:
            return text.format(**kwargs)
        except:
            return text

# Convenience function
def lang(lang_code: str = DEFAULT_LANG) -> Language:
    """Get Language instance"""
    return Language(lang_code)
