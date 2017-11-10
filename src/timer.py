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

import os
from caseconfigparser import CaseConfigParser
from os.path import expanduser


class Timer(object):
    def __init__(self):
        home = expanduser("~")
        timer_dir = os.path.join(home, '.config', 'systemd', 'user')
        if not os.path.exists(timer_dir):
            os.makedirs(timer_dir)
        self.timer_file = os.path.join(
            timer_dir, 'national-geographic-wallpaper.timer')

    def create(self):
        config = CaseConfigParser()
        config['Unit'] = {
            'Description': 'National Geographic Wallpaper Timer'
        }
        config['Timer'] = {
            'OnBootSec': '5s',
            'OnUnitActiveSec': '12h',
            'Unit': 'national-geographic-wallpaper.service'
        }
        config['Install'] = {
            'WantedBy': 'national-geographic-wallpaper.service'
        }
        with open(self.timer_file, 'w') as configfile:
            config.write(configfile)

    def delete(self):
        if not os.path.exists(self.timer_file):
            os.remove(self.timer_file)


if __name__ == '__main__':
    timer = Timer()
    timer.timer()
