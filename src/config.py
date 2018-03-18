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


class Config(object):
    def __init__(self, autostart=True):
        home = expanduser("~")
        config_dir = os.path.join(home, '.config',
                                  'national-geographic-wallpaper')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        self.config_file = os.path.join(
            config_dir, 'national-geographic-wallpaper.conf')

    def create(self):
        config = configparser.ConfigParser()
        config['Configuration'] = {
            'source': 'gopro'
        }
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def set_source(self, source):
        if not os.path.exists(self.config_file):
            self.create()
        else:
            config = configparser.ConfigParser()
            try:
                config.read(self.config_file)
            except configparser.MissingSectionHeaderError as e:
                print(e)
                self.create()
            config['Configuration']['source'] = source
            with open(self.config_file, 'w') as configfile:
                config.write(configfile)

    def get_source(self):
        if not os.path.exists(self.config_file):
            self.create()
            return 'gopro'
        config = configparser.ConfigParser()
        try:
            config.read(self.config_file)
        except configparser.MissingSectionHeaderError as e:
            print(e)
            self.create()
            return 'gopro'
        return config['Configuration']['source']


if __name__ == '__main__':
    config = Config()
    print(config.get_source())
