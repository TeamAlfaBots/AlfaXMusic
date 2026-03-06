#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import os
import aiohttp
from io import BytesIO
from pathlib import Path
from typing import Optional, Dict

from PIL import Image, ImageDraw, ImageFont

from AlfaXmusic.utils.logger import LOGGER

logger = LOGGER("Thumbnails")

# Paths
ASSETS_DIR = Path(__file__).parent.parent / "assets"
FONTS = {
    'regular': ASSETS_DIR / "font.ttf",
    'bold': ASSETS_DIR / "font2.ttf"
}

# Default thumbnail
DEFAULT_THUMB = ASSETS_DIR / "default_thumb.jpg"

async def download_image(url: str) -> Optional[bytes]:
    """Download image from URL"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status == 200:
                    return await response.read()
    except Exception as e:
        logger.error(f"Error downloading image: {e}")
    return None

def wrap_text(text: str, font: ImageFont, max_width: int) -> str:
    """Wrap text to fit within max width"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = font.getbbox(test_line)
        if bbox[2] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

async def generate_thumbnail(song: Dict, output_path: Optional[str] = None) -> Optional[str]:
    """Generate thumbnail for a song"""
    try:
        # Create output path
        if not output_path:
            output_path = ASSETS_DIR / f"thumb_{song.get('id', 'unknown')}.jpg"
        
        # Load background image
        thumb_url = song.get('thumbnail')
        bg_image = None
        
        if thumb_url:
            img_data = await download_image(thumb_url)
            if img_data:
                bg_image = Image.open(BytesIO(img_data))
        
        # Use default if no background
        if not bg_image:
            if DEFAULT_THUMB.exists():
                bg_image = Image.open(DEFAULT_THUMB)
            else:
                # Create blank image
                bg_image = Image.new('RGB', (1280, 720), color='#1a1a2e')
        
        # Resize to 1280x720
        bg_image = bg_image.convert('RGB')
        bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
        
        # Create overlay
        overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 150))
        
        # Load fonts
        try:
            title_font = ImageFont.truetype(str(FONTS['bold']), 60)
            artist_font = ImageFont.truetype(str(FONTS['regular']), 40)
            info_font = ImageFont.truetype(str(FONTS['regular']), 30)
        except:
            title_font = ImageFont.load_default()
            artist_font = ImageFont.load_default()
            info_font = ImageFont.load_default()
        
        # Draw text
        draw = ImageDraw.Draw(overlay)
        
        # Title
        title = song.get('title', 'Unknown Title')
        title = title[:60] + '...' if len(title) > 60 else title
        title = wrap_text(title, title_font, 1000)
        
        # Artist
        artist = song.get('artist', 'Unknown Artist')
        artist = artist[:50] + '...' if len(artist) > 50 else artist
        
        # Duration
        duration = song.get('duration', 0)
        if isinstance(duration, int):
            minutes = duration // 60
            seconds = duration % 60
            duration_str = f"{minutes}:{seconds:02d}"
        else:
            duration_str = str(duration)
        
        # Platform
        platform = song.get('platform', 'Unknown').upper()
        
        # Draw text on overlay
        # Title
        draw.text((100, 250), title, font=title_font, fill=(255, 255, 255, 255))
        
        # Artist
        draw.text((100, 400), f"by {artist}", font=artist_font, fill=(200, 200, 200, 255))
        
        # Duration and Platform
        draw.text((100, 500), f"⏱ {duration_str}  |  🎵 {platform}", font=info_font, fill=(180, 180, 180, 255))
        
        # Add branding
        draw.text((100, 600), "🎶 AlfaXMusic", font=info_font, fill=(0, 200, 255, 255))
        
        # Composite images
        bg_image.paste(overlay, (0, 0), overlay)
        
        # Save
        bg_image.save(output_path, quality=95)
        
        return str(output_path)
        
    except Exception as e:
        logger.error(f"Error generating thumbnail: {e}")
        return None

async def generate_banner(text: str, output_path: str) -> Optional[str]:
    """Generate a simple banner with text"""
    try:
        # Create image
        img = Image.new('RGB', (1280, 400), color='#16213e')
        draw = ImageDraw.Draw(img)
        
        # Load font
        try:
            font = ImageFont.truetype(str(FONTS['bold']), 80)
        except:
            font = ImageFont.load_default()
        
        # Draw text centered
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1280 - text_width) // 2
        y = (400 - text_height) // 2
        
        draw.text((x, y), text, font=font, fill=(255, 255, 255))
        
        # Save
        img.save(output_path, quality=95)
        
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating banner: {e}")
        return None
