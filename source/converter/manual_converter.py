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

from source.converter.interface_pandoc import get_pandoc_formats
from source.converter.interface_pandoc import get_path_pandoc
from source.language.messages import *

settings = QSettings('Pandoc', 'PanConvert')
path_pandoc = settings.value('path_pandoc')



def convert_universal(text, ToFormat, FromFormat, extra_args):
    try:
        os.path.isfile(path_pandoc)




        args = [path_pandoc, '--from=' + FromFormat, '--to=' + ToFormat]

        output = ''
        if extra_args is not '' :
            extra_args = extra_args.split(';')
            for arg in extra_args:
                args.append(arg)


        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)



        output1, error1 = p.communicate(text.encode('utf-8'))

        try:
            output = output1.decode('utf-8')
            error = error1.decode('utf-8')

            if p.returncode != 0:
                QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                              'An Error occurred. <br><br>{}'.format(error))
            else:

                if output == '':
                    output = error_no_output()


        except:
            error_fatal()

        return output

    except OSError:
        error_converter_path()

def convert_binary(openfile,ToFormat,FromFormat,extra_args):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')

    try:
        path_pandoc = get_path_pandoc()


        args = [path_pandoc, '--from=' + FromFormat, '--to=' + ToFormat, openfile]

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

        output1, error1 = p.communicate(output.encode('utf-8'))

        try:
            output = output1.decode('utf-8')
            error = error1.decode('utf-8')

            if p.returncode != 0:
                QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                              'An Error occurred. <br><br>{}'.format(error))
            else:
                if output != '':
                    return output
                else:
                    message = error_no_output()
                    return message

        except:
            error_fatal()

        return output




        #return p.communicate(output.encode('utf-8'))[0].decode('utf-8')

    except OSError:
        error_converter_path()
