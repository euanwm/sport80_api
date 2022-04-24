""" Busy backend shit """
import logging
import requests
from typing import Union
from pprint import pprint

from urllib.parse import urljoin

from .pages_enum import OpenApiEndpoint, EndPoint
from .helpers import findall_uuid4, pull_tables, convert_to_json


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str, ret_dict: bool = False, debug_lvl: logging = logging.WARNING):
        self.http_session = requests.Session()
        self.domain: str = domain
        self.ret_dict: bool = ret_dict
        logging.basicConfig(level=debug_lvl)
        self.standard_headers = self.load_standard_headers()

    def load_standard_headers(self):
        """ Usual shit """
        # Todo: Extract full JSON object from main page
        headers = {"X-API-TOKEN": self.acquire_token(),
                   "authority": "admin-bwl-rankings.sport80.com",
                   "accept": "application/json",
                   "Content-Type": "application/json"}
        return headers

    def app_data(self):
        """ Fetches OpenAPI server details """
        get_page = self.http_session.get(OpenApiEndpoint.CORE_SERVICES_API_URL.value)
        return get_page.json()

    def acquire_token(self):
        """ Acquires API token from landing page """
        api_url = urljoin(self.domain, "/public/rankings/")
        get_page = self.http_session.post(api_url)
        tokens = findall_uuid4(get_page.text)
        for uuid in tokens:
            if self.test_token(uuid):
                return uuid

    def test_token(self, token: str):
        api_url = "https://admin-bwl-rankings.sport80.com/api/categories/featured"
        get_page = self.http_session.get(api_url, headers={"X-API-TOKEN": token})
        if get_page.status_code == 200:
            return True

    def test_core_api(self):
        api_url = "https://core.sport80.com/api/docs"
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def get_weight_class(self):
        api_url = "https://admin-bwl-rankings.sport80.com/api/categories/rankings"
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def lookup_lifter(self, lifter_id):
        """ Takes a lifter id and returns their data """

    def get_ranking_index(self):
        """ Working """
        api_url = "https://admin-bwl-rankings.sport80.com/api/categories/featured"
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def _get_rankings_table(self, cat):
        """ Simple GET call for the ranking category specified """
        api_url = f"https://admin-bwl-rankings.sport80.com/api/categories/{cat}/rankings/table"
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        return get_page.json()

    def quick_ranking_search(self):
        """ Cycles through the API endpoint available for rankings table """
        start_cat_int = 1
        start_cat = self._get_rankings_table(start_cat_int)
        err_msg = "An error occurred"
        available_end_points = {}
        while err_msg not in start_cat['title']:
            available_end_points.update({start_cat['title']: start_cat['data_url']})
            start_cat_int += 1
            start_cat = self._get_rankings_table(start_cat_int)
        return available_end_points

    def rankings_table_post(self, category, start_date, end_date, wt_class):
        api_url = f'https://admin-bwl-rankings.sport80.com/api/categories/{category}/rankings/table'
        payload = {"date_range_start": start_date, "date_range_end": end_date, "weight_class": wt_class}
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        return get_page.json()

    def get_rankings(self, wt_class: int, start_date: str, end_date: str):
        api_url = "https://admin-bwl-rankings.sport80.com/api/categories/all/rankings/table/data"
        get_page = self.http_session.post(api_url, headers=self.standard_headers, json={"date_range_start": start_date,
                                                                                        "date_range_end": end_date,
                                                                                        "weight_class": wt_class})
        if get_page.ok:
            return get_page.json()

    def get_event_index(self, start_date: str, end_date: str) -> dict:
        api_url = "https://admin-bwl-rankings.sport80.com/api/events/table/data"
        payload = {"date_range_start": start_date, "date_range_end": end_date}
        get_page = self.http_session.post(api_url, headers=self.standard_headers, json=payload)
        if get_page.ok:
            return get_page.json()

    def get_event_results(self, event_id):
        # Todo: add in something to collate pages together
        api_url = f"https://admin-bwl-rankings.sport80.com/api/events/{event_id}/table/data"
        get_page = self.http_session.post(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    #### LEGACY CODE THAT STILL WORKS
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
