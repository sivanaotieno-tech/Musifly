"""
Spotify Authentication Manager
Handles OAuth2 authentication flow using Spotipy
"""
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta


class SpotifyAuthManager:
    """Manages Spotify OAuth authentication"""
    
    def __init__(self):
        """Initialize Spotify OAuth manager"""
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:5000/api/auth/callback')
        self.scope = self._parse_scopes()
        
        if not self.client_id or not self.client_secret:
            raise ValueError(
                "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET. "
                "Please set these environment variables."
            )
        
        self.oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            cache_handler=None  # Don't cache - we'll handle tokens in session
        )
    
    def _parse_scopes(self):
        """
        Parse scopes from environment variable or use defaults
        """
        default_scopes = [
            'user-read-private',
            'user-read-email',
            'user-library-read',
            'user-library-modify',
            'user-top-read',
            'user-read-currently-playing',
            'user-read-playback-state',
            'user-modify-playback-state',
            'playlist-read-private',
            'playlist-read-collaborative',
            'playlist-modify-public',
            'playlist-modify-private',
        ]
        
        env_scopes = os.getenv('SPOTIFY_SCOPES')
        if env_scopes:
            return env_scopes.split(',')
        
        return ' '.join(default_scopes)
    
    def get_auth_url(self):
        """
        Get Spotify authorization URL
        User should be redirected to this URL to authorize the app
        
        Returns:
            str: Authorization URL
        """
        return self.oauth.get_authorize_url()
    
    def get_token(self, code, state=None):
        """
        Exchange authorization code for access token
        
        Args:
            code (str): Authorization code from Spotify callback
            state (str): State parameter for CSRF protection
        
        Returns:
            dict: Token info containing access_token, refresh_token, expires_at, etc.
        """
        try:
            token_info = self.oauth.get_access_token(code)
            return token_info
        except Exception as e:
            raise Exception(f"Failed to get access token: {str(e)}")
    
    def refresh_token_if_needed(self, token_info):
        """
        Check if token is expired and refresh if necessary
        
        Args:
            token_info (dict): Current token info
        
        Returns:
            dict: Refreshed token info if needed, otherwise original token_info
        """
        try:
            if not token_info:
                return None
            
            # Check if token is expired or about to expire (within 5 minutes)
            expires_at = token_info.get('expires_at', 0)
            if expires_at - datetime.now().timestamp() < 300:
                # Token is expired or expiring soon, refresh it
                refresh_token = token_info.get('refresh_token')
                if refresh_token:
                    token_info = self.oauth.refresh_access_token(refresh_token)
            
            return token_info
        except Exception as e:
            raise Exception(f"Failed to refresh token: {str(e)}")
    
    def get_spotify_client(self, token_info):
        """
        Get an authenticated Spotify client
        
        Args:
            token_info (dict): Token info containing access_token
        
        Returns:
            spotipy.Spotify: Authenticated Spotify client
        """
        access_token = token_info.get('access_token')
        if not access_token:
            raise ValueError("No access token in token_info")
        
        return spotipy.Spotify(auth=access_token)
    
    def validate_token(self, token_info):
        """
        Validate token is still valid
        
        Args:
            token_info (dict): Token info to validate
        
        Returns:
            bool: True if token is valid, False otherwise
        """
        if not token_info:
            return False
        
        expires_at = token_info.get('expires_at', 0)
        return expires_at > datetime.now().timestamp()
