#!/usr/bin/env python
__author__ = "Timothy McFadden"
__date__ = "99/99/9999"
__copyright__ = "Timothy McFadden, 2014"
__license__ = "MIT"
__version__ = "0.01"
"""
This is the unit test for SAMPEPROJ.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import rss_podcast_downloader


class Test(unittest.TestCase):

    def test_f1(self):
        rss_podcast_downloader.f1("testing")


if __name__ == '__main__':
    unittest.main()
