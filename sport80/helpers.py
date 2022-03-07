"""
Helpers library of static functions
"""
import re
import socket
from logging import info, debug
from bs4 import BeautifulSoup
from requests import Response


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
                if len(tbl_dat.find_all('i')) == 1:
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
