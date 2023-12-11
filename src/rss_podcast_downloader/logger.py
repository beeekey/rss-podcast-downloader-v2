#!/usr/bin/env python
"""
This module creates and initializes a project-wide logger.

Example::

    >>> from SAMPLEPROJ.logger import get_logger()
    >>> get_logger.debug("test")
    >>>
"""
# Imports ######################################################################

import logging
from .settings import get_settings


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
LOGGER = None
SCREEN_LEVEL = logging.INFO


def _init():
    global LOGGER

    if LOGGER is None:
        LOGGER = logging.getLogger('rss-podcast-downloader')
        LOGGER.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        screen_formatter = logging.Formatter(get_settings()["screen-formatter"])
        ch.setFormatter(screen_formatter)
        ch.setLevel(SCREEN_LEVEL)
        LOGGER.addHandler(ch)

        logfile_path = get_settings()["log-file"]
        if logfile_path:
            logfile_formatter = logging.Formatter(get_settings()["log-file-formatter"])
            fh = logging.FileHandler(logfile_path, get_settings()["log-file-mode"])
            fh.setLevel(get_settings()["log-file-level"])
            fh.setFormatter(logfile_formatter)
            LOGGER.addHandler(fh)


def get_logger():
    if LOGGER is None:
        _init()

    return LOGGER
