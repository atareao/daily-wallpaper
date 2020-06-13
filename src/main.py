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

import gi
try:
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Gdk
import sys
import importlib
import comun
from config import Configuration
from croni import Croni
from autostart import Autostart
from dwdownloader import change_wallpaper
from fsync import async_function
from comun import get_modules
from comun import _
from singleton import listen_for_activation, activate_if_already_running

sys.path.insert(1, comun.DAILIESDIR)
sys.path.insert(1, comun.USERDAILIESDIR)


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


class DWW(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_title(_('Daily Wallpaper'))
        self.set_modal(True)
        self.set_destroy_with_parent(True)
        self.set_size_request(370, 80)
        self.set_icon_from_file(comun.ICON)
        self.connect('realize', self.on_realize)
        self.connect('destroy', self.close_application)

        self.croni = Croni()
        self.autostart = Autostart()

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_border_width(10)
        self.add(grid)

        label10 = Gtk.Label.new(_('Change wallpaper automatically?'))
        label10.set_halign(True)
        grid.add(label10)

        self.switch = Gtk.Switch.new()
        self.switch.set_halign(True)
        self.switch.set_active(self.croni.is_enabled())
        grid.attach(self.switch, 1, 0, 1, 1)

        label20 = Gtk.Label.new(_('Random source?'))
        label20.set_halign(True)
        grid.attach(label20, 0, 1, 1, 1)

        self.switch_random = Gtk.Switch.new()
        self.switch_random.set_halign(True)
        self.switch_random.set_active(True)
        self.switch_random.connect('state-set', self.on_switch_random_changed)
        grid.attach(self.switch_random, 1, 1, 1, 1)

        self.label30 = Gtk.Label.new(_('Select backgrounds source:'))
        self.label30.set_halign(True)
        grid.attach(self.label30, 0, 2, 1, 1)

        source_store = Gtk.ListStore(str, str)
        source_store.set_sort_func(0, self.tree_compare_func, None)
        for module_name in get_modules():
            module = importlib.import_module(module_name)
            daily = module.get_daily()
            source_store.append([daily.get_name(), daily.get_id()])
        self.combobox_source = Gtk.ComboBox.new()
        self.combobox_source.set_model(source_store)
        cell1 = Gtk.CellRendererText()
        self.combobox_source.pack_start(cell1, True)
        self.combobox_source.add_attribute(cell1, 'text', 0)
        grid.attach(self.combobox_source, 1, 2, 1, 1)

        button = Gtk.Button.new_with_label(_('Change now'))
        button.set_halign(Gtk.Align.CENTER)
        button.connect('clicked', self.button_pressed)
        grid.attach(button, 0, 3, 2, 1)

        hb = Gtk.HeaderBar()
        self.set_titlebar(hb)
        hb.set_show_close_button(True)
        hb.props.title = comun.APP

        button_cancel = Gtk.Button.new_with_label(_('Cancel'))
        button_cancel.set_halign(Gtk.Align.START)
        button_cancel.connect('clicked', self.on_button_cancel_clicked)
        hb.pack_start(button_cancel)

        button_ok = Gtk.Button.new_with_label(_('Ok'))
        button_ok.set_halign(Gtk.Align.END)
        button_ok.connect('clicked', self.on_button_ok_clicked)
        hb.pack_end(button_ok)

        self.load_preferences()
        self.show_all()

    def tree_compare_func(self, row1, row2):
        """
        a negative integer, zero or a positive integer depending on whether a
        sorts before, with or after b
        """
        print(type(row1), row1)
        if row1 < row2:
            return -1
        elif row1 > row2:
            return 1
        return 0

    def on_button_ok_clicked(self, widget):
        self.hide()
        self.set_autostart_activate()
        self.save_preferences()
        self.destroy()

    def on_button_cancel_clicked(self, widget):
        self.destroy()

    def set_source_state(self, state):
        self.label30.set_sensitive(state)
        self.combobox_source.set_sensitive(state)

    def on_switch_random_changed(self, widget, state):
        state = self.switch_random.get_active()
        self.set_source_state(not state)

    def set_autostart_activate(self):
        if self.switch.get_active():
            self.croni.set_jobs()
            self.autostart.set_autostart(True)
        else:
            self.croni.unset_jobs()
            self.autostart.set_autostart(False)

    def button_pressed(self, widget):
        self.change_wallpaper_async()

    def close_application(self, widget, data=None):
        exit(0)

    def load_preferences(self):
        config = Configuration()
        select_value_in_combo(self.combobox_source, config.get('source'))
        self.switch_random.set_active(config.get('random'))
        self.set_source_state(not config.get('random'))

    def save_preferences(self):
        config = Configuration()
        config.set('source', get_selected_value_in_combo(self.combobox_source))
        config.set('random', self.switch_random.get_active())
        config.save()

    def change_wallpaper_async(self):

        def on_change_wallpaper_done(result, error):
            self.get_window().set_cursor(None)

        @async_function(on_done=on_change_wallpaper_done)
        def do_change_wallpaper_in_thread():
            self.save_preferences()
            change_wallpaper()
            return True

        self.get_window().set_cursor(Gdk.Cursor(Gdk.CursorType.WATCH))
        do_change_wallpaper_in_thread()

    def on_realize(self, *_):
        monitor = Gdk.Display.get_primary_monitor(Gdk.Display.get_default())
        scale = monitor.get_scale_factor()
        monitor_width = monitor.get_geometry().width / scale
        monitor_height = monitor.get_geometry().height / scale
        width = self.get_preferred_width()[0]
        height = self.get_preferred_height()[0]
        self.move((monitor_width - width)/2, (monitor_height - height)/2)


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    APP_ID = 'es.atareao.daily_wallpaper'

    activated = activate_if_already_running(APP_ID)
    if activated:
        sys.exit(0)

    dww = DWW()
    listen_for_activation(APP_ID, dww)
    Gtk.main()


if __name__ == '__main__':
    main()
