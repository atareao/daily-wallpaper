#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of national-geographic-wallpaper
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

import os
from crontab import CronTab
from comun import get_desktop_environment

PARAMS = 'export DISPLAY=:0;\
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus;\
export GSETTINGS_BACKEND=dconf'
SLEEP = 'sleep 5'
EXEC = '/usr/bin/python3'
SCRIPT = '/usr/share/national-geographic-wallpaper/ngdownloader.py'
GSET_GNOME = 'gsettings set org.gnome.desktop.background picture-uri \
"file://%s"'
GSET_MATE = 'gsettings set org.mate.background picture-filename "%s"'
GSET_CINNAMON = 'gsettings set org.cinnamon.background picture-filename \
"file://%s"'
FILE = '.config/national-geographic-wallpaper/potd.jpg'


class Croni(object):
    def __init__(self):
        self.cron = CronTab(user=True)
        params = PARAMS % os.getuid()
        filename = os.path.join(os.path.expanduser('~'), FILE)
        desktop_environment = get_desktop_environment()
        if desktop_environment == 'gnome' or \
                get_desktop_environment() == 'unity':
            gset = GSET_GNOME % filename
        elif desktop_environment == "mate":
            gset = GSET_MATE % filename
        elif desktop_environment == "cinnamon":
            gset = GSET_CINNAMON % filename
        else:
            gset = None
        if gset is not None:
            self.command = '{0};{1};{2} {3} && {4}'.format(SLEEP, params,
                                                           EXEC, SCRIPT, gset)
        else:
            self.command = None

    def set_jobs(self):
        self.unset_jobs()
        if self.command is not None:
            job = self.cron.new(command=self.command,
                                comment='NGW_EVERY_TWELVE')
            job.hour.every(12)
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
