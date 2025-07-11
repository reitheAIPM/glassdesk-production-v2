#!/usr/bin/env python3
"""
Test meeting processing functionality with mock data

See docs/mock_data_guidelines.md for information about mock data usage and transition plans.
"""

import json
import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.data_ingestion import normalize_zoom_meeting


def load_mock_meeting_data():
    """Load mock meeting data for testing"""
    try:
        with open("mock_data/sample_zoom_meetings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        pytest.skip("Mock meeting data not found")


def test_meeting_normalization():
    """Test meeting data normalization"""
    meeting_data = load_mock_meeting_data()

    for meeting in meeting_data["meetings"]:
        normalized = normalize_zoom_meeting(meeting)

        # Check required fields
        assert "id" in normalized
        assert "topic" in normalized
        assert "start_time" in normalized
        assert "duration" in normalized

        # Check data types
        assert isinstance(normalized["id"], str)
        assert isinstance(normalized["topic"], str)
        assert isinstance(normalized["start_time"], str)
        assert isinstance(normalized["duration"], int)

        # Check recording files
        assert "recording_files" in normalized
        assert isinstance(normalized["recording_files"], list)


def test_meeting_transcript_processing():
    """Test meeting transcript processing"""
    meeting_data = load_mock_meeting_data()

    for meeting in meeting_data["meetings"]:
        transcript = meeting.get("transcript", "")

        # Check transcript exists
        assert len(transcript) > 0

        # Check for key meeting elements
        assert "Meeting started" in transcript or "Meeting ended" in transcript

        # Check for participant interactions
        participants = meeting.get("participants", [])
        for participant in participants:
            if participant in transcript:
                # Participant mentioned in transcript
                pass


def test_meeting_metadata():
    """Test meeting metadata structure"""
    meeting_data = load_mock_meeting_data()

    # Check metadata structure
    assert "metadata" in meeting_data
    metadata = meeting_data["metadata"]

    assert "total_meetings" in metadata
    assert "date_range" in metadata
    assert "total_duration" in metadata
    assert "recordings_available" in metadata

    # Check data types
    assert isinstance(metadata["total_meetings"], int)
    assert isinstance(metadata["total_duration"], int)
    assert isinstance(metadata["recordings_available"], int)


def test_recording_file_structure():
    """Test recording file structure"""
    meeting_data = load_mock_meeting_data()

    for meeting in meeting_data["meetings"]:
        recording_files = meeting.get("recording_files", [])

        for recording in recording_files:
            # Check required fields
            assert "id" in recording
            assert "file_name" in recording
            assert "file_size" in recording
            assert "download_url" in recording

            # Check data types
            assert isinstance(recording["id"], str)
            assert isinstance(recording["file_name"], str)
            assert isinstance(recording["file_size"], int)
            assert isinstance(recording["download_url"], str)


if __name__ == "__main__":
    pytest.main([__file__])
