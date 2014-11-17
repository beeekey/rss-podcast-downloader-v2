#!/usr/bin/env python
"""
This module implements the caching interface.
"""
# Imports ######################################################################
from __future__ import print_function
import sqlite3
from rss_podcast_downloader.logger import get_logger


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
            self.cur.execute("CREATE TABLE podcasts(id INTEGER PRIMARY KEY, date REAL, title TEXT, url TEXT, prefix TEXT, filename TEXT);")

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

    def has(self, object, log=True):
        cmd = "SELECT * FROM podcasts WHERE title='%s' AND prefix='%s'" % (object.title, object.prefix)
        self.cur.execute(cmd)
        item = self.cur.fetchone()
        if item:
            return True

        cmd = "SELECT * FROM podcasts WHERE filename='%s'" % object.filename
        self.cur.execute(cmd)
        item = self.cur.fetchone()
        if item:
            return True

        if log:
            self.logger.debug("Couldn't find [%s] in podcasts table" % object.url)

        return False

    def has_filename(self, filename):
        cmd = "SELECT * FROM podcasts WHERE filename='%s'" % filename
        self.cur.execute(cmd)
        item = self.cur.fetchone()
        if item:
            return True
        else:
            self.logger.debug("Couldn't find [%s] in podcasts table" % object.url)
            return False

    def remove_by_filename(self, filename):
        """Removes the entry with the given filename from the cache."""
        cmd = "DELETE FROM podcasts WHERE filename='%s' " % filename
        self.cur.execute(cmd)

    def add(self, object):
        if (self.has(object, log=False)):
            return False

        cmd = "INSERT INTO podcasts(date,title,url,prefix,filename) VALUES('%s', '%s', '%s', '%s', '%s')" % (object.date, object.title, object.url, object.prefix, object.filename)
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
