#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of national-geographic-wallpaper
#
# Copyright (C) 2017-2018
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
import configparser
from os.path import expanduser


class Autostart(object):
    def __init__(self, autostart=True):
        home = expanduser("~")
        autostart_dir = os.path.join(home, '.config', 'autostart')
        if not os.path.exists(autostart_dir):
            os.makedirs(autostart_dir)
        self.autostart_file = os.path.join(
            autostart_dir, 'national-geographic-wallpaper.desktop')
        self.autostart = autostart

    def create(self, autostart=None):
        if autostart is None:
            autostart = self.autostart
        execfile = '/usr/share/national-geographic-wallpaper/ngdownloader.py'
        config = configparser.ConfigParser()
        config['Desktop Entry'] = {
            'Type': 'Application',
            'Version': '1.0',
            'Name': 'National Geographic Wallpaper',
            'Exec': '/usr/bin/python3 {0}'.format(execfile),
            'Hidden': 'false',
            'NoDisplay': 'false',
            'Terminal': 'false',
            'StartupNotify': 'false',
            'X-GNOME-Autostart-enabled': str(autostart).lower(),
            'X-GNOME-Autostart-Delay': 5,
            'X-GNOME-Autostart-Phase': 'Applications',
            'X-MATE-Autostart-enabled': str(autostart).lower(),
            'X-MATE-Autostart-Delay': 5,
            'X-MATE-Autostart-Phase': 'Applications',
            'NGV': '1.0'
        }
        with open(self.autostart_file, 'w') as configfile:
            config.write(configfile)

    def set_autostart(self, autostart):
        self.autostart = autostart
        if not os.path.exists(self.autostart_file):
            self.create(autostart)
        else:
            config = configparser.ConfigParser()
            config.read(self.autostart_file)
            config['Desktop Entry']['X-GNOME-Autostart-enabled'] = \
                str(autostart).lower()
            config['Desktop Entry']['X-MATE-Autostart-enabled'] = \
                str(autostart).lower()
            with open(self.autostart_file, 'w') as configfile:
                config.write(configfile)

    def get_autostart(self):
        if not os.path.exists(self.autostart_file):
            self.create(False)
            return False
        config = configparser.ConfigParser()
        config.read(self.autostart_file)
        if config['Desktop Entry']['X-GNOME-Autostart-enabled'] == 'true':
            return True
        return False


if __name__ == '__main__':
    autostart = Autostart()
    # autostart.create()
    autostart.set_autostart(False)
    print(autostart.get_autostart())
