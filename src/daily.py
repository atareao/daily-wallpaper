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

class Daily():

    _id = 'daily'
    _name = __name__

    def __init__(self):
        self._url = None
        self._title = None
        self._caption = None
        self._credit = None

    def get_name(cls):
        return cls._name

    def get_id(cls):
        return cls._id

    def get_url(self):
        return self._url

    def get_title(self):
        return self._title

    def get_caption(self):
        return self._caption

    def get_credit(self):
        return self._credit

    def resolve_url(self):
        return False

    def __eq__(self, other):
        self._name == other.get_name()

    def __str__(self):
        string = 'Name: {}\n'.format(self._name)
        string += 'Url: {}\n'.format(self._url)
        string += 'Title: {}\n'.format(self._title)
        string += 'Caption: {}\n'.format(self._caption)
        string += 'Credit: {}\n'.format(self._credit)
        return string
