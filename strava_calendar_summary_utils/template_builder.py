from stravalib import unithelper
from stravalib.model import Activity
import re
import logging
import time

VALID_DEFAULT_TEMPLATE_KEYS = ['name', 'description', 'type', 'distance_miles', 'distance_kilometers',
                               'distance_meters', 'calories', 'start_date', 'start_time', 'duration', 'end_time',
                               'total_elevation_gain_feet', 'total_elevation_gain_meters', 'elev_high_feet',
                               'elev_low_feet', 'elev_high_meters', 'elev_low_meters',
                               'average_speed_meters_per_second', 'average_speed_kilometers_per_hour',
                               'average_speed_miles_per_hour', 'max_speed_meters_per_second',
                               'max_speed_kilometers_per_hour', 'max_speed_miles_per_hour', 'kilojoules',
                               'average_watts', 'max_watts', 'pace_min_per_mile', 'pace_min_per_km']


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
        'end_time': str((activity.start_date_local + activity.moving_time).time()),
        'total_elevation_gain_feet': str(unithelper.feet(activity.total_elevation_gain)),
        'total_elevation_gain_meters': str(unithelper.meters(activity.total_elevation_gain)),
        'elev_high_feet': str(unithelper.feet(activity.elev_high)),
        'elev_low_feet': str(unithelper.feet(activity.elev_low)),
        'elev_high_meters': str(unithelper.meters(activity.elev_high)),
        'elev_low_meters': str(unithelper.meters(activity.elev_low)),
        'average_speed_meters_per_second': str(unithelper.meters_per_second(activity.average_speed)),
        'average_speed_kilometers_per_hour': str(unithelper.kilometers_per_hour(activity.average_speed)),
        'average_speed_miles_per_hour': str(unithelper.miles_per_hour(activity.average_speed)),
        'max_speed_meters_per_second': str(unithelper.meters_per_second(activity.max_speed)),
        'max_speed_kilometers_per_hour': str(unithelper.kilometers_per_hour(activity.max_speed)),
        'max_speed_miles_per_hour': str(unithelper.miles_per_hour(activity.max_speed)),
        'kilojoules': str(activity.kilojoules),  # Rides only
        'average_watts': str(activity.average_watts),  # Rides only
        'max_watts': str(activity.max_watts),
        'pace_min_per_mile': time.strftime('%M:%S', time.gmtime(
            activity.moving_time.total_seconds() / float(unithelper.miles(activity.distance)))),
        'pace_min_per_km': time.strftime('%M:%S', time.gmtime(
            activity.moving_time.total_seconds() / float(unithelper.kilometers(activity.distance))))
    }


def fill_template(template: str, activity: Activity) -> str:
    """
    Fill a template with the details from an activity
    :param template: the template to fill
    :param activity: the activity to pull information for the activity for
    :return: the filled template
    """

    filled_template: str = template
    vals: dict = _value_dict(activity)
    temp_keys = re.findall(r'{[a-zA-Z_. ]*}', filled_template)
    found_keys = map(lambda k: k.replace('{', '').replace('}', '').strip(), temp_keys)

    for key in found_keys:
        if key in vals:
            filled_template = re.sub(r'{ *' + key + ' *}', vals[key], filled_template)
        else:
            # Log error with key, but do not throw an exception so the template is still built
            logging.error('Failed to find key : {} while building template for activity: {}'.format(key, activity.id))

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
