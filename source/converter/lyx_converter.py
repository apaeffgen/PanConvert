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


from source.converter.interface_pandoc import *
import subprocess
import platform, os, glob
import fnmatch
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings
from distutils.util import strtobool

#global openfile

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

        if os.path.isfile(path_multimarkdown):


            args = [path_multimarkdown, openfile, '--to=' + 'lyx',  '--output=' + openfile + '.' + 'lyx']

            p = subprocess.Popen(
                    args,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)



            return p.communicate(openfile.encode('utf-8'))[0].decode('utf-8')





