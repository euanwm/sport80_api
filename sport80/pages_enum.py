""" Throw all the endpoint strings in here """
import enum


class LegacyEndPoint(enum.Enum):
    """ As mentioned before... """
    EVENT_INDEX = "event_results?id_ranking=8"
    EVENT_RESULTS = f"{EVENT_INDEX}&resource="
    UPCOMING_EVENTS = "events"
    START_LIST = "public_reports/index/"
    IS_LOGGED_IN = "register/user_status?id_ranking=8"


class EndPoint(enum.Enum):
    """ This is for the OpenAPI endpoints that the latest Sport80 pages are using """
    ORGANISATIONS = "/api/organisations"
    EVENT_INDEX = "/api/events/table/data"
    INDEX_PAGE = "/public/rankings/"
    ALL_RANKINGS = "/api/categories/all/rankings/table/data"
    RANKINGS_INDEX = "/api/categories/featured"
    RANKINGS_DATA = "/api/categories/rankings"

    @staticmethod
    def event_results_url(event_id) -> str:
        """ Simple method for creating the correct API call """
        api_url = f"/api/events/{event_id}/table/data"
        return api_url

    @staticmethod
    def lifter_url(lifter_id) -> str:
        """ Simple method for creating the correct API call """
        api_url = f"/api/athletes/{lifter_id}/table"
        return api_url

    @staticmethod
    def rankings_url(category_id) -> str:
        """ Simple method for creating the correct API call """
        api_url = f"/api/categories/{category_id}/rankings/table"
        return api_url
