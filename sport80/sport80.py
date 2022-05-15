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

    def event_index(self, year: int) -> dict:
        """ Now working """
        return self.__http_client.get_event_index(year)

    def event_results(self, event_dict: dict) -> dict:
        """ Now working """
        return self.__http_client.get_event_results(event_dict)

    def upcoming_events(self) -> Union[list, dict]:
        """ Now working """
        return self.__http_client.get_upcoming_events()

    def start_list(self, event_id: str) -> Union[list, dict]:
        """ Now working """
        return self.__http_client.get_start_list(event_id)

    def rankings_index(self) -> dict:
        """ Returns a dict containing endpoints for all available ranking categories """
        return self.__http_client.get_ranking_index()
