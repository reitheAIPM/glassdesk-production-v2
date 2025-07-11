"""
OAuth Token Manager for GlassDesk
Handles secure storage, refresh, and management of OAuth tokens
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
import httpx
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TokenData(BaseModel):
    """Token data model for secure storage"""

    access_token: str
    refresh_token: Optional[str] = None
    expires_at: Optional[datetime] = None
    scope: str
    token_type: str = "Bearer"
    provider: str


class OAuthTokenManager:
    """Secure OAuth token management for GlassDesk"""

    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")
        if not self.secret_key:
            # Generate a temporary key for development
            self.secret_key = Fernet.generate_key().decode()
            logger.warning("No SECRET_KEY found, using temporary key for development")
        else:
            # Ensure the secret key is properly formatted for Fernet
            # Fernet requires a 32-byte key encoded in base64
            import base64
            try:
                # Try to decode and re-encode to ensure proper format
                key_bytes = base64.urlsafe_b64decode(self.secret_key + '=' * (4 - len(self.secret_key) % 4))
                self.secret_key = base64.urlsafe_b64encode(key_bytes).decode()
            except Exception:
                # If the key is not properly formatted, generate a new one
                logger.warning("SECRET_KEY is not properly formatted, generating new key")
                self.secret_key = Fernet.generate_key().decode()

        self.cipher = Fernet(self.secret_key.encode())
        self.tokens_file = "tokens.enc"

    def _encrypt_data(self, data: str) -> bytes:
        """Encrypt sensitive data"""
        return self.cipher.encrypt(data.encode())

    def _decrypt_data(self, encrypted_data: bytes) -> str:
        """Decrypt sensitive data"""
        return self.cipher.decrypt(encrypted_data).decode()

    def _load_tokens(self) -> Dict[str, TokenData]:
        """Load encrypted tokens from file"""
        if not os.path.exists(self.tokens_file):
            return {}

        try:
            with open(self.tokens_file, "rb") as f:
                encrypted_data = f.read()
                decrypted_data = self._decrypt_data(encrypted_data)
                tokens_dict = json.loads(decrypted_data)

                # Convert back to TokenData objects
                return {
                    provider: TokenData(**token_data)
                    for provider, token_data in tokens_dict.items()
                }
        except Exception as e:
            logger.error(f"Error loading tokens: {e}")
            return {}

    def _save_tokens(self, tokens: Dict[str, TokenData]):
        """Save encrypted tokens to file"""
        try:
            # Convert TokenData objects to dict for JSON serialization
            tokens_dict = {provider: token.dict() for provider, token in tokens.items()}

            encrypted_data = self._encrypt_data(json.dumps(tokens_dict))

            with open(self.tokens_file, "wb") as f:
                f.write(encrypted_data)

            logger.info("Tokens saved successfully")
        except Exception as e:
            logger.error(f"Error saving tokens: {e}")

    def store_tokens(self, provider: str, token_data: Dict[str, Any]):
        """Store OAuth tokens for a provider"""
        try:
            # Calculate expiration if not provided
            expires_in = token_data.get("expires_in")
            expires_at = None
            if expires_in:
                expires_at = datetime.now() + timedelta(seconds=expires_in)

            token = TokenData(
                access_token=token_data["access_token"],
                refresh_token=token_data.get("refresh_token"),
                expires_at=expires_at,
                scope=token_data.get("scope", ""),
                token_type=token_data.get("token_type", "Bearer"),
                provider=provider,
            )

            tokens = self._load_tokens()
            tokens[provider] = token
            self._save_tokens(tokens)

            logger.info(f"Stored tokens for {provider}")
            return True

        except Exception as e:
            logger.error(f"Error storing tokens for {provider}: {e}")
            return False

    def get_tokens(self, provider: str) -> Optional[TokenData]:
        """Get stored tokens for a provider"""
        tokens = self._load_tokens()
        return tokens.get(provider)

    def is_token_valid(self, provider: str) -> bool:
        """Check if token is valid and not expired"""
        token = self.get_tokens(provider)
        if not token:
            return False

        # Check if token is expired (with 5 minute buffer)
        if token.expires_at:
            return datetime.now() < token.expires_at - timedelta(minutes=5)

        return True

    async def refresh_token(self, provider: str) -> bool:
        """Refresh OAuth token for a provider"""
        token = self.get_tokens(provider)
        if not token or not token.refresh_token:
            logger.error(f"No refresh token available for {provider}")
            return False

        try:
            if provider == "google":
                return await self._refresh_google_token(token)
            elif provider == "zoom":
                return await self._refresh_zoom_token(token)
            elif provider == "asana":
                return await self._refresh_asana_token(token)
            else:
                logger.error(f"Unknown provider: {provider}")
                return False

        except Exception as e:
            logger.error(f"Error refreshing token for {provider}: {e}")
            return False

    async def _refresh_google_token(self, token: TokenData) -> bool:
        """Refresh Google OAuth token"""
        refresh_url = "https://oauth2.googleapis.com/token"
        refresh_data = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "refresh_token": token.refresh_token,
            "grant_type": "refresh_token",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(refresh_url, data=refresh_data)
            response.raise_for_status()
            new_token_data = response.json()

            # Update token with new data
            new_token = TokenData(
                access_token=new_token_data["access_token"],
                refresh_token=token.refresh_token,  # Keep existing refresh token
                expires_at=datetime.now()
                + timedelta(seconds=new_token_data.get("expires_in", 3600)),
                scope=token.scope,
                token_type=token.token_type,
                provider=token.provider,
            )

            tokens = self._load_tokens()
            tokens[token.provider] = new_token
            self._save_tokens(tokens)

            logger.info("Google token refreshed successfully")
            return True

    async def _refresh_zoom_token(self, token: TokenData) -> bool:
        """Refresh Zoom OAuth token"""
        # TODO: Implement Zoom token refresh
        logger.warning("Zoom token refresh not implemented yet")
        return False

    async def _refresh_asana_token(self, token: TokenData) -> bool:
        """Refresh Asana OAuth token"""
        # TODO: Implement Asana token refresh
        logger.warning("Asana token refresh not implemented yet")
        return False

    def revoke_tokens(self, provider: str) -> bool:
        """Revoke and remove tokens for a provider"""
        try:
            tokens = self._load_tokens()
            if provider in tokens:
                del tokens[provider]
                self._save_tokens(tokens)
                logger.info(f"Revoked tokens for {provider}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error revoking tokens for {provider}: {e}")
            return False

    def get_all_providers(self) -> Dict[str, bool]:
        """Get status of all OAuth providers"""
        tokens = self._load_tokens()
        return {provider: self.is_token_valid(provider) for provider in tokens.keys()}


# Global token manager instance
token_manager = OAuthTokenManager()
