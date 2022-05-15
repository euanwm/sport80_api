""" Busy backend shit """
import logging
import requests
from typing import Union, Optional

from urllib.parse import urljoin
from bs4 import BeautifulSoup

from .pages_enum import EndPoint, LegacyEndPoint
from .helpers import pull_tables, convert_to_json, convert_to_py, collate_index


class SportEightyHTTP:
    """ Contains all the big annoying functions so the main API file is nice and neat """

    def __init__(self, domain: str, return_dict: bool = True, debug_lvl: logging = logging.WARNING):
        self.http_session = requests.Session()
        self.domain: str = domain
        self.ret_dict: bool = return_dict
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
            return get_page.json()['cards']

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

    def get_event_index(self, year: int) -> dict:
        """ Fetches the event index per year """
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.EVENT_INDEX.value)
        payload = {"date_range_start": f"{year}-01-01", "date_range_end": f"{year}-12-31"}
        get_page = self.http_session.post(api_url, headers=self.standard_headers, json=payload)
        if get_page.ok:
            page_data = self.__collate_results(get_page.json(), payload)
            collated_index = collate_index(page_data)
            return collated_index

    def get_event_results(self, event_dict: dict):
        """ Uses the integer that follows the event url API """
        # todo: below line needs serious refactoring
        event_id: str = event_dict['action'][0]['route'].split('/')[-1]
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.event_results_url(event_id))
        get_page = self.http_session.post(api_url, headers=self.standard_headers)
        collated_pages = self.__collate_results(get_page.json())
        combined_data = collate_index(collated_pages)
        if get_page.ok:
            return combined_data

    def __collate_results(self, page_one: dict, payload: Optional[dict] = None) -> dict:
        """ Cycles through the passed dict and checks for a URL """
        all_pages = {0: page_one}
        current_page = page_one
        index = 1
        while current_page['next_page_url']:
            all_pages[index] = current_page = self.__next_page(current_page['next_page_url'], payload)
            index = index + 1
        return all_pages

    def __next_page(self, next_url: str, payload: dict) -> dict:
        """ Designed around the events dict """
        get_page = self.http_session.post(next_url, headers=self.standard_headers, json=payload)
        if get_page.ok:
            return get_page.json()

    def get_lifter_data(self, lifter_id):
        """ Historical performance of a lifter  """
        api_url = urljoin(self.domain_env['RANKINGS_DOMAIN_URL'], EndPoint.lifter_url(lifter_id))
        get_page = self.http_session.post(api_url, headers=self.standard_headers)
        if get_page.ok:
            return self.__collate_results(get_page.json())

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
