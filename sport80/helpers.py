"""
Helpers library of static functions
"""
import socket
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

if __name__ == '__main__':
    print(resolve_to_ip("bwl.sport80.com"))
