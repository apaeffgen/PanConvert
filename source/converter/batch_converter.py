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
import glob
import fnmatch
import os
from source.converter.interface_pandoc import convert
from source.converter.interface_pandoc import get_path_pandoc
from source.converter.interface_pandoc import get_pandoc_formats

global openfiles


def create_filelist(directory):


    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, '*.*'):
            if filename != '.DS_Store':
                matches.append(os.path.join(root, filename))

    return matches


def batch_convert_manual(openfile,FromFormat,ToFormat,extra_args):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')

    try:
        path_pandoc = get_path_pandoc()

        if extra_args is '':
            args = [path_pandoc, '--from=' + FromFormat, '--to=' + ToFormat, openfile, '--output=' + openfile + '.' + ToFormat]
        else:
            args = [path_pandoc, '--from=' + FromFormat, '--to=' + ToFormat, openfile, '--output=' + openfile + '.' + ToFormat, extra_args]

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
                #stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        error1 = p.communicate(output.encode('utf-8'))

        #error = error1.decode('utf-8')
        message = '\n Converted files should have been written to the same place as the original files.' \
                  ' \n There is no visual output. So please check your converted files at the filesystem level.' \
                  '\n \n When in batch-file-mode, for a better experience, please clear the window before starting a new conversion'
        error = ''


        if p.returncode != 0:
            result = ''
            error = 'An Error occurred. <br><br>{}'.format(error1)
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'An Error occurred. <br><br>{}'.format(error1))




        return message


        #return p.communicate(output.encode('utf-8'))[0].decode('utf-8')

    except OSError:
        QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Pandoc could not be found on your System. Is it installed?'
                                          'If so, please check the Pandoc Path in your Preferences.')