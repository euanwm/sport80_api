""" Main file """
import logging
from typing import Union
from .sport80_http_client import SportEightyHTTP


class SportEighty:
    """
    This class enables a variety of functions that can be carried out with a sport80 subdomain.
    """
    def __init__(self, subdomain: str, return_dict=True, debug: logging = logging.WARNING):
        self.__http_client = SportEightyHTTP(subdomain, return_dict=return_dict, debug_lvl=debug)

    def event_index(self, year: int) -> dict:
        """ Now working """
        return self.__http_client.get_event_index(year)

    def event_results(self, event_dict: dict) -> Union[list, dict]:
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

    def lifter_history(self, lifter_id: int) -> Union[list, dict]:
        """ Returns a dict containing a lifter history. The lifter_id does NOT correlate to the membership number """
        return self.__http_client.get_lifter_data(lifter_id)

    def rankings(self, wt_class: int, a_date: str, z_date: str, region: int) -> dict:
        """ Returns a dict containing the rankings table for the specified weight class and date range """
        # todo: have this handle a kwargs dict instead of a bunch of args
        return self.__http_client.get_rankings(wt_class, a_date, z_date, region)

    def ranking_filters(self):
        """ Pulls all the available ranking filters """
        # todo: make this return an object or some shit
        return self.__http_client.get_ranking_filters()['filters']
