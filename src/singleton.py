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

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop


def _get_path(app_id):
    return '/' + app_id.replace('.', '/')


def listen_for_activation(app_id, window):
    """
    Listen for 'activate' events. If one is sent, activate 'window'.
    """
    class MyDBUSService(dbus.service.Object):
        def __init__(self, window):
            self.window = window

            bus_name = dbus.service.BusName(app_id, bus=dbus.SessionBus())
            dbus.service.Object.__init__(self, bus_name, _get_path(app_id))

        @dbus.service.method(app_id)
        def activate(self):
            self.window.present()
            self.window.set_focus(None)

    DBusGMainLoop(set_as_default=True)
    MyDBUSService(window)


def activate_if_already_running(app_id):
    """
    Activate the existing window if it's already running. Return True if found
    an existing window, and False otherwise.
    """
    bus = dbus.SessionBus()
    try:
        programinstance = bus.get_object(app_id, _get_path(app_id))
        activate = programinstance.get_dbus_method('activate', app_id)
    except dbus.exceptions.DBusException:
        return False
    else:
        activate()
        return True
    finally:
        bus.close()
