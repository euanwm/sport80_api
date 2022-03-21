""" Busy backend shit """
import logging
from urllib.parse import urljoin
from typing import Union
import requests
from .pages_enum import EndPoint
from .helpers import pull_tables, convert_to_json


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str, ret_dict: bool = False, debug_lvl: logging = logging.WARNING):
        self.http_session = requests.Session()
        self.domain: str = domain
        self.ret_dict: bool = ret_dict
        logging.basicConfig(level=debug_lvl)

    def get_event_index(self) -> Union[list, dict]:
        """ Returns the main event list """
        logging.info("get_event_index called")
        api_url = urljoin(self.domain, EndPoint.EVENT_INDEX.value)
        get_page = self.http_session.get(api_url)
        event_index = pull_tables(get_page)
        if self.ret_dict:
            return convert_to_json(event_index)
        return event_index

    def get_event_results(self, event_id: str) -> Union[list, dict]:
        """ Returns specific event result """
        logging.info("get_event_results called")
        api_url = urljoin(self.domain, EndPoint.EVENT_RESULTS.value + event_id)
        get_page = self.http_session.get(api_url)
        event_results = pull_tables(get_page)
        if self.ret_dict:
            return convert_to_json(event_results)
        return event_results

    def get_upcoming_events(self) -> Union[list, dict]:
        """ Returns the upcoming events list """
        logging.info("get_upcoming_events called")
        api_url = urljoin(self.domain, EndPoint.UPCOMING_EVENTS.value)
        get_page = self.http_session.get(api_url)
        upcoming_events = pull_tables(get_page)
        if self.ret_dict:
            return convert_to_json(upcoming_events)
        return upcoming_events

    def get_start_list(self, event_id: str) -> Union[list, dict]:
        """ Returns a specific upcoming events start list """
        logging.info("get_start_list called")
        api_url = urljoin(self.domain, EndPoint.START_LIST.value + event_id)
        get_page = self.http_session.get(api_url)
        start_list = pull_tables(get_page)
        if self.ret_dict:
            return convert_to_json(start_list)
        return start_list
