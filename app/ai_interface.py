# LEGACY: This file is deprecated. Use app/enhanced_ai_interface.py (EnhancedAIInterface) for all new AI query logic.
# This file is retained for reference only and should not be used for new development.

"""
AI Interface for GlassDesk
Handles natural language queries and provides intelligent responses
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from .user_communication import user_comm
from .logging_config import log_api_error


class AIInterface:
    """Handles natural language queries and provides intelligent responses"""

    def __init__(self, data_processor):
        self.logger = logging.getLogger("glassdesk.ai_interface")
        self.data_processor = data_processor
        self.user_comm = user_comm
        self.conversation_history = []

    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process user query and return intelligent response"""
        try:
            self.logger.info(f"Processing query: {user_query}")

            # Add to conversation history
            self.conversation_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "user_query": user_query,
                    "type": "user",
                }
            )

            # Analyze query intent
            intent = self._analyze_intent(user_query)

            # Generate response based on intent
            response = self._generate_response(user_query, intent)

            # Add response to conversation history
            self.conversation_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "response": response,
                    "type": "assistant",
                }
            )

            self.user_comm.notify_user("Query processed successfully", level="info")
            return response

        except Exception as e:
            log_api_error("process_query", e, {"query": user_query})
            self.user_comm.log_operation_error("process_query", e)
            return {
                "response": "I'm sorry, I had trouble processing your request. Could you try asking again?",
                "type": "error",
            }

    def _analyze_intent(self, query: str) -> str:
        """Analyze user query to determine intent"""
        query_lower = query.lower()

        # Intent patterns
        if any(
            word in query_lower for word in ["what", "how many", "count", "summary"]
        ):
            if any(word in query_lower for word in ["email", "emails", "mail"]):
                return "email_summary"
            elif any(word in query_lower for word in ["meeting", "meetings", "call"]):
                return "meeting_summary"
            elif any(
                word in query_lower for word in ["task", "tasks", "todo", "project"]
            ):
                return "task_summary"
            else:
                return "general_summary"

        elif any(
            word in query_lower for word in ["action", "todo", "need to do", "next"]
        ):
            return "action_items"

        elif any(
            word in query_lower
            for word in ["priority", "urgent", "important", "overdue"]
        ):
            return "priorities"

        elif any(word in query_lower for word in ["deadline", "due", "when"]):
            return "deadlines"

        elif any(
            word in query_lower
            for word in ["today", "accomplished", "done", "completed"]
        ):
            return "daily_accomplishments"

        elif any(word in query_lower for word in ["insight", "analysis", "pattern"]):
            return "insights"

        else:
            return "general_query"

    def _generate_response(self, query: str, intent: str) -> Dict[str, Any]:
        """Generate response based on intent and available data"""

        if intent == "email_summary":
            return self._handle_email_summary(query)
        elif intent == "meeting_summary":
            return self._handle_meeting_summary(query)
        elif intent == "task_summary":
            return self._handle_task_summary(query)
        elif intent == "action_items":
            return self._handle_action_items(query)
        elif intent == "priorities":
            return self._handle_priorities(query)
        elif intent == "deadlines":
            return self._handle_deadlines(query)
        elif intent == "daily_accomplishments":
            return self._handle_daily_accomplishments(query)
        elif intent == "insights":
            return self._handle_insights(query)
        else:
            return self._handle_general_query(query)

    def _handle_email_summary(self, query: str) -> Dict[str, Any]:
        """Handle email-related queries"""
        gmail_data = self.data_processor.processed_data.get("gmail", {})

        total_emails = gmail_data.get("total_emails", 0)
        important_emails = len(gmail_data.get("important_emails", []))
        action_items = len(gmail_data.get("action_items", []))

        response_text = f"You have {total_emails} emails in your inbox. "
        response_text += f"Of these, {important_emails} are marked as important and {action_items} contain action items."

        if important_emails > 0:
            response_text += " I recommend reviewing the important emails first."

        return {
            "response": response_text,
            "type": "email_summary",
            "data": {
                "total_emails": total_emails,
                "important_emails": important_emails,
                "action_items": action_items,
            },
        }

    def _handle_meeting_summary(self, query: str) -> Dict[str, Any]:
        """Handle meeting-related queries"""
        zoom_data = self.data_processor.processed_data.get("zoom", {})

        total_meetings = zoom_data.get("total_meetings", 0)
        upcoming_meetings = len(zoom_data.get("upcoming_meetings", []))
        past_meetings = len(zoom_data.get("past_meetings", []))
        action_items = len(zoom_data.get("action_items", []))

        response_text = f"You have {total_meetings} meetings in your schedule. "
        response_text += (
            f"{upcoming_meetings} are upcoming and {past_meetings} are past meetings. "
        )
        response_text += f"There are {action_items} action items from your meetings."

        if upcoming_meetings > 0:
            response_text += " You should prepare for your upcoming meetings."

        return {
            "response": response_text,
            "type": "meeting_summary",
            "data": {
                "total_meetings": total_meetings,
                "upcoming_meetings": upcoming_meetings,
                "past_meetings": past_meetings,
                "action_items": action_items,
            },
        }

    def _handle_task_summary(self, query: str) -> Dict[str, Any]:
        """Handle task-related queries"""
        asana_data = self.data_processor.processed_data.get("asana", {})

        total_tasks = asana_data.get("total_tasks", 0)
        completed_tasks = len(asana_data.get("completed_tasks", []))
        pending_tasks = len(asana_data.get("pending_tasks", []))
        overdue_tasks = len(asana_data.get("overdue_tasks", []))
        high_priority = len(asana_data.get("high_priority", []))

        response_text = f"You have {total_tasks} tasks total. "
        response_text += f"{completed_tasks} are completed, {pending_tasks} are pending, and {overdue_tasks} are overdue. "
        response_text += f"There are {high_priority} high-priority tasks."

        if overdue_tasks > 0:
            response_text += " You should focus on the overdue tasks first."
        elif high_priority > 0:
            response_text += " Focus on the high-priority tasks."

        return {
            "response": response_text,
            "type": "task_summary",
            "data": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "overdue_tasks": overdue_tasks,
                "high_priority": high_priority,
            },
        }

    def _handle_action_items(self, query: str) -> Dict[str, Any]:
        """Handle action item queries"""
        all_action_items = self.data_processor._consolidate_action_items()

        if not all_action_items:
            return {
                "response": "You don't have any pending action items right now. Great job staying on top of things!",
                "type": "action_items",
                "data": {"action_items": []},
            }

        response_text = f"You have {len(all_action_items)} action items to address:"

        # Group by source
        email_items = [
            item for item in all_action_items if item.get("source") == "email"
        ]
        meeting_items = [
            item for item in all_action_items if item.get("source") == "meeting"
        ]
        task_items = [item for item in all_action_items if item.get("source") == "task"]

        if email_items:
            response_text += f"\n• {len(email_items)} from emails"
        if meeting_items:
            response_text += f"\n• {len(meeting_items)} from meetings"
        if task_items:
            response_text += f"\n• {len(task_items)} pending tasks"

        return {
            "response": response_text,
            "type": "action_items",
            "data": {
                "total_action_items": len(all_action_items),
                "by_source": {
                    "email": len(email_items),
                    "meeting": len(meeting_items),
                    "task": len(task_items),
                },
                "action_items": all_action_items[:5],  # Show first 5
            },
        }

    def _handle_priorities(self, query: str) -> Dict[str, Any]:
        """Handle priority-related queries"""
        priorities = self.data_processor._identify_priorities()

        if not priorities:
            return {
                "response": "You don't have any urgent priorities right now. You're doing great!",
                "type": "priorities",
                "data": {"priorities": []},
            }

        response_text = (
            f"You have {len(priorities)} high-priority items that need attention:"
        )

        overdue_tasks = [p for p in priorities if p.get("type") == "overdue_task"]
        high_priority_tasks = [
            p for p in priorities if p.get("type") == "high_priority_task"
        ]
        urgent_emails = [p for p in priorities if p.get("type") == "urgent_email"]

        if overdue_tasks:
            response_text += f"\n• {len(overdue_tasks)} overdue tasks"
        if high_priority_tasks:
            response_text += f"\n• {len(high_priority_tasks)} high-priority tasks"
        if urgent_emails:
            response_text += f"\n• {len(urgent_emails)} urgent emails"

        return {
            "response": response_text,
            "type": "priorities",
            "data": {
                "total_priorities": len(priorities),
                "by_type": {
                    "overdue_tasks": len(overdue_tasks),
                    "high_priority_tasks": len(high_priority_tasks),
                    "urgent_emails": len(urgent_emails),
                },
                "priorities": priorities[:5],  # Show first 5
            },
        }

    def _handle_deadlines(self, query: str) -> Dict[str, Any]:
        """Handle deadline-related queries"""
        gmail_data = self.data_processor.processed_data.get("gmail", {})
        asana_data = self.data_processor.processed_data.get("asana", {})

        email_deadlines = gmail_data.get("deadlines", [])
        task_deadlines = asana_data.get("deadlines", [])

        total_deadlines = len(email_deadlines) + len(task_deadlines)

        if total_deadlines == 0:
            return {
                "response": "You don't have any specific deadlines mentioned in your emails or tasks.",
                "type": "deadlines",
                "data": {"deadlines": []},
            }

        response_text = f"You have {total_deadlines} items with deadlines:"
        response_text += f"\n• {len(email_deadlines)} mentioned in emails"
        response_text += f"\n• {len(task_deadlines)} tasks with due dates"

        return {
            "response": response_text,
            "type": "deadlines",
            "data": {
                "total_deadlines": total_deadlines,
                "email_deadlines": len(email_deadlines),
                "task_deadlines": len(task_deadlines),
            },
        }

    def _handle_daily_accomplishments(self, query: str) -> Dict[str, Any]:
        """Handle daily accomplishment queries"""
        asana_data = self.data_processor.processed_data.get("asana", {})
        completed_tasks = asana_data.get("completed_tasks", [])

        if not completed_tasks:
            return {
                "response": "You haven't completed any tasks today yet. Let's get started!",
                "type": "daily_accomplishments",
                "data": {"completed_tasks": []},
            }

        response_text = f"Today you've completed {len(completed_tasks)} tasks:"

        # Show completed tasks
        for i, task in enumerate(completed_tasks[:3], 1):
            response_text += f"\n{i}. {task.get('name', 'Unknown task')}"

        if len(completed_tasks) > 3:
            response_text += f"\n... and {len(completed_tasks) - 3} more tasks"

        return {
            "response": response_text,
            "type": "daily_accomplishments",
            "data": {"completed_tasks": len(completed_tasks), "tasks": completed_tasks},
        }

    def _handle_insights(self, query: str) -> Dict[str, Any]:
        """Handle insight and analysis queries"""
        insights = self.data_processor._generate_insights()

        if not insights:
            return {
                "response": "Everything looks good! You're on top of your work.",
                "type": "insights",
                "data": {"insights": []},
            }

        response_text = "Here are some insights from your data:\n"
        for insight in insights:
            response_text += f"• {insight}\n"

        return {
            "response": response_text,
            "type": "insights",
            "data": {"insights": insights},
        }

    def _handle_general_query(self, query: str) -> Dict[str, Any]:
        """Handle general queries"""
        # Create a daily summary
        daily_summary = self.data_processor.create_daily_summary()

        response_text = "Here's a quick overview of your day:\n"
        response_text += f"• {daily_summary.get('email_summary', {}).get('total_emails', 0)} emails\n"
        response_text += f"• {daily_summary.get('meeting_summary', {}).get('total_meetings', 0)} meetings\n"
        response_text += (
            f"• {daily_summary.get('task_summary', {}).get('total_tasks', 0)} tasks\n"
        )
        response_text += (
            f"• {len(daily_summary.get('action_items', []))} action items\n"
        )
        response_text += f"• {len(daily_summary.get('priorities', []))} priorities"

        return {
            "response": response_text,
            "type": "general_summary",
            "data": daily_summary,
        }

    def get_conversation_history(self) -> List[Dict]:
        """Get conversation history"""
        return self.conversation_history

    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        self.logger.info("Conversation history cleared")
