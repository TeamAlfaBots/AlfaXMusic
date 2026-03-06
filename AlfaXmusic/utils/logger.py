#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import logging

def LOGGER(name: str) -> logging.Logger:
    """Get logger instance with given name"""
    return logging.getLogger(name)
