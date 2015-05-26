#!/usr/bin/env python
"""
This module holds the representation of the RSS feed.
"""
# Imports ######################################################################
from __future__ import print_function
import re
import time
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from xml.dom.minidom import parseString
from .episode import Episode
from .logger import get_logger


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
class RSSFeed:
    def __init__(self, url, title, prefix, use_date_prefix=False):
        self.episodes = []
        self.url = url
        self.title = title
        self.prefix = prefix
        self.use_date_prefix = use_date_prefix
        self.download()
        self.parse()

    def __str__(self):
        return "RSSFeed '%s' (%i episodes)" % (self.title, len(self.episodes))

    def download(self):
        """Downloads the RSS feed."""
        file = urllib2.urlopen(self.url)
        data = file.read()
        file.close()
        self.dom = parseString(data)

    def parse(self):
        """Parses the already-downloaded feed.

        This function returns a list of episodes in the feed.
        """
        items = self.dom.getElementsByTagName('item')
        for item in items:
            enclosure = item.getElementsByTagName('enclosure').item(0)
            title = item.getElementsByTagName('title').item(0)

            if (enclosure and title):
                url = enclosure.getAttribute('url')

                try:
                    url = re.search('(.*\.mp3).*', url).group(1)
                except AttributeError as e:
                    get_logger().debug("Couldn't parse url [%s]: %s", url, e)
                    continue

                title = title.toxml().replace('<title>', '').replace('</title>', '')
                title = re.sub("'", "", title)

                episode = Episode(time.time(), title, url, self.prefix, self.title, use_date_prefix=self.use_date_prefix)
                self.episodes.append(episode)

        get_logger().debug("found [%i] episode(s) in [%s]", len(self.episodes), self.title)
