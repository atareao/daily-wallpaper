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


PARAMS = 'export DISPLAY=:0;\
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus;\
export GSETTINGS_BACKEND=dconf'
SLEEP = 'sleep 5'
EXEC = '/usr/bin/python3'
SCRIPT = '/usr/share/national-geographic-wallpaper/ngdownloader.py'
GSET_GNOME = 'gsettings set org.gnome.desktop.background picture-uri \
"file://%s"'
GSET_MATE = 'gsettings set org.mate.background picture-filename "%s"'
FILE = '/home/%s/.config/national-geographic-wallpaper/potd.jpg'


class Croni(object):
    def __init__(self):
        self.cron = CronTab(user=True)
        params = PARAMS % os.getegid()
        filename = FILE % os.getlogin()
        if os.environ.get("GNOME_DESKTOP_SESSION_ID"):
            gset = GSET_GNOME % filename
        elif os.environ.get("DESKTOP_SESSION") == "mate":
            gset = GSET_MATE % filename
        else:
            gset = None
        if gset is not None:
            self.command = '{0};{1};{2} {3} && {4}'.format(SLEEP, params,
                                                           EXEC, SCRIPT, gset)
        else:
            self.command = None

    def __set_job(self, command, comment):
        if command is None:
            return
        job = self.cron.new(command=command, comment=comment)
        if comment == 'NGW_REBOOT':
            job.every_reboot()
        else:
            job.hour.on(1)
        job.enable()

    def set_jobs(self):
        self.unset_jobs()
        self.__set_job(self.command, 'NGW_REBOOT')
        self.__set_job(self.command, 'NGW_AT_ONE')
        self.cron.write()

    def unset_jobs(self):
        self.cron.remove_all(comment='NGW_REBOOT')
        self.cron.remove_all(comment='NGW_AT_ONE')
        self.cron.write()

    def is_enabled(self):
        for job in self.cron.find_comment('NGW_REBOOT'):
            return job.is_enabled()
        return False


if __name__ == '__main__':
    croni = Croni()
    croni.set_jobs()
