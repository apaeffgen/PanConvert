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


from PyQt5.QtCore import QSettings
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
        normalized_uri = 'http://' + uri
    return normalized_uri



# class Helper(StartQT5):
#     def __init__(self):
#         StartQT5.__init__(self)
#
#     def batch_settings(self):
#         batch_settings = QSettings('Pandoc', 'PanConvert')
#         batch_settings.setValue('batch_convert_directory', self.ui.ParameterBatchconvertDirectory.isChecked())
#         batch_settings.setValue('batch_convert_files', self.ui.ParameterBatchconvertFiles.isChecked())
#         batch_settings.setValue('batch_convert_recursive', self.ui.ParameterBatchconvertRecursive.isChecked())
#         batch_settings.setValue('batch_open_path', self.ui.OpenPath.text())
#         batch_settings.setValue('batch_open_path_output', self.ui.OpenPathOutput.text())
#         batch_settings.setValue('batch_convert_filter', self.ui.Filter.text())
#         batch_settings.sync()
#         batch_settings.status()


