import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]


def get_credentials():
    """Retrieve and refresh Google API credentials."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    return creds


def get_events_for_today(calendar_id="primary"):
    """Get events from Google Calendar for today."""
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds, cache_discovery=False)
        today = datetime.date.today()
        start_datetime = (
            datetime.datetime.combine(today, datetime.datetime.min.time()).isoformat()
            + "Z"
        )
        end_datetime = (
            datetime.datetime.combine(today, datetime.datetime.max.time()).isoformat()
            + "Z"
        )
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=start_datetime,
                timeMax=end_datetime,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        return events
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
