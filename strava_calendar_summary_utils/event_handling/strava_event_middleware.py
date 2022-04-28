from strava_calendar_summary_data_access_layer import StravaEvent

from google.cloud import pubsub_v1
import os
import json

STRAVA_EVENT_PUB_SUB_TOPIC = 'StravaCalendarSummaryStravaWebhookEvents'


class StravaEventMiddleware():

    def __init__(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_name = 'projects/{project_id}/topics/{topic}'.format(
            project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
            topic=STRAVA_EVENT_PUB_SUB_TOPIC,
        )

    def publish_strava_event(self, new_event: StravaEvent):
        self.publisher.publish(self.topic_name, json.dumps(new_event.to_dict()).encode('utf-8'))
