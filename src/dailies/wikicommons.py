#!/usr/bin/env python3
#
# This file is part of daily-wallpaper
#
# Copyright (c) 2021 Ahmad Gharbeia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

__author__ = 'Ahmad Gharbeia'
__email__ = 'ahmad@gharbeia.org'
__copyright__ = 'Copyright (c) 2021 Ahmad Gharbeia'
__license__ = 'GPLV3'
__url__ = 'https://ahmad.gharbeia.org'
__version__ = '0.1.0'

import requests
import os
import sys

if __file__.startswith('/usr') or os.getcwd().startswith('/usr'):
    sys.path.insert(1, '/usr/share/daily-wallpaper')
else:
    sys.path.insert(1, os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..')))

from daily import Daily
from comun import _

def get_daily():
    return Wikicommons()


class Wikicommons(Daily):
    _id = __name__
    _name = _('Wikimedia Commons')

    ENDPOINT = 'https://commons.wikimedia.org/w/api.php'
    SESSION = requests.Session()

    def __init__(self):
        Daily.__init__(self)
        
    def resolve_url(self):
        try:
            metadata = next(
               iter(
                (self.SESSION.get(
                  url = self.ENDPOINT,
                  params = {
                    'action': 'query',
                    'format': 'json',
                    'prop': 'imageinfo',
                    'iiprop': 'url|extmetadata',
                    'titles': self.SESSION.get(
                        url = self.ENDPOINT,
                        params = {
                          'action': 'query',
                          'format': 'json',
                          'formatversion': '2',
                          'prop': 'images',
                          'titles': 'Commons:Picture_of_the_day'
                        }).json()['query']['pages'][0]['images'][0]['title']
                  }).json()['query']['pages']).values()))
            self._title = metadata['title']
            self._url = metadata['imageinfo'][0]['url']
            extmetadata = metadata['imageinfo'][0]['extmetadata']
            self._caption = extmetadata['ImageDescription']['value']
            self._credit = extmetadata['Credit']['value']
            return True
        except Exception as exception:
            print(exception)
        return False


if __name__ == '__main__':
    daily = get_daily()
    if daily.resolve_url():
        print(daily)
