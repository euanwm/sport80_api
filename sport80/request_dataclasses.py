""" Moving the request dicts here as dataclasses """
from dataclasses import dataclass


@dataclass
class FilterByYear:
    """ Allows a neater call for any year filtering """
    year: int

    def __init__(self, year: int):
        self.year = year
        self.start_date = f"{year}-01-01"
        self.end_date = f"{year}-12-31"

    def as_dict(self) -> dict:
        """ Returns a dict """
        return {"date_range_start": self.start_date, "date_range_end": self.end_date}


@dataclass
class RequestHeaders:
    """ RequestHeaders that are required for all API calls """
    api_token: str
    auth_url: str

    def __init__(self, api_token: str, auth_url: str):
        self.api_token = api_token
        self.auth_url = auth_url

    def as_dict(self) -> dict:
        """ Returns a dict """
        headers = {"X-API-TOKEN": self.api_token,
                   "authority": self.auth_url,
                   "accept": "application/json",
                   "Content-Type": "application/json"}
        return headers


@dataclass
class PayloadGenerator:
    """ Kinda self-explanatory """
    year: int
    weight_class: int

    def __init__(self, year: int = None, weight_class: int = None):
        self.year: int = year
        self.weight_class: int = weight_class
        self.payload: dict = {}

    def generate(self) -> dict:
        """ Returns a dict """
