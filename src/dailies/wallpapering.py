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
from lxml.html import fromstring
from random import randint
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

URL = 'https://www.socwall.com/{}'


def get_daily():
    return Wallpapering()


class Wallpapering(Daily):
    _id = __name__
    _name = _('Social Wallpapering')

    def __init__(self):
        Daily.__init__(self)

    def resolve_url(self):
        try:
            r = requests.get(URL.format(''))
            if r.status_code == 200:
                doc = fromstring(r.text)
                results = doc.cssselect('li.pageNumber a')
                page = randint(1, int(results[-1].text))
                url = URL.format('wallpapers/page:{}/'.format(page))
                r = requests.get(url)
                if r.status_code == 200:
                    doc = fromstring(r.text)
                    results = doc.cssselect(
                        'ul.wallpaperList li.wallpaper a.image')
                    if len(results) > 0:
                        image = randint(0, len(results) - 1)
                        url = URL.format(results[image].attrib['href'][1:])
                        r = requests.get(url)
                        if r.status_code == 200:
                            doc = fromstring(r.text)
                            results = doc.cssselect(
                                'div.wallpaperProfile div.wallpaper \
        a.wallpaperImageLink')
                            if len(results) > 0:
                                self._url = URL.format(
                                    results[0].attrib['href'][1:])
                                return True
        except Exception as exception:
            print(exception)
        return False


if __name__ == '__main__':
    daily = get_daily()
    if daily.resolve_url():
        print(daily)
