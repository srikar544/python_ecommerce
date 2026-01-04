"""
cache.py
--------
Flask-Caching configuration.
"""

#Your cart count query runs on every page load

from flask_caching import Cache

cache = Cache(config={"CACHE_TYPE": "SimpleCache"})