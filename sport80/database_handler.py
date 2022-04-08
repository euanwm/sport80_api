""" Storing, updating, and checking database entries """
import csv

from .sport80 import SportEighty
from .helpers import dump_to_csv

class DBHandler:
    """ Stuff """

    def __init__(self, subdomain: str):
        self.api_func = SportEighty(subdomain)

    def create_full_db(self):
        """ Create a DB of all available results """

    def update_db(self):
        """ Checks local index and remote index then updates as appropriate  """

    def parity_check(self):
        """ Runs through main DB and pulls non-conforming results & duplicates """
