"""
API integration functions for GlassDesk

See docs/mock_data_guidelines.md for information about mock data usage and transition plans.
During development, these functions may be replaced with mock data calls.
"""

import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def fetch_gmail_messages(creds: Credentials, max_results=10):
    service = build("gmail", "v1", credentials=creds)
    results = (
        service.users().messages().list(userId="me", maxResults=max_results).execute()
    )
    messages = results.get("messages", [])
    fetched_messages = []
    for msg in messages:
        msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()
        fetched_messages.append(msg_data)
    return fetched_messages


def fetch_zoom_meetings(token, user_id, page_size=30):
    url = f"https://api.zoom.us/v2/users/{user_id}/recordings?page_size={page_size}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("meetings", [])
    else:
        raise Exception(f"Zoom API error: {response.status_code} - {response.text}")


def fetch_asana_tasks(token, workspace_id, project_id):
    url = f"https://app.asana.com/api/1.0/projects/{project_id}/tasks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"workspace": workspace_id, "opt_fields": "name,completed,assignee,status"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        raise Exception(f"Asana API error: {response.status_code} - {response.text}")
