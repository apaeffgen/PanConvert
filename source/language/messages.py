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

from PyQt5 import QtCore, QtGui, QtWidgets
import datetime
from source.dialogs.dialog_preferences import *
import os

settings = QSettings('Pandoc', 'PanConvert')
path_pandoc = settings.value('path_pandoc','')

_translate = QtCore.QCoreApplication.translate

versionnumber = '0.2.6'
versiondate = '02.2017'
versionname = 'PanConvert - A Gui Wrapper for Pandoc'
copyrightinfo = 'Copyright by APaeffgen'



def version():
    versiontext = versionname + '<br>' + 'Version ' + versionnumber + ' on ' + versiondate + '<br>' + copyrightinfo
    return versiontext

def timestamp():
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return timestamp




'''' Messages in the Log Viewer'''''

def message_file_selection():
    time = timestamp()
    file_selection_message = _translate('message', 'The following file selection was made: ')
    message = time + '\n' + file_selection_message + '\n'
    return message

def error_buffer_name():
    time = timestamp()
    buffer_name_error = _translate('message', 'To use this function, you have to fill in '\
                        'BufferSaveName and BufferSaveSuffix in the Preference Dialog.')
    message = time + '\n' + buffer_name_error + '\n'
    return message

def error_formats():
    warning_fromFormat = _translate('message', 'Invalid from format! Expected one of these: ')
    warning_toFormat = _translate('message', 'Invalid to format! Expected one of these: ')

    return warning_fromFormat, warning_toFormat

def error_file_selection():
    time = timestamp()
    file_selection_error = _translate('message', 'No file has been selected. Check your Filters and settings.'\
                                               'Check your files.')
    message = time + '\n' + file_selection_error + '\n'
    return message


def error_converter_path():
    time = timestamp()
    converter_error = _translate('message', 'No Converter (Pandoc or Multimardown) could be found on your System. Are they installed?' \
                      'If so, please check the Pandoc / Multimarkdown Path in your Preferences.')
    QString = converter_error
    message = time +  '\n' +  converter_error + '\n'
    return message

def error_os_detection():
    time = timestamp()
    os_detection_error = _translate('message', 'Could not detect a Converter. Please fill in the Path' \
                     ' to Pandoc or Multimarkdown manually via Preferences.')
    message = time + '\n' + os_detection_error + '\n'
    return message

def error_open_file():
    open_file_error = _translate('message', 'No Preview of the File-Data possible. Try to manually convert. Good Luck.')
    QString = open_file_error
    message = open_file_error

    return message

def error_no_input():
    time = timestamp()
    no_input_error = (_translate('message', 'You have no Data to be converted. Please make an input'))
    QString = no_input_error
    message = time +  '\n' + no_input_error +  '\n'

    return message

def error_no_file():
    time = timestamp()
    no_file_error = _translate('message', 'You have to open at least one file in file conversion mode.'\
                                              ' <br>Did you put in from / to - formats?'\
                                              ' <br>If you are in directory mode, did you specify a directory?'\
                                              ' <br> Check your settings.')
    QString = no_file_error
    message = time +  '\n' + no_file_error +  '\n'
    return message



def error_binary_file():
    time = timestamp()
    binary_file_error = _translate('message', 'The Standard Converter can not handle binary files. If it is a docx-file, try the '\
                    'Manual Converter. ')
    QString = binary_file_error
    message = time +  '\n' + binary_file_error +  '\n'
    return message


def error_equal_formats():
    time = timestamp()
    equal_format_error = _translate('message', 'The from-Format and to-Format should not be identical.<br><br> '\
                                              'If you picked to-Lyx, only from-markdown is a valid option.<br><br>'\
                                              'Please make a different choice.')
    QString = equal_format_error
    message = time +  '\n' + equal_format_error +  '\n'
    return message

def error_empty_formats():
    time = timestamp()
    empty_format_error = _translate('message', 'If you fill in Arguments and uncheck the Box "Standard", you have to '\
                                          'provide at least the following Parameters: From, To. <br><br>'\
                                          '  Some Formats like odt, epub need an input '\
                                          'for "Parameter". Otherwise there will be no output at all')
    QString = empty_format_error
    message = time +  '\n' + empty_format_error +  '\n'
    return message

def error_unknown():
    time = timestamp()
    unknown_error = _translate('message', 'If you can read this message, something went wrong. Get some help at ' \
                 'http://panconvert.sourceforge.net/help')
    QString = unknown_error
    message = time +  '\n' + unknown_error +  '\n'
    return unknown_error


def error_no_output():
    time = timestamp()
    output_error = (_translate('message', 'There had been no output. Did you use the --output option to write a file?' \
                         '\nIf so, check your filesystem in the folder where Pandoc is installed'))
    QString = output_error
    message = time +  '\n' + output_error +  '\n'
    return message

def error_no_preview():
    time = timestamp()
    no_preview = _translate('message', 'No Preview of the File-Data possible. Try to manually convert. Good Luck.')
    Qstring = no_preview
    message = time +  '\n' + no_preview +  '\n'
    return message


def error_filelist():
    time = timestamp()
    file_list_error = _translate('message', 'Some file input was not correct')
    QString = file_list_error
    message = time +  '\n' + file_list_error +  '\n'
    return message

def message_file_converted():
    time = timestamp()
    file_converted_message = _translate('message', 'The following file was convertet: ')
    QString = file_converted_message
    message = time +  '\n' + file_converted_message +  '\n'
    return message


'''' Important QMessageBox errors - 1 Messages'''

def error_fatal():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', _translate('message', 'Somthing went terribly wrong. '\
                ' Hopefully only your Options are incorrect!' \
                '\n\nOr get some help from Panconvert / Pandoc!'))

def debug_message(message):
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', message)

