"""
Totally unofficial Sport80 API package. Meh.
"""

from .sport80 import SportEighty
from .sport80_http_client import SportEightyHTTP
from .pages_enum import EndPoint
from .helpers import pull_tables, convert_to_json

__version__ = "0.1.2"
__author__ = "Euan Meston"
