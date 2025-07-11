"""
Tests for API integration functions
"""

import unittest
from unittest.mock import Mock, patch
from app.api_integration import (
    fetch_gmail_messages,
    fetch_zoom_meetings,
    fetch_asana_tasks,
)
from app.error_handling import safe_api_call


class TestAPIIntegration(unittest.TestCase):
    """Test cases for API integration functions"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_credentials = Mock()
        self.mock_token = "test_token"
        self.mock_user_id = "test_user_id"
        self.mock_workspace_id = "test_workspace_id"
        self.mock_project_id = "test_project_id"

    @patch("app.api_integration.build")
    def test_fetch_gmail_messages_success(self, mock_build):
        """Test successful Gmail message fetching"""
        # Mock the Gmail service
        mock_service = Mock()
        mock_messages = [
            {"id": "msg1", "threadId": "thread1"},
            {"id": "msg2", "threadId": "thread2"},
        ]
        mock_service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
            "messages": mock_messages
        }
        mock_service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
            "id": "msg1",
            "threadId": "thread1",
            "snippet": "Test message",
        }
        mock_build.return_value = mock_service

        # Test the function
        result = fetch_gmail_messages(self.mock_credentials, max_results=2)

        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        mock_build.assert_called_once_with(
            "gmail", "v1", credentials=self.mock_credentials
        )

    @patch("app.api_integration.requests.get")
    def test_fetch_zoom_meetings_success(self, mock_get):
        """Test successful Zoom meetings fetching"""
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "meetings": [
                {"id": "meeting1", "topic": "Test Meeting"},
                {"id": "meeting2", "topic": "Another Meeting"},
            ]
        }
        mock_get.return_value = mock_response

        # Test the function
        result = fetch_zoom_meetings(self.mock_token, self.mock_user_id)

        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        mock_get.assert_called_once()

    @patch("app.api_integration.requests.get")
    def test_fetch_zoom_meetings_error(self, mock_get):
        """Test Zoom API error handling"""
        # Mock the response with error
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        # Test that exception is raised
        with self.assertRaises(Exception) as context:
            fetch_zoom_meetings(self.mock_token, self.mock_user_id)

        self.assertIn("Zoom API error: 401", str(context.exception))

    @patch("app.api_integration.requests.get")
    def test_fetch_asana_tasks_success(self, mock_get):
        """Test successful Asana tasks fetching"""
        # Mock the response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"gid": "task1", "name": "Task 1"},
                {"gid": "task2", "name": "Task 2"},
            ]
        }
        mock_get.return_value = mock_response

        # Test the function
        result = fetch_asana_tasks(
            self.mock_token, self.mock_workspace_id, self.mock_project_id
        )

        # Assertions
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)
        mock_get.assert_called_once()


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling functions"""

    def test_safe_api_call_success(self):
        """Test safe_api_call with successful function"""

        def test_func():
            return "success"

        result = safe_api_call(test_func)
        self.assertEqual(result, "success")

    def test_safe_api_call_failure(self):
        """Test safe_api_call with failing function"""

        def test_func():
            raise Exception("Test error")

        result = safe_api_call(test_func)
        self.assertIsNone(result)

    def test_validate_data_success(self):
        """Test validate_data with valid data"""
        from app.error_handling import validate_data

        data = {"key1": "value1", "key2": "value2"}
        required_keys = ["key1", "key2"]

        result = validate_data(data, required_keys)
        self.assertTrue(result)

    def test_validate_data_missing_keys(self):
        """Test validate_data with missing keys"""
        from app.error_handling import validate_data

        data = {"key1": "value1"}
        required_keys = ["key1", "key2"]

        result = validate_data(data, required_keys)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
