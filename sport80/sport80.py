""" Main file """
from .sport80_http_client import SportEightyHTTP


class SportEighty:
    """
    This class enables a variety of functions that can be carried out with a sport80 subdomain.
    """
    def __init__(self, subdomain: str):
        self.__http_client = SportEightyHTTP(subdomain)

    def event_index(self) -> list:
        """ Shorthand call """
        return self.__http_client.get_event_index()

    def event_results(self, event_id: str) -> list:
        """ Shorthand call """
        return self.__http_client.get_event_results(event_id)

    def upcoming_events(self) -> list:
        """ Shorthand call """
        return self.__http_client.get_upcoming_events()

    def start_list(self, event_id: str):
        """ Shorthand call """
        return self.__http_client.get_start_list(event_id)
