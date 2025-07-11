"""
User Communication Module for GlassDesk
Provides simple, non-technical messages for users who are not developers
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime


class UserCommunicator:
    """Handles all user-facing communication with simple, non-technical language"""

    def __init__(self):
        self.logger = logging.getLogger("glassdesk.user_communication")

        # Predefined user-friendly messages
        self.status_messages = {
            # Connection status
            "connecting_email": "Connecting to your email...",
            "connecting_zoom": "Connecting to your Zoom account...",
            "connecting_asana": "Connecting to your Asana workspace...",
            "connecting_database": "Setting up your data storage...",
            # Processing status
            "processing_emails": "Reading your emails...",
            "processing_meetings": "Getting your meeting information...",
            "processing_tasks": "Collecting your task data...",
            "processing_data": "Organizing your information...",
            # Completion status
            "emails_complete": "✅ Your emails have been processed successfully",
            "meetings_complete": "✅ Your meeting data is ready",
            "tasks_complete": "✅ Your task information has been collected",
            "all_complete": "🎉 All done! Your data is organized and ready for analysis",
            # Error status
            "email_error": "I'm having trouble accessing your email, but I'll keep trying",
            "zoom_error": "There's an issue with your Zoom connection, but I'm working on it",
            "asana_error": "I'm having trouble with your Asana data, but I'll try again",
            "database_error": "There's a storage issue, but I'm trying to fix it automatically",
            "general_error": "Something went wrong, but I'm working to fix it automatically",
            # Progress messages
            "progress_template": "Processing... ({current} of {total} complete)",
            "retrying": "Trying again...",
            "fixing_automatically": "I found an issue and I'm fixing it automatically...",
            # Setup messages
            "setup_start": "Setting up GlassDesk for you...",
            "setup_config": "Checking your settings...",
            "setup_database": "Preparing your data storage...",
            "setup_complete": "Setup complete! You're ready to go.",
            # Health check messages
            "health_check": "Checking everything is working properly...",
            "health_good": "Everything looks good!",
            "health_issues": "I found some issues, but I'm fixing them automatically...",
        }

    def get_status_message(self, key: str, **kwargs) -> str:
        """Get a user-friendly status message"""
        message = self.status_messages.get(key, "Working on it...")

        # Replace template variables
        if kwargs:
            message = message.format(**kwargs)

        # Log the message for AI debugging
        self.logger.info(f"User message: {key} -> {message}")

        return message

    def log_operation_start(self, operation: str, user_context: Dict[str, Any] = None):
        """Log the start of an operation with user-friendly context"""
        self.logger.info(
            f"Operation started: {operation}",
            extra={
                "operation": operation,
                "user_context": user_context or {},
                "timestamp": datetime.now().isoformat(),
            },
        )

    def log_operation_progress(self, operation: str, progress: Dict[str, Any]):
        """Log operation progress with user-friendly updates"""
        current = progress.get("current", 0)
        total = progress.get("total", 0)

        if total > 0:
            percentage = (current / total) * 100
            message = self.get_status_message(
                "progress_template", current=current, total=total
            )
        else:
            message = self.get_status_message(f"{operation}_progress")

        self.logger.info(
            f"Operation progress: {operation} - {current}/{total}",
            extra={
                "operation": operation,
                "progress": progress,
                "user_message": message,
            },
        )

        return message

    def log_operation_complete(self, operation: str, result: Dict[str, Any] = None):
        """Log operation completion with success message"""
        message = self.get_status_message(f"{operation}_complete")

        self.logger.info(
            f"Operation completed: {operation}",
            extra={
                "operation": operation,
                "result": result or {},
                "user_message": message,
            },
        )

        return message

    def log_operation_error(
        self, operation: str, error: Exception, auto_fix_attempted: bool = False
    ) -> str:
        """Log operation error with user-friendly message"""
        # Get appropriate error message
        error_key = f"{operation}_error"
        if error_key not in self.status_messages:
            error_key = "general_error"

        message = self.get_status_message(error_key)

        if auto_fix_attempted:
            message += " " + self.get_status_message("fixing_automatically")

        # Log detailed error for AI debugging
        self.logger.error(
            f"Operation failed: {operation}",
            extra={
                "operation": operation,
                "error_type": type(error).__name__,
                "error_message": str(error),
                "auto_fix_attempted": auto_fix_attempted,
                "user_message": message,
            },
        )

        return message

    def notify_user(self, message: str, level: str = "info"):
        """Send a notification to the user"""
        # Log the notification
        self.logger.info(
            f"User notification: {message}",
            extra={"notification_level": level, "user_message": message},
        )

        return message

    def get_system_status(self) -> Dict[str, Any]:
        """Get a user-friendly system status report"""
        # This would integrate with actual system health checks
        status = {
            "database": "Connected",
            "email_service": "Ready",
            "meeting_service": "Ready",
            "task_service": "Ready",
            "overall_status": "All systems operational",
        }

        return status

    def format_error_for_user(self, technical_error: str) -> str:
        """Convert technical error messages to user-friendly language"""
        # Common error patterns and their user-friendly translations
        error_translations = {
            "connection refused": "I'm having trouble connecting to the service",
            "timeout": "The connection is taking longer than expected",
            "authentication failed": "I need to check your login credentials",
            "permission denied": "I don't have the right permissions to access this",
            "not found": "I couldn't find the information you're looking for",
            "rate limit": "I'm making too many requests, let me slow down",
            "invalid token": "Your login session has expired",
            "database error": "There's an issue with data storage",
            "api error": "There's a problem with one of the services I'm using",
        }

        # Find the most appropriate translation
        for pattern, translation in error_translations.items():
            if pattern.lower() in technical_error.lower():
                return translation

        # Default user-friendly message
        return "Something went wrong, but I'm working to fix it"


# Global user communicator instance
user_comm = UserCommunicator()
