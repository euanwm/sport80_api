"""
Helpers library of static functions
"""
import csv
import re
import socket
from logging import info, debug
from bs4 import BeautifulSoup
from requests import Response
from js2py import eval_js

from .pages_enum import LegacyEndPoint


def list_to_dict(dict_list: list[dict]) -> dict:
    """ Takes a list of dicts and puts them into an index dict """
    new_dict: dict = {}
    for index, contents in enumerate(dict_list):
        new_dict[index] = contents
    return new_dict


def collate_index(page_data: dict) -> dict:
    """ Combines the data values """
    data_list: list = []
    for stuff in page_data:
        data_list.append(page_data[stuff]['data'])
    final_list: list = []
    for dicty_bois in data_list:
        for single_dict in dicty_bois:
            final_list.append(single_dict)
    switch_to_dict = list_to_dict(final_list)
    return switch_to_dict


def convert_to_py(js_vars: str) -> dict:
    """ I really don't care at this stage """
    py_dict = eval_js(js_vars.lstrip('[<script type="application/javascript">').rstrip('</script>]'))
    return py_dict


def resolve_to_ip(url: str) -> str:
    """ Returns IP address of the subdomain """
    return socket.gethostbyname(url)


def pull_tables(page_content: Response) -> list:
    """ Returns a dict with details of all the tables within it """
    debug("pull_tables called")
    soup_parse = BeautifulSoup(page_content.text, "html.parser")
    table_list: list = []
    formatted_table: list = []
    for tables in soup_parse.find_all("table"):
        table_list.append(tables)
    if len(table_list) > 1:
        info(f"multiple tables: {len(table_list)}")
        formatted_table = extract_table(table_list, multiple_tables=True)
    elif len(table_list) == 1:
        info("single table")
        formatted_table = extract_table(table_list[0])
    return formatted_table


def extract_table(table, multiple_tables=False) -> list:
    """ Extracts the HTML table """
    debug("extract_table called")
    parsed_table: list = []
    if not multiple_tables:
        parsed_table.append(strip_table_headers(table))
        parsed_table.append(strip_table_body(table))
    elif multiple_tables:
        # Strip the headers from the first table only
        parsed_table.append(strip_table_headers(table[0]))
        for rows in table:
            parsed_table.append(strip_table_body(rows))
    return flatten_list(parsed_table)


def flatten_list(nested_list: list) -> list:
    """ Removes any nested lists, so we have one big list for each row """
    debug("flatten_list called")
    start_list = [x for x in nested_list if x != []]  # Drop any empty lists initially
    return recursive_anti_nester(start_list)


def recursive_anti_nester(nested_list: list) -> list:
    """ IT'S YA BOI, RECURSION! """
    debug("recursive_anti_nester called")

    class AntiNester(list):
        """ Being simultaneously lazy and extra """

        def __init__(self):
            super().__init__()
            self.flat_list: list = []

        def flatten_that_shit(self, big_list: list) -> None:
            """ RUN IT """
            for line_count, lines in enumerate(big_list):
                if not any(isinstance(index, list) for index in lines):
                    self.flat_list.append(lines)
                    # big_list.pop(line_count)
                else:
                    self.flatten_that_shit(big_list[line_count])

    magic_thing = AntiNester()
    magic_thing.flatten_that_shit(nested_list)
    return magic_thing.flat_list


def strip_table_headers(table) -> list:
    """ Strips the table headers """
    debug("strip_table_headers called")
    headers = []
    for tbl_hdr in table.find("tr").find_all("th"):
        headers.append(tbl_hdr.text.strip())
    return headers


def strip_table_body(table):
    """Given a table, returns all its rows"""
    debug("strip_table_body called")
    rows = []
    for tbl_row in table.find_all("tr")[1:]:
        cells = []
        tds = tbl_row.find_all("td")
        if len(tds) == 0:
            ths = tbl_row.find_all("th")
            for tbl_hdr in ths:
                cells.append(tbl_hdr.text.strip())
        else:
            for tbl_dat in tds:
                links = tbl_dat.find_all(href=True)
                if len(links) == 1:
                    cells.append(strip_report_id(links[0]['href']))
                elif len(tbl_dat.find_all('i')) == 1:
                    strip_it = str(tbl_dat.find_all('i'))
                    if "data-id-resource" in strip_it:
                        re_search = re.search(r'\d+', strip_it)
                        cells.append(re_search.group())
                    else:
                        cells.append(strip_it)
                else:
                    cells.append(tbl_dat.text.strip())
        rows.append(cells)
    return rows


def strip_report_id(url: str) -> str:
    """ This could probably be done a bit neater but IDC currently """
    url_endpoint = LegacyEndPoint.START_LIST.value
    if url_endpoint in url:
        extracted_url = re.search(url_endpoint, url)
        return url[extracted_url.regs[0][1]::]
    return url


def convert_to_json(big_list: list) -> dict:
    """ Takes the data and converts it to a dict so its easier to handle on a webpage FE """
    col_heads = big_list[0]
    dict_to_return = {}
    for index, line in enumerate(big_list[1::]):
        dict_to_return[index] = _insert_json_contents(col_heads, line)
    return dict_to_return


def _insert_json_contents(headers: list, contents: list) -> dict:
    """ Uses the headers supplied to generate the contents of the dict returned"""
    small_dict = {}
    for index, details in enumerate(headers):
        small_dict.update({details: contents[index]})
    return small_dict


def dump_to_csv(filename: str, data_list: list):
    """ This is really lazy and i'll probably remove this """
    full_filename = f"{filename}.csv"
    with open(full_filename, "w", encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, lineterminator='\n')
        for line in data_list:
            writer.writerow(line)
    return full_filename
