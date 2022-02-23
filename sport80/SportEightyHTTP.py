""" Busy backend shit """
import requests
import logging
from urllib.parse import urljoin
from pages_enum import EndPoint
from helpers import pull_tables


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str, debug_lvl: logging = logging.INFO):
        self.http_session = requests.Session()
        self.domain = domain
        logging.basicConfig(level=debug_lvl)

    def get_event_index(self):
        """ Returns the main event list """
        api_url = urljoin(self.domain, EndPoint.EVENT_INDEX.value)
        get_page = self.http_session.get(api_url)
        pull_tables(get_page)

    def get_event_results(self, event_id):
        """ Returns specific event result """
        api_url = urljoin(self.domain, EndPoint.EVENT_RESULTS.value + event_id)
        get_page = self.http_session.get(api_url)
        pull_tables(get_page)

    def get_upcoming_events(self):
        """ Returns the upcoming events list """
        api_url = urljoin(self.domain, EndPoint.UPCOMING_EVENTS.value)
        get_page = self.http_session.get(api_url)
        pull_tables(get_page)

    def get_start_list(self, event_id):
        """ Returns a specific upcoming events start list """
        logging.info("get_start_list called")
        api_url = urljoin(self.domain, EndPoint.START_LIST.value + event_id)
        get_page = self.http_session.get(api_url)
        pull_tables(get_page)


if __name__ == '__main__':
    thing = SportEightyHTTP("http://bwl.sport80.com", logging.INFO)
    thing.get_start_list("37905")
    # thing.get_event_index()
