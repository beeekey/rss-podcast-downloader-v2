#!/usr/bin/env python2.7
"""
This module holds the representation of a single podcast episode.
"""

# Imports ######################################################################
from __future__ import print_function
import re
import urllib2
from rss_podcast_downloader.logger import get_logger


# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"

# Globals ######################################################################
DEBUG = False


class Episode:
    def __init__(self, date, title, url, prefix, feed_title):
        self.url = url
        self.title = title
        self.prefix = prefix
        self.date = date
        self.feed_title = feed_title
        self.logger = get_logger()

    def __repr__(self):
        return "<Episode url:[%s] title:[%s] filename:[%s] feed:[%s]>" % (self.url, self.title, self.Filename(), self.feed_title)

    def filename(self):
        ## The purpose of this function is to normalize the title into something that
        ## won't be an issue for the file-system, or using the file later on.
        temp_title = re.sub('[-\'#,:\.!\?"]', '', self.title)   # There's probably more needed here, but it's just convenience
        temp_title = re.sub('&.*?;', '', temp_title)            # URL Escapes
        temp_title = re.sub(r'[/\\]', '-', temp_title)          # Path characters mess up the filename
        temp_title = re.sub(' ', '-', temp_title)
        temp_title += '.mp3'
        return self.prefix + '-' + temp_title.lower()

    def download(self, directory):
        try:
            mp3file = urllib2.urlopen(self.url)
            output = open("%s/%s" % (directory, self.Filename()), 'wb')
            output.write(mp3file.read())
            output.close()
        except Exception as e:
            self.logger.error(str(e))
            self.logger.debug(e, exc_info=True)
            raise e
