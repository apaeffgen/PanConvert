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
            message = error_uncatched()

        return message


    except OSError:
        error_converter_path()



