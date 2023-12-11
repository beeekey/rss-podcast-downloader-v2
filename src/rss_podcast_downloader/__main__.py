
import os
from . import VERSION

if __name__ == '__main__':
    print("rss_podcast_downloader version [%s] from [%s]" % (VERSION, os.path.dirname(os.path.abspath(__file__))))
