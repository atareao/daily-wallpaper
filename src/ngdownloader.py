#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of national-geographic-background
#
# Copyright (C) 2017
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Dependencies:
# python3-cssselect

import requests
import os
from lxml.html import fromstring
import datetime
import comun
from gi.repository import Gio
from gi.repository import GLib

URL = 'http://www.nationalgeographic.com/photography/photo-of-the-day/'


def set_background(afile=None):
    if os.environ.get("GNOME_DESKTOP_SESSION_ID"):
        gso = Gio.Settings.new('org.gnome.desktop.background')
        if afile and os.path.exists(afile):
            variant = GLib.Variant('s', 'file://%s' % (afile))
            gso.set_value('picture-uri', variant)
    elif os.environ.get("DESKTOP_SESSION") == "mate":
        gso = Gio.Settings.new('org.mate.background')
        if afile and os.path.exists(afile):
            variant = GLib.Variant('s', afile)
            gso.set_value('picture-filename', variant)


def main():
    r = requests.get(URL)
    if r.status_code == 200:
        doc = fromstring(r.text)
        for meta in doc.cssselect('meta'):
            prop = meta.get('property')
            if prop == 'og:image':
                image_url = meta.get('content')
                print(image_url)
                r = requests.get(image_url, stream=True)
                print(r.status_code)
                if r.status_code == 200:
                    with open(comun.POTD, 'wb') as f:
                        for chunk in r.iter_content(1024):
                            f.write(chunk)
                    set_background(comun.POTD)


if __name__ == '__main__':
    main()
    today = datetime.date.today()
    print(today.strftime('%Y%M%d'))
    exit(0)
