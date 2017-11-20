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

# Dependencies:
# python3-cssselect

import gi
try:
    gi.require_version('Notify', '0.7')
    gi.require_version('Gio', '2.0')
    gi.require_version('GLib', '2.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Notify
# from gi.repository import Gio
# from gi.repository import GLib
from datetime import datetime
import time
import requests
import os
from lxml.html import fromstring
from lxml import etree
import json
import tempfile
import hashlib
import pprint
import shutil
import comun
from config import Config
from comun import get_desktop_environment
from comun import _


URL00 = 'http://www.nationalgeographic.com/photography/photo-of-the-day/\
_jcr_content/.gallery.'
URL01 = 'http://www.bing.com/HPImageArchive.aspx?\
format=xml&idx=0&n=1&mkt=en-ww'
URL02 = 'https://api.gopro.com/v2/channels/feed/playlists/\
photo-of-the-day.json?platform=web&page=1&per_page=1'
URL03 = 'http://www.powder.com/photo-of-the-day/'
URL04 = 'http://www.vokrugsveta.ru/photo_of_the_day/'
URL05 = 'https://fstoppers.com/potd'
URL06 = 'https://api.desktoppr.co/1/wallpapers/random'
URL07 = 'https://apod.nasa.gov/apod/ap{0}.html'


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def set_background(afile=None):
    desktop_environment = get_desktop_environment()
    if desktop_environment == 'gnome' or desktop_environment == 'unity' or \
            desktop_environment == 'budgie-desktop':
        if afile and os.path.exists(afile):
            os.system("DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set \
org.gnome.desktop.background picture-uri file://'%s'" % afile)
    elif desktop_environment == "mate":
        if afile and os.path.exists(afile):
            os.system("DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set \
org.mate.background picture-filename '%s'" % afile)
    elif desktop_environment == "cinnamon":
        if afile and os.path.exists(afile):
            os.system("DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set \
org.cinnamon.background picture-filename file://'%s'" % afile)


def get_national_geographic_data():
    # Filename with data: .gallery.<currentYear>-<currentMonth>.json
    today = datetime.today()
    year = str(today.year)
    if today.month < 10:
        month = '0' + str(today.month)
    else:
        month = str(today.month)
    url = URL00 + year + '-' + month + '.json'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        if 'items' in data:
            current_photo = data['items'][0]
            # TODO: include preferred image size in configuration
            url = current_photo['url'] + current_photo['sizes']['1600']
            return dict(url=url,
                        title=current_photo['title'],
                        caption=current_photo['caption'],
                        credit=current_photo['credit'])
    return None


def set_nasa_wallpaper():
    st = datetime.fromtimestamp(time.time()).strftime('%y%m%d')
    url = URL07.format(st)
    r = requests.get(url)
    if r.status_code == 200:
        try:
            parser = etree.HTMLParser(recover=True)
            html = etree.HTML(r.content, parser)
            images = html.iter('img')
            if images is not None:
                images = list(images)
                if len(images) > 0:
                    image_url = images[0].getparent().attrib['href']
                    image_url = 'https://apod.nasa.gov/' + image_url
                    if download(image_url) is True:
                        set_background(comun.POTD)
        except Exception as e:
            print(e)


def set_fstoppers_wallpaper():
    r = requests.get(URL05)
    url = None
    image_url = None
    if r.status_code == 200:
        try:
            parser = etree.HTMLParser(recover=True)
            html = etree.HTML(r.content, parser)
            print(etree.tostring(html))
            print('===========')
            for element in html.iter('img'):
                # print(element.tag, element.attrib, element.text)
                try:
                    print(element.attrib['data-original'])
                    url = 'https://fstoppers.com' +\
                        element.getparent().attrib['href']
                    break
                except Exception as e:
                    print(e)
            if url is not None:
                print(url)
                r = requests.get(url)
                if r.status_code == 200:
                    html = etree.HTML(r.content, parser)
                    print(etree.tostring(html))
                    for element in html.iter('div'):
                        try:
                            if element.attrib['class'] == 'photo':
                                image_url = element.attrib['data-xlarge']
                                break
                        except Exception as e:
                            print(e)
        except Exception as e:
            print(e)
        if image_url is not None:
            if download(image_url) is True:
                set_background(comun.POTD)


def notify_photo_caption(title, caption, credit):
    if len(caption) > 60:
        caption = description_max(caption, 60)
    for m in ['<p>', '</p>', '<br>', '<br />']:
        caption = caption.replace(m, '')
    caption = caption + '\n<i>' + _('Photo credit') + '</i>: ' + credit
    Notify.init(title)
    info = Notify.Notification.new(title, caption, 'dialog-information')
    info.set_timeout(Notify.EXPIRES_NEVER)
    info.set_urgency(Notify.Urgency.CRITICAL)  # Notification stays longer
    info.show()


def set_national_geographic_wallpaper():
    data = get_national_geographic_data()
    if data:
        url = data['url']
        if download(url) is True:
            set_background(comun.POTD)
            notify_photo_caption(data['title'],
                                 data['caption'],
                                 data['credit'])


def set_bing_wallpaper():
    r = requests.get(URL01)
    if r.status_code == 200:
        try:
            parser = etree.XMLParser(recover=True)
            xml = etree.XML(r.content, parser)
            print(etree.tostring(xml))
            print('===========')
            image = xml.find('image')
            urlBase = image.find('urlBase')
            url = 'http://www.bing.com%s_1920x1200.jpg' % (urlBase.text)
            if download(url) is True:
                set_background(comun.POTD)
            print('===========')
        except Exception as e:
            print(e)


def set_gopro_wallpaper():
    try:
        r = requests.get(URL02)
        print(r.status_code)
        if r.status_code == 200:
            data = json.loads(r.text)
            url = data['media'][0]['thumbnails']['full']['image']
            print(url)
            if download(url) is True:
                print(url)
                set_background(comun.POTD)
                notify_photo_caption(data['media'][0]['title'],
                                     data['media'][0]['description'],
                                     data['media'][0]['author'])
    except Exception as e:
        print(e)


def set_powder_wallpaper():
    try:
        r = requests.get(URL03)
        if r.status_code == 200:
            doc = fromstring(r.text)
            results = doc.cssselect('img.entry-image')
            print(len(results), results[0])
            for key in results[0].keys():
                print(key, results[0].get(key))
            url = results[0].get('data-srcset').split(',')[0].split(' ')[0]
            url = '-'.join(url.split('-')[:-1]) + '.' + url.split('.')[-1]
            if download(url) is True:
                set_background(comun.POTD)
    except Exception as e:
        print(e)


def set_vokrugsveta_wallpaper():
    try:
        r = requests.get(URL04)
        if r.status_code == 200:
            doc = fromstring(r.text)
            results = doc.cssselect('a.article__pic')
            url = 'http://www.vokrugsveta.ru/' + results[0].get('href')
            print(url)
            r = requests.get(url, stream=True)
            if r.status_code == 200:
                doc = fromstring(r.text)
                results = doc.cssselect('img')
                for index, result in enumerate(results):
                    print(index, result.get('src'))
                i_url = 'http://www.vokrugsveta.ru/' + results[2].get('src')
                if download(i_url) is True:
                    set_background(comun.POTD)

            print(url)
    except Exception as e:
        print(e)


def set_desktoppr_wallpaper():
    try:
        r = requests.get(URL06)
        if r.status_code == 200:
            ans = r.json()
            pprint.pprint(ans)
            url = ans['response']['image']['url']
            if download(url) is True:
                set_background(comun.POTD)
    except Exception as e:
        print(e)


def download(url):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            if os.path.exists(comun.POTD):
                md5_old = md5(comun.POTD)
                tempfilename = tempfile.NamedTemporaryFile().name
                with open(tempfilename, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                md5_new = md5(tempfilename)
                if md5_old == md5_new:
                    os.remove(tempfilename)
                else:
                    os.remove(comun.POTD)
                    shutil.move(tempfilename, comun.POTD)
                    return True
            else:
                with open(comun.POTD, 'wb') as f:
                    for chunk in r.iter_content(1024):
                        f.write(chunk)
                    return True
    except Exception as e:
        print(e)
    return False


def change_wallpaper():
    config = Config()
    source = config.get_source()
    print(source)
    if source == 'national-geographic':
        set_national_geographic_wallpaper()
    elif source == 'bing':
        set_bing_wallpaper()
    elif source == 'gopro':
        set_gopro_wallpaper()
    elif source == 'powder':
        set_powder_wallpaper()
    elif source == 'fstoppers':
        set_fstoppers_wallpaper()
    elif source == 'desktoppr':
        set_desktoppr_wallpaper()
    elif source == 'nasa':
        set_nasa_wallpaper()


def description_max(astring, max_length):
    phrase = ''
    description = []
    for chain in astring.split(' '):
        if len(phrase) == 0:
            new_phrase = chain
        else:
            new_phrase = phrase + ' ' + chain
        if len(new_phrase) > max_length:
            description.append(phrase)
            phrase = chain
        else:
            phrase = new_phrase
    if len(phrase) > 0 and description[-1] != phrase:
        description.append(phrase)
    return '\n'.join(description)


if __name__ == '__main__':
    change_wallpaper()
    exit(0)
