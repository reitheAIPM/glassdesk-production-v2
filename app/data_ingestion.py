"""
Data normalization functions for GlassDesk

See docs/mock_data_guidelines.md for information about mock data usage and transition plans.
"""


def normalize_gmail_message(msg):
    headers = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    return {
        "id": msg.get("id"),
        "threadId": msg.get("threadId"),
        "subject": headers.get("Subject", ""),
        "from": headers.get("From", ""),
        "to": headers.get("To", ""),
        "date": headers.get("Date", ""),
        "snippet": msg.get("snippet", ""),
        "body": extract_body(msg.get("payload", {})),
    }


def extract_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    import base64

                    return base64.urlsafe_b64decode(data).decode("utf-8")
    return ""


def normalize_zoom_meeting(meeting):
    return {
        "id": meeting.get("id"),
        "topic": meeting.get("topic"),
        "start_time": meeting.get("start_time"),
        "duration": meeting.get("duration"),
        "recording_files": meeting.get("recording_files", []),
    }


def normalize_asana_task(task):
    return {
        "id": task.get("gid"),
        "name": task.get("name"),
        "completed": task.get("completed"),
        "assignee": (
            task.get("assignee", {}).get("name") if task.get("assignee") else None
        ),
        "status": task.get("status") if "status" in task else None,
    }
