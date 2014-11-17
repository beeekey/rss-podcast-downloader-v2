#!/usr/bin/env python
"""
This module does awesome stuff!

Example::

    >>> from rss_podcast_downloader import f1
    >>> f1(1)
    >>>
"""
# Imports ######################################################################
from __future__ import print_function
from .persistent_pineapple import PersistentPineapple
from .cache import Cache


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
def f1(something):
    print("Hello World!", something)


def process(config_file, cache_file, logfile=None):
    """Process the config file, download the podcasts, and store the results
    in the cache_file.
    """
    settings = PersistentPineapple(config_file, woc=False, lofc=False)
    cache = Cache(settings["cache-file"])

    print(settings["podcasts"])
    print(cache)
