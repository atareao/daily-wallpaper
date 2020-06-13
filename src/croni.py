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
from crontab import CronTab
from comun import get_desktop_environment

PARAMS = 'export DISPLAY=:0;\
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus;\
export GSETTINGS_BACKEND=dconf'
EXEC = '/usr/bin/python3'
SCRIPT = '/usr/share/daily-wallpaper/dwdownloader.py'
GSET_GNOME = 'gsettings set org.gnome.desktop.background picture-uri \
"file://%s"'
GSET_MATE = 'gsettings set org.mate.background picture-filename "%s"'
GSET_CINNAMON = 'gsettings set org.cinnamon.desktop.background picture-uri \
"file://%s"'
FILE = '.config/daily-wallpaper/potd.jpg'
NO_OUTPUT = '>/dev/null 2>&1'


class Croni(object):
    def __init__(self):
        self.cron = CronTab(user=True)
        params = PARAMS % os.getuid()
        filename = os.path.join(os.path.expanduser('~'), FILE)
        desktop_environment = get_desktop_environment()
        if desktop_environment == 'gnome' or \
                desktop_environment == 'unity' or \
                desktop_environment == 'budgie-desktop':
            gset = GSET_GNOME % filename
        elif desktop_environment == "mate":
            gset = GSET_MATE % filename
        elif desktop_environment == "cinnamon":
            gset = GSET_CINNAMON % filename
        else:
            gset = None
        if gset is not None:
            self.command = 'sleep 20;{0};{1} {2} {4} && {3} {4}'.format(
                params, EXEC, SCRIPT, gset, NO_OUTPUT)
        else:
            self.command = None

    def set_jobs(self):
        self.unset_jobs()
        if self.command is not None:
            job = self.cron.new(command=self.command,
                                comment='NGW_EVERY_TWELVE')
            job.hour.every(12)
            job.minute.on(5)
            job.enable()
            self.cron.write()

    def unset_jobs(self):
        self.cron.remove_all(comment='NGW_EVERY_TWELVE')
        self.cron.write()

    def is_enabled(self):
        for job in self.cron.find_comment('NGW_EVERY_TWELVE'):
            if job.is_enabled():
                return True
        return False


if __name__ == '__main__':
    croni = Croni()
    print(croni.is_enabled())
