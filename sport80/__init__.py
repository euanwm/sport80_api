"""
Totally unofficial Sport80 API package. Meh.
"""

from .sport80 import SportEighty
from .sport80_http_client import SportEightyHTTP
from .helpers import pull_tables, convert_to_json, convert_to_py
from .pages_enum import EndPoint

__version__ = "2.2.0"
__author__ = "Euan Meston"
