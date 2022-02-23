"""
Helpers library of static functions
"""
import socket
from logging import info
from bs4 import BeautifulSoup
from requests import Response


def resolve_to_ip(url: str) -> str:
    """ Returns IP address of the subdomain """
    return socket.gethostbyname(url)


def pull_tables(page_content: Response):
    """ Returns a dict with details of all the tables within it """
    soup_parse = BeautifulSoup(page_content.text, "html.parser")
    table_list = []
    for tables in soup_parse.find_all("table"):
        table_list.append(tables)
    if len(table_list) > 1:
        info(f"multiple tables: {len(table_list)}")
        return extract_table(table_list, multiple_tables=True)
    elif len(table_list) == 1:
        info("single table")
        return extract_table(table_list[0])


def extract_table(table, multiple_tables=False) -> list:
    """ Extracts the HTML table """
    parsed_table: list = []
    if not multiple_tables:
        parsed_table.append(strip_table_headers(table))
        parsed_table.append(strip_table_body(table))
    elif multiple_tables:
        parsed_table.append(strip_table_headers(table[0]))  # Strip the headers from the first table only
        for rows in table:
            parsed_table.append(strip_table_body(rows))
    return flatten_list(parsed_table)


def flatten_list(nested_list: list) -> list:
    """ Removes any nested lists so we have one big list for each row """
    info("flattening list")
    start_list = [x for x in nested_list if x != []]  # Drop any empty lists initially
    flat_list = recursive_anti_nester(start_list)


def recursive_anti_nester(nested_list: list) -> list:
    """ IT'S YA BOI, RECURSION! """
    class AntiNester(list):
        """ Being simultaneously lazy and extra """
        def __init__(self, big_nested_list: list):
            super().__init__()
            self.nested_list: list = big_nested_list
            self.flat_list: list = []

        def recursionator(self, something):
            """ Yeah... """

        def flatten_that_shit(self):
            """ RUN IT """

        def gimme_that_list_plz(self) -> list:
            """ RETURN THE GOODS AND CALL ME PAPI """
            return self.flat_list

    magic_thing = AntiNester(nested_list)
    magic_thing.flatten_that_shit()
    return magic_thing.gimme_that_list_plz()

def strip_table_headers(table) -> list:
    """ Strips the table headers """
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers


def strip_table_body(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        tds = tr.find_all("td")
        if len(tds) == 0:
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            for td in tds:
                if len(td.find_all('i')) == 1:
                    strip_it = td.find_all('i')
                    cells.append(str(strip_it))
                else:
                    cells.append(td.text.strip())
        rows.append(cells)
    return rows
