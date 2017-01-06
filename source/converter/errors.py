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

    ## All Errormessages used in the Program##

no_converter_detected = 'No Converter (Pandoc or Multimardown) could be found on your System. Are they installed?'+\
                         'If so, please check the Pandoc / Multimarkdown Path in your Preferences.';

os_detection_error = 'Could not detect the actual operating system. Please fill in the Path'+\
                     ' to Pandoc or Multimarkdown manually via Preferences.'

file_selection_error = 'No file has been selected. Check your Filters and settings.'+\
                                                  'Check your files.'

output_error = 'There had been no output. Did you use the --output option to write a file?' \
                         '\nIf so, check your filesystem in the folder where Pandoc is installed'

no_preview = 'No Preview of the File-Data possible. Try to manually convert. Good Luck.'

no_input =  'You have no Data to be converted. Please make an input'


no_uncatched_error = '\n If no uncatched Error occured, the batch conversion should have produced some files.' \
                              '\n Converted files should have been written to the same place as the original files.' \
                              ' \n There is no visual output. So please check your converted files at the filesystem level.' \
                              '\n \n When in batch-file-mode, for a better experience, please clear the window before starting a new conversion'


no_file_error = 'You have to open at least one file in file conversion mode.'\
                                              ' <br>Did you put in from / to - formats?'\
                                              ' <br>If you are in directory mode, did you specify a directory?'\
                                              ' <br> Check your settings.'

fatal_error = 'Somthing went terribly wrong. '\
                ' Hopefully only your Options are incorrect!' \
                '\n\nOr get some help from Panconvert / Pandoc!'

binary_file_error = 'The Standard Converter can not handle binary files. If it is a docx-file, try the '\
                    'Manual Converter. '

file_list_error = 'Some file input was not correct'

missing_file_error = 'You have to open at least one file in file conversion mode.'\
                                                  ' <br>Did you put in from / to - formats?'\
                                                  ' <br>If you are in directory mode, did you specify a directory?'\
                                                  ' <br> Check your settings.'

equal_format_error = 'The from-Format and to-Format should not be identical.<br><br> '\
                                              'If you picked to-Lyx, only from-markdown is a valid option.<br><br>'\
                                              'Please make a different choice.'


empty_format_error = 'If you fill in Arguments and uncheck the Box "Standard", you have to '\
                                          'provide at least the following Parameters: From, To. <br><br>'\
                                          '  Some Formats like odt, epub need an input '\
                                          'for "Parameter". Otherwise there will be no output at all'

unknown_error = 'If you can read this message, something went wrong. Get some help at ' \
                 'http://panconvert.sourceforge.net/help'

    ## All functions used to call the above declared error messages##

def error_converter_path():
    QtWidgets.QMessageBox.warning(None, 'Error-Message', no_converter_detected)

def error_os_detection():
    QtWidgets.QMessageBox.warning(None, 'Error-Message',os_detection_error)

def error_file_selection():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message',file_selection_error)

def error_no_output():
    output_error
    return output_error

def error_no_preview():
    no_preview
    return no_preview

def error_no_input():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', no_input)

def error_uncatched():
    no_uncatched_error
    return no_uncatched_error

def error_no_file():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', no_file_error)

def error_fatal():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', fatal_error)

def error_binary_file():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', binary_file_error)

def error_filelist():
    file_list_error
    return file_list_error

def error_missing_file():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', missing_file_error)

def error_equal_formats():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', equal_format_error)

def error_empty_formats():
    QtWidgets.QMessageBox.warning(None, 'Warning-Message', empty_format_error)

def error_unknown():
    unknown_error
    return unknown_error

