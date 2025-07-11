"""
Data Processor for GlassDesk
Handles processing of mock data from Gmail, Zoom, and Asana
"""

import logging
from typing import Dict, List, Any
from datetime import datetime
from .user_communication import user_comm
from .logging_config import log_api_error


class DataProcessor:
    """Processes and organizes data from various sources"""

    def __init__(self):
        self.logger = logging.getLogger("glassdesk.data_processor")
        self.processed_data = {}
        self.user_comm = user_comm

    def process_gmail_data(self, emails: List[Dict]) -> Dict[str, Any]:
        """Process Gmail data and extract key information"""
        try:
            self.logger.info(f"Processing {len(emails)} emails")

            processed_emails = {
                "total_emails": len(emails),
                "important_emails": [],
                "action_items": [],
                "meetings": [],
                "deadlines": [],
                "categories": {
                    "work": [],
                    "personal": [],
                    "urgent": [],
                    "follow_up": [],
                },
            }

            for email in emails:
                # Extract key information
                email_data = self._extract_email_info(email)

                # Categorize email
                category = self._categorize_email(email_data)
                processed_emails["categories"][category].append(email_data)

                # Extract action items
                action_items = self._extract_action_items(email_data)
                processed_emails["action_items"].extend(action_items)

                # Extract meeting information
                if self._is_meeting_related(email_data):
                    processed_emails["meetings"].append(email_data)

                # Extract deadlines
                deadlines = self._extract_deadlines(email_data)
                processed_emails["deadlines"].extend(deadlines)

                # Mark important emails
                if self._is_important(email_data):
                    processed_emails["important_emails"].append(email_data)

            self.processed_data["gmail"] = processed_emails
            self.user_comm.notify_user(
                "Email processing completed successfully", level="info"
            )
            return processed_emails

        except Exception as e:
            log_api_error("process_gmail_data", e, {"email_count": len(emails)})
            self.user_comm.log_operation_error("process_gmail_data", e)
            return {}

    def process_zoom_data(self, meetings: List[Dict]) -> Dict[str, Any]:
        """Process Zoom meeting data and extract key information"""
        try:
            self.logger.info(f"Processing {len(meetings)} meetings")

            processed_meetings = {
                "total_meetings": len(meetings),
                "meeting_summaries": [],
                "action_items": [],
                "decisions": [],
                "participants": set(),
                "upcoming_meetings": [],
                "past_meetings": [],
            }

            for meeting in meetings:
                # Extract meeting information
                meeting_data = self._extract_meeting_info(meeting)

                # Categorize by time
                if self._is_upcoming(meeting_data):
                    processed_meetings["upcoming_meetings"].append(meeting_data)
                else:
                    processed_meetings["past_meetings"].append(meeting_data)

                # Extract action items from meeting
                action_items = self._extract_meeting_action_items(meeting_data)
                processed_meetings["action_items"].extend(action_items)

                # Extract decisions
                decisions = self._extract_decisions(meeting_data)
                processed_meetings["decisions"].extend(decisions)

                # Track participants
                if "participants" in meeting_data:
                    processed_meetings["participants"].update(
                        meeting_data["participants"]
                    )

                # Create meeting summary
                summary = self._create_meeting_summary(meeting_data)
                processed_meetings["meeting_summaries"].append(summary)

            # Convert set to list for JSON serialization
            processed_meetings["participants"] = list(
                processed_meetings["participants"]
            )

            self.processed_data["zoom"] = processed_meetings
            self.user_comm.notify_user(
                "Meeting processing completed successfully", level="info"
            )
            return processed_meetings

        except Exception as e:
            log_api_error("process_zoom_data", e, {"meeting_count": len(meetings)})
            self.user_comm.log_operation_error("process_zoom_data", e)
            return {}

    def process_asana_data(self, tasks: List[Dict]) -> Dict[str, Any]:
        """Process Asana task data and extract key information"""
        try:
            self.logger.info(f"Processing {len(tasks)} tasks")

            processed_tasks = {
                "total_tasks": len(tasks),
                "completed_tasks": [],
                "pending_tasks": [],
                "overdue_tasks": [],
                "high_priority": [],
                "projects": {},
                "deadlines": [],
                "assignees": set(),
            }

            for task in tasks:
                # Extract task information
                task_data = self._extract_task_info(task)

                # Categorize by status
                if task_data.get("completed"):
                    processed_tasks["completed_tasks"].append(task_data)
                elif self._is_overdue(task_data):
                    processed_tasks["overdue_tasks"].append(task_data)
                else:
                    processed_tasks["pending_tasks"].append(task_data)

                # Track priority
                if task_data.get("priority") == "high":
                    processed_tasks["high_priority"].append(task_data)

                # Group by project
                project = task_data.get("project", "Unassigned")
                if project not in processed_tasks["projects"]:
                    processed_tasks["projects"][project] = []
                processed_tasks["projects"][project].append(task_data)

                # Track deadlines
                if task_data.get("due_date"):
                    processed_tasks["deadlines"].append(task_data)

                # Track assignees
                if task_data.get("assignee"):
                    processed_tasks["assignees"].add(task_data["assignee"])

            # Convert set to list for JSON serialization
            processed_tasks["assignees"] = list(processed_tasks["assignees"])

            self.processed_data["asana"] = processed_tasks
            self.user_comm.notify_user(
                "Task processing completed successfully", level="info"
            )
            return processed_tasks

        except Exception as e:
            log_api_error("process_asana_data", e, {"task_count": len(tasks)})
            self.user_comm.log_operation_error("process_asana_data", e)
            return {}

    def create_daily_summary(self) -> Dict[str, Any]:
        """Create a comprehensive daily summary from all processed data"""
        try:
            self.logger.info("Creating daily summary")

            summary = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "email_summary": self._summarize_emails(),
                "meeting_summary": self._summarize_meetings(),
                "task_summary": self._summarize_tasks(),
                "action_items": self._consolidate_action_items(),
                "priorities": self._identify_priorities(),
                "insights": self._generate_insights(),
            }

            self.user_comm.notify_user(
                "Daily summary created successfully", level="info"
            )
            return summary

        except Exception as e:
            log_api_error("create_daily_summary", e, {})
            self.user_comm.log_operation_error("create_daily_summary", e)
            return {}

    # Helper methods for data extraction and categorization
    def _extract_email_info(self, email: Dict) -> Dict[str, Any]:
        """Extract key information from email"""
        return {
            "id": email.get("id"),
            "subject": email.get("subject", ""),
            "sender": email.get("from", ""),
            "recipients": email.get("to", []),
            "date": email.get("date"),
            "body": email.get("body", ""),
            "labels": email.get("labels", []),
            "thread_id": email.get("thread_id"),
        }

    def _categorize_email(self, email_data: Dict) -> str:
        """Categorize email based on content and metadata"""
        subject = email_data.get("subject", "").lower()
        body = email_data.get("body", "").lower()

        # Simple categorization logic
        if any(word in subject for word in ["urgent", "asap", "important"]):
            return "urgent"
        elif any(word in subject for word in ["meeting", "call", "zoom"]):
            return "work"
        elif any(word in body for word in ["follow up", "reminder", "check"]):
            return "follow_up"
        else:
            return "work"  # Default to work

    def _extract_action_items(self, email_data: Dict) -> List[Dict]:
        """Extract action items from email content"""
        action_items = []
        body = email_data.get("body", "")

        # Simple action item extraction
        action_keywords = ["please", "need to", "should", "must", "action required"]
        sentences = body.split(".")

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in action_keywords):
                action_items.append(
                    {
                        "source": "email",
                        "content": sentence.strip(),
                        "email_subject": email_data.get("subject"),
                        "date": email_data.get("date"),
                    }
                )

        return action_items

    def _is_meeting_related(self, email_data: Dict) -> bool:
        """Check if email is meeting-related"""
        subject = email_data.get("subject", "").lower()
        meeting_keywords = ["meeting", "call", "zoom", "teams", "calendar"]
        return any(keyword in subject for keyword in meeting_keywords)

    def _extract_deadlines(self, email_data: Dict) -> List[Dict]:
        """Extract deadlines from email content"""
        deadlines = []
        body = email_data.get("body", "")

        # Simple deadline extraction
        deadline_keywords = ["deadline", "due", "by", "end of"]
        sentences = body.split(".")

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in deadline_keywords):
                deadlines.append(
                    {
                        "source": "email",
                        "content": sentence.strip(),
                        "email_subject": email_data.get("subject"),
                        "date": email_data.get("date"),
                    }
                )

        return deadlines

    def _is_important(self, email_data: Dict) -> bool:
        """Determine if email is important"""
        subject = email_data.get("subject", "").lower()
        important_keywords = ["urgent", "important", "asap", "critical"]
        return any(keyword in subject for keyword in important_keywords)

    def _extract_meeting_info(self, meeting: Dict) -> Dict[str, Any]:
        """Extract key information from meeting"""
        return {
            "id": meeting.get("id"),
            "topic": meeting.get("topic", ""),
            "start_time": meeting.get("start_time"),
            "end_time": meeting.get("end_time"),
            "participants": meeting.get("participants", []),
            "transcript": meeting.get("transcript", ""),
            "summary": meeting.get("summary", ""),
            "action_items": meeting.get("action_items", []),
        }

    def _is_upcoming(self, meeting_data: Dict) -> bool:
        """Check if meeting is upcoming"""
        start_time = meeting_data.get("start_time")
        if not start_time:
            return False

        try:
            meeting_date = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
            return meeting_date > datetime.now()
        except (ValueError, TypeError):
            return False

    def _extract_meeting_action_items(self, meeting_data: Dict) -> List[Dict]:
        """Extract action items from meeting"""
        action_items = meeting_data.get("action_items", [])
        return [
            {
                "source": "meeting",
                "content": item,
                "meeting_topic": meeting_data.get("topic"),
            }
            for item in action_items
        ]

    def _extract_decisions(self, meeting_data: Dict) -> List[Dict]:
        """Extract decisions from meeting"""
        transcript = meeting_data.get("transcript", "")
        decisions = []

        # Simple decision extraction
        decision_keywords = ["decided", "agreed", "concluded", "resolved"]
        sentences = transcript.split(".")

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in decision_keywords):
                decisions.append(
                    {
                        "source": "meeting",
                        "content": sentence.strip(),
                        "meeting_topic": meeting_data.get("topic"),
                    }
                )

        return decisions

    def _create_meeting_summary(self, meeting_data: Dict) -> Dict[str, Any]:
        """Create meeting summary"""
        return {
            "topic": meeting_data.get("topic"),
            "date": meeting_data.get("start_time"),
            "participants": meeting_data.get("participants", []),
            "summary": meeting_data.get("summary", ""),
            "action_items": meeting_data.get("action_items", []),
        }

    def _extract_task_info(self, task: Dict) -> Dict[str, Any]:
        """Extract key information from task"""
        return {
            "id": task.get("id"),
            "name": task.get("name", ""),
            "description": task.get("description", ""),
            "status": task.get("status", ""),
            "completed": task.get("completed", False),
            "due_date": task.get("due_date"),
            "priority": task.get("priority", "medium"),
            "project": task.get("project", ""),
            "assignee": task.get("assignee", ""),
            "tags": task.get("tags", []),
        }

    def _is_overdue(self, task_data: Dict) -> bool:
        """Check if task is overdue"""
        due_date = task_data.get("due_date")
        if not due_date or task_data.get("completed"):
            return False

        try:
            task_due = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            return task_due < datetime.now()
        except (ValueError, TypeError):
            return False

    def _summarize_emails(self) -> Dict[str, Any]:
        """Create email summary"""
        gmail_data = self.processed_data.get("gmail", {})
        return {
            "total_emails": gmail_data.get("total_emails", 0),
            "important_emails": len(gmail_data.get("important_emails", [])),
            "action_items": len(gmail_data.get("action_items", [])),
            "categories": {
                k: len(v) for k, v in gmail_data.get("categories", {}).items()
            },
        }

    def _summarize_meetings(self) -> Dict[str, Any]:
        """Create meeting summary"""
        zoom_data = self.processed_data.get("zoom", {})
        return {
            "total_meetings": zoom_data.get("total_meetings", 0),
            "upcoming_meetings": len(zoom_data.get("upcoming_meetings", [])),
            "past_meetings": len(zoom_data.get("past_meetings", [])),
            "action_items": len(zoom_data.get("action_items", [])),
            "decisions": len(zoom_data.get("decisions", [])),
        }

    def _summarize_tasks(self) -> Dict[str, Any]:
        """Create task summary"""
        asana_data = self.processed_data.get("asana", {})
        return {
            "total_tasks": asana_data.get("total_tasks", 0),
            "completed_tasks": len(asana_data.get("completed_tasks", [])),
            "pending_tasks": len(asana_data.get("pending_tasks", [])),
            "overdue_tasks": len(asana_data.get("overdue_tasks", [])),
            "high_priority": len(asana_data.get("high_priority", [])),
            "projects": len(asana_data.get("projects", {})),
        }

    def _consolidate_action_items(self) -> List[Dict]:
        """Consolidate action items from all sources"""
        all_action_items = []

        # From emails
        gmail_data = self.processed_data.get("gmail", {})
        all_action_items.extend(gmail_data.get("action_items", []))

        # From meetings
        zoom_data = self.processed_data.get("zoom", {})
        all_action_items.extend(zoom_data.get("action_items", []))

        # From tasks (pending tasks are action items)
        asana_data = self.processed_data.get("asana", {})
        for task in asana_data.get("pending_tasks", []):
            all_action_items.append(
                {
                    "source": "task",
                    "content": f"Complete: {task.get('name')}",
                    "due_date": task.get("due_date"),
                    "priority": task.get("priority"),
                }
            )

        return all_action_items

    def _identify_priorities(self) -> List[Dict]:
        """Identify high-priority items"""
        priorities = []

        # Overdue tasks
        asana_data = self.processed_data.get("asana", {})
        for task in asana_data.get("overdue_tasks", []):
            priorities.append(
                {
                    "type": "overdue_task",
                    "content": task.get("name"),
                    "priority": "high",
                }
            )

        # High priority tasks
        for task in asana_data.get("high_priority", []):
            priorities.append(
                {
                    "type": "high_priority_task",
                    "content": task.get("name"),
                    "priority": "high",
                }
            )

        # Urgent emails
        gmail_data = self.processed_data.get("gmail", {})
        for email in gmail_data.get("important_emails", []):
            priorities.append(
                {
                    "type": "urgent_email",
                    "content": email.get("subject"),
                    "priority": "high",
                }
            )

        return priorities

    def _generate_insights(self) -> List[str]:
        """Generate insights from processed data"""
        insights = []

        # Task insights
        asana_data = self.processed_data.get("asana", {})
        overdue_count = len(asana_data.get("overdue_tasks", []))
        if overdue_count > 0:
            insights.append(
                f"You have {overdue_count} overdue tasks that need attention"
            )

        # Meeting insights
        zoom_data = self.processed_data.get("zoom", {})
        upcoming_count = len(zoom_data.get("upcoming_meetings", []))
        if upcoming_count > 0:
            insights.append(f"You have {upcoming_count} upcoming meetings today")

        # Email insights
        gmail_data = self.processed_data.get("gmail", {})
        important_count = len(gmail_data.get("important_emails", []))
        if important_count > 0:
            insights.append(f"You have {important_count} important emails to review")

        return insights
