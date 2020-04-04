import os.path
import os.path
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarHandler:
    def create_event(self, calendar_id, start_time, end_time, subject, notes, guest_emails):
        service = self._get_authenticated_service()
        event = self._get_event_dict(start_time, end_time, subject, notes, guest_emails)
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        return event

    def _get_authenticated_service(self):
        credentials = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                credentials = pickle.load(token)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(credentials, token)
        return build('calendar', 'v3', credentials=credentials)

    def _get_event_dict(self, start_time, end_time, subject, notes, guest_emails):
        event = {
            'summary': subject,
            'description': notes,
            'start': {
                'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S+05:30'),
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [{'email': email} for email in guest_emails]
        }
        return event
