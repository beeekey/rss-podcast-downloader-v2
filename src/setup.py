#!/usr/bin/env python
'''rss-podcast-downloader package setup script.'''
from __future__ import print_function
import os
import re
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: This package requires setuptools in order to install.", file=sys.stderr)
    sys.exit(1)

THIS_DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(THIS_DIR, 'rss_podcast_downloader', '__init__.py')


# Read the version from our project.  There are various ways of doing this, but
# scraping the file has the least problems across Python versions 2.6 through
# 3.4.
def scrape_version(path=VERSION_FILE):
    re_version = re.compile("^(VERSION|__version__)\s*=\s*['\"](.*?)['\"]")

    with open(path, 'rb') as fh:
        for line in fh:
            if re_version.match(line):
                return re_version.match(line).group(2)

    raise Exception("Can't find version in [{}]".format(path))


if __name__ == '__main__':
    setup(
        name="rss-podcast-downloader",
        version=scrape_version(),
        description="Data rss-podcast-downloader package",
        author="Timothy McFadden",
        url="https://github.com/mtik00/rss-podcast-downloader",
        install_requires=['persistent_pineapple'],
        packages=find_packages(),
        package_data={"rss-podcast-downloader": ['.*']},
        zip_safe=True,
        include_package_data=True,
        test_suite="tests",

        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Other Environment',
            'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Intended Audience :: Developers',
            'Environment :: Console',
            'Natural Language :: English',
            'Operating System :: OS Independent',
        ],

        long_description=open(os.path.join(THIS_DIR, "README.rst"), 'r').read()
    )
