""" Main file """
import logging
from typing import Union
from .sport80_http_client import SportEightyHTTP


class SportEighty:
    """
    This class enables a variety of functions that can be carried out with a sport80 subdomain.
    """
    def __init__(self, subdomain: str, debug: logging = logging.WARNING):
        self.__http_client = SportEightyHTTP(subdomain, debug_lvl=debug)

    def event_index(self, start_date: str, end_date: str) -> dict:
        """ Shorthand call """
        return self.__http_client.get_event_index(start_date, end_date)

    def event_results(self, event_id: str) -> dict:
        """ Shorthand call """
        return self.__http_client.get_event_results(event_id)

    def upcoming_events(self) -> Union[list, dict]:
        """ Shorthand call """
        return self.__http_client.get_upcoming_events()

    def start_list(self, event_id: str) -> Union[list, dict]:
        """ Shorthand call """
        return self.__http_client.get_start_list(event_id)

    def rankings_index(self) -> dict:
        """ Returns a dict containing endpoints for all available ranking categories """
        return self.__http_client.get_ranking_index()