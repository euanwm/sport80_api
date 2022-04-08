""" Throw all the endpoint strings in here """
import enum


class EndPoint(enum.Enum):
    """ As mentioned before... """
    # Todo: id_ranking is different for the USAW page (and other pages)
    EVENT_INDEX = "event_results?id_ranking=8"
    EVENT_RESULTS = f"{EVENT_INDEX}&resource="
    UPCOMING_EVENTS = "events"
    START_LIST = "public_reports/index/"
    IS_LOGGED_IN = "register/user_status?id_ranking=8"
