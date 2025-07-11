#!/usr/bin/env python3
"""
Test email processing functionality with mock data

See docs/mock_data_guidelines.md for information about mock data usage and transition plans.
"""

import json
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_ingestion import normalize_gmail_message


def load_mock_email_data():
    """Load mock email data for testing"""
    try:
        with open("mock_data/sample_gmail_messages.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.skip("Mock email data not found")


def test_email_normalization():
    """Test email data normalization"""
    email_data = load_mock_email_data()

    for message in email_data["messages"]:
        # Create a mock Gmail API message structure
        mock_gmail_message = {
            "id": message["id"],
            "threadId": message["threadId"],
            "snippet": message["snippet"],
            "payload": {
                "headers": [
                    {"name": "Subject", "value": message["subject"]},
                    {"name": "From", "value": message["from"]},
                    {"name": "To", "value": message["to"]},
                    {"name": "Date", "value": message["date"]},
                ],
                "body": {"data": message.get("body", "")},
            },
        }

        normalized = normalize_gmail_message(mock_gmail_message)

        # Check required fields
        assert "id" in normalized
        assert "threadId" in normalized
        assert "subject" in normalized
        assert "from" in normalized
        assert "to" in normalized
        assert "date" in normalized
        assert "snippet" in normalized

        # Check data types
        assert isinstance(normalized["id"], str)
        assert isinstance(normalized["threadId"], str)
        assert isinstance(normalized["subject"], str)
        assert isinstance(normalized["from"], str)
        assert isinstance(normalized["to"], str)
        assert isinstance(normalized["date"], str)
        assert isinstance(normalized["snippet"], str)


def test_spam_detection():
    """Test spam detection in email data"""
    email_data = load_mock_email_data()

    spam_count = 0
    for message in email_data["messages"]:
        subject = message["subject"].lower()
        body = message.get("body", "").lower()

        # Simple spam detection logic
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
        ]

        is_spam = any(
            indicator in subject or indicator in body for indicator in spam_indicators
        )

        if is_spam:
            spam_count += 1

    # Check that we detect the spam message in our mock data
    assert spam_count >= 1


def test_priority_detection():
    """Test priority detection in email data"""
    email_data = load_mock_email_data()

    priority_indicators = [
        "urgent",
        "asap",
        "immediate",
        "critical",
        "action required",
        "deadline",
        "important",
        "review",
        "approval needed",
    ]

    priority_count = 0
    for message in email_data["messages"]:
        subject = message["subject"].lower()
        body = message.get("body", "").lower()

        has_priority = any(
            indicator in subject or indicator in body
            for indicator in priority_indicators
        )

        if has_priority:
            priority_count += 1

    # Check that we detect priority messages in our mock data
    assert priority_count >= 1


def test_email_metadata():
    """Test email metadata structure"""
    email_data = load_mock_email_data()

    # Check metadata structure
    assert "metadata" in email_data
    metadata = email_data["metadata"]

    assert "total_messages" in metadata
    assert "date_range" in metadata
    assert "spam_count" in metadata
    assert "important_count" in metadata
    assert "action_required_count" in metadata

    # Check data types
    assert isinstance(metadata["total_messages"], int)
    assert isinstance(metadata["spam_count"], int)
    assert isinstance(metadata["important_count"], int)
    assert isinstance(metadata["action_required_count"], int)


def test_email_thread_processing():
    """Test email thread processing"""
    email_data = load_mock_email_data()

    # Group messages by thread
    threads = {}
    for message in email_data["messages"]:
        thread_id = message["threadId"]
        if thread_id not in threads:
            threads[thread_id] = []
        threads[thread_id].append(message)

    # Check thread structure
    assert len(threads) > 0

    for thread_id, messages in threads.items():
        # Each thread should have at least one message
        assert len(messages) >= 1

        # Messages in a thread should have the same threadId
        for message in messages:
            assert message["threadId"] == thread_id


if __name__ == "__main__":
    pytest.main([__file__])
