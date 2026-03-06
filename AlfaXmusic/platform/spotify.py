#!/usr/bin/env python3
# ===========================================
#  AlfaXMusic - Telegram Music Bot
#  Powered by Alfa Bots
#  (c) 2024 Alfa Bots. All Rights Reserved.
# ===========================================

import re
from typing import Optional, Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import Config
from AlfaXmusic.utils.logger import LOGGER

class SpotifyPlatform:
    """Spotify music platform handler"""
    
    def __init__(self):
        self.logger = LOGGER("Spotify")
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize Spotify client"""
        try:
            client_id = getattr(Config, 'SPOTIFY_CLIENT_ID', None)
            client_secret = getattr(Config, 'SPOTIFY_CLIENT_SECRET', None)
            
            if client_id and client_secret:
                credentials = SpotifyClientCredentials(
                    client_id=client_id,
                    client_secret=client_secret
                )
                self.client = spotipy.Spotify(client_credentials_manager=credentials)
                self.logger.info("Spotify client initialized")
            else:
                self.logger.warning("Spotify credentials not configured")
                
        except Exception as e:
            self.logger.error(f"Failed to initialize Spotify: {e}")
            self.client = None
    
    def is_spotify_url(self, url: str) -> bool:
        """Check if URL is a Spotify link"""
        spotify_pattern = r'https?://open\.spotify\.com/(track|album|playlist|artist)/([a-zA-Z0-9]+)'
        return bool(re.match(spotify_pattern, url))
    
    def extract_spotify_id(self, url: str) -> tuple:
        """Extract Spotify ID and type from URL"""
        match = re.match(r'https?://open\.spotify\.com/(track|album|playlist|artist)/([a-zA-Z0-9]+)', url)
        if match:
            return match.group(1), match.group(2)
        return None, None
    
    async def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Search Spotify for tracks"""
        if not self.client:
            return []
        
        try:
            results = self.client.search(q=query, type='track', limit=limit)
            tracks = []
            
            for track in results.get('tracks', {}).get('items', []):
                artists = [a['name'] for a in track.get('artists', [])]
                
                tracks.append({
                    'title': track.get('name'),
                    'artist': ', '.join(artists),
                    'id': track.get('id'),
                    'url': track.get('external_urls', {}).get('spotify'),
                    'duration': track.get('duration_ms', 0) // 1000,
                    'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url'),
                    'album': track.get('album', {}).get('name'),
                    'platform': 'spotify'
                })
            
            return tracks
            
        except Exception as e:
            self.logger.error(f"Search error: {e}")
            return []
    
    async def get_track(self, track_id: str) -> Optional[Dict]:
        """Get track information"""
        if not self.client:
            return None
        
        try:
            track = self.client.track(track_id)
            artists = [a['name'] for a in track.get('artists', [])]
            
            return {
                'title': track.get('name'),
                'artist': ', '.join(artists),
                'id': track.get('id'),
                'url': track.get('external_urls', {}).get('spotify'),
                'duration': track.get('duration_ms', 0) // 1000,
                'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url'),
                'album': track.get('album', {}).get('name'),
                'platform': 'spotify'
            }
            
        except Exception as e:
            self.logger.error(f"Error getting track: {e}")
            return None
    
    async def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """Get tracks from a playlist"""
        if not self.client:
            return []
        
        try:
            results = self.client.playlist_tracks(playlist_id)
            tracks = []
            
            for item in results.get('items', []):
                track = item.get('track')
                if track:
                    artists = [a['name'] for a in track.get('artists', [])]
                    
                    tracks.append({
                        'title': track.get('name'),
                        'artist': ', '.join(artists),
                        'id': track.get('id'),
                        'url': track.get('external_urls', {}).get('spotify'),
                        'duration': track.get('duration_ms', 0) // 1000,
                        'thumbnail': track.get('album', {}).get('images', [{}])[0].get('url'),
                        'platform': 'spotify'
                    })
            
            return tracks
            
        except Exception as e:
            self.logger.error(f"Error getting playlist: {e}")
            return []
    
    async def get_album_tracks(self, album_id: str) -> List[Dict]:
        """Get tracks from an album"""
        if not self.client:
            return []
        
        try:
            results = self.client.album_tracks(album_id)
            album_info = self.client.album(album_id)
            tracks = []
            
            for track in results.get('items', []):
                artists = [a['name'] for a in track.get('artists', [])]
                
                tracks.append({
                    'title': track.get('name'),
                    'artist': ', '.join(artists),
                    'id': track.get('id'),
                    'url': track.get('external_urls', {}).get('spotify'),
                    'duration': track.get('duration_ms', 0) // 1000,
                    'thumbnail': album_info.get('images', [{}])[0].get('url'),
                    'album': album_info.get('name'),
                    'platform': 'spotify'
                })
            
            return tracks
            
        except Exception as e:
            self.logger.error(f"Error getting album: {e}")
            return []

# Global instance
spotify = SpotifyPlatform()
