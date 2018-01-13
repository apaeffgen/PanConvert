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

import os, shutil, io, sys
from os import path
import platform
import subprocess
from PyQt5.QtCore import QSettings
from source.language.messages import *


global fromFormat

settings = QSettings('Pandoc', 'PanConvert')
path_pandoc = settings.value('path_pandoc','')


def get_path_pandoc():

    settings = QSettings('Pandoc', 'PanConvert')
    path_pandoc = settings.value('path_pandoc','')

    if not os.path.isfile(path_pandoc):

        if platform.system() == 'Darwin' or os.name == 'posix':
            path_pandoc = which("pandoc")
            settings.setValue('path_pandoc', path_pandoc)
            settings.sync()
        else:
            path_pandoc = where("pandoc")
            settings.setValue('path_pandoc', path_pandoc)
            settings.sync()


def get_path_multimarkdown():
    settings = QSettings('Pandoc', 'PanConvert')
    path_multimarkdown = settings.value('path_multimarkdown','')

    if getattr( sys, 'frozen', False ):
            if platform.system() == 'Darwin' or os.name == 'posix':
                path_multimarkdown = which("multimarkdown")
                settings.setValue('path_multimarkdown', path_multimarkdown)
                settings.sync()
            else:
                args = ['where', 'multimarkdown']
                p = subprocess.Popen(
                    args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)

                path_multimarkdown = str.rstrip(p.communicate(path_multimarkdown.encode('utf-8'))[0].decode('utf-8'))
                settings.setValue('path_multimarkdown', path_multimarkdown)
                settings.sync()
                return path_multimarkdown
    else:

        if platform.system() == 'Darwin' or os.name == 'posix':
            args = ['which', 'multimarkdown']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path_multimarkdown = str.rstrip(p.communicate(path_multimarkdown.encode('utf-8'))[0].decode('utf-8'))
            settings.setValue('path_multimarkdown', path_multimarkdown)
            settings.sync()
            return path_multimarkdown

        elif platform.system() == 'Windows':
            args = ['where', 'multimarkdown']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path_multimarkdown = str.rstrip(p.communicate(path_multimarkdown.encode('utf-8'))[0].decode('utf-8'))
            settings.setValue('path_multimarkdown', path_multimarkdown)
            settings.sync()
            return path_multimarkdown


def get_pandoc_version():

    settings = QSettings('Pandoc', 'PanConvert')
    path_pandoc = settings.value('path_pandoc','')

    if os.path.isfile(path_pandoc):

        p = subprocess.Popen(
            [path_pandoc, '-v'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        output = p.communicate()[0].decode().splitlines(False)
        versionstr = output[0]


        if platform.system() == 'Windows':
            version_tmp = versionstr.replace(".","")
            version = int(version_tmp[10:15])
        else:
            version_tmp = versionstr.replace(".","")
            version = int(version_tmp[7:10])

    return version



def get_pandoc_formats():
    """
    Dynamic preprocessor for Pandoc formats.
    Return 2 lists. "from_formats" and "to_formats".
    """
    settings = QSettings('Pandoc', 'PanConvert')
    path_pandoc = settings.value('path_pandoc','')

    if os.path.isfile(path_pandoc):

        version = get_pandoc_version()

        if version < 118:

                p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
                help_text = p.communicate()[0].decode().splitlines(False)
                txt = ' '.join(help_text[1:help_text.index('Options:')])


                aux = txt.split('Output formats: ')
                in_ = aux[0].split('Input formats: ')[1].split(',')
                out = aux[1].split(',')

                return [f.strip() for f in in_], [f.strip() for f in out]


        else:

            p = subprocess.Popen(
                [path_pandoc, '--list-input-formats'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            inputformats = p.communicate()[0].decode().splitlines(False)


            p = subprocess.Popen(
                [path_pandoc, '--list-output-formats'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            outputformats = p.communicate()[0].decode().splitlines(False)

            in_ = inputformats
            out = outputformats

            return [f.strip() for f in in_], [f.strip() for f in out]


    else:
        path_pandoc = get_path_pandoc()
        path_pandoc = settings.value('path_pandoc','')
        if not os.path.isfile(path_pandoc):
            message = error_converter_path()
            return message


def get_pandoc_options():
    """
    Get the Options of the Pandoc help section
    """
    settings = QSettings('Pandoc', 'PanConvert')
    path_pandoc = settings.value('path_pandoc','')
    if os.path.isfile(path_pandoc):

        version = get_pandoc_version()

        if version < 1.18:

            p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(True)


            aux = help_text[15:89]

            return aux


        else:

            p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(True)
            aux = help_text

            return aux

    else:
        path_pandoc = get_path_pandoc()
        path_pandoc = settings.value('path_pandoc','')
        if not os.path.isfile(path_pandoc):
            message = error_converter_path()
            return message

def which(target):
    pathlist_tmp = '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/Applications/Panconvert:~/Panconvert:/opt/Panconvert'
    pathlist = pathlist_tmp.split(":")
    for p in pathlist:
        fullpath = p + "/" + target
        if os.path.isfile(fullpath) and os.access(fullpath, os.X_OK):
            path_pandoc = fullpath

            return path_pandoc

def where(target):
    pathlist_tmp = '/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/Applications/Panconvert:~/Panconvert:/opt/Panconvert'
    pathlist = pathlist_tmp.split(":")
    for p in pathlist:
        fullpath = p + "/" + target
        if os.path.isfile(fullpath) and os.access(fullpath, os.X_OK):
            path_pandoc = fullpath

            return path_pandoc



