from strava_calendar_summary_data_access_layer import User, UserController

from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import datetime
import logging

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
            self._calendar_id = self._create_app_calendar(CALENDAR_NAME)
            self._save_app_calendar_id(self._calendar_id)

    # Get the calendar id for the app calendar.
    def get_calendar_id(self):
        return self._calendar_id

    def _before_each_request(self):
        self._refresh_creds_if_needed()

    def _refresh_creds_if_needed(self):
        if self._calendar_auth and self._calendar_auth.refresh_token:
            self._calendar_auth.refresh(Request())

    def _create_app_calendar(self, calendar_name):
        self._before_each_request()

        calendar = {
            'kind': 'calendar#calendar',
            'summary': calendar_name
        }

        created_calendar_id = self._service.calendars().insert(body=calendar).execute()['id']
        return created_calendar_id

    def _save_app_calendar_id(self, calendar_id: int):
        if self._user is not None and self._user.calendar_id != calendar_id:
            self._user.calendar_id = calendar_id
            UserController().update(self._user.user_id, self._user)
            logging.info('Saved app calendar: {} for user: {}'.format(calendar_id, self._user.user_id))

    def add_all_day_event(self, name: str, description: str, timezone: str, date: str):
        return self.add_event(name, description, timezone, date, date)

    def add_event(self, name: str, description: str, timezone: str, start: str, end: str):

        event_body = {
            'summary': name,
            'description': description,
            'start': {
                'timeZone': timezone
            },
            'end': {
                'timeZone': timezone
            }
        }

        if len(start) == 10 and len(end) == 10:
            event_body['start']['date'] = start
            event_body['end']['date'] = end
        elif len(start) == 19 and len(end) == 19:
            event_body['start']['dateTime'] = start
            event_body['end']['dateTime'] = end
        else:
            return -1

        event = self._service.events().insert(calendarId=self._calendar_id, body=event_body).execute()
        return event.get('id')
