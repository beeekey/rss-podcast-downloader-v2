#!/usr/bin/env python
"""
This module implements the caching interface.
"""
# Imports ######################################################################
from __future__ import print_function
import sqlite3
from rss_podcast_downloader.logger import get_logger
from rss_podcast_downloader.episode import Episode

# Metadata #####################################################################
__author__ = "Timothy McFadden"
__date__ = "11/16/2014"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "1.0.0dev"


# Globals ######################################################################
class Cache:
    def __init__(self, cache_file):
        self.logger = get_logger()
        self.filename = cache_file
        self.conn = sqlite3.connect(self.filename)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("SELECT * FROM podcasts")
        except:
            self.logger.warn("Creating the podcasts table")
            self.cur.execute("CREATE TABLE podcasts(id INTEGER PRIMARY KEY, date REAL, title TEXT, url TEXT, prefix TEXT);")

        try:
            self.cur.execute("SELECT * FROM sync_date")
            (id, date) = self.cur.fetchone()

        except Exception:
            self.logger.warn("Creating sync_date table")
            self.cur.execute("CREATE TABLE sync_date(id INTEGER, date REAL);")
            self.cur.execute("INSERT INTO sync_date(id,date) VALUES('0','0');")

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def has(self, object):
        cmd = "SELECT * FROM podcasts WHERE title='%s' AND prefix='%s'" % (object.title, object.prefix)
        self.cur.execute(cmd)
        try:
            (id, date, title, url, prefix) = self.cur.fetchone()
            return Episode(date, title, url, prefix, '')
        except Exception as e:
            self.logger.debug("Couldn't find [%s] in podcasts table: [%s]" % (object.url, e))
            return None

    def add(self, object):
        if (self.Has(object)):
            return False

        cmd = "INSERT INTO podcasts(date,title,url,prefix) VALUES('%s', '%s', '%s', '%s')" % (object.date, object.title, object.url, object.prefix)
        self.cur.execute(cmd)
        return True

    def sync_date(self, date=None):
        if (date is None):
            cmd = "SELECT * FROM sync_date WHERE id='0'"
            self.cur.execute(cmd)
            (id, date) = self.cur.fetchone()
            self.logger.debug("SyncDate returning [%s]" % date)
            return date
        else:
            cmd = "UPDATE sync_date SET date='%s' WHERE id='0'" % date
            self.cur.execute(cmd)
