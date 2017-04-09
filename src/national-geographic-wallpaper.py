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
import comun
import shutil
from configurator import Configuration
from ngdownloader import change_wallpaper

COMMENT = '**national-geographic-wallpaper**'
FILESTART = os.path.join(os.getenv("HOME"), ".config/autostart/\
national-geographic-wallpaper-autostart.desktop")


def select_value_in_combo(combo, value):
    model = combo.get_model()
    for i, item in enumerate(model):
        if value == item[1]:
            combo.set_active(i)
            return
    combo.set_active(0)


def get_selected_value_in_combo(combo):
    model = combo.get_model()
    return model.get_value(combo.get_active_iter(), 1)


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

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        self.get_content_area().add(grid)

        label10 = Gtk.Label('Change wallpaper automatically?:')
        label10.set_alignment(0, 0.5)
        grid.add(label10)

        self.switch = Gtk.Switch()
        os.path.exists(FILESTART)
        self.switch.set_active(os.path.exists(FILESTART))
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(self.switch, False, False, 0)
        grid.attach(hbox, 1, 0, 1, 1)

        label20 = Gtk.Label('Select backgrounds source:')
        label20.set_alignment(0, 0.5)
        grid.attach(label20, 0, 1, 1, 1)

        source_store = Gtk.ListStore(str, str)
        source_store.append(['National Geographic', 'national-geographic'])
        source_store.append(['Bing', 'bing'])
        source_store.append(['GoPro', 'gopro'])
        source_store.append(['Powder', 'powder'])
        self.combobox_source = Gtk.ComboBox.new()
        self.combobox_source.set_model(source_store)
        cell1 = Gtk.CellRendererText()
        self.combobox_source.pack_start(cell1, True)
        self.combobox_source.add_attribute(cell1, 'text', 0)
        grid.attach(self.combobox_source, 1, 1, 1, 1)

        button = Gtk.Button('Change now')
        button.connect('clicked', self.button_pressed)
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(button, True, False, 0)
        grid.attach(hbox, 0, 2, 2, 1)

        self.load_preferences()

        self.show_all()

    def button_pressed(self, widget):
        ngw.save_preferences()
        change_wallpaper()

    def close_application(self, widget, data=None):
        exit(0)

    def load_preferences(self):
        configuration = Configuration()
        select_value_in_combo(self.combobox_source,
                              configuration.get('source'))

    def save_preferences(self):
        configuration = Configuration()
        configuration.set(
            'source', get_selected_value_in_combo(self.combobox_source))
        configuration.save()


if __name__ == '__main__':
    if not os.path.exists(comun.CONFIG_APP_DIR):
        os.makedirs(comun.CONFIG_APP_DIR)
    ngw = NGW()
    if ngw.run() == Gtk.ResponseType.ACCEPT:
        ngw.hide()
        ngw.save_preferences()
        if ngw.switch.get_active():
            if not os.path.exists(os.path.dirname(FILESTART)):
                os.makedirs(os.path.dirname(FILESTART))
            shutil.copyfile(comun.AUTOSTART, FILESTART)
        else:
            if os.path.exists(FILESTART):
                os.remove(FILESTART)

    ngw.destroy()
