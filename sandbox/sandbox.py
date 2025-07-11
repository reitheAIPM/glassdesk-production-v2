#!/usr/bin/env python3
"""
GlassDesk Sandbox - Isolated Testing Environment
Allows testing of ingestion, summarization, and analysis functions without full backend
"""

import sys
import os
import json
import logging
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.logging_config import setup_logging
from app.user_communication import user_comm
from app.self_healing import self_healing

def load_mock_data(data_type: str):
    """Load mock data for testing
    
    See docs/mock_data_guidelines.md for comprehensive usage rules and transition plans.
    Mock data is for development/testing only - production must use real APIs.
    """
    mock_file = f"mock_data/sample_{data_type}.json"
    
    try:
        with open(mock_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Mock data file not found: {mock_file}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {mock_file}: {e}")
        return None

def test_email_processing():
    """Test email processing with mock data"""
    print("📧 Testing email processing...")
    
    # Load mock email data
    email_data = load_mock_data("gmail_messages")
    if not email_data:
        return False
    
    # Process each email
    for message in email_data['messages']:
        print(f"\n📨 Processing: {message['subject']}")
        print(f"   From: {message['from']}")
        print(f"   Snippet: {message['snippet'][:100]}...")
        
        # TODO: Add email processing logic here
        # - Extract action items
        # - Identify priority level
        # - Categorize by type (work, personal, spam)
    
    print(f"\n✅ Processed {len(email_data['messages'])} emails")
    return True

def test_meeting_summarization():
    """Test meeting summarization with mock data"""
    print("\n📹 Testing meeting summarization...")
    
    # Load mock meeting data
    meeting_data = load_mock_data("zoom_meetings")
    if not meeting_data:
        return False
    
    # Process each meeting
    for meeting in meeting_data['meetings']:
        print(f"\n🎥 Processing: {meeting['topic']}")
        print(f"   Duration: {meeting['duration']} minutes")
        print(f"   Participants: {len(meeting['participants'])}")
        
        # Load meeting summarization prompt
        try:
            with open("prompts/summarize_meeting.txt", 'r') as f:
                prompt_template = f.read()
            
            # TODO: Add meeting summarization logic here
            # - Apply prompt template
            # - Extract key topics
            # - Identify action items
            # - Generate executive summary
            
            print(f"   Transcript length: {len(meeting['transcript'])} characters")
            
        except FileNotFoundError:
            print("   ❌ Meeting summarization prompt not found")
    
    print(f"\n✅ Processed {len(meeting_data['meetings'])} meetings")
    return True

def test_task_prioritization():
    """Test task prioritization with mock data"""
    print("\n📋 Testing task prioritization...")
    
    # Simulate tasks from multiple sources
    tasks = [
        {"source": "email", "task": "Q4 budget review", "deadline": "Friday", "priority": "high"},
        {"source": "meeting", "task": "Review mobile app design", "deadline": "Next week", "priority": "medium"},
        {"source": "asana", "task": "Update website content", "deadline": "Monday", "priority": "medium"},
        {"source": "email", "task": "Follow up with client", "deadline": "Today", "priority": "high"}
    ]
    
    # Load task prioritization prompt
    try:
        with open("prompts/task_prioritizer.txt", 'r') as f:
            prompt_template = f.read()
        
        # TODO: Add task prioritization logic here
        # - Apply prioritization prompt
        # - Categorize by urgency/importance
        # - Identify dependencies
        # - Suggest optimal order
        
        print(f"   📊 Prioritizing {len(tasks)} tasks from multiple sources")
        
    except FileNotFoundError:
        print("   ❌ Task prioritization prompt not found")
    
    print("\n✅ Task prioritization test completed")
    return True

def test_system_health():
    """Test system health monitoring"""
    print("\n🏥 Testing system health monitoring...")
    
    # Run diagnostics
    health_status = self_healing.run_full_diagnostics()
    
    print(f"   Overall Health: {health_status['health_percentage']:.1f}%")
    print(f"   Healthy Components: {health_status['healthy_components']}/{health_status['total_components']}")
    
    if health_status['issues_found']:
        print(f"   Issues Found: {health_status['issues_found']}")
        
        # Attempt auto-fixes
        print("   🔧 Attempting auto-fixes...")
        fix_results = self_healing.attempt_auto_fixes(health_status['issues_found'])
        
        successful_fixes = sum(1 for result in fix_results.values() if result)
        print(f"   ✅ Successfully fixed {successful_fixes} issues")
    else:
        print("   ✅ No issues detected")
    
    return True

def test_user_communication():
    """Test user communication system"""
    print("\n💬 Testing user communication...")
    
    # Test various user messages
    messages = [
        ("connecting_email", "Connecting to your email..."),
        ("processing_emails", "Reading your emails..."),
        ("emails_complete", "✅ Your emails have been processed successfully"),
        ("general_error", "Something went wrong, but I'm working to fix it automatically")
    ]
    
    for key, expected in messages:
        actual = user_comm.get_status_message(key)
        print(f"   {key}: {actual}")
        assert actual == expected, f"Message mismatch for {key}"
    
    print("   ✅ All user messages working correctly")
    return True

def run_sandbox_tests():
    """Run all sandbox tests"""
    print("🧪 GlassDesk Sandbox - Running Tests")
    print("=" * 50)
    
    # Setup logging
    logger = setup_logging()
    logger.info("Starting sandbox tests")
    
    # Run tests
    tests = [
        ("Email Processing", test_email_processing),
        ("Meeting Summarization", test_meeting_summarization),
        ("Task Prioritization", test_task_prioritization),
        ("System Health", test_system_health),
        ("User Communication", test_user_communication)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        except Exception as e:
            results.append((test_name, False))
            print(f"❌ FAIL {test_name} - Error: {str(e)}")
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Sandbox is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    # Log results
    logger.info(f"Sandbox tests completed: {passed}/{total} passed")
    
    return passed == total

if __name__ == "__main__":
    success = run_sandbox_tests()
    sys.exit(0 if success else 1) 