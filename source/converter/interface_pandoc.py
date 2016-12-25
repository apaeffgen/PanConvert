from __future__ import with_statement
#!/usr/local/bin/python3
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

import subprocess
import platform, os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings

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
            settings.setValue('path_pandoc', path_pandoc)
            settings.sync()
            return path_pandoc

        elif platform.system() == 'Windows':
            args = ['where', 'pandoc']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path_pandoc = str.rstrip(p.communicate(path_pandoc.encode('utf-8'))[0].decode('utf-8'))
            settings.setValue('path_pandoc', path_pandoc)
            settings.sync()
            return path_pandoc
        else:
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Could not detect the actual operating system. Please fill in the Path'
                                          ' to Pandoc manually via Preferences.')

    elif len(path_pandoc) != 0:
        return path_pandoc

    else:
       QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'I tried automagically to detect pandoc. But it failed.'
                                          'Please input the path of pandoc manually via preferences')


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

    # if not format:
    #     raise RuntimeError('Missing format!')

    from_formats, to_formats = get_pandoc_formats()

    if format == '': # not in from_formats:
        QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Empty from format! Expected one of these: ' + ', '.join(from_formats))
        raise RuntimeError('Missing format!')

    if to == '': # not in to_formats:
        QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Empty to format! Expected one of these: ' + ', '.join(to_formats))
        raise RuntimeError('Missing format!')

    return processor(source, to, format, extra_args)


def _read_file(source, format, encoding='utf-8'):

    return source, format


# noinspection PyPep8
def _process_file(source, to, format, extra_args):
    try:
        path_pandoc = get_path_pandoc()
        args = [path_pandoc, '--from=' + format, '--to=' + to]

        if extra_args is not '' :
            extra_args = extra_args.split(';')
            for arg in extra_args:
                args.append(arg)


        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

        #Original Code without error-handling
        #output = p.communicate(source.encode('utf-8'))[0].decode('utf-8')

        output1, error1 = p.communicate(source.encode('utf-8'))
        output = output1.decode('utf-8')
        error = error1.decode('utf-8')

        if p.returncode != 0:
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'An Error occurred. <br><br>{}'.format(error))
        else:
            return output



    except OSError:
        QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Pandoc could not be found on your System. Is it installed?'
                                          'If so, please check the Pandoc Path in your Preferences.')

# noinspection PyPep8
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
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Pandoc could not be found on your System. Is it installed?'
                                          'If so, please check the Pandoc Path in your Preferences.')
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
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Pandoc could not be found on your System. Is it installed?'
                                          'If so, please check the Pandoc Path in your Preferences.')


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
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                              'Pandoc could not be found on your System. Is it installed?'
                                              'If so, please check the Pandoc Path in your Preferences.')
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
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                              'Pandoc could not be found on your System. Is it installed?'
                                              'If so, please check the Pandoc Path in your Preferences.')



