#!/usr/local/bin/python3
__author__ = 'apaeffgen'
# -*- coding: utf-8 -*-

    # This file is part of Panconvert.
    #
    # Panconvert is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # Panconvert is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with Panconvert.  If not, see <http://www.gnu.org/licenses/>.

import os, io, shutil,sys
from os import path
from shutil import which, Error
import platform
import subprocess
from source.language.messages import *

pathlistorig = os.environ["PATH"].split(":")
pathlist_tmp = '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin'

pathlist = pathlist_tmp.split(":")
settings = QSettings('Pandoc', 'PanConvert')


def search_pandoc():
    debug_message('We search for an installed pandoc Version.')

    which("pandoc")

    shutildef("pandoc")

def write_log_info(messages):
    logfp = open('/Users/apaeffgen/Downloads/logfile.txt', 'a')
    print(messages, file=logfp)
    logfp.close()


def which(target):
    for p in pathlist:
        fullpath = p + "/" + target
        if os.path.isfile(fullpath) and os.access(fullpath, os.X_OK):
            path_pandoc = fullpath
    message = 'which path: ' + fullpath
    write_log_info(message)
    write_log_info(target)
    write_log_info(sys.path)
    write_log_info(os.environ)

def shutildef(target):
    try:
        pandoc_path = shutil.which("pandoc", mode=os.X_OK)
        message = 'shutil path:' + os.environ['PATH']
        write_log_info(message)
        write_log_info(target)
        write_log_info(sys.path)
        write_log_info(os.environ)

    except:
        debug_message('An Exeption occured')


def search():
    path_pandoc = settings.value('path_pandoc','')

    args = ['which', 'pandoc']
    p = subprocess.Popen(
        args,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    path_pandoc = str.rstrip(p.communicate(path_pandoc.encode('utf-8'))[0].decode('utf-8'))



