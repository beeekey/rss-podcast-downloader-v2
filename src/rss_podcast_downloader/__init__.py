#!/usr/bin/env python
"""
This module does awesome stuff!

Example::

    >>> from rss_podcast_downloader import f1
    >>> f1(1)
    >>>
"""
# Imports ######################################################################

import os
import re
import time
import threading
from stat import S_ISREG, ST_MTIME, ST_MODE
from contextlib import contextmanager
# from .persistent_pineapple import PersistentPineapple
from .settings import get_settings
from .cache import Cache
from .rss_feed import RSSFeed
from .logger import _init, get_logger


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
VERSION = __version__
__PRINT_DOTS = False
__INITIALIZED = False


def f1(something):
    print("Hello World!", something)


@contextmanager
def dots(message):
    global __PRINT_DOTS

    print(message, end="")
    __PRINT_DOTS = True
    yield
    __PRINT_DOTS = False
    print()


def print_dots():
    while True:
        if __PRINT_DOTS:
            print(".", end="")
            time.sleep(1)


def _current_episodes(podcast, directory):
    """Returns a list of all filenames of the given podcast that exist in the
    directory.  They will be sorted by file modification time.
    """
    files = [
        os.path.abspath(os.path.join(directory, x)) for x in os.listdir(directory)
        if re.match("^(\d+-)?%s" % podcast["file-prefix"], x)
    ]
    files = ((os.stat(path), path) for path in files)
    files = (
        (stat[ST_MTIME], path)
        for stat, path in files if S_ISREG(stat[ST_MODE]))

    return sorted(files)


def _download_episode(episode, directory):
    if get_settings()["no-download"]:
        get_logger().debug("would be downloading [%s]", episode.filename)
        return

    with dots("Downloading %s: %s" % (episode.feed_title, episode.title)):
        get_logger().debug("downloading [%s]", episode.filename)
        episode.download(directory)


def _new_episodes(cache, feed):
    """Returns all episodes in the feed that have not been previously added
    to the cache.
    """
    episodes = []

    for episode in feed.episodes:
        if not cache.has(episode):
            episodes.append(episode)

    return episodes


def _handle_feed(cache, feed, podcast, directory):
    current_episodes = _current_episodes(podcast, directory)
    new_episodes = _new_episodes(cache, feed)

    if podcast["max-downloads"] and (len(current_episodes) > podcast["max-downloads"]) and (not podcast["rotate"]):
        return
    elif podcast["max-downloads"] and (len(current_episodes) > podcast["max-downloads"]) and podcast["rotate"]:
        # Only download the latest ones
        new_episodes = new_episodes[:podcast["max-downloads"]]

    if new_episodes:
        get_logger().debug("downloading [%i] new episodes of [%s]", len(new_episodes), feed.title)

        # Download all of the new episodes
        for episode in new_episodes:
            _download_episode(episode, directory)
            cache.add(episode)
    else:
        get_logger().debug("no new episodes in [%s]", feed.title)

    # Prune them if needed
    current_episodes = _current_episodes(podcast, directory)
    if podcast["max-downloads"] and (len(current_episodes) > podcast["max-downloads"]) and podcast["rotate"]:
        # delete the oldest episode
        for _, path in current_episodes[:-podcast["max-downloads"]]:
            get_logger().debug("removing old episode [%s]", path)
            os.unlink(path)

            if podcast["clear-cache-on-rotate"]:
                cache.remove_by_filename(episode.filename)


def initialize(config_file):
    global __INITIALIZED
    get_settings(config_file)
    _init()
    __INITIALIZED = True


def cache_all(config_file, cache_file, logfile=None):
    """This function will read the feeds and add each episode found to the
    cache, WITHOUT download the episode.  This is used to create a baseline to
    start from.
    """
    if not __INITIALIZED:
        raise Exception("Must call initialize() first")

    get_logger().debug("##### Start cache all " + "#" * 58)
    cache = Cache(get_settings()["cache-file"])

    for podcast in get_settings()["podcasts"]:
        feed = RSSFeed(
            podcast["url"], podcast["title"], podcast["file-prefix"],
            get_settings()["use-date-prefix"])

        for episode in feed.episodes:
            cache.add(episode)

    print("Done")


def process(cache_file):
    """Process the config file, download the podcasts, and store the results
    in the cache_file.
    """
    if not __INITIALIZED:
        raise Exception("Must call initialize() first")

    get_logger().debug("##### Start process " + "#" * 60)

    # Start up our status indicator
    print_dot_thread = threading.Thread(target=print_dots)
    print_dot_thread.daemon = True
    print_dot_thread.start()

    download_dir = get_settings()["download-directory"]
    cache = Cache(get_settings()["cache-file"])

    for podcast in get_settings()["podcasts"]:
        feed = RSSFeed(
            podcast["url"], podcast["title"], podcast["file-prefix"],
            get_settings()["use-date-prefix"])

        _handle_feed(cache, feed, podcast, download_dir)

    print("Done")
