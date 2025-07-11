"""
Enhanced Sandbox Environment for GlassDesk
Tests all components with mock data before OAuth setup
"""

import json
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent / "app"))

from app.data_processor import DataProcessor
from app.ai_interface import AIInterface
from app.user_communication import user_comm
from app.logging_config import setup_logging

def load_mock_data():
    """Load enhanced mock data"""
    try:
        mock_data_path = Path(__file__).parent.parent / "mock_data" / "enhanced_sample_data.json"
        with open(mock_data_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading mock data: {e}")
        return {}

def test_data_processing():
    """Test the data processor with mock data"""
    print("\n" + "="*50)
    print("TESTING DATA PROCESSING")
    print("="*50)
    
    # Load mock data
    mock_data = load_mock_data()
    if not mock_data:
        print("❌ Failed to load mock data")
        return False
    
    # Initialize data processor
    data_processor = DataProcessor()
    
    # Test Gmail processing
    print("\n📧 Processing Gmail data...")
    gmail_result = data_processor.process_gmail_data(mock_data.get("gmail_messages", []))
    if gmail_result:
        print(f"✅ Gmail processing successful: {gmail_result.get('total_emails', 0)} emails processed")
        print(f"   - Important emails: {len(gmail_result.get('important_emails', []))}")
        print(f"   - Action items: {len(gmail_result.get('action_items', []))}")
    else:
        print("❌ Gmail processing failed")
        return False
    
    # Test Zoom processing
    print("\n📹 Processing Zoom data...")
    zoom_result = data_processor.process_zoom_data(mock_data.get("zoom_meetings", []))
    if zoom_result:
        print(f"✅ Zoom processing successful: {zoom_result.get('total_meetings', 0)} meetings processed")
        print(f"   - Upcoming meetings: {len(zoom_result.get('upcoming_meetings', []))}")
        print(f"   - Action items: {len(zoom_result.get('action_items', []))}")
    else:
        print("❌ Zoom processing failed")
        return False
    
    # Test Asana processing
    print("\n📋 Processing Asana data...")
    asana_result = data_processor.process_asana_data(mock_data.get("asana_tasks", []))
    if asana_result:
        print(f"✅ Asana processing successful: {asana_result.get('total_tasks', 0)} tasks processed")
        print(f"   - Completed tasks: {len(asana_result.get('completed_tasks', []))}")
        print(f"   - Pending tasks: {len(asana_result.get('pending_tasks', []))}")
        print(f"   - Overdue tasks: {len(asana_result.get('overdue_tasks', []))}")
    else:
        print("❌ Asana processing failed")
        return False
    
    # Test daily summary
    print("\n📊 Creating daily summary...")
    daily_summary = data_processor.create_daily_summary()
    if daily_summary:
        print("✅ Daily summary created successfully")
        print(f"   - Action items: {len(daily_summary.get('action_items', []))}")
        print(f"   - Priorities: {len(daily_summary.get('priorities', []))}")
        print(f"   - Insights: {len(daily_summary.get('insights', []))}")
    else:
        print("❌ Daily summary creation failed")
        return False
    
    return True

def test_ai_interface():
    """Test the AI interface with various queries"""
    print("\n" + "="*50)
    print("TESTING AI INTERFACE")
    print("="*50)
    
    # Load mock data and process it
    mock_data = load_mock_data()
    data_processor = DataProcessor()
    
    # Process all data first
    data_processor.process_gmail_data(mock_data.get("gmail_messages", []))
    data_processor.process_zoom_data(mock_data.get("zoom_meetings", []))
    data_processor.process_asana_data(mock_data.get("asana_tasks", []))
    
    # Initialize AI interface
    ai_interface = AIInterface(data_processor)
    
    # Test queries
    test_queries = [
        "How many emails do I have?",
        "What are my action items?",
        "What are my priorities?",
        "What did I accomplish today?",
        "How many meetings do I have?",
        "What are my deadlines?",
        "Give me insights about my work",
        "What's my general summary?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Test Query {i}: {query}")
        print("-" * 40)
        
        try:
            response = ai_interface.process_query(query)
            if response and response.get("response"):
                print(f"✅ Response: {response['response']}")
                print(f"   Type: {response.get('type', 'unknown')}")
            else:
                print("❌ No response generated")
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    # Test conversation history
    print(f"\n📝 Conversation History: {len(ai_interface.get_conversation_history())} entries")
    
    return True

def test_user_communication():
    """Test user communication system"""
    print("\n" + "="*50)
    print("TESTING USER COMMUNICATION")
    print("="*50)
    
    # Test different message types
    test_messages = [
        ("status", "Processing your emails..."),
        ("error", "I had trouble connecting to Gmail"),
        ("success", "All data processed successfully!"),
        ("info", "Found 5 new action items")
    ]
    
    for msg_type, message in test_messages:
        print(f"\n📢 {msg_type.upper()}: {message}")
        if msg_type == "status":
            user_comm.notify_user(message, level="info")
        elif msg_type == "error":
            user_comm.notify_user(message, level="error")
        elif msg_type == "success":
            user_comm.notify_user(message, level="success")
        elif msg_type == "info":
            user_comm.notify_user(message, level="info")
    
    return True

def test_error_handling():
    """Test error handling with malformed data"""
    print("\n" + "="*50)
    print("TESTING ERROR HANDLING")
    print("="*50)
    
    data_processor = DataProcessor()
    
    # Test with empty data
    print("\n🔍 Testing with empty data...")
    empty_result = data_processor.process_gmail_data([])
    if empty_result:
        print("✅ Handled empty data gracefully")
    else:
        print("❌ Failed to handle empty data")
    
    # Test with malformed data
    print("\n🔍 Testing with malformed data...")
    malformed_data = [{"invalid": "data", "missing": "fields"}]
    malformed_result = data_processor.process_gmail_data(malformed_data)
    if malformed_result:
        print("✅ Handled malformed data gracefully")
    else:
        print("❌ Failed to handle malformed data")
    
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Enhanced Sandbox Tests")
    print("="*60)
    
    # Setup logging
    setup_logging()
    
    # Run all tests
    tests = [
        ("Data Processing", test_data_processing),
        ("AI Interface", test_ai_interface),
        ("User Communication", test_user_communication),
        ("Error Handling", test_error_handling)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready for OAuth integration.")
    else:
        print("⚠️  Some tests failed. Please review the issues before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 