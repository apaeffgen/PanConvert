from __future__ import with_statement

__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_

import subprocess
import platform
import os
from PyQt5 import QtWidgets

def get_path():
    systempath = os.getcwd()
    d = open(systempath + "/source/preferences.txt", "r")
    #d = open("preferences.txt", "r")
    path = d.readline()
    d.close()

    if len(path) == 0:

        if platform.system() == 'Darwin' or platform.system() == 'Linux':
            args = ['which', 'pandoc']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path = str.rstrip(p.communicate(path.encode('utf-8'))[0].decode('utf-8'))
            return path

        elif platform.system() == 'Windows':
            args = ['where', 'pandoc']
            p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            path = str.rstrip(p.communicate(path.encode('utf-8'))[0].decode('utf-8'))
            return path
        else:
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Could not detect the actual operating system. Please fill in the Path'
                                          ' to Pandoc manually via Preferences.')

    elif len(path) != 0:
        return path

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
        'md': 'markdown',
        'rest': 'rst',
        'tex': 'latex',
    }

    format = formats.get(format, format)
    to = formats.get(to, to)

    if not format:
        raise RuntimeError('Missing format!')

    from_formats, to_formats = get_pandoc_formats()

    if format not in from_formats:
        QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Invalid from format! Expected one of these: ' + ', '.join(from_formats))

    if to not in to_formats:
        QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Invalid to format! Expected one of these: ' + ', '.join(to_formats))

    return processor(source, to, format, extra_args)


def _read_file(source, format, encoding='utf-8'):

    return source, format


# noinspection PyPep8
def _process_file(source, to, format, extra_args):
    try:
        path = get_path()
        args = [path, '--from=' + format, '--to=' + to]

        if extra_args is not '' :
            args.append(extra_args)

        p = subprocess.Popen(
                args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

        return p.communicate(source.encode('utf-8'))[0].decode('utf-8')

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
    try:
        path = get_path()
        p = subprocess.Popen(
                [path, '-h'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)
        help_text = p.communicate()[0].decode().splitlines(False)
        txt = ' '.join(help_text[1:help_text.index('Options:')])

        aux = txt.split('Output formats: ')
        in_ = aux[0].split('Input formats: ')[1].split(',')
        out = aux[1].split(',')

        return [f.strip() for f in in_], [f.strip() for f in out]

    except OSError:
        QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Pandoc could not be found on your System. Is it installed?'
                                          'If so, please check the Pandoc Path in your Preferences.')





