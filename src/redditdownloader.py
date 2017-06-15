#!/usr/bin/env python3 
import argparse
import ctypes
import os
import platform
import pwd
import shutil
import sys
import time

import praw
import requests
from PIL import Image


def sanitize(link):
    if 'jpg' in link or 'png' in link:
        return link
    elif 'imgur' in link:
        return link + '.png'
    else:
        raise ValueError('cant sanitize url' + link)


def get_username():
    return pwd.getpwuid(os.getuid())[0]


def main():
    r = praw.Reddit(user_agent='RedditWallpaper Script by ' + get_username())

    sub_reddit = 'EarthPorn'
    sort_method = 'get_top_from_all'
    count = 1
    print(sub_reddit, sort_method, count)
    submissions = getattr(
        r.get_subreddit(sub_reddit), sort_method)(limit=count)

    i = 0
    wlinks = []
    for each in submissions:
        wlinks.append(each)
    wcounts = len(wlinks)

    while True:
        fail = False
        print(i)
        each = wlinks[i]
        try:
            url = sanitize(each.url)
            imgext = url.split('.')[-1]
        except ValueError as e:
            print(e)
            i+=1
            continue
        print(url)
        '''
        response = requests.get(url, stream=True)

        # Download images in  ~/.epwallpapers directory all images
        with open(my_dir + '/' + str(i) + '.' + imgext, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        imagePath = my_dir + '/' + str(i) + '.' + imgext

        with Image.open(imagePath) as im:
            width, height = im.size
            # We only want high resolution images
            if int(width) < 2000 or int(height) < 1300:
                i+=1
                print('poor pic, failed')
                fail = True

        if fail:
            continue
        if platform.system() == 'Darwin':
            osxcmd = 'osascript -e \'tell application "Finder" to set desktop picture to POSIX file "' + imagePath + '" \''
            os.system(osxcmd)
        elif platform.system() == 'Windows':
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, imagePath, 3)
        elif platform.system() == 'Linux':
            linuxcmd = 'gsettings set org.gnome.desktop.background picture-uri file://' + imagePath
            os.system(linuxcmd)
        else:
            print('Platform not recognized')
            sys.exit()
        print('Done')

        i += 1
        if i == wcounts -1:
            i = 0
        time.sleep(wall_duration * 60)
        '''


if __name__ == '__main__':
    main()