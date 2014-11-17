#!/usr/bin/env python
'''rss-podcast-downloader package setup script.'''
from __future__ import print_function
import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print("ERROR: This package requires setuptools in order to install.", file=sys.stderr)
    sys.exit(1)


# Read the version from our project
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
PKG_DIR = os.path.join(THIS_DIR, 'src')
sys.path.insert(0, PKG_DIR)
from rss_podcast_downloader import __version__


if __name__ == '__main__':
    setup(
        name="rss-podcast-downloader",
        version=__version__,
        description="Data rss-podcast-downloader package",
        author="Timothy McFadden",
        url="https://github.com/mtik00/rss-podcast-downloader",
        install_requires=[],  # ['persistent-pineapple >= 0.0.0.2'],
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
