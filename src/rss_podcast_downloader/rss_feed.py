#!/usr/bin/env python
"""
This module holds the representation of the RSS feed.
"""
# Imports ######################################################################

import re
import time
import datetime as dt

from rss_podcast_downloader import get_logger
from rss_podcast_downloader.episode import Episode

try:
    import urllib2
except ImportError:
    import urllib.request, urllib.error, urllib.parse
from xml.dom.minidom import parseString


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

        if self.dom:
            self.parse()

    def __str__(self):
        return "RSSFeed '%s' (%i episodes)" % (self.title, len(self.episodes))

    def download(self):
        """Downloads the RSS feed."""
        try:
            file = urllib.request.urlopen(self.url)
        except urllib.error.HTTPError as e:
            get_logger().error("Couldn't download [%s]: %s", self.url, e)
            self.dom = None
            return

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
            release_date = item.getElementsByTagName('pubDate').item(0)
            release_date = release_date.toxml().replace('<pubDate>', '').replace('</pubDate>', '')

            # convert the string date 'Fri, 25 Jun 2021 06:00:00 +0200' to a datetime object
            release_date = dt.datetime.strptime(release_date, '%a, %d %b %Y %H:%M:%S %z')
            print(release_date)

            if (enclosure and title):
                url = enclosure.getAttribute('url')

                title = title.toxml().replace('<title>', '').replace('</title>', '')
                title = re.sub("'", "", title)

                episode = Episode(release_date, title, url, self.prefix, self.title, use_date_prefix=self.use_date_prefix)
                self.episodes.append(episode)

        # get_logger().debug("found [%i] episode(s) in [%s]", len(self.episodes), self.title)
        print("found [%i] episode(s) in [%s]", len(self.episodes), self.title)


if __name__ == '__main__':
    feed = RSSFeed("https://feeds.br.de/anna-und-die-wilden-tiere/feed.xml", "Anna und die wilden Tiere", "anna-wt", use_date_prefix=False)
    print(feed)
    print(feed.episodes[0])
    print(feed.episodes[-1])