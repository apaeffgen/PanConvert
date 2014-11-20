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


import subprocess
import platform
import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings


def get_path_multimarkdown():
    settings = QSettings('Pandoc', 'PanConvert')
    path_multimarkdown = settings.value('path_multimarkdown','')

    if len(path_multimarkdown) == 0:

        if platform.system() == 'Darwin' or platform.system() == 'Linux':
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
        else:
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Could not detect the actual operating system. Please fill in the Path'
                                          ' to MultiMarkdown manually via Preferences.')

    elif len(path_multimarkdown) != 0:
        return path_multimarkdown

    else:
       QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'I tried automagically to detect MultiMarkdown. But it failed.'
                                          'Please input the path of MultiMarkdown manually via preferences')

def convert_markdown2lyx(text):
    try:
        path_multimarkdown = get_path_multimarkdown()
        args = [path_multimarkdown, '--to=lyx']

        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

        return p.communicate(text.encode('utf-8'))[0].decode('utf-8')

    except OSError:
        QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'MultiMarkdown could not be found on your System. Is it installed?'
                                          'If so, please check the MultiMarkdown Path in your Preferences.')