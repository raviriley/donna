from collections import defaultdict

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
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    return creds

def get_events_for_today(calendar_id='primary'):
    """Get events from Google Calendar for today."""
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds, cache_discovery=False)
        today = datetime.date.today()
        start_datetime = datetime.datetime.combine(today, datetime.datetime.min.time()).isoformat() + 'Z'
        end_datetime = datetime.datetime.combine(today, datetime.datetime.max.time()).isoformat() + 'Z'
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_datetime,
            timeMax=end_datetime,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return events
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def get_events_between_dates(start_date, end_date, calendar_id='primary'):
    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds, cache_discovery=False)
        start_datetime = datetime.datetime.combine(start_date, datetime.datetime.min.time()).isoformat() + 'Z'
        end_datetime = datetime.datetime.combine(end_date, datetime.datetime.max.time()).isoformat() + 'Z'
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_datetime,
            timeMax=end_datetime,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        return events
    except HttpError as error:
        print(f"An error occurred: {error}")

def get_busy_schedule(start_date, end_date):
    try: 
        events = get_events_between_dates(start_date, end_date)
        busy = [(e['start'], e['end']) for e in events]
        busy_dict = defaultdict(list)

        for start_time, end_time in busy:
            start_time_str = start_time['dateTime'][11:19]
            end_time_str = end_time['dateTime'][11:19]
            date_str = start_time['dateTime'][0:10]
            busy_dict[date_str].append((start_time_str, end_time_str))

        s = ""
        for date, times in busy_dict.items():
            d = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%A")
            s += f"On {d},{date}:\n ["
            for start_time, end_time in times:
                s += f"  Busy from {start_time} to {end_time}\n"
            s += "] \n"

        return s
    except Exception as e:
        return "Not busy at all"

def create_event(start_date, start_time, end_date, end_time, user_email, user_pno):
    event = {
        "summary": "Dart.cx Demo",
        "location": ZOOMLINK,
        "description": f"Demo for {user_pno}",
        "start": {
            'dateTime': f"{start_date}T{start_time}-07:00",
            'timeZone': 'America/Los_Angeles'
        },
        "end": {
            'dateTime': f"{end_date}T{end_time}-07:00",
            'timeZone': 'America/Los_Angeles'
        },
        "attendees": [{'email': user_email}, {'email': 'saarth@berkeley.edu'}]
    }

    creds = get_credentials()
    try:
        service = build("calendar", "v3", credentials=creds)
        event = service.events().insert(calendarId='primary', body=event).execute()

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    import datetime

    # Assuming get_events_between_dates is a function that retrieves events
    today = datetime.date.today()
    events_for_today = get_events_between_dates(today, today)

    if events_for_today:
        print("Events for today:")
        for event in events_for_today:
            start_time = event['start']['dateTime'][11:19]
            end_time = event['end']['dateTime'][11:19]
            print(f"Event: {event['summary']}, Start: {start_time}, End: {end_time}")
    else:
        print("No events for today.")

if __name__ == "__main__":
    main()
