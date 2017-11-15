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
    gi.require_version('Gdk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Gdk
import comun
from config import Config
from croni import Croni
from autostart import Autostart
from ngdownloader import change_wallpaper
from async import async_function
from comun import _


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
            _('National Geographic Wallpaper'),
            None,
            Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
             Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.set_size_request(350, 80)
        self.set_icon_from_file(comun.ICON)
        self.connect('destroy', self.close_application)

        self.config = Config()
        self.croni = Croni()
        self.autostart = Autostart()

        grid = Gtk.Grid()
        grid.set_row_spacing(5)
        grid.set_column_spacing(5)
        grid.set_border_width(5)
        self.get_content_area().add(grid)

        label10 = Gtk.Label(_('Change wallpaper automatically?') + ':')
        label10.set_alignment(0, 0.5)
        grid.add(label10)

        self.switch = Gtk.Switch()
        self.switch.set_active(self.croni.is_enabled())
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(self.switch, False, False, 0)
        grid.attach(hbox, 1, 0, 1, 1)

        label20 = Gtk.Label(_('Select backgrounds source') + ':')
        label20.set_alignment(0, 0.5)
        grid.attach(label20, 0, 1, 1, 1)

        source_store = Gtk.ListStore(str, str)
        source_store.append([_('National Geographic'), 'national-geographic'])
        source_store.append([_('Bing'), 'bing'])
        source_store.append([_('GoPro'), 'gopro'])
        source_store.append([_('Powder'), 'powder'])
        source_store.append([_('Fstoppers'), 'fstoppers'])
        source_store.append([_('Desktoppr'), 'desktoppr'])
        source_store.append([_('Nasa'), 'nasa'])
        self.combobox_source = Gtk.ComboBox.new()
        self.combobox_source.set_model(source_store)
        cell1 = Gtk.CellRendererText()
        self.combobox_source.pack_start(cell1, True)
        self.combobox_source.add_attribute(cell1, 'text', 0)
        grid.attach(self.combobox_source, 1, 1, 1, 1)

        button = Gtk.Button(_('Change now'))
        button.connect('clicked', self.button_pressed)
        hbox = Gtk.Box(Gtk.Orientation.HORIZONTAL, 5)
        hbox.pack_start(button, True, False, 0)
        grid.attach(hbox, 0, 2, 2, 1)

        self.load_preferences()

        self.show_all()

    def set_autostart_activate(self):
        if self.switch.get_active():
            self.croni.set_jobs()
            self.autostart.set_autostart(True)
            self.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
            change_wallpaper()
            self.get_window().set_cursor(None)
        else:
            self.croni.unset_jobs()
            self.autostart.set_autostart(False)

    def button_pressed(self, widget):
        self.change_wallpaper()

    def close_application(self, widget, data=None):
        exit(0)

    def load_preferences(self):
        select_value_in_combo(self.combobox_source,
                              self.config.get_source())

    def save_preferences(self):
        self.config.set_source(get_selected_value_in_combo(
            self.combobox_source))

    def change_wallpaper(self):

        def on_change_wallpaper_done(result, error):
            self.get_window().set_cursor(None)

        @async_function(on_done=on_change_wallpaper_done)
        def do_change_wallpaper_in_thread():
            self.save_preferences()
            change_wallpaper()
            return True

        self.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
        do_change_wallpaper_in_thread()


if __name__ == '__main__':
    ngw = NGW()
    if ngw.run() == Gtk.ResponseType.ACCEPT:
        ngw.hide()
        ngw.set_autostart_activate()
        ngw.save_preferences()
    ngw.destroy()
