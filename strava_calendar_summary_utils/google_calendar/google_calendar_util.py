from strava_calendar_summary_data_access_layer import User, UserController

from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# from googleapiclient.errors import HttpError

import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
CALENDAR_NAME = 'Strava Summary'


class GoogleCalendarUtil:
    def __init__(self, calendar_credentials: Credentials, calendar_id: str = None, user: User = None):
        """Init GoogleCalendarUtil for Google Calendar API Calls
        calendar_credentials: the credentials to authenticate each API call with
        calendar_id: the id of the calendar created for this application IF one exists
        user: the User object of the requesting user. If present, updates calendar_credentials on refresh of credentials
        """
        self._calendar_auth = calendar_credentials
        self._calendar_id = calendar_id
        self._user = user

        self._refresh_creds_if_needed()
        self._service = build('calendar', 'v3', credentials=self._calendar_auth)

        if self._calendar_id is None:
            self._calendar_id = self._get_calendar_id_or_create_new_calendar_if_not_exist(CALENDAR_NAME)

    # Get the calendar id for the app calendar.
    def get_calendar_id(self):
        return self._calendar_id

    def _before_each_request(self):
        self._refresh_creds_if_needed()

    def _refresh_creds_if_needed(self):
        if self._calendar_auth and self._calendar_auth.refresh_token:
            self._calendar_auth.refresh(Request())

    def _get_calendar_id_or_create_new_calendar_if_not_exist(self, calendar_name):
        self._before_each_request()

        page_token = None
        while True:
            calendar_list = self._service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry['summary'] == calendar_name:
                    return calendar_list_entry['id']

            calendar = {
                'kind': 'calendar#calendar',
                'summary': calendar_name
            }

            created_calendar = self._service.calendars().insert(body=calendar).execute()
            return created_calendar['id']

    def add_all_day_event(self, name: str, description: str, date: str):
        self.add_event(name, description, date, date)

    def add_event(self, name: str, description: str, start: str, end: str):
        event_date_type = ''  # date = all day, dateTime = specific start and end time
        if end is None and len(start) == 10:
            event_date_type = 'date'
        elif len(start) == 19 and len(end) == 19:
            event_date_type = 'dateTime'
        else:
            return -1

        event_body = {
            'summary': name,
            'description': description,
            'start': {
                event_date_type: start,
                'timeZone': 'GMT'
            },
            'end': {
                event_date_type: end,
                'timeZone': 'GMT'
            }
        }

        event = self._service.events().insert(event_body).execute()
        return event.get('id')
