"""
Test Routes for GlassDesk
API endpoints for testing data processing and AI interface
"""

from fastapi import APIRouter, HTTPException, Request
from typing import Dict, List, Any
import json
from pathlib import Path

from ..data_processor import DataProcessor
from ..ai_interface import AIInterface
from ..user_communication import user_comm
from app.enhanced_ai_interface import EnhancedAIInterface

router = APIRouter(prefix="/test", tags=["testing"])

data_processor = DataProcessor()
enhanced_ai = EnhancedAIInterface(data_processor)


def load_mock_data():
    """Load enhanced mock data"""
    try:
        mock_data_path = (
            Path(__file__).parent.parent.parent
            / "mock_data"
            / "enhanced_sample_data.json"
        )
        with open(mock_data_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to load mock data: {str(e)}"
        )


@router.post("/process-data")
async def process_mock_data():
    """Process all mock data and return results"""
    try:
        mock_data = load_mock_data()
        data_processor = DataProcessor()

        # Process all data sources
        gmail_result = data_processor.process_gmail_data(
            mock_data.get("gmail_messages", [])
        )
        zoom_result = data_processor.process_zoom_data(
            mock_data.get("zoom_meetings", [])
        )
        asana_result = data_processor.process_asana_data(
            mock_data.get("asana_tasks", [])
        )

        # Create daily summary
        daily_summary = data_processor.create_daily_summary()

        return {
            "success": True,
            "message": "Data processed successfully",
            "data": {
                "gmail": gmail_result,
                "zoom": zoom_result,
                "asana": asana_result,
                "daily_summary": daily_summary,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Data processing failed: {str(e)}")


@router.post("/query")
async def test_ai_query(query: str):
    """Test AI interface with a query"""
    try:
        mock_data = load_mock_data()
        data_processor = DataProcessor()

        # Process data first
        data_processor.process_gmail_data(mock_data.get("gmail_messages", []))
        data_processor.process_zoom_data(mock_data.get("zoom_meetings", []))
        data_processor.process_asana_data(mock_data.get("asana_tasks", []))

        # Initialize AI interface
        ai_interface = AIInterface(data_processor)

        # Process query
        response = ai_interface.process_query(query)

        return {"success": True, "query": query, "response": response}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Query processing failed: {str(e)}"
        )


@router.post("/ai/enhanced_query")
async def enhanced_query(request: Request):
    """Process a user query using the enhanced AI interface (LangChain RAG)"""
    body = await request.json()
    user_query = body.get("query")
    if not user_query:
        return {"error": "Missing 'query' in request body"}
    response = enhanced_ai.process_query(user_query)
    return response


@router.get("/sample-queries")
async def get_sample_queries():
    """Get sample queries for testing"""
    return {
        "queries": [
            "How many emails do I have?",
            "What are my action items?",
            "What are my priorities?",
            "What did I accomplish today?",
            "How many meetings do I have?",
            "What are my deadlines?",
            "Give me insights about my work",
            "What's my general summary?",
        ]
    }


@router.get("/mock-data-summary")
async def get_mock_data_summary():
    """Get summary of available mock data"""
    try:
        mock_data = load_mock_data()

        return {
            "gmail_messages": len(mock_data.get("gmail_messages", [])),
            "zoom_meetings": len(mock_data.get("zoom_meetings", [])),
            "asana_tasks": len(mock_data.get("asana_tasks", [])),
            "total_items": (
                len(mock_data.get("gmail_messages", []))
                + len(mock_data.get("zoom_meetings", []))
                + len(mock_data.get("asana_tasks", []))
            ),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get mock data summary: {str(e)}"
        )


@router.post("/test-error-handling")
async def test_error_handling():
    """Test error handling with malformed data"""
    try:
        data_processor = DataProcessor()

        # Test with empty data
        empty_result = data_processor.process_gmail_data([])

        # Test with malformed data
        malformed_data = [{"invalid": "data", "missing": "fields"}]
        malformed_result = data_processor.process_gmail_data(malformed_data)

        return {
            "success": True,
            "empty_data_handled": bool(empty_result),
            "malformed_data_handled": bool(malformed_result),
            "message": "Error handling tests completed",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error handling test failed: {str(e)}"
        )


@router.get("/system-status")
async def get_system_status():
    """Get overall system status"""
    try:
        # Test data loading
        mock_data = load_mock_data()

        # Test data processor
        data_processor = DataProcessor()
        gmail_result = data_processor.process_gmail_data(
            mock_data.get("gmail_messages", [])
        )

        # Test AI interface
        ai_interface = AIInterface(data_processor)
        test_response = ai_interface.process_query("How many emails do I have?")

        return {
            "status": "healthy",
            "components": {
                "mock_data_loading": True,
                "data_processor": bool(gmail_result),
                "ai_interface": bool(test_response),
                "user_communication": True,
            },
            "message": "All components are working correctly",
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "message": "System has issues that need attention",
        }
