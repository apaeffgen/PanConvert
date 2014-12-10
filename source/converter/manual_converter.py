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
from source.converter.interface_pandoc import convert
from source.converter.interface_pandoc import get_path_pandoc
from source.converter.interface_pandoc import get_pandoc_formats


def convert_universal(text,ToFormat,FromFormat,arg):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    output = convert(text, ToFormat, FromFormat, arg)

    return output

def convert_binary(openfile,ToFormat,FromFormat,extra_args):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')

    try:
        path_pandoc = get_path_pandoc()


        args = [path_pandoc, '--from=' + FromFormat, '--to=' + ToFormat, openfile]

        if extra_args is not '' :
            extra_args = extra_args.split(';')
            for arg in extra_args:
                args.append(arg)

        get_pandoc_formats()

        from_formats, to_formats = get_pandoc_formats()

        if FromFormat not in from_formats:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Invalid from format! Expected one of these: ' + ', '.join(from_formats))

        if ToFormat not in to_formats:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Invalid to format! Expected one of these: ' + ', '.join(to_formats))

        output = 'If you can read this message, something went wrong. Get some help at ' \
                 'http://panconvert.sourceforge.net/help'

        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        output1, error1 = p.communicate(output.encode('utf-8'))
        output = output1.decode('utf-8')
        error = error1.decode('utf-8')

        if p.returncode != 0:
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'An Error occurred. <br><br>{}'.format(error))
        else:
            if output != '':
                return output
            else:
                message = 'There was no visible output. Did you write output to the filesystem?' \
                          ' Please look in the folder of PanConvert for some output-file'
                return message


        #return p.communicate(output.encode('utf-8'))[0].decode('utf-8')

    except OSError:
        QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Pandoc could not be found on your System. Is it installed?'
                                          'If so, please check the Pandoc Path in your Preferences.')

