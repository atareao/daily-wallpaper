#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from plumbum.cmd import systemctl

class SysTimer():
    def __init__(self, name):
        self._name = name

    def get_status(self):
        try:
            ans = systemctl['--user', 'status', self._name]()
        except Exception as e:
            ans = None
        return ans

if __name__ == '__main__':
    sys_timer = SysTimer('test')
    print(sys_timer.get_status())

