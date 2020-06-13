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
