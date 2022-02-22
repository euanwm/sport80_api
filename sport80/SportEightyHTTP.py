""" Busy backend shit """
import requests
from urllib.parse import urljoin
from pages_enum import EndPoint
from helpers import pull_tables


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str):
        self.http_session = requests.Session()
        self.domain = domain

    def get_event_index(self) -> list:
        get_page = self.http_session.get(urljoin(self.domain, EndPoint.EVENT_INDEX.value))
        pull_tables(get_page)

if __name__ == '__main__':
    thing = SportEightyHTTP("http://bwl.sport80.com")
    thing.get_event_index()