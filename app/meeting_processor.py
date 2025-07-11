#!/usr/bin/env python3
"""
Meeting processing functionality for GlassDesk

See docs/mock_data_guidelines.md for information about mock data usage and transition plans.
"""

import json
import logging
from typing import Dict, List, Any
from datetime import datetime

from .data_ingestion import normalize_zoom_meeting
from .error_handling import safe_api_call
from .logging_config import log_ai_output

logger = logging.getLogger(__name__)


class MeetingProcessor:
    """Processes meeting data from various sources"""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.use_mock_data = config_manager.should_use_mock_data()
        self.mock_data_path = config_manager.get_mock_data_path()

    def load_meetings(self, source: str = "zoom") -> List[Dict[str, Any]]:
        """Load meetings from source (mock data or real API)"""
        if self.use_mock_data:
            return self._load_mock_meetings(source)
        else:
            return self._load_real_meetings(source)

    def _load_mock_meetings(self, source: str) -> List[Dict[str, Any]]:
        """Load meetings from mock data"""
        try:
            mock_file = f"{self.mock_data_path}sample_{source}_meetings.json"
            with open(mock_file, "r") as f:
                data = json.load(f)
            logger.info(
                f"Loaded {len(data.get('meetings', []))} mock meetings from {source}"
            )
            return data.get("meetings", [])
        except FileNotFoundError:
            logger.error(f"Mock data file not found: {mock_file}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in mock data file: {e}")
            return []

    def _load_real_meetings(self, source: str) -> List[Dict[str, Any]]:
        """Load meetings from real API"""
        # TODO: Implement real API calls
        # This will be implemented when transitioning from mock data
        logger.warning("Real API calls not yet implemented")
        return []

    def process_meeting(self, meeting: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single meeting"""
        try:
            # Normalize meeting data
            normalized = normalize_zoom_meeting(meeting)

            # Extract key information
            processed = {
                "id": normalized["id"],
                "topic": normalized["topic"],
                "start_time": normalized["start_time"],
                "duration": normalized["duration"],
                "participants": meeting.get("participants", []),
                "transcript": meeting.get("transcript", ""),
                "recording_files": normalized["recording_files"],
                "processed_at": datetime.now().isoformat(),
                "summary": None,  # Will be filled by AI summarization
                "action_items": [],  # Will be extracted by AI
                "key_topics": [],  # Will be extracted by AI
            }

            # TODO: Add AI summarization here
            # processed['summary'] = self._summarize_meeting(processed['transcript'])
            # processed['action_items'] = self._extract_action_items(processed['transcript'])
            # processed['key_topics'] = self._extract_key_topics(processed['transcript'])

            logger.info(f"Processed meeting: {processed['topic']}")
            return processed

        except Exception as e:
            logger.error(
                f"Error processing meeting {meeting.get('id', 'unknown')}: {str(e)}"
            )
            return {}

    def process_all_meetings(self, source: str = "zoom") -> List[Dict[str, Any]]:
        """Process all meetings from a source"""
        meetings = self.load_meetings(source)
        processed_meetings = []

        for meeting in meetings:
            processed = self.process_meeting(meeting)
            if processed:
                processed_meetings.append(processed)

        logger.info(f"Processed {len(processed_meetings)} meetings from {source}")
        return processed_meetings

    def get_meeting_summary(self, meetings: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate summary of all meetings"""
        if not meetings:
            return {}

        total_duration = sum(m.get("duration", 0) for m in meetings)
        total_participants = len(
            set(
                participant
                for meeting in meetings
                for participant in meeting.get("participants", [])
            )
        )

        return {
            "total_meetings": len(meetings),
            "total_duration": total_duration,
            "unique_participants": total_participants,
            "date_range": {
                "earliest": min(m.get("start_time", "") for m in meetings),
                "latest": max(m.get("start_time", "") for m in meetings),
            },
            "recordings_available": sum(
                1 for m in meetings if m.get("recording_files")
            ),
        }


# Global instance
meeting_processor = None


def get_meeting_processor(config_manager):
    """Get global meeting processor instance"""
    global meeting_processor
    if meeting_processor is None:
        meeting_processor = MeetingProcessor(config_manager)
    return meeting_processor
