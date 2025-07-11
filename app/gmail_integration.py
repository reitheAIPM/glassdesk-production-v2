"""
Gmail Integration for GlassDesk

Real Gmail API integration using OAuth tokens and Google API client.
Replaces mock data with actual Gmail API calls.
"""

import logging
from typing import Dict, List, Any, Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

from .api_integration import fetch_gmail_messages
from .enhanced_oauth_manager import enhanced_oauth_manager
from .data_processor import DataProcessor
from .user_communication import user_comm
from .error_handling import log_api_error

logger = logging.getLogger(__name__)


class GmailIntegration:
    """Real Gmail API integration for GlassDesk"""

    def __init__(self):
        self.data_processor = DataProcessor()
        self.user_comm = user_comm

    def get_user_emails(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Fetch real emails from Gmail API using OAuth tokens
        
        Args:
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of processed email data
        """
        try:
            # Get OAuth credentials for Gmail
            credentials = self._get_gmail_credentials()
            if not credentials:
                self.user_comm.notify_user(
                    "Gmail access not configured. Please authenticate with Gmail first.",
                    level="warning"
                )
                return []

            # Fetch emails from Gmail API
            logger.info(f"Fetching {max_results} emails from Gmail API")
            raw_messages = fetch_gmail_messages(credentials, max_results=max_results)
            
            # Process and normalize email data
            processed_emails = []
            for message in raw_messages:
                email_data = self._normalize_gmail_message(message)
                if email_data:
                    processed_emails.append(email_data)

            self.user_comm.notify_user(
                f"Successfully fetched {len(processed_emails)} emails from Gmail",
                level="info"
            )
            
            return processed_emails

        except HttpError as e:
            error_msg = f"Gmail API error: {e.resp.status} - {e.content.decode()}"
            log_api_error("get_user_emails", e, {"max_results": max_results})
            self.user_comm.notify_user(
                "I had trouble accessing your Gmail. Please check your permissions.",
                level="error"
            )
            return []

        except Exception as e:
            log_api_error("get_user_emails", e, {"max_results": max_results})
            self.user_comm.notify_user(
                "I encountered an error while accessing Gmail. Please try again.",
                level="error"
            )
            return []

    def _get_gmail_credentials(self) -> Optional[Credentials]:
        """Get Gmail OAuth credentials from the enhanced OAuth manager"""
        try:
            # Get tokens for Google OAuth
            tokens = enhanced_oauth_manager.token_manager.get_tokens("google")
            if not tokens:
                logger.warning("No Google OAuth tokens found")
                return None

            # Create credentials object
            credentials = Credentials(
                token=tokens.get("access_token"),
                refresh_token=tokens.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=enhanced_oauth_manager.config.get("gmail", {}).get("client_id"),
                client_secret=enhanced_oauth_manager.config.get("gmail", {}).get("client_secret"),
                scopes=["https://www.googleapis.com/auth/gmail.readonly"]
            )

            # Refresh token if needed
            if credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                # Update stored tokens
                enhanced_oauth_manager.token_manager.update_tokens("google", {
                    "access_token": credentials.token,
                    "refresh_token": credentials.refresh_token
                })

            return credentials

        except Exception as e:
            log_api_error("_get_gmail_credentials", e, {})
            return None

    def _normalize_gmail_message(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Normalize Gmail API message format to GlassDesk format
        
        Args:
            message: Raw Gmail API message
            
        Returns:
            Normalized email data or None if invalid
        """
        try:
            # Extract headers
            headers = message.get("payload", {}).get("headers", [])
            header_dict = {h["name"]: h["value"] for h in headers}

            # Extract body
            body = self._extract_message_body(message)

            # Create normalized email data
            email_data = {
                "id": message.get("id"),
                "thread_id": message.get("threadId"),
                "subject": header_dict.get("Subject", "No Subject"),
                "from": header_dict.get("From", "Unknown"),
                "to": header_dict.get("To", ""),
                "date": header_dict.get("Date", ""),
                "body": body,
                "snippet": message.get("snippet", ""),
                "labels": message.get("labelIds", []),
                "internal_date": message.get("internalDate"),
                "size_estimate": message.get("sizeEstimate", 0)
            }

            return email_data

        except Exception as e:
            log_api_error("_normalize_gmail_message", e, {"message_id": message.get("id")})
            return None

    def _extract_message_body(self, message: Dict[str, Any]) -> str:
        """Extract message body from Gmail API message structure"""
        try:
            payload = message.get("payload", {})
            
            # Handle multipart messages
            if payload.get("mimeType") == "multipart/alternative":
                parts = payload.get("parts", [])
                for part in parts:
                    if part.get("mimeType") == "text/plain":
                        return self._decode_body(part.get("body", {}).get("data", ""))
                # Fallback to first part
                if parts:
                    return self._decode_body(parts[0].get("body", {}).get("data", ""))
            
            # Handle simple text messages
            elif payload.get("mimeType") == "text/plain":
                return self._decode_body(payload.get("body", {}).get("data", ""))
            
            # Handle HTML messages
            elif payload.get("mimeType") == "text/html":
                return self._decode_body(payload.get("body", {}).get("data", ""))
            
            return ""

        except Exception as e:
            log_api_error("_extract_message_body", e, {"message_id": message.get("id")})
            return ""

    def _decode_body(self, encoded_data: str) -> str:
        """Decode base64 encoded message body"""
        try:
            import base64
            if encoded_data:
                return base64.urlsafe_b64decode(encoded_data).decode("utf-8")
            return ""
        except Exception as e:
            log_api_error("_decode_body", e, {})
            return ""

    def process_gmail_data(self, max_results: int = 50) -> Dict[str, Any]:
        """
        Fetch and process real Gmail data
        
        Args:
            max_results: Maximum number of emails to fetch
            
        Returns:
            Processed Gmail data summary
        """
        try:
            # Fetch real emails
            emails = self.get_user_emails(max_results=max_results)
            
            if not emails:
                self.user_comm.notify_user(
                    "No emails found or Gmail access not configured",
                    level="info"
                )
                return {}

            # Process emails using existing data processor
            processed_data = self.data_processor.process_gmail_data(emails)
            
            self.user_comm.notify_user(
                f"Successfully processed {len(emails)} emails from Gmail",
                level="info"
            )
            
            return processed_data

        except Exception as e:
            log_api_error("process_gmail_data", e, {"max_results": max_results})
            self.user_comm.notify_user(
                "I encountered an error while processing Gmail data",
                level="error"
            )
            return {}


# Global instance for easy access
gmail_integration = GmailIntegration() 