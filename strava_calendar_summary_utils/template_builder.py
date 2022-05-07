from stravalib import unithelper
from stravalib.model import Activity


class TemplateBuilder:

    @staticmethod
    def _value_dict(activity: Activity):
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

    @staticmethod
    def fill_template(template: str, activity: Activity):
        filled_template = template
        vals = TemplateBuilder._value_dict(activity)
        for k, v in vals.items():
            filled_template = filled_template.replace('{' + k + '}', v)

        filled_template = filled_template.replace('\\{', '{').replace('\\}', '}')
        return filled_template
