#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import asyncio
import re
from typing import Optional, Dict, List
from urllib.parse import urlparse, parse_qs

import yt_dlp
from youtubesearchpython import VideosSearch

from AlfaXmusic.utils.logger import LOGGER

class YouTubePlatform:
    """YouTube music platform handler"""
    
    def __init__(self):
        self.logger = LOGGER("YouTube")
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0',
        }
    
    def is_youtube_url(self, url: str) -> bool:
        """Check if URL is a YouTube link"""
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|\.\S+)?([^&=\s]{11})'
        return bool(re.match(youtube_regex, url))
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL"""
        parsed_url = urlparse(url)
        
        if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
            return parsed_url.path[1:]
        
        if parsed_url.hostname in ('youtube.com', 'www.youtube.com', 'm.youtube.com'):
            if parsed_url.path == '/watch':
                return parse_qs(parsed_url.query).get('v', [None])[0]
            if parsed_url.path.startswith('/embed/'):
                return parsed_url.path.split('/')[2]
            if parsed_url.path.startswith('/v/'):
                return parsed_url.path.split('/')[2]
        
        return None
    
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search YouTube for videos"""
        try:
            search = VideosSearch(query, limit=limit)
            results = search.result()
            
            videos = []
            for video in results.get('result', []):
                videos.append({
                    'title': video.get('title'),
                    'id': video.get('id'),
                    'url': video.get('link'),
                    'duration': video.get('duration'),
                    'thumbnail': video.get('thumbnails', [{}])[0].get('url'),
                    'channel': video.get('channel', {}).get('name'),
                    'views': video.get('viewCount', {}).get('text'),
                    'platform': 'youtube'
                })
            
            return videos
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return []
    
    async def get_video_info(self, video_id: str) -> Optional[Dict]:
        """Get video information"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title'),
                    'id': info.get('id'),
                    'url': url,
                    'audio_url': self._get_audio_url(info),
                    'duration': info.get('duration'),
                    'thumbnail': info.get('thumbnail'),
                    'channel': info.get('uploader'),
                    'views': info.get('view_count'),
                    'platform': 'youtube'
                }
                
        except Exception as e:
            self.logger.error(f"Error getting video info: {e}")
            return None
    
    async def get_audio(self, query: str) -> Optional[Dict]:
        """Get audio from query (URL or search)"""
        try:
            # Check if it's a URL
            if self.is_youtube_url(query):
                video_id = self.extract_video_id(query)
                if video_id:
                    return await self.get_video_info(video_id)
            
            # Search for the query
            search_results = await self.search(query, limit=1)
            if not search_results:
                return None
            
            video = search_results[0]
            return await self.get_video_info(video['id'])
            
        except Exception as e:
            self.logger.error(f"Error getting audio: {e}")
            return None
    
    def _get_audio_url(self, info: Dict) -> Optional[str]:
        """Extract audio URL from yt-dlp info"""
        formats = info.get('formats', [])
        
        # Find best audio format
        audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
        
        if audio_formats:
            # Sort by quality
            audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
            return audio_formats[0].get('url')
        
        # Fallback to any format with audio
        for f in formats:
            if f.get('acodec') != 'none':
                return f.get('url')
        
        return None
    
    async def get_playlist_videos(self, playlist_url: str) -> List[Dict]:
        """Get videos from a playlist"""
        try:
            ydl_opts = {
                **self.ydl_opts,
                'extract_flat': True,
                'playlistend': 50,  # Limit to 50 songs
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                
                videos = []
                entries = info.get('entries', [])
                
                for entry in entries:
                    if entry:
                        videos.append({
                            'title': entry.get('title'),
                            'id': entry.get('id'),
                            'url': f"https://www.youtube.com/watch?v={entry.get('id')}",
                            'duration': entry.get('duration'),
                            'thumbnail': f"https://img.youtube.com/vi/{entry.get('id')}/0.jpg",
                            'platform': 'youtube'
                        })
                
                return videos
                
        except Exception as e:
            self.logger.error(f"Error getting playlist: {e}")
            return []

# Global instance
youtube = YouTubePlatform()
