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

import gi
try:
    gi.require_version('Gtk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
import os
from crontab import CronTab
import comun


COMMENT = '**national-geographic-wallpaper**'


def set_ngw():
    cron = CronTab(user=True)
    job = cron.new(command=comun.NGD,
                   comment=COMMENT)
    job.every_reboot()
    job.enable(True)
    cron.write()
    job = cron.new(command=comun.NGD,
                   comment=COMMENT)
    job.hour.on(0)
    job.minute.on(15)
    job.enable(True)
    cron.write()


def is_ngw_on():
    cron = CronTab(user=True)
    iter = cron.find_comment(comment=COMMENT)
    for job in iter:
        if job.is_enabled():
            return True
    return False


def unset_ngw():
    cron = CronTab(user=True)
    cron.remove_all(comment=COMMENT)
    cron.write()


class NGW(Gtk.Dialog):  # needs GTK, Python, Webkit-GTK
    def __init__(self):
        Gtk.Dialog.__init__(
            self,
            'National Geographic Wallpaper',
            None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
             Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(350, 80)
        self.set_icon_from_file(comun.ICON)
        self.connect('destroy', self.close_application)
        #
        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        self.get_content_area().add(grid)
        #
        label10 = Gtk.Label('Change wallpaper automatically?:')
        label10.set_alignment(0, 0.5)
        grid.add(label10)
        #
        self.switch = Gtk.Switch()
        self.switch.set_active(is_ngw_on())
        grid.attach(self.switch, 1, 0, 1, 1)
        #
        self.show_all()

    def close_application(self, widget, data=None):
        exit(0)


if __name__ == '__main__':
    if not os.path.exists(comun.CONFIG_APP_DIR):
        os.makedirs(comun.CONFIG_APP_DIR)
    ngw = NGW()
    if ngw.run() == Gtk.ResponseType.ACCEPT:
        ngw.hide()
        unset_ngw()
        if ngw.switch.get_active() is True:
            set_ngw()
    ngw.destroy()
