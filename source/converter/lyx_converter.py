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

import os
import subprocess

from PyQt5.QtCore import QSettings

from source.helpers.interface_pandoc import *

settings = QSettings('Pandoc', 'PanConvert')
path_pandoc = settings.value('path_pandoc')

def convert_markdown2lyx(text):
    settings = QSettings('Pandoc', 'PanConvert')
    path_multimarkdown = settings.value('path_multimarkdown','')

    if os.path.isfile(path_multimarkdown):

            args = [path_multimarkdown, '--to=lyx']

            p = subprocess.Popen(
                    args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)

            return p.communicate(text.encode('utf-8'))[0].decode('utf-8')

def batch_convert_markdown2lyx(openfile):

    settings = QSettings('Pandoc', 'PanConvert')
    path_multimarkdown = settings.value('path_multimarkdown','')
    batch_settings = QSettings('Pandoc', 'PanConvert')
    batch_open_path_output = batch_settings.value('batch_open_path_output')

    if os.path.isfile(path_multimarkdown):

        filename, file_extension = os.path.splitext(openfile)

        if batch_open_path_output == '':
            args = [path_multimarkdown, openfile, '--to=' + 'lyx',  '--output=' + filename + '.' + 'lyx']

        else:
            outputfile = os.path.basename(filename)
            args = [path_multimarkdown, openfile, '--to=' + 'lyx',  '--output=' + batch_open_path_output + '/' + outputfile + '.' + 'lyx']

        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
#TODO# WRITE ERROR RETURN CODES
        return p.communicate(openfile.encode('utf-8'))[0].decode('utf-8')