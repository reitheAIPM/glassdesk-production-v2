"""
Slack integration example for GlassDesk
Follows the contributing guidelines pattern for new integrations
"""

import requests
from typing import List, Dict, Any
from .error_handling import safe_api_call
from .logging_config import log_api_error, log_data_ingestion


def fetch_slack_messages(
    token: str, channel_id: str, limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Fetch messages from a Slack channel

    Args:
        token: Slack bot token
        channel_id: Channel ID to fetch messages from
        limit: Maximum number of messages to fetch

    Returns:
        List of message dictionaries
    """
    url = "https://slack.com/api/conversations.history"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"channel": channel_id, "limit": limit}

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                messages = data.get("messages", [])
                log_data_ingestion("slack", len(messages), True)
                return messages
            else:
                error_msg = data.get("error", "Unknown Slack API error")
                log_api_error("slack", Exception(error_msg), {"channel_id": channel_id})
                return []
        else:
            log_api_error(
                "slack",
                Exception(f"HTTP {response.status_code}"),
                {"channel_id": channel_id},
            )
            return []
    except Exception as e:
        log_api_error("slack", e, {"channel_id": channel_id})
        return []


def normalize_slack_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize Slack message data to standard format

    Args:
        message: Raw Slack message data

    Returns:
        Normalized message data
    """
    return {
        "id": message.get("ts"),
        "channel_id": message.get("channel"),
        "user_id": message.get("user"),
        "text": message.get("text", ""),
        "timestamp": message.get("ts"),
        "thread_ts": message.get("thread_ts"),
        "reactions": message.get("reactions", []),
        "attachments": message.get("attachments", []),
    }


# TODO: Add more Slack API endpoints (channels, users, etc.)
# FIXME: Need to handle Slack rate limiting and pagination
