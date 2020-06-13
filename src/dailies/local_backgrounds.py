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

import os
import sys
import mimetypes
import random

if __file__.startswith('/usr') or os.getcwd().startswith('/usr'):
    sys.path.insert(1, '/usr/share/daily-wallpaper')
else:
    sys.path.insert(1, os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..')))

from daily import Daily
from comun import _

DIR = '/usr/share/backgrounds'


def get_daily():
    return LocalBackgrounds()


def get_list_of_files(dirname):
    list_of_file = os.listdir(dirname)
    files = list()
    for entry in list_of_file:
        path = os.path.join(dirname, entry)
        if os.path.isdir(path):
            files = files + get_list_of_files(path)
        else:
            if mimetypes.guess_type(path)[0] in ['image/png', 'image/jpeg']:
                files.append(path)
    return files


class LocalBackgrounds(Daily):
    _id = __name__
    _name = _('Local backgrounds')

    def __init__(self):
        Daily.__init__(self)

    def resolve_url(self):
        list_of_files = get_list_of_files(DIR)
        if list_of_files:
            selected = random.randint(0, len(list_of_files) - 1)
            self._url = 'file://' + list_of_files[selected]
            return True
        return False


if __name__ == '__main__':
    daily = get_daily()
    if daily.resolve_url():
        print(daily)
