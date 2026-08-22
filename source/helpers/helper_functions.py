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


from PyQt6.QtCore import QSettings
from urllib.parse import urlparse, unquote
#from source.main_gui import StartQT5

global uri


def convert_boolean(value):
    if str(value).lower() in ("yes", "y", "true", "t", "1"): return True
    if str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False

def check_uri():
    weburi = False
    try:
        if 'http://' in uri:
            weburi = True
        if 'www' in uri:
            weburi = True
        return weburi
    except:
        return

def parse_uri():
    if 'file://' in uri:
        file = unquote(uri)[7:]
    else:
        file = uri
    return file

def normalize_uri():
    global uri
    if 'http://' not in uri:
        uri = 'http://' + uri
    return uri


def save_dialog_position(dialog, size_key, pos_key):
    """
    Save dialog position and size to settings.

    This is a centralized function to save dialog window position and size
    to prevent position drift when dialogs are reopened.

    Args:
        dialog: The dialog widget instance (must have pos() and size() methods)
        size_key: Settings key for dialog size (e.g., "FromFormat_size")
        pos_key: Settings key for dialog position (e.g., "FromFormat_pos")
    """
    settings = QSettings('Pandoc', 'PanConvert')
    Dialog_Size = settings.value('Dialog_Size')

    if Dialog_Size is True or Dialog_Size == 'true':
        settings.setValue(size_key, dialog.size())
        settings.setValue(pos_key, dialog.pos())
        settings.sync()





