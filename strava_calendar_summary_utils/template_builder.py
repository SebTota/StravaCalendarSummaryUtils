from stravalib import unithelper
from stravalib.model import Activity
from typing import List
import re
from collections import defaultdict

DEFAULT_TITLE_TEMPLATE = '{distance_miles} mile {type}'
DEFAULT_PER_RUN_SUMMARY_TEMPLATE = 'Distance: {distance_miles} mile(s)\nDuration: {duration}'

VALID_DEFAULT_TEMPLATE_KEYS = ['name', 'description', 'type', 'distance_miles', 'distance_kilometers',
                               'distance_meters', 'calories', 'start_date', 'start_time', 'duration', 'end_time',
                               'total_elevation_gain', 'elev_high', 'elev_low', 'average_speed_meters_per_second',
                               'average_speed_kilometers_per_hour', 'average_speed_miles_per_hour',
                               'max_speed_meters_per_second', 'max_kilometers_per_hour', 'max_miles_per_hour',
                               'kilojoules', 'average_watts', 'max_watts']


def _value_dict(activity: Activity) -> dict:
    return {
        'name': str(activity.name),
        'description': str(activity.description),
        'type': str(activity.type),
        'distance_miles': str(unithelper.miles(activity.distance)),
        'distance_kilometers': str(unithelper.kilometers(activity.distance)),
        'distance_meters': str(unithelper.meters(activity.distance)),
        'calories': str(activity.calories),
        'start_date': str(activity.start_date_local.date()),
        'start_time': str(activity.start_date_local.time()),
        'duration': str(activity.moving_time),
        'end_time': str(activity.start_date_local + activity.moving_time),
        'total_elevation_gain': str(activity.total_elevation_gain),
        'elev_high': str(activity.elev_high),
        'elev_low': str(activity.elev_low),
        'average_speed_meters_per_second': str(unithelper.meters_per_second(activity.average_speed)),
        'average_speed_kilometers_per_hour': str(unithelper.kilometers_per_hour(activity.average_speed)),
        'average_speed_miles_per_hour': str(unithelper.miles_per_hour(activity.average_speed)),
        'max_speed_meters_per_second': str(unithelper.meters_per_second(activity.max_speed)),
        'max_kilometers_per_hour': str(unithelper.kilometers_per_hour(activity.max_speed)),
        'max_miles_per_hour': str(unithelper.miles_per_hour(activity.max_speed)),
        'kilojoules': str(activity.kilojoules),  # Rides only
        'average_watts': str(activity.average_watts),  # Rides only
        'max_watts': str(activity.max_watts)
    }


def fill_template(template: str, activity: Activity) -> str:
    filled_template: str = template
    vals: dict = _value_dict(activity)
    for k, v in vals.items():
        filled_template = filled_template.replace('{' + k + '}', v)

    filled_template = filled_template.replace('\\{', '{').replace('\\}', '}')
    return filled_template


def verify_template(template: str) -> list:
    """
    Verify the template configuration returning any invalid template keys
    :param template: the template to verify
    :return: a list of invalid template keys if there are any
    """

    temp_keys = re.findall(r'{[a-zA-Z_. ]*}', template)
    found_keys = map(lambda k: k.replace('{', '').replace('}', '').strip(), temp_keys)
    invalid_keys = []

    for key in found_keys:
        if key not in VALID_DEFAULT_TEMPLATE_KEYS:
            invalid_keys.append(key)

    return invalid_keys
