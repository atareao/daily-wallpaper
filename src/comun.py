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
import locale
import gettext
from plumbum import local
import re
from pathlib import Path

__author__ = 'Lorenzo Carbonell <lorenzo.carbonell.cerezo@gmail.com>'
__copyright__ = 'Copyright (c) 2017 Lorenzo Carbonell'
__license__ = 'GPLV3'
__url__ = 'http://www.atareao.es'
__version__ = '0.1.0'
VERSION = __version__
APP = 'daily-wallpaper'
APPNAME = APP
APP_CONF = APP + '.conf'
CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config')
CONFIG_APP_DIR = os.path.join(CONFIG_DIR, APP)
CONFIG_FILE = os.path.join(CONFIG_APP_DIR, APP_CONF)
POTD = os.path.join(CONFIG_APP_DIR, 'potd.jpg')
PARAMS = {
    'random': True,
    'source': []
}
# check if running from source
if str(Path(__file__).parent.absolute()).startswith('/usr'):
    SHAREDIR = os.path.join('/usr', 'share')
    APPDIR = os.path.join(SHAREDIR, APP)
    LANGDIR = os.path.join(SHAREDIR, 'locale-langpack')
    ICONDIR = os.path.join(SHAREDIR, 'icons', 'hicolor', 'scalable', 'apps')
    DAILIESDIR = os.path.join(APPDIR, 'dailies')
    NGD = os.path.join(APPDIR, 'dwdownloader.py')
else:
    VERSION = VERSION + '-src'
    ROOTDIR = os.path.dirname(__file__)
    LANGDIR = os.path.normpath(os.path.join(ROOTDIR, '../po'))
    APPDIR = ROOTDIR
    ICONDIR = os.path.normpath(
        os.path.join(ROOTDIR, '../data/icons/hicolor/scalable/apps'))
    DAILIESDIR = os.path.join(APPDIR, 'dailies')
    NGD = os.path.join(APPDIR, 'dwdownloader.py')

USERDAILIESDIR = os.path.expanduser('~/.config/daily-wallpaper/dailies')
ICON = os.path.join(ICONDIR, APP + '.svg')

try:
    current_locale, encoding = locale.getdefaultlocale()
    language = gettext.translation(APP, LANGDIR, [current_locale])
    language.install()
    _ = language.gettext
except Exception as e:
    print(e)
    _ = str


def is_running(process):
    ps = local['ps']
    result = ps['asw']()
    return re.search(process, result)


def get_desktop_environment():
    desktop_session = os.environ.get("DESKTOP_SESSION")
    if desktop_session is not None:
        desktop_session = desktop_session.lower()
        if desktop_session in ["gnome", "unity", "cinnamon",
                               "budgie-desktop", "xfce4", "lxde", "fluxbox",
                               "blackbox", "openbox", "icewm", "jwm",
                               "afterstep", "trinity", "kde"]:
            return desktop_session
        if "xfce" in desktop_session or\
                desktop_session.startswith("xubuntu"):
            return "xfce4"
        if desktop_session.startswith("ubuntu"):
            return "unity"
        if desktop_session.startswith("lubuntu"):
            return "lxde"
        if desktop_session.startswith("kubuntu"):
            return "kde"
        if desktop_session.startswith("razor"):  # e.g. razorkwin
            return "razor-qt"
        if desktop_session.startswith("wmaker"):  # eg. wmaker-common
            return "windowmaker"
    if os.environ.get('KDE_FULL_SESSION') == 'true':
        return "kde"
    elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        if "deprecated" not in os.environ.get(
                'GNOME_DESKTOP_SESSION_ID'):
            return "gnome2"
    elif is_running("xfce-mcs-manage"):
        return "xfce4"
    elif is_running("ksmserver"):
        return "kde"
    return "unknown"


def get_modules():
    p = Path(DAILIESDIR)
    modules = [x.stem for x in p.glob('**/*.py') if x.is_file()]
    up = Path('~/.config/daily-wallpaper/dailies').expanduser()
    modules += [x.stem for x in up.glob('**/*.py') if x.is_file()]
    modules.sort()
    return modules
