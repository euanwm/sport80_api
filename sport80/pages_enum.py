""" Throw all the endpoint strings in here """
import enum


class EndPoint(enum.Enum):
    """ As mentioned before... """
    EVENT_INDEX = "event_results?id_ranking=8"
    EVENT_RESULTS = f"{EVENT_INDEX}&resource="
    UPCOMING_EVENTS = "events"
    START_LIST = "public_reports/index/"
