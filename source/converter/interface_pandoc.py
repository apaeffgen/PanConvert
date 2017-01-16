#!/usr/local/bin/python3
__author__ = 'Juho Vepsäläinen, apaeffgen'
# -*- coding: utf-8 -*-
# The original file is modified from the following source:
# https://github.com/bebraw/pypandoc
# Thin wrapper for "pandoc" (MIT)
# http://pypi.python.org/pypi/pypandoc/

#    Copyright (c) 2011 Juho Vepsäläinen
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import fnmatch
import glob
import os
import platform
import subprocess

from PyQt5.QtCore import QSettings



from source.language.messages import *


global fromFormat

def get_path_pandoc():

    settings = QSettings('Pandoc', 'PanConvert')
    path_pandoc = settings.value('path_pandoc','')

    if len(path_pandoc) == 0:

        if platform.system() == 'Darwin' or os.name == 'posix':
            args = ['which', 'pandoc']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)


            path_pandoc = str.rstrip(p.communicate(path_pandoc.encode('utf-8'))[0].decode('utf-8'))

            if len(path_pandoc) != 0:


                settings.setValue('path_pandoc', path_pandoc)
                settings.sync()
                return path_pandoc


            else:
                error_converter_path()





        elif platform.system() == 'Windows':



            args = ['where', 'pandoc']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path_pandoc = str.rstrip(p.communicate(path_pandoc.encode('utf-8'))[0].decode('utf-8'))

            if len(path_pandoc) != 0:

                settings.setValue('path_pandoc', path_pandoc)
                settings.sync()
                return path_pandoc
            else:
                error_converter_path()



        else:
            error_os_detection()


    elif len(path_pandoc) != 0:
        return path_pandoc

    else:
        error_converter_path()




def get_path_multimarkdown():
    settings = QSettings('Pandoc', 'PanConvert')
    path_multimarkdown = settings.value('path_multimarkdown','')

    if len(path_multimarkdown) == 0:

        if platform.system() == 'Darwin' or os.name == 'posix':
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
            error_os_detection()

    elif len(path_multimarkdown) != 0:
        return path_multimarkdown

    else:
       error_converter_path()


def get_pandoc_formats():
    """
    Dynamic preprocessor for Pandoc formats.
    Return 2 lists. "from_formats" and "to_formats".
    """
    path_pandoc = get_path_pandoc()
    p = subprocess.Popen(
        [path_pandoc, '-v'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    output = p.communicate()[0].decode().splitlines(False)
    versionstr = output[0]

    if platform.system() == 'Windows':
        version = float(versionstr[10:15])
    else:
        version = float(versionstr[6:11])

    if version < 1.18:
        try:
            path_pandoc = get_path_pandoc()
            p = subprocess.Popen(
                [path_pandoc, '-h'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(False)
            txt = ' '.join(help_text[1:help_text.index('Options:')])
            #txt = ' '.join(help_text)

            aux = txt.split('Output formats: ')
            in_ = aux[0].split('Input formats: ')[1].split(',')
            out = aux[1].split(',')

            return [f.strip() for f in in_], [f.strip() for f in out]

        except OSError:
            error_converter_path()
    else:
        try:
            path_pandoc = get_path_pandoc()
            p = subprocess.Popen(
                [path_pandoc, '--list-input-formats'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            inputformats = p.communicate()[0].decode().splitlines(False)


            path_pandoc = get_path_pandoc()
            p = subprocess.Popen(
                [path_pandoc, '--list-output-formats'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
            outputformats = p.communicate()[0].decode().splitlines(False)

            in_ = inputformats
            out = outputformats

            return [f.strip() for f in in_], [f.strip() for f in out]
        except OSError:
            error_converter_path()


def get_pandoc_options():
    """
    Dynamic preprocessor for Pandoc formats.
    Return 2 lists. "from_formats" and "to_formats".
    """

    path_pandoc = get_path_pandoc()
    p = subprocess.Popen(
        [path_pandoc, '-v'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE)
    output = p.communicate()[0].decode().splitlines(False)
    versionstr = output[0]
    if platform.system() == 'Windows':
        version = float(versionstr[10:15])
    else:
        version = float(versionstr[6:11])

    if version < 1.18:
        try:
            path_pandoc = get_path_pandoc()
            p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(True)
            aux = help_text[15:89]

            return aux

        except OSError:
            error_converter_path()
    else:
        try:
            path_pandoc = get_path_pandoc()
            p = subprocess.Popen(
                    [path_pandoc, '-h'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE)
            help_text = p.communicate()[0].decode().splitlines(True)
            aux = help_text

            return aux

        except OSError:
            error_converter_path()





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

        error_file_selection()




    return matching

def create_simplefilelist():
    settings = QSettings('Pandoc', 'PanConvert')
    batch_settings = QSettings('Pandoc', 'PanConvert')
    batch_open_path = batch_settings.value('batch_open_path')
    filefilter = settings.value('batch_convert_filter','')

    filelist = glob.glob(batch_open_path + '/*')
    filter = filefilter.split(';')

    matching = []

    for filteritem in filter:

        matching_filter = [s for s in filelist if filteritem in s]
        for i in matching_filter:
            matching.append(i)
    if len(matching) == 0:

        error_file_selection()

    return matching


def convert(source, to, format=None, extra_args=(), encoding='utf-8'):

    """Converts given `source` from `format` `to` another. `source` may be either a file path or a string to be
    converted. It's possible to pass `extra_args` if needed. In case `format` is not provided, it will try to invert
    the format based on given `source`.
    Raises OSError if pandoc is not found! Make sure it has been installed and is available at path.
    """

    return _convert(_read_file, _process_file, source, to, format, extra_args, encoding=encoding)


def _convert(reader, processor, source, to, format=None, extra_args=(), encoding=None):
    source, format = reader(source, format, encoding=encoding)

    formats = {
        'dbk': 'docbook',
        'md': 'markdown_strict',
        'rest': 'rst',
        'tex': 'latex',
    }

    format = formats.get(format, format)
    to = formats.get(to, to)



    return processor(source, to, format, extra_args)


def _read_file(source, format, encoding='utf-8'):

    return source, format



def _process_file(source, to, format, extra_args):
    try:
        path_pandoc = get_path_pandoc()
        args = [path_pandoc, '--from=' + format, '--to=' + to]

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



        output1, error1 = p.communicate(source.encode('utf-8'))

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


