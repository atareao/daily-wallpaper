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
import re
import json

if __file__.startswith('/usr') or os.getcwd().startswith('/usr'):
    sys.path.insert(1, '/usr/share/daily-wallpaper')
else:
    sys.path.insert(1, os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..')))
from daily import Daily
from comun import _

URL = 'https://www.nationalgeographic.com/photography/photo-of-the-day/{}'
URL = 'https://www.nationalgeographic.com/photo-of-the-day/'


def get_daily():
    return NationalGeographic()


class NationalGeographic(Daily):
    _id = __name__
    _name = _('National Geographic')

    def __init__(self):
        Daily.__init__(self)

    def resolve_url(self):
        url = URL.format('_jcr_content/.gallery.json')
        url = URL.format("index.html")
        url = URL
        try:
            r = requests.get(url, allow_redirects=True)
            if r.status_code == 200:
                pattern = r"window\['__natgeo__'\]=(.*);\s*</script>"
                data = re.findall(pattern, r.text)
                if len(data) > 0:
                    data = json.loads(data[0])
                    if 'page' in data and \
                            'content' in data['page'] and \
                            'mediaspotlight' in data['page']['content'] and \
                            'frms' in data['page']['content']['mediaspotlight']:
                        frames = data['page']['content']['mediaspotlight']['frms']
                        if len(frames) > 0 and \
                                'mods' in frames[0] and \
                                len(frames[0]['mods']) > 0 and \
                                'edgs' in frames[0]['mods'][0] and \
                                len(frames[0]['mods'][0]['edgs']) > 1 and \
                                'media' in frames[0]['mods'][0]['edgs'][1]:
                            media = frames[0]['mods'][0]['edgs'][1]['media']
                            if len(media) > 0 and 'img' in media[0]:
                                photo = media[0]['img']
                                self._url = photo['src']
                                self._title = photo['altText']
                                self._caption = photo['dsc']
                                self._credit = photo['crdt']
                                return True
            else:
                print(r.status_code)
        except Exception as exception:
            print(exception)
        return False


if __name__ == '__main__':
    daily = get_daily()
    if daily.resolve_url():
        print(daily)
