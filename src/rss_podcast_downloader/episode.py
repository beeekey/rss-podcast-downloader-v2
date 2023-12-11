#!/usr/bin/env python2.7
"""
This module holds the representation of a single podcast episode.
"""

# Imports ######################################################################


from slugify import slugify
from time import strftime, time, localtime
from rss_podcast_downloader.logger import get_logger

try:
    import urllib.request as urllib2
except ImportError:
    import urllib.request, urllib.error, urllib.parse

try:
    from html.parser import HTMLParser
except ImportError:
    from html.parser import HTMLParser


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014-2015"
__license__ = "MIT"
__version__ = "1.0.0dev"

# Globals ######################################################################
DEBUG = False


class Episode:
    def __init__(self, date, title, url, prefix, feed_title, use_date_prefix=False):
        self.url = url

        # Remove all non-ascii-printable characters from the title (cuz I'm lazy)
        self.title = ''.join(x for x in title if 32 <= ord(x) <= 126)
        self.title = HTMLParser().unescape(self.title)

        self.prefix = prefix
        self.date = date or time.time()
        self.feed_title = feed_title
        self.use_date_prefix = use_date_prefix
        self.logger = get_logger()

    def __repr__(self):
        return "<Episode url:[%s] title:[%s] filename:[%s] feed:[%s]>" % (self.url, self.title, self.filename, self.feed_title)

    @property
    def filename(self):
        # The purpose of this function is to normalize the title into something that
        # won't be an issue for the file-system, or using the file later on.
        temp_title = slugify(self.title)
        temp_title += '.mp3'

        if self.use_date_prefix:
            return self.prefix + '-' + strftime("%Y%m%d-", localtime(self.date)) + temp_title.lower()
        else:
            return self.prefix + '-' + temp_title.lower()

    def download(self, directory):
        try:
            mp3file = urllib.request.urlopen(self.url)
            output = open("%s/%s" % (directory, self.filename), 'wb')
            output.write(mp3file.read())
            output.close()
        except Exception as e:
            self.logger.error(str(e))
            self.logger.debug(e, exc_info=True)
            raise e
