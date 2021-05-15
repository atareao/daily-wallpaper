#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of daily-wallpaper
#
# Copyright (c) 2021 Lorenzo Carbonell Cerezo <a.k.a. atareao>
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
import shutil
from plumbum import local

USER_PATH = os.path.join(os.path.expanduser('~'), '.config', 'systemd', 'user')

class SystemdUser(object):
    def __init__(self):
        if not os.path.exists(USER_PATH):
            os.makedirs(USER_PATH)

    def install(self, service):
        if os.path.exists(service):
            basename = os.path.basename(service)
            service_path = os.path.join(USER_PATH, basename)
            if not os.path.exists(service_path):
                shutil.copyfile(service, service_path)
                self.daemon_reload()
        return os.path.exists(service_path)

    def uninstall(self, service):
        basename = os.path.basename(service)
        service_path = os.path.join(USER_PATH, basename)
        if  os.path.exists(service_path):
            os.remove(service_path)
            self.daemon_reload()
        return not os.path.exists(service_path)


    def enable(self, service):
        return self.__command('enable', service)

    def disable(self, service):
        return self.__command('disable', service)

    def start(self, service):
        return self.__command('start', service)

    def stop(self, service):
        return self.__command('stop', service)

    def is_active(self, service):
        try:
            return self.__command('is-active', service)
        except:
            pass
        return False

    def is_enabled(self, service):
        try:
            return self.__command('is-enabled', service)
        except:
            pass
        return False

    def is_failed(self, service):
        try:
            return self.__command('is-failed', service)
        except:
            pass
        return False

    def status(self, service):
        try:
            return self.__command('status', service)
        except:
            pass
        return False

    def daemon_reload(self):
        stderr = ''
        try:
            systemctl = local['systemctl']
            exitcode, stdout, stderr = systemctl.run(['--user', 'daemon-reload'])
            return exitcode == 0
        except:
            raise Exception(stderr)
        return False

    def __command(self, command, service):
        stderr = ''
        try:
            systemctl = local['systemctl']
            exitcode, stdout, stderr = systemctl.run(['--user', command, service])
            return exitcode == 0
        except:
            raise Exception(stderr)
        return False



if __name__ == '__main__':
    systemdu = SystemdUser()
    print('Install', systemdu.install("/home/lorenzo/apps/daily-wallpaper/data/daily-wallpaper.timer"))
    print('Enable', systemdu.enable('daily-wallpaper.timer'))
    print('Start', systemdu.start('daily-wallpaper.timer'))
    print('Is_active', systemdu.is_active('daily-wallpaper.timer'))
    print('Status', systemdu.status('daily-wallpaper.timer'))
    print('Stop', systemdu.stop('daily-wallpaper.timer'))
    print('Is_active', systemdu.is_active('daily-wallpaper.timer'))
    print('Status', systemdu.status('daily-wallpaper.timer'))
    print('Disable', systemdu.disable('daily-wallpaper.timer'))
    print('Status', systemdu.status('daily-wallpaper.timer'))
    print('Uninstall', systemdu.uninstall('daily-wallpaper.timer'))
    

         
