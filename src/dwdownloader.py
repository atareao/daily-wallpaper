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

import gi
try:
    gi.require_version('Notify', '0.7')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Notify
import requests
import os
import sys
import importlib
from random import randrange
import tempfile
import hashlib
import shutil
import comun
from config import Configuration
from comun import get_desktop_environment, get_modules
from comun import _
from plumbum import local

sys.path.insert(1, comun.DAILIESDIR)
sys.path.insert(1, comun.USERDAILIESDIR)


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def set_background(afile=None):
    if afile and os.path.exists(afile):
        local.env['DISPLAY'] = ':0'
        local.env['GSETTINGS_BACKEND'] = 'dconf'
        gsettings = local['gsettings']
        desktop_environment = get_desktop_environment()
        if desktop_environment == 'gnome' or \
                desktop_environment == 'unity' or \
                desktop_environment == 'budgie-desktop':
            gsettings['set', 'org.gnome.desktop.background', 'picture-uri',
                      'file://{}'.format(afile)]()
        elif desktop_environment == "mate":
            gsettings['set', 'org.mate.desktop.background', 'picture-filename',
                      '\'{}\''.format(afile)]()
        elif desktop_environment == "cinnamon":
            gsettings['set', 'org.cinnamon.desktop.background', 'picture-uri',
                      'file://{}'.format(afile)]()


def notify_photo_caption(title, caption=None, credit=None):
    if caption:
        caption = max_length(caption, 60) if len(caption) > 60 else caption
        for m in ['<p>', '</p>', '<br>', '<br />']:
            caption = caption.replace(m, '')
        if credit:
            caption = '\n{}\n\n<i>{}</i>: {}'.format(caption,
                                                     _('Photo credit'),
                                                     credit)
    else:
        caption = ''
    try:
        Notify.init(title)
        info = Notify.Notification.new(title, caption, 'dialog-information')
        info.set_timeout(Notify.EXPIRES_DEFAULT)
        info.set_urgency(Notify.Urgency.LOW)
        info.show()
    except Exception as e:
        print(e)


def download(url):
    if url.startswith('file://'):
        filename = url[7:]
        if os.path.exists(filename):
            if os.path.exists(comun.POTD):
                md5_new = md5(filename)
                md5_old = md5(comun.POTD)
                if md5_old == md5_new:
                    return False
            shutil.copy(filename, comun.POTD)
            return True
        return False
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            if os.path.exists(comun.POTD):
                md5_old = md5(comun.POTD)
                tempfilename = tempfile.NamedTemporaryFile().name
                with open(tempfilename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                md5_new = md5(tempfilename)
                if md5_old == md5_new:
                    os.remove(tempfilename)
                else:
                    os.remove(comun.POTD)
                    shutil.move(tempfilename, comun.POTD)
                    return True
            else:
                with open(comun.POTD, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                    return True
    except Exception as e:
        print(e)
    return False


def change_wallpaper():
    config = Configuration()
    if config.get('random'):
        sources = config.get('source')
        source = sources[randrange(len(sources))]
    else:
        source = config.get('source')[0]
    module = importlib.import_module(source)
    daily = module.get_daily()
    if daily.resolve_url():
        if download(daily.get_url()):
            if daily.get_title():
                title = '{}: {}'.format(daily.get_name(), daily.get_title())
            else:
                title = daily.get_name()
            caption = daily.get_caption()
            credit = daily.get_credit()
            notify_photo_caption(title, caption, credit)
            set_background(comun.POTD)


def max_length(astring, max_length):
    phrase = ''
    description = []
    for chain in astring.split(' '):
        if len(phrase) == 0:
            new_phrase = chain
        else:
            new_phrase = phrase + ' ' + chain
        if len(new_phrase) > max_length:
            description.append(phrase)
            phrase = chain
        else:
            phrase = new_phrase
    if len(phrase) > 0 and description[-1] != phrase:
        description.append(phrase)
    return '\n'.join(description)


if __name__ == '__main__':
    change_wallpaper()
    exit(0)
