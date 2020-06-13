#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of daily-wallpaper
#
# Copyright (c) 2017 Lorenzo Carbonell Cerezo <a.k.a. atareao>
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

URL = 'https://www.bing.com{}'


def get_daily():
    return Bing()


class Bing(Daily):
    _id = __name__
    _name = _('Bing')

    def __init__(self):
        Daily.__init__(self)

    def resolve_url(self):
        url = URL.format('/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=en-US')
        try:
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                urlbase = data['images'][0]['urlbase']
                self._url = URL.format('{}_1920x1200.jpg'.format(urlbase))
                self._title = data['images'][0]['title']
                self._credit = data['images'][0]['copyright']
                return True
        except Exception:
            pass
        return False


if __name__ == '__main__':
    daily = get_daily()
    if daily.resolve_url():
        print(daily)
