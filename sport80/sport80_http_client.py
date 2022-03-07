""" Busy backend shit """
import logging
from urllib.parse import urljoin
import requests
from .pages_enum import EndPoint
from .helpers import pull_tables


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str, debug_lvl: logging = logging.WARNING):
        self.http_session = requests.Session()
        self.domain = domain
        logging.basicConfig(level=debug_lvl)

    def get_event_index(self) -> list:
        """ Returns the main event list """
        logging.info("get_event_index called")
        api_url = urljoin(self.domain, EndPoint.EVENT_INDEX.value)
        get_page = self.http_session.get(api_url)
        return pull_tables(get_page)

    def get_event_results(self, event_id) -> list:
        """ Returns specific event result """
        logging.info("get_event_results called")
        api_url = urljoin(self.domain, EndPoint.EVENT_RESULTS.value + event_id)
        get_page = self.http_session.get(api_url)
        return pull_tables(get_page)

    def get_upcoming_events(self):
        """ Returns the upcoming events list """
        # Todo: Fix "Entry List" and "Registration" columns
        logging.info("get_upcoming_events called")
        api_url = urljoin(self.domain, EndPoint.UPCOMING_EVENTS.value)
        get_page = self.http_session.get(api_url)
        return pull_tables(get_page)

    def get_start_list(self, event_id):
        """ Returns a specific upcoming events start list """
        logging.info("get_start_list called")
        api_url = urljoin(self.domain, EndPoint.START_LIST.value + event_id)
        get_page = self.http_session.get(api_url)
        return pull_tables(get_page)
