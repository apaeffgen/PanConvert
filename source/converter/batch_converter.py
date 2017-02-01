#!/usr/local/bin/python3
import fnmatch
import glob

from PyQt5.QtCore import QSettings

from source.language.messages import *

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


from PyQt5 import QtWidgets
import subprocess

import os
from source.converter.interface_pandoc import *


global openfiles


def batch_convert_manual(openfile,FromFormat,ToFormat,extra_args):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')

    try:
        path_pandoc = get_path_pandoc()


        args = [path_pandoc, '--from=' + FromFormat, '--to=' + ToFormat, openfile, '--output=' + openfile + '.' + ToFormat]

        if extra_args is not '' :
            extra_args = extra_args.split(';')
            for arg in extra_args:
                args.append(arg)


        output = error_unknown()

        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        error1 = p.communicate(output.encode('utf-8'))


        if p.returncode != 0:
            result = ''
            message = 'An Error occurred. {}'.format(error1)

        else:
            message_tmp = message_file_converted()
            message = message_tmp + openfile + '\n'

        return message


    except OSError:
        message = error_converter_path()
        return message


def create_filelist(directory):

    settings = QSettings('Pandoc', 'PanConvert')
    filefilter = settings.value('batch_convert_filter','')

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.*'):
            if filename != '.DS_Store':
                matches.append(os.path.join(root, filename))

    filter = filefilter.split(';')
    matching = []

    for filteritem in filter:

        matching_filter = [s for s in matches if filteritem in s]
        for i in matching_filter:
            matching.append(i)

    if len(matching) == 0:

        message = error_file_selection()
    else:
        message_tmp = message_file_selection()
        message = message_tmp + filefilter


    return matching, message


def create_simplefilelist():
    settings = QSettings('Pandoc', 'PanConvert')
    batch_settings = QSettings('Pandoc', 'PanConvert')
    batch_open_path = batch_settings.value('batch_open_path')
    filefilter = settings.value('batch_convert_filter','')
    message = ''

    filelist = glob.glob(batch_open_path + '/*')
    filter = filefilter.split(';')

    matching = []

    for filteritem in filter:
        matching_filter = [s for s in filelist if filteritem in s]
        for i in matching_filter:
            matching.append(i)

    if len(matching) == 0:
        message = error_file_selection()

    return matching, message