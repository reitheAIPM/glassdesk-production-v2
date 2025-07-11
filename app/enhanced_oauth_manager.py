"""
Enhanced OAuth Manager for GlassDesk using Authlib
Provides secure OAuth 2.0 flows with PKCE support for desktop applications
"""

import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime, timedelta
from authlib.integrations.starlette_client import OAuth
from authlib.integrations.base_client import OAuthError
from starlette.config import Config
from .services.oauth_manager import OAuthTokenManager

logger = logging.getLogger(__name__)


class EnhancedOAuthManager:
    """Enhanced OAuth manager using Authlib for better security and features"""

    def __init__(self):
        self.token_manager = OAuthTokenManager()
        self.oauth = OAuth()
        self._setup_oauth_clients()

    def _setup_oauth_clients(self):
        """Setup OAuth clients for different providers"""
        
        # Google OAuth with PKCE support
        self.oauth.register(
            name='google',
            client_id=os.getenv("GOOGLE_CLIENT_ID"),
            client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
            server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
            client_kwargs={
                'scope': 'openid email profile https://www.googleapis.com/auth/gmail.readonly',
                'code_challenge_method': 'S256',  # PKCE support
                'code_challenge': None  # Will be generated dynamically
            }
        )

        # Zoom OAuth (when implemented)
        zoom_client_id = os.getenv("ZOOM_CLIENT_ID")
        zoom_client_secret = os.getenv("ZOOM_CLIENT_SECRET")
        if zoom_client_id and zoom_client_secret:
            self.oauth.register(
                name='zoom',
                client_id=zoom_client_id,
                client_secret=zoom_client_secret,
                access_token_url='https://zoom.us/oauth/token',
                authorize_url='https://zoom.us/oauth/authorize',
                client_kwargs={
                    'scope': 'meeting:read recording:read',
                    'code_challenge_method': 'S256',
                    'code_challenge': None
                }
            )

    async def initiate_oauth_flow(self, provider: str, is_desktop: bool = False) -> Dict[str, Any]:
        """Initiate OAuth flow with PKCE support for desktop apps"""
        try:
            if provider not in self.oauth._clients:
                raise ValueError(f"Unsupported provider: {provider}")

            client = self.oauth.create_client(provider)
            
            # Generate PKCE challenge for desktop apps
            if is_desktop:
                code_verifier = client.generate_code_verifier()
                code_challenge = client.generate_code_challenge(code_verifier)
                client.code_challenge = code_challenge
                client.code_verifier = code_verifier
                
                # Store code verifier for later use
                self.token_manager._store_code_verifier(provider, code_verifier)

            # Generate authorization URL
            redirect_uri = self._get_redirect_uri(provider, is_desktop)
            auth_url = client.create_authorization_url(redirect_uri)
            
            logger.info(f"Initiated OAuth flow for {provider} (desktop: {is_desktop})")
            
            return {
                "auth_url": auth_url,
                "provider": provider,
                "is_desktop": is_desktop
            }

        except Exception as e:
            logger.error(f"Error initiating OAuth flow for {provider}: {e}")
            raise

    async def handle_oauth_callback(self, provider: str, code: str, state: Optional[str] = None, is_desktop: bool = False) -> Dict[str, Any]:
        """Handle OAuth callback and exchange code for tokens"""
        try:
            client = self.oauth.create_client(provider)
            redirect_uri = self._get_redirect_uri(provider, is_desktop)
            
            # For desktop apps, retrieve stored code verifier
            if is_desktop:
                code_verifier = self.token_manager._get_code_verifier(provider)
                if code_verifier:
                    client.code_verifier = code_verifier

            # Exchange code for tokens
            token = await client.fetch_token(
                token_url=client.token_endpoint,
                authorization_response=f"?code={code}&state={state or ''}",
                redirect_uri=redirect_uri
            )

            # Store tokens securely
            success = self.token_manager.store_tokens(provider, token)
            if not success:
                raise Exception("Failed to store tokens securely")

            # Clean up code verifier for desktop apps
            if is_desktop:
                self.token_manager._clear_code_verifier(provider)

            logger.info(f"Successfully completed OAuth flow for {provider}")
            
            return {
                "success": True,
                "provider": provider,
                "message": f"{provider.title()} access granted successfully!"
            }

        except OAuthError as e:
            logger.error(f"OAuth error for {provider}: {e}")
            raise Exception(f"OAuth authentication failed: {e}")
        except Exception as e:
            logger.error(f"Error handling OAuth callback for {provider}: {e}")
            raise

    def _get_redirect_uri(self, provider: str, is_desktop: bool) -> str:
        """Get appropriate redirect URI based on provider and platform"""
        base_url = os.getenv("BASE_URL", "http://localhost:8000")
        
        if is_desktop:
            return f"{base_url}/auth/{provider}/desktop/callback"
        else:
            return f"{base_url}/auth/{provider}/callback"

    def get_oauth_client(self, provider: str):
        """Get OAuth client for a provider"""
        return self.oauth.create_client(provider)

    def is_provider_configured(self, provider: str) -> bool:
        """Check if OAuth provider is properly configured"""
        if provider == "google":
            return bool(os.getenv("GOOGLE_CLIENT_ID") and os.getenv("GOOGLE_CLIENT_SECRET"))
        elif provider == "zoom":
            return bool(os.getenv("ZOOM_CLIENT_ID") and os.getenv("ZOOM_CLIENT_SECRET"))
        elif provider == "asana":
            # Asana uses personal access tokens, not OAuth
            return bool(os.getenv("ASANA_PERSONAL_ACCESS_TOKEN"))
        return False

    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all OAuth providers"""
        providers = ["google", "zoom", "asana"]
        status = {}
        
        for provider in providers:
            status[provider] = {
                "configured": self.is_provider_configured(provider),
                "connected": self.token_manager.is_token_valid(provider),
                "oauth_flow": provider != "asana"  # Asana uses PAT, not OAuth
            }
        
        return status


# Global enhanced OAuth manager instance
enhanced_oauth_manager = EnhancedOAuthManager() 