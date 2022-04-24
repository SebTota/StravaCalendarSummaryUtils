from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

class GoogleCalendarUtil():
    def __init__(self, calendar_auth):
        self.calendar_auth = calendar_auth
        # self.service = build('calendar', 'v3', credentials=creds)



