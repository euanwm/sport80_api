""" Throw all the endpoint strings in here """
import enum

class EndPoint(enum.Enum):
    """ As mentioned before... """
    EVENT_INDEX = "event_results?id_ranking=8"
    EVENT_RESULTS = f"{EVENT_INDEX}&resource="
    UPCOMING_EVENTS = "events"
    START_LIST = "public_reports/index/"
    IS_LOGGED_IN = "register/user_status?id_ranking=8"


class OpenApiEndpoint(enum.Enum):
    """ This is for the OpenAPI endpoints that the latest Sport80 pages are using """
    CORE_SERVICES_API_URL = "https://auth.sport80.com/api/app_data"
    ORGANISATIONS = "/api/organisations"
    EVENT_TABLE = "/api/events/table/data"
