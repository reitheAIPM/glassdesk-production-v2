#!/usr/bin/env python3
"""
Email processing functionality for GlassDesk

See docs/mock_data_guidelines.md for information about mock data usage and transition plans.
"""

import json
import logging
import re
from typing import Dict, List, Any
from datetime import datetime

from .data_ingestion import normalize_gmail_message
from .error_handling import safe_api_call
from .logging_config import log_ai_output

logger = logging.getLogger(__name__)


class EmailProcessor:
    """Processes email data from various sources"""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.use_mock_data = config_manager.should_use_mock_data()
        self.mock_data_path = config_manager.get_mock_data_path()

    def load_emails(self, source: str = "gmail") -> List[Dict[str, Any]]:
        """Load emails from source (mock data or real API)"""
        if self.use_mock_data:
            return self._load_mock_emails(source)
        else:
            return self._load_real_emails(source)

    def _load_mock_emails(self, source: str) -> List[Dict[str, Any]]:
        """Load emails from mock data"""
        try:
            mock_file = f"{self.mock_data_path}sample_{source}_messages.json"
            with open(mock_file, "r") as f:
                data = json.load(f)
            logger.info(
                f"Loaded {len(data.get('messages', []))} mock emails from {source}"
            )
            return data.get("messages", [])
        except FileNotFoundError:
            logger.error(f"Mock data file not found: {mock_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in mock data file: {e}")
            return []

    def _load_real_emails(self, source: str) -> List[Dict[str, Any]]:
        """Load emails from real API"""
        # TODO: Implement real API calls
        # This will be implemented when transitioning from mock data
        logger.warning("Real API calls not yet implemented")
        return []

    def detect_spam(self, email: Dict[str, Any]) -> bool:
        """Detect if an email is spam"""
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()

        spam_indicators = [
            "congratulations",
            "winner",
            "prize",
            "claim",
            "limited time",
            "click here",
            "free money",
            "lottery",
            "inheritance",
            "urgent action",
            "bank transfer",
            "unclaimed funds",
            "lottery winner",
        ]

        return any(
            indicator in subject or indicator in body for indicator in spam_indicators
        )

    def detect_priority(self, email: Dict[str, Any]) -> str:
        """Detect priority level of an email"""
        subject = email.get("subject", "").lower()
        body = email.get("body", "").lower()

        high_priority_indicators = [
            "urgent",
            "asap",
            "immediate",
            "critical",
            "action required",
            "deadline",
            "important",
            "review",
            "approval needed",
            "emergency",
        ]

        medium_priority_indicators = [
            "follow up",
            "meeting",
            "update",
            "status",
            "progress",
            "discussion",
            "feedback",
            "review",
        ]

        if any(
            indicator in subject or indicator in body
            for indicator in high_priority_indicators
        ):
            return "high"
        elif any(
            indicator in subject or indicator in body
            for indicator in medium_priority_indicators
        ):
            return "medium"
        else:
            return "low"

    def extract_action_items(self, email: Dict[str, Any]) -> List[str]:
        """Extract action items from email content"""
        body = email.get("body", "")
        action_items = []

        # Simple regex patterns for action items
        action_patterns = [
            r"please\s+(\w+\s+)*",  # "Please do something"
            r"need\s+to\s+(\w+\s+)*",  # "Need to do something"
            r"should\s+(\w+\s+)*",  # "Should do something"
            r"action\s+required",  # "Action required"
            r"deadline",  # Deadline mentioned
        ]

        for pattern in action_patterns:
            matches = re.findall(pattern, body, re.IGNORECASE)
            action_items.extend(matches)

        return list(set(action_items))  # Remove duplicates

    def process_email(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single email"""
        try:
            # Create mock Gmail API message structure for normalization
            mock_gmail_message = {
                "id": email["id"],
                "threadId": email["threadId"],
                "snippet": email["snippet"],
                "payload": {
                    "headers": [
                        {"name": "Subject", "value": email["subject"]},
                        {"name": "From", "value": email["from"]},
                        {"name": "To", "value": email["to"]},
                        {"name": "Date", "value": email["date"]},
                    ],
                    "body": {"data": email.get("body", "")},
                },
            }

            # Normalize email data
            normalized = normalize_gmail_message(mock_gmail_message)

            # Process email
            processed = {
                "id": normalized["id"],
                "threadId": normalized["threadId"],
                "subject": normalized["subject"],
                "from": normalized["from"],
                "to": normalized["to"],
                "date": normalized["date"],
                "snippet": normalized["snippet"],
                "body": email.get("body", ""),
                "processed_at": datetime.now().isoformat(),
                "is_spam": self.detect_spam(email),
                "priority": self.detect_priority(email),
                "action_items": self.extract_action_items(email),
                "summary": None,  # Will be filled by AI summarization
            }

            # TODO: Add AI summarization here
            # processed['summary'] = self._summarize_email(processed['body'])

            logger.info(
                f"Processed email: {processed['subject']} (Priority: {processed['priority']})"
            )
            return processed

        except Exception as e:
            logger.error(
                f"Error processing email {email.get('id', 'unknown')}: {str(e)}"
            )
            return {}

    def process_all_emails(self, source: str = "gmail") -> List[Dict[str, Any]]:
        """Process all emails from a source"""
        emails = self.load_emails(source)
        processed_emails = []

        for email in emails:
            processed = self.process_email(email)
            if processed:
                processed_emails.append(processed)

        logger.info(f"Processed {len(processed_emails)} emails from {source}")
        return processed_emails

    def get_email_summary(self, emails: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of all emails"""
        if not emails:
            return {}

        spam_count = sum(1 for e in emails if e.get("is_spam", False))
        priority_counts = {
            "high": sum(1 for e in emails if e.get("priority") == "high"),
            "medium": sum(1 for e in emails if e.get("priority") == "medium"),
            "low": sum(1 for e in emails if e.get("priority") == "low"),
        }

        total_action_items = sum(len(e.get("action_items", [])) for e in emails)

        return {
            "total_emails": len(emails),
            "spam_count": spam_count,
            "priority_breakdown": priority_counts,
            "total_action_items": total_action_items,
            "date_range": {
                "earliest": min(e.get("date", "") for e in emails),
                "latest": max(e.get("date", "") for e in emails),
            },
        }


# Global instance
email_processor = None


def get_email_processor(config_manager):
    """Get global email processor instance"""
    global email_processor
    if email_processor is None:
        email_processor = EmailProcessor(config_manager)
    return email_processor
