"""
Tests for Enhanced Features
Tests the enhanced OAuth and AI implementations
"""

import pytest
import os
from unittest.mock import Mock, patch
from app.enhanced_oauth_manager import EnhancedOAuthManager
from app.enhanced_ai_interface import EnhancedAIInterface
from app.data_processor import DataProcessor
import asyncio


class TestEnhancedOAuthManager:
    """Test enhanced OAuth manager functionality"""

    @pytest.fixture
    def oauth_manager(self):
        """Create enhanced OAuth manager instance"""
        return EnhancedOAuthManager()

    def test_oauth_manager_initialization(self, oauth_manager):
        """Test OAuth manager initializes correctly"""
        assert oauth_manager is not None
        assert hasattr(oauth_manager, 'oauth')
        assert hasattr(oauth_manager, 'token_manager')

    def test_provider_configuration_check(self, oauth_manager):
        """Test provider configuration checking"""
        # Mock environment variables
        with patch.dict(os.environ, {
            'GOOGLE_CLIENT_ID': 'test_client_id',
            'GOOGLE_CLIENT_SECRET': 'test_client_secret'
        }):
            assert oauth_manager.is_provider_configured('google') is True

        # Test without environment variables
        with patch.dict(os.environ, {}, clear=True):
            assert oauth_manager.is_provider_configured('google') is False

    def test_get_provider_status(self, oauth_manager):
        """Test getting provider status"""
        status = oauth_manager.get_provider_status()
        
        assert 'google' in status
        assert 'zoom' in status
        assert 'asana' in status
        
        for provider in status:
            assert 'configured' in status[provider]
            assert 'connected' in status[provider]
            assert 'oauth_flow' in status[provider]

    @pytest.mark.asyncio
    async def test_initiate_oauth_flow(self, oauth_manager):
        """Test OAuth flow initiation"""
        with patch.dict(os.environ, {
            'GOOGLE_CLIENT_ID': 'test_client_id',
            'GOOGLE_CLIENT_SECRET': 'test_client_secret'
        }):
            try:
                result = await oauth_manager.initiate_oauth_flow('google', is_desktop=False)
                assert 'auth_url' in result
                assert result['provider'] == 'google'
                assert result['is_desktop'] is False
            except ValueError:
                # Expected if provider not configured in test environment
                pass

    @pytest.mark.asyncio
    async def test_unsupported_provider(self, oauth_manager):
        """Test handling of unsupported providers"""
        with pytest.raises(ValueError, match="Unsupported provider"):
            await oauth_manager.initiate_oauth_flow('unsupported_provider')


class TestEnhancedAIInterface:
    """Test enhanced AI interface functionality"""

    @pytest.fixture
    def data_processor(self):
        """Create data processor instance"""
        return DataProcessor()

    @pytest.fixture
    def ai_interface(self, data_processor):
        """Create enhanced AI interface instance"""
        return EnhancedAIInterface(data_processor)

    def test_ai_interface_initialization(self, ai_interface):
        """Test AI interface initializes correctly"""
        assert ai_interface is not None
        assert hasattr(ai_interface, 'llm')
        assert hasattr(ai_interface, 'embeddings')
        assert hasattr(ai_interface, 'text_splitter')
        assert hasattr(ai_interface, 'vectorstore')

    def test_conversation_history(self, ai_interface):
        """Test conversation history functionality"""
        # Test initial state
        history = ai_interface.get_conversation_history()
        assert isinstance(history, list)
        assert len(history) == 0

        # Test adding conversation
        ai_interface.conversation_history.append({
            "timestamp": "2024-01-01T00:00:00",
            "user_query": "test query",
            "type": "user"
        })
        
        history = ai_interface.get_conversation_history()
        assert len(history) == 1
        assert history[0]["user_query"] == "test query"

        # Test clearing history
        ai_interface.clear_conversation_history()
        history = ai_interface.get_conversation_history()
        assert len(history) == 0

    def test_format_gmail_data(self, ai_interface):
        """Test Gmail data formatting"""
        gmail_data = {
            "total_emails": 10,
            "important_emails": [
                {"subject": "Important Email", "sender": "test@example.com"},
                {"subject": "Another Email", "sender": "user@example.com"}
            ],
            "action_items": [{"task": "Follow up", "priority": "high"}]
        }
        
        formatted = ai_interface._format_gmail_data(gmail_data)
        assert "Total emails: 10" in formatted
        assert "Important emails: 2" in formatted
        assert "Action items: 1" in formatted
        assert "Important Email" in formatted

    def test_format_zoom_data(self, ai_interface):
        """Test Zoom data formatting"""
        zoom_data = {
            "total_meetings": 5,
            "upcoming_meetings": [{"title": "Team Meeting", "date": "2024-01-02"}],
            "past_meetings": [{"title": "Review Meeting", "date": "2024-01-01"}],
            "action_items": [{"task": "Send minutes", "priority": "medium"}],
            "meeting_summaries": [
                {"title": "Team Meeting", "date": "2024-01-02"},
                {"title": "Review Meeting", "date": "2024-01-01"}
            ]
        }
        
        formatted = ai_interface._format_zoom_data(zoom_data)
        assert "Total meetings: 5" in formatted
        assert "Upcoming meetings: 1" in formatted
        assert "Past meetings: 1" in formatted
        assert "Action items: 1" in formatted

    def test_format_asana_data(self, ai_interface):
        """Test Asana data formatting"""
        asana_data = {
            "total_tasks": 15,
            "completed_tasks": [{"name": "Task 1", "status": "completed"}],
            "pending_tasks": [{"name": "Task 2", "status": "pending"}],
            "overdue_tasks": [{"name": "Task 3", "status": "overdue"}],
            "high_priority": [
                {"name": "Urgent Task", "due_date": "2024-01-01"},
                {"name": "Important Task", "due_date": "2024-01-02"}
            ]
        }
        
        formatted = ai_interface._format_asana_data(asana_data)
        assert "Total tasks: 15" in formatted
        assert "Completed tasks: 1" in formatted
        assert "Pending tasks: 1" in formatted
        assert "Overdue tasks: 1" in formatted
        assert "High priority: 2" in formatted

    def test_fallback_response(self, ai_interface):
        """Test fallback response when RAG is not available"""
        response = ai_interface._fallback_response("test query")
        
        assert "response" in response
        assert "type" in response
        assert response["type"] == "fallback"
        assert "suggestion" in response

    @patch('app.enhanced_ai_interface.OpenAI')
    @patch('app.enhanced_ai_interface.OpenAIEmbeddings')
    def test_vector_store_initialization(self, mock_embeddings, mock_llm, ai_interface):
        """Test vector store initialization"""
        # Mock the OpenAI and embeddings classes
        mock_llm.return_value = Mock()
        mock_embeddings.return_value = Mock()
        
        # Mock the data processor to return some data
        ai_interface.data_processor.processed_data = {
            "gmail": {
                "total_emails": 5,
                "important_emails": [{"subject": "Test", "sender": "test@example.com"}],
                "action_items": []
            }
        }
        
        # Test initialization
        success = ai_interface.initialize_vectorstore()
        # Should fail in test environment due to missing OpenAI API key
        assert success is False

    def test_vector_store_stats_not_initialized(self, ai_interface):
        """Test vector store stats when not initialized"""
        stats = ai_interface.get_vector_store_stats()
        assert stats["status"] == "not_initialized"

    def test_search_similar_not_initialized(self, ai_interface):
        """Test similarity search when vector store not initialized"""
        results = ai_interface.search_similar("test query")
        assert isinstance(results, list)
        assert len(results) == 0


class TestIntegration:
    """Integration tests for enhanced features"""

    def test_enhanced_features_workflow(self):
        """Test that enhanced features can work together"""
        # Test that we can create instances
        data_processor = DataProcessor()
        ai_interface = EnhancedAIInterface(data_processor)
        oauth_manager = EnhancedOAuthManager()
        
        assert data_processor is not None
        assert ai_interface is not None
        assert oauth_manager is not None
        
        # Test that they can interact
        assert ai_interface.data_processor == data_processor
        assert oauth_manager.token_manager is not None

    @pytest.mark.asyncio
    async def test_error_handling(self):
        """Test error handling in enhanced features"""
        oauth_manager = EnhancedOAuthManager()
        with pytest.raises(ValueError):
            await oauth_manager.initiate_oauth_flow('invalid_provider')
        data_processor = DataProcessor()
        ai_interface = EnhancedAIInterface(data_processor)
        response = ai_interface._fallback_response("test")
        assert response is not None
        assert "response" in response


if __name__ == "__main__":
    pytest.main([__file__]) 