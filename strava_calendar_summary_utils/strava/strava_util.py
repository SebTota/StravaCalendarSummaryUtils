from ..config import STRAVA_API
from strava_calendar_summary_data_access_layer import User, UserController
from stravalib.client import Client
from stravalib.model import Athlete, Activity

from typing import List


import time

class StravaUtil:
    def __init__(self, user: User):
        self.user = user
        self.init_strava_client()
        
    def init_strava_client(self):
        self.client = Client()
        self.client.access_token = self.user.strava_auth.access_token
        self.client.refresh_token = self.user.strava_auth.refresh_token
        self.client.token_expires_at = self.user.strava_auth.expiry_date

    def before_api_call(self) -> None:
        self.update_access_token_if_necessary()

    def update_access_token_if_necessary(self) -> None:
        if time.time() > self.client.token_expires_at:
            refresh_response = self.client.refresh_access_token(
                client_id=STRAVA_API['STRAVA_CLIENT_ID'], 
                client_secret=STRAVA_API['STRAVA_CLIENT_SECRET'],
                refresh_token=self.client.refresh_token)

            self.user.strava_auth.access_token = refresh_response['access_token']
            self.user.strava_auth.refresh_token = refresh_response['refresh_token']
            self.user.strava_auth.expiry_date = refresh_response['expires_at']
            UserController().update(self.user.id, self.user)

    def get_athlete(self) -> Athlete:
        self.before_api_call()
        return self.client.get_athlete()

    def get_activities(self, before=None, after=None, limit=None) -> List[Activity]:
        self.before_api_call()
        return self.client.get_activities(before, after, limit)

    def get_activity(self, activity_id) -> Activity:
        self.before_api_call()
        return self.client.get_activity(activity_id=activity_id)
