""" Busy backend shit """
import logging
import requests
from typing import Union

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from .pages_enum import EndPoint, LegacyEndPoint
from .helpers import pull_tables, convert_to_json, convert_to_py


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str, ret_dict: bool = False, debug_lvl: logging = logging.WARNING):
        self.http_session = requests.Session()
        self.domain: str = domain
        self.ret_dict: bool = ret_dict
        logging.basicConfig(level=debug_lvl)
        self.domain_env = self.pull_domain_env()
        self.standard_headers = self.load_standard_headers()

    def load_standard_headers(self):
        """ Standard header payload for each API request """
        headers = {"X-API-TOKEN": self.domain_env['SERVICES_API_PUBLIC_KEY'],
                   "authority": self.domain_env['RANKINGS_DOMAIN_URL'],
                   "accept": "application/json",
                   "Content-Type": "application/json"}
        return headers

    def app_data(self):
        """ Fetches OpenAPI server details """
        get_page = self.http_session.get(self.domain_env['CORE_SERVICE_API_URL'])
        return get_page.json()

    def pull_domain_env(self) -> dict:
        """ On both BWL and USAW sites, there is a JS dict needed for the API calls to work """
        get_page = requests.get(urljoin(self.domain, EndPoint.INDEX_PAGE.value))
        soup = BeautifulSoup(get_page.content, "html.parser")
        scripts_in_page = soup.find_all('script')
        js_extract = []
        for js_section in scripts_in_page:
            if "application/javascript" in js_section.attrs.values():
                js_extract.append(js_section)
        if len(js_extract) == 1:
            return convert_to_py(str(js_extract))

    def test_token(self, token: str):
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.RANKINGS_INDEX.value)
        get_page = self.http_session.get(api_url, headers={"X-API-TOKEN": token})
        if get_page.status_code == 200:
            return True

    def test_core_api(self):
        api_url = "https://core.sport80.com/api/docs"
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def get_weight_class(self):
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.RANKINGS_DATA.value)
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def get_ranking_index(self):
        """ Working """
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.RANKINGS_INDEX.value)
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def _get_rankings_table(self, category):
        """ Simple GET call for the ranking category specified """
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.rankings_url(category))
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

    def get_rankings_table(self, category, a_date, z_date, wt_class):
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.rankings_url(category))
        payload = {"date_range_start": a_date, "date_range_end": z_date, "weight_class": wt_class}
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        return get_page.json()

    def get_rankings(self, wt_class: int, a_date: str, z_date: str):
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.ALL_RANKINGS.value)
        payload = {"date_range_start": a_date, "date_range_end": z_date, "weight_class": wt_class}
        get_page = self.http_session.post(api_url, headers=self.standard_headers, json=payload)
        if get_page.ok:
            return get_page.json()

    def get_event_index(self, start_date: str, end_date: str) -> dict:
        """ start_date="2022-01-01", end_date="2022-12-31" """
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.EVENT_INDEX.value)
        payload = {"date_range_start": start_date, "date_range_end": end_date}
        get_page = self.http_session.post(api_url, headers=self.standard_headers, json=payload)
        if get_page.ok:
            return get_page.json()

    def get_event_results(self, event_id):
        # Todo: add in something to collate pages together
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.event_results_url(event_id))
        get_page = self.http_session.post(api_url, headers=self.standard_headers)
        if get_page.ok:
            return get_page.json()

    def get_lifter_data(self, lifter_id):
        # Todo: make this actually work, think it's server side though
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.lifter_url(lifter_id))
        get_page = self.http_session.get(api_url, headers=self.standard_headers)
        return get_page.json()

    # LEGACY CODE THAT STILL WORKS
    def get_upcoming_events(self) -> Union[list, dict]:
        """ Returns the upcoming events list """
        logging.info("get_upcoming_events called")
        api_url = urljoin(self.domain, LegacyEndPoint.UPCOMING_EVENTS.value)
        get_page = self.http_session.get(api_url)
        upcoming_events = pull_tables(get_page)
        if self.ret_dict:
            return convert_to_json(upcoming_events)
        return upcoming_events

    def get_start_list(self, event_id: str) -> Union[list, dict]:
        """ Returns a specific upcoming events start list """
        logging.info("get_start_list called")
        api_url = urljoin(self.domain, LegacyEndPoint.START_LIST.value + event_id)
        get_page = self.http_session.get(api_url)
        start_list = pull_tables(get_page)
        if self.ret_dict:
            return convert_to_json(start_list)
        return start_list
