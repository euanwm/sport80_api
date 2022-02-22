""" Main file """

from helpers import resolve_to_ip
from SportEightyHTTP import SportEightyHTTP


class SportEighty:
    """
    This class enables a variety of functions that can be carried out with a sport80 subdomain.
    """

    def __init__(self, subdomain: str):
        self.__http_client = SportEightyHTTP(subdomain)


if __name__ == '__main__':
    pass