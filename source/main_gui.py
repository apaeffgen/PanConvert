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

import codecs
from os import *
from os.path import isfile
from PyQt5 import QtCore
from PyQt5.QtCore import QPoint, QSize
from source.dialogs.dialog_preferences import *
from source.dialogs.dialog_batch import *
from source.dialogs.dialog_info import *
from source.dialogs.dialog_fromformat import *
from source.dialogs.dialog_toformat import *
from source.dialogs.dialog_help import *
from source.converter.lyx_converter import *
from source.converter.manual_converter import *
from source.converter.batch_converter import *
from source.gui.panconvert_gui import Ui_notepad_New
from source.gui.panconvert_gui_ext import Ui_notepad

global openfile, filelist, actualLanguage, number

class StartQT5(QtWidgets.QMainWindow):
    global openfile, filelist

    """File Dialog Functions"""

    def file_new(self):
        global text, number
        number = 0
        text = ''
        self.ui.editor_window.setPlainText(text)
        self.ui.logBrowser.setPlainText(text)
        self.ui.actionSave.setEnabled(True)
        self.ui.MessageNumber.display(number)

    def file_open(self):
        global text, data, openfile, filelist, path_dialog

        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_open_path = batch_settings.value('batch_open_path')

        batchConversion = self.ui.BatchConversion.isChecked()

        if batchConversion is False:
            fd = QtWidgets.QFileDialog(self)

            if path_dialog == '':
                fd.setDirectory(QtCore.QDir.homePath())
            else:
                fd.setDirectory(path_dialog)

            self.filename = fd.getOpenFileName()
            openfile = self.filename[0]

            if isfile(self.filename[0]):
                try:
                    text = codecs.open(self.filename[0], 'r', 'utf-8').read()
                    data = self.ui.editor_window.setPlainText(text)

                except:
                    logtext = error_no_preview()
                    text = error_open_file()
                    data = self.ui.editor_window.setPlainText(text)
                    self.print_log_messages(logtext)

        elif batchConversion is True:

            fd = QtWidgets.QFileDialog(self)

            if batch_open_path == '':
                fd.setDirectory(QtCore.QDir.homePath())
            else:
                fd.setDirectory(batch_open_path)

            self.filename = fd.getOpenFileNames()
            openfile = self.filename[0]

            data = ('\n').join(openfile)

            self.ui.editor_window.appendPlainText(data)
            files = self.ui.editor_window.toPlainText()
            filelist = files.split('\n')

    def file_batch_input_directory(self):
        global data, openfiles, batch_open_path

        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_open_path = batch_settings.value('batch_open_path')

        self.ui.OpenPath.clear()

        fd = QtWidgets.QFileDialog(self)

        if batch_open_path == '':
            fd.setDirectory(QtCore.QDir.homePath())
        else:
            fd.setDirectory(batch_open_path)

        batch_directory = fd.getExistingDirectory()
        self.ui.OpenPath.insert(batch_directory)

    def file_batch_output_directory(self):
        global data, openfiles, batch_open_path_output

        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_open_path_output = batch_settings.value('batch_open_path_output')

        self.ui.OpenPathOutput.clear()

        fd = QtWidgets.QFileDialog(self)

        if batch_open_path_output == '':
            fd.setDirectory(QtCore.QDir.homePath())
        else:
            fd.setDirectory(batch_open_path_output)

        batch_directory = fd.getExistingDirectory()
        self.ui.OpenPathOutput.insert(batch_directory)


    def file_save(self):
        try:
            isfile(self.filename[0])
            file = codecs.open(self.filename[0], 'w', 'utf-8')
            file.write(self.ui.editor_window.toPlainText())
            file.close()
        except AttributeError:
            self.file_save_as()

    def file_save_as(self):
        global path_dialog

        fd = QtWidgets.QFileDialog(self)

        if path_dialog == '':
            fd.setDirectory(QtCore.QDir.homePath())
        else:
            fd.setDirectory(path_dialog)

        self.filename = fd.getSaveFileName(self)
        file = codecs.open(self.filename[0], 'w', 'utf-8')
        filedata = self.ui.editor_window.toPlainText()
        file.write(filedata)
        file.close()

    def buffer_save(self):
        global text, text_undo
        text_undo = text

        path_dialog = settings.value('path_dialog')
        BufferSaveSuffix = settings.value('BufferSaveSuffix')
        BufferSaveName = settings.value('BufferSaveName')

        try:
            os.path.exists(self.filename[0])
            file_exists = 1
        except:
            file_exists = 0

        if file_exists == 1:
            file, file_extension = os.path.splitext(self.filename[0])
            if BufferSaveSuffix != '':
                buffer = io.open(file + BufferSaveSuffix, "w")
                buffer.write(self.ui.editor_window.toPlainText())
                buffer.close()
            else:
                message = error_buffer_name()
                self.print_log_messages(message)
        else:
            if BufferSaveName != '':
                file_tmp = path_dialog + '/' +  BufferSaveName
                buffer = io.open(file_tmp, "w")
                buffer.write(self.ui.editor_window.toPlainText())
                buffer.close()
            else:
                message = error_buffer_name()
                self.print_log_messages(message)

    def undo(self):
        global text,text_undo
        text = text_undo
        self.ui.editor_window.setPlainText(text_undo)

    def closeEvent(self, event):
        settings = QSettings('Pandoc', 'PanConvert')

        Dock_Size = settings.value('Dock_Size')
        Window_Size = settings.value('Window_Size')
        if Dock_Size is True or Dock_Size == 'true':
            settings.setValue("geometry", self.saveState())
        if Window_Size is True or Window_Size == 'true':
            settings.setValue("size", self.size())
            settings.setValue("pos", self.pos())

    def print_log_messages(self, message):
        global number
        self.ui.logBrowser.appendPlainText(message)
        number = number + 1
        self.ui.MessageNumber.display(number)

    def windows_log_open(self):
        self.ui.dockLogWindow.show()

    def logviewer_above(self):
        self.ui.dockLogWindow.close()
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, self.ui.dockLogWindow)
        self.ui.dockLogWindow.show()

    def logviewer_bottom(self):
        self.ui.dockLogWindow.close()
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.ui.dockLogWindow)
        self.ui.dockLogWindow.show()

    def logviewer_left(self):
        self.ui.dockLogWindow.close()
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.ui.dockLogWindow)
        self.ui.dockLogWindow.show()

    def logviewer_right(self):
        self.ui.dockLogWindow.close()
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.ui.dockLogWindow)
        self.ui.dockLogWindow.show()

    def check_path(self):
        global error
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')

        if len(path_pandoc) == 0:
            get_path_pandoc()
            path_pandoc = settings.value('path_pandoc')

        elif not os.path.isfile(path_pandoc):
            get_path_pandoc()
            path_pandoc = settings.value('path_pandoc')

            if not os.path.isfile(path_pandoc):
                message = get_path_pandoc()
                self.print_log_messages(message)

    def check_path_markdown(self):
        global error
        settings = QSettings('Pandoc', 'PanConvert')
        path_multimarkdown = settings.value('path_multimarkdown','')

        if len(path_multimarkdown) == 0:
            get_path_multimarkdown()
            path_multimarkdown = settings.value('path_multimarkdown','')
        elif not os.path.isfile(path_multimarkdown):
            get_path_multimarkdown()
            path_multimarkdown = settings.value('path_multimarkdown','')

            if not os.path.isfile(path_multimarkdown):
                message = error_converter_path()
                self.print_log_messages(message)

    def check_format(self,FromFormat,ToFormat):
        _translate = QtCore.QCoreApplication.translate
        global error
        error = 0

        if not os.path.isfile(path_pandoc):
            get_pandoc_formats()


        from_formats, to_formats = get_pandoc_formats()
        warning_fromFormat, warning_toFormat = error_formats()

        if FromFormat not in from_formats:
            error = 1
            FromFormats = warning_fromFormat + '\n' + ', '.join(from_formats)
            time = timestamp()
            message = time + '\n' + FromFormats + '\n'
            self.print_log_messages(message)

        if ToFormat not in to_formats:
            error =2
            ToFormats = warning_toFormat + '\n' + ', '.join(to_formats)
            time = timestamp()
            message = _translate('extra_message', time + '\n' + ToFormats + '\n')
            self.print_log_messages(message)

        return error

    def batch_settings(self):
        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_settings.setValue('batch_convert_directory', self.ui.ParameterBatchconvertDirectory.isChecked())
        batch_settings.setValue('batch_convert_files', self.ui.ParameterBatchconvertFiles.isChecked())
        batch_settings.setValue('batch_convert_recursive', self.ui.ParameterBatchconvertRecursive.isChecked())
        batch_settings.setValue('batch_open_path', self.ui.OpenPath.text())
        batch_settings.setValue('batch_open_path_output', self.ui.OpenPathOutput.text())
        batch_settings.setValue('batch_convert_filter', self.ui.Filter.text())
        batch_settings.sync()
        batch_settings.status()

    '''Export Functions'''
    ''' Function for the seperate multimarkdown to lyx converter. Only works, when multimarkdown is installed '''

    def export_markdown2lyx(self):
        settings = QSettings('Pandoc', 'PanConvert')
        path_multimarkdown = settings.value('path_multimarkdown','')

        if not os.path.isfile(path_multimarkdown):
            self.check_path_markdown()
            path_multimarkdown = settings.value('path_multimarkdown','')

        global text, text_undo

        text = self.ui.editor_window.toPlainText()
        text_undo = text

        if os.path.isfile(path_multimarkdown):

            if text is not "":
                output_content = convert_markdown2lyx(text)
                self.ui.editor_window.setPlainText(output_content)
                text = output_content
            else:
                message = error_no_input()
                self.print_log_messages(message)

        else:
            error = error_converter_path()
            self.print_log_messages(error)

    def export_batch_convert_lyx(self):
        global error
        error = 0

        settings = QSettings('Pandoc', 'PanConvert')
        path_multimarkdown = settings.value('path_multimarkdown', '')

        if not os.path.isfile(path_multimarkdown):
            self.check_path_markdown()
            path_multimarkdown = settings.value('path_multimarkdown', '')

        if os.path.isfile(path_multimarkdown):
            global openfile, filelist

            batch_settings = QSettings('Pandoc', 'PanConvert')
            if platform.system() == 'Darwin':

                batch_convert_files = batch_settings.value('batch_convert_files')
                batch_convert_directory = batch_settings.value('batch_convert_directory')
                batch_convert_recursive = batch_settings.value('batch_convert_recursive')

            else:

                batch_convert_files = bool(strtobool(batch_settings.value('batch_convert_files')))
                batch_convert_directory = bool(strtobool(batch_settings.value('batch_convert_directory')))
                batch_convert_recursive = bool(strtobool(batch_settings.value('batch_convert_recursive')))

            data = self.ui.editor_window.toPlainText()

            if data is not '' and batch_convert_files is True:

                for openfiles in filelist:
                    if os.path.isfile(openfiles) is True:
                        message = batch_convert_markdown2lyx(openfiles)

                    else:
                        errormessage = ('Some file input was not correct:')
                        self.print_log_messages(errormessage)

                    if message == '':
                        message_tmp = message_file_converted()
                        message = message_tmp + openfiles + '\n'
                        self.print_log_messages(message)

            elif batch_convert_recursive is False and batch_convert_directory is True:
                message = ''
                filelist, message = create_simplefilelist()
                for openfiles in filelist:
                    if os.path.isfile(openfiles):
                        files = batch_convert_markdown2lyx(openfiles)
                        if files == '':
                            message_tmp = message_file_converted()
                            message = message_tmp + openfiles + '\n'
                            self.print_log_messages(message)

                    else:
                        errormessage = error_filelist()
                        self.print_log_messages(errormessage)


            elif batch_convert_recursive is True and batch_convert_directory is True:
                batch_open_path = batch_settings.value('batch_open_path')

                filelistrecursive, message = create_filelist(batch_open_path)
                for openfiles in filelistrecursive:
                    files = batch_convert_markdown2lyx(openfiles)

                    if files == '':
                        message_tmp = message_file_converted()
                        message = message_tmp + openfiles + '\n'
                        self.print_log_messages(message)

            else:
                message = error_no_file()
                self.print_log_messages(message)
        else:
            error = error_converter_path()
            self.print_log_messages(error)




    ''' Standard Converter for quick conversion: Parameters are fix coded in the function event_triggered(self) '''




    '''Function for the manual converter. Here the parameters have to be typed in.'''

    def export_manualconverter(self, fromFormat, toFormat, extraParameter):
        global error
        error = 0

        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')

        if not os.path.isfile(path_pandoc):
            self.check_path()
            path_pandoc = settings.value('path_pandoc')

        if os.path.isfile(path_pandoc):
            global text, text_undo, openfile

            text = self.ui.editor_window.toPlainText()
            text_undo = text
            if text == '':
                message = error_no_input()
                self.print_log_messages(message)

            elif text != error_open_file():

                error = self.check_format(fromFormat,toFormat)

                if error < 1:
                    output_content = convert_universal(text,toFormat,fromFormat,extraParameter)

                    if output_content is not None:
                        self.ui.editor_window.setPlainText(output_content)
                    else:
                        error_fatal()

            elif text == error_open_file():
                error = self.check_format(fromFormat,toFormat)

                if error < 1:
                    output_content = convert_binary(openfile,toFormat,fromFormat,extraParameter)

                    if output_content is not None:
                        self.ui.editor_window.setPlainText(output_content)
                    else:
                        error_fatal()

                    text = output_content
            else:
                error_fatal()
        else:
            error = error_converter_path()
            self.print_log_messages(error)

    ''' Functions for the batch conversion. '''
    ''' The main export batch function just decides which option of conversion '''

    def export_batch_conversion_manual(self, fromFormat, toFormat, extraParameter):
        global error
        error = 0

        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')

        if not os.path.isfile(path_pandoc):
            self.check_path()
            path_pandoc = settings.value('path_pandoc','')

        if os.path.isfile(path_pandoc):
            global openfile, filelist

            batch_settings = QSettings('Pandoc', 'PanConvert')

            if platform.system() == 'Darwin':
                batch_convert_files = batch_settings.value('batch_convert_files')
                batch_convert_directory = batch_settings.value('batch_convert_directory')
                batch_convert_recursive = batch_settings.value('batch_convert_recursive')

            else:
                batch_convert_files = bool(strtobool(batch_settings.value('batch_convert_files')))
                batch_convert_directory = bool(strtobool(batch_settings.value('batch_convert_directory')))
                batch_convert_recursive = bool(strtobool(batch_settings.value('batch_convert_recursive')))

            data = self.ui.editor_window.toPlainText()
            error = self.check_format(fromFormat,toFormat)

            if error < 1:
                if data is not '' and batch_convert_files is True:
                    self.convert_batch_singlefile(fromFormat, toFormat, extraParameter)

                elif batch_convert_recursive is False and batch_convert_directory is True:
                    self.convert_batch_directory(fromFormat, toFormat, extraParameter)

                elif batch_convert_recursive is True and batch_convert_directory is True:
                    self.convert_batch_drectory_recursive(fromFormat, toFormat, extraParameter)

                else:
                    message = error_no_file()
                    self.print_log_messages(message)
        else:
            error = error_converter_path()
            self.print_log_messages(error)

    def convert_batch_singlefile(self, fromFormat, toFormat, extraParameter):

        for openfiles in filelist:

            if os.path.isfile(openfiles) is True:
                self.ui.editor_window.setPlainText(data)
                message = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                self.print_log_messages(message)

            else:
                errormessage = error_filelist()
                self.print_log_messages(message)

    def convert_batch_directory(self, fromFormat, toFormat, extraParameter):
        message = ''
        filelist, message = create_simplefilelist()

        for openfiles in filelist:

            if os.path.isfile(openfiles):
                files = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                self.print_log_messages(files)

            else:
                errormessage = error_filelist()
                self.print_log_messages(errormessage)
        if message != '':
            self.print_log_messages(message)

    def convert_batch_drectory_recursive(self, fromFormat, toFormat, extraParameter):
        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_open_path = batch_settings.value('batch_open_path')
        message = ''

        filelistrecursive, message = create_filelist(batch_open_path)

        for openfiles in filelistrecursive:
            files = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
            self.print_log_messages(files)
        if message != '':
            self.print_log_messages(message)


    """External Dialog Windows - Trigger Functions"""

    def help_dialog(self):
        self.HelpDialog = HelpDialog(self)
        self.HelpDialog.show()



    def about_dialog(self):
        ## About Dialog with some Version info##
        msg = QtWidgets.QMessageBox()
        msg.setText(version())
        msg.setWindowTitle("About Dialog")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


    def preference_dialog(self):
        """ References to dialog_preferences.py"""
        self.PreferenceDialog = PreferenceDialog(self)
        self.PreferenceDialog.show()

    def batch_dialog(self):
        """ References to dialog_batch.py"""
        self.BatchDialog = BatchDialog(self)
        self.BatchDialog.show()

    def info_dialog(self):
        """ References to dialog_info.py"""
        self.InfoDialog = InfoDialog(self)
        self.InfoDialog.show()

    def fromformats_dialog(self):
        self.FromFormatDialog = FromFormatDialog(self)
        self.FromFormatDialog.show()

    def toformats_dialog(self):
        self.ToFormatsDialog = ToFormatDialog(self)
        self.ToFormatsDialog.show()







    """Gui-Trigger-Function for RadioButtons"""

    def event_triggered(self):
        settings = QSettings('Pandoc', 'PanConvert')

        Button_OldGui = settings.value('Button_OldGui', True)
        Button_NewGui = settings.value('Button_NewGui', False)

        global fromFormat,toFormat,extraParameter
        fromFormat = self.ui.FromParameter.text()
        toFormat = self.ui.ToParameter.text()






        ''' Old Gui Events '''

        standard_conversion = self.ui.StandardConversion.isChecked()
        extraParameter = self.ui.ExtraParameter.text()
        batchConversion = self.ui.BatchConversion.isChecked()


        if standard_conversion is True and batchConversion is False:
            if self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_manualconverter("markdown", "latex", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_manualconverter("markdown", "opml", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLyx.isChecked() is True:
                self.export_markdown2lyx()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_manualconverter("opml", "markdown", "--atx-header")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_manualconverter("opml", "latex", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_manualconverter("latex", "markdown", "--atx-header")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToOpml.isChecked()is True:
                self.export_manualconverter("latex", "opml", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_manualconverter("html", "markdown", "--atx-header")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_manualconverter("markdown", "html", "--standalone")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_manualconverter("opml", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_manualconverter("html", "opml", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_manualconverter("latex", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_manualconverter("html", "latex", "--standalone")
            else:
                message = error_equal_formats()
                self.print_log_messages(message)

        elif standard_conversion is True and batchConversion is True:
            if self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_batch_conversion_manual("markdown", "latex", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_batch_conversion_manual("markdown", "opml", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLyx.isChecked() is True:
                self.export_batch_convert_lyx()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_batch_conversion_manual("opml", "markdown", "--atx-header")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_batch_conversion_manual("opml", "latex", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_batch_conversion_manual("latex", "markdown", "--atx-header")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToOpml.isChecked()is True:
                self.export_batch_conversion_manual("latex", "opml", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_batch_conversion_manual("html", "markdown", "--atx-header")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_batch_conversion_manual("markdown", "html", "--standalone")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_batch_conversion_manual("opml", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_batch_conversion_manual("html", "opml", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_batch_conversion_manual("latex", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_batch_conversion_manual("html", "latex", "--standalone")
            else:
                message = error_equal_formats()
                self.print_log_messages(message)

        elif standard_conversion is False and batchConversion is False:# and extraParameter is not "":
            self.export_manualconverter(fromFormat, toFormat, extraParameter)


        elif standard_conversion is False and batchConversion is True:
            self.export_batch_conversion_manual(fromFormat, toFormat, extraParameter)

        elif fromFormat is "" or toFormat is "":
            message = error_empty_formats()
            self.print_log_messages(message)

        else:
            error_fatal()


    """Gui-Event Definitions"""

    def __init__(self, parent=None):
        global path_dialog, text, text_undo, openfile, actualLanguage, number

        number = 0
        text = ''
        text_undo = ''
        settings = QSettings('Pandoc', 'PanConvert')

        Button_OldGui = settings.value('Button_OldGui', True)
        Button_NewGui = settings.value('Button_NewGui', False)

        QtWidgets.QWidget.__init__(self, parent)
        if Button_OldGui is True or Button_OldGui is 'True' or Button_OldGui == 'true':
            self.ui = Ui_notepad()
        else:
            self.ui = Ui_notepad_New()

        self.ui.setupUi(self)
        self.ui.closeEvent = self.closeEvent

        if Button_NewGui is True or Button_NewGui is 'true' or Button_NewGui == 'true':

            Tab_StandardConverter = settings.value('Tab_StandardConverter', True)
            Tab_ManualConverter = settings.value('Tab_ManualConverter', False)
            Tab_BatchConverter = settings.value('Tab_BatchConverter', False)

            if Tab_StandardConverter is True or Tab_StandardConverter is 'True' or Tab_StandardConverter == 'true':
                self.ui.Converter_Type.setCurrentIndex(0)
            if Tab_ManualConverter is True or Tab_ManualConverter is 'True' or Tab_ManualConverter == 'true':
                self.ui.Converter_Type.setCurrentIndex(1)
            if Tab_BatchConverter is True or Tab_BatchConverter is 'True' or Tab_BatchConverter == 'true':
                self.ui.Converter_Type.setCurrentIndex(2)

            ## Batch Settings##
            batch_settings = QSettings('Pandoc', 'PanConvert')
            settings = QSettings('Pandoc', 'PanConvert')

            parameterBatchconvertDirectory = batch_settings.value('batch_convert_directory', True)
            parameterBatchconvertFiles = batch_settings.value('batch_convert_files', False)
            parameterBatchconvertRecursive = batch_settings.value('batch_convert_recursive', True)

            # Batch Path Settings
            batch_open_path = batch_settings.value('batch_open_path')
            self.ui.OpenPath.insert(batch_open_path)
            batch_open_path_output = batch_settings.value('batch_open_path_output')
            self.ui.OpenPathOutput.insert(batch_open_path_output)

            # Batch Option Settings
            batch_convert_filter = batch_settings.value('batch_convert_filter')
            self.ui.Filter.insert(batch_convert_filter)
            self.ui.Button_SetBatchConverter.clicked.connect(self.batch_settings)
            self.ui.Button_Open_Path.clicked.connect(self.file_batch_input_directory)
            self.ui.Button_Open_Path_Output.clicked.connect(self.file_batch_output_directory)

        '''File-Dialog Functions'''
        self.ui.actionOpen.triggered.connect(self.file_open)
        self.ui.actionSave.triggered.connect(self.buffer_save)
        self.ui.actionSave_AS.triggered.connect(self.file_save_as)
        self.ui.actionNew.triggered.connect(self.file_new)

        '''File-Edit Menu Functions'''
        self.ui.actionUndo.triggered.connect(self.undo)

        '''Window Functions'''
        self.ui.actionLogViewer.triggered.connect(self.windows_log_open)
        self.ui.actionAbove.triggered.connect(self.logviewer_above)
        self.ui.actionBelow.triggered.connect(self.logviewer_bottom)
        self.ui.actionLeft.triggered.connect(self.logviewer_left)
        self.ui.actionRight.triggered.connect(self.logviewer_right)

        '''Helper-Functions for manual conversion'''
        self.ui.ButtonFromFormat.clicked.connect(self.fromformats_dialog)
        self.ui.ButtonToFormat.clicked.connect(self.toformats_dialog)
        self.ui.ButtonOptions.clicked.connect(self.info_dialog)

        ''' Main Button Functions'''

        self.ui.ButtonRevert.clicked.connect(self.undo)
        self.ui.ButtonConvert.clicked.connect(self.event_triggered)

        '''Help Menu Functions'''
        self.ui.actionHelp.triggered.connect(self.help_dialog)
        self.ui.actionAbout.triggered.connect(self.about_dialog)

        '''Preference Functions'''
        self.ui.actionPreferences.triggered.connect(self.preference_dialog)
        self.ui.actionSave.setEnabled(True)

        '''Old Gui Functions '''''

        if Button_OldGui is True or Button_OldGui == 'true':
            self.ui.ButtonBatch.clicked.connect(self.batch_dialog)

        '''Setting-Initialization and Default Settings for the first start'''

        Window_Size = settings.value('Window_Size')
        Dock_Size = settings.value('Dock_Size')
        if Dock_Size is True or Dock_Size == 'true':

            self.restoreState(settings.value('geometry'))
        if Window_Size is True or Window_Size == 'true':
            self.resize(settings.value("size", QSize(270, 225)))
            self.move(settings.value("pos", QPoint(50, 50)))

        path_dialog = settings.value('path_dialog')
        fromParameter = settings.value('fromParameter')
        toParameter = settings.value('toParameter')
        xtraParameter = settings.value('xtraParameter')

        From_Markdown = settings.value('From_Markdown', False)
        From_Html = settings.value('From_Html', False)
        From_Latex = settings.value('From_Latex', False)
        From_Opml = settings.value('From_Opml', False)

        To_Markdown = settings.value('To_Markdown', False)
        To_Html = settings.value('To_Html', False)
        To_Latex = settings.value('To_Latex', False)
        To_Opml = settings.value('To_Opml', False)
        To_Lyx = settings.value('To_Lyx', False)

        Standard_Conversion = settings.value('Standard_Conversion', False)
        Batch_Conversion = settings.value('Batch_Conversion', False)

        if settings.value('From_Markdown') is not None:
            if platform.system() == 'Darwin':
                self.ui.StandardConversion.setChecked(Standard_Conversion)
                self.ui.BatchConversion.setChecked(Batch_Conversion)
                self.ui.ButtonFromMarkdown.setChecked(From_Markdown)
                self.ui.ButtonFromHtml.setChecked(From_Html)
                self.ui.ButtonFromLatex.setChecked(From_Latex)
                self.ui.ButtonFromOpml.setChecked(From_Opml)
                self.ui.ButtonToMarkdown.setChecked(To_Markdown)
                self.ui.ButtonToHtml.setChecked(To_Html)
                self.ui.ButtonToLatex.setChecked(To_Latex)
                self.ui.ButtonToOpml.setChecked(To_Opml)
                self.ui.ButtonToLyx.setChecked(To_Lyx)
                self.ui.FromParameter.setText(fromParameter)
                self.ui.ToParameter.setText(toParameter)
                self.ui.ExtraParameter.setText(xtraParameter)

            else:
                self.ui.StandardConversion.setChecked(strtobool(Standard_Conversion))
                self.ui.BatchConversion.setChecked(strtobool(Batch_Conversion))
                self.ui.ButtonFromMarkdown.setChecked(strtobool(From_Markdown))
                self.ui.ButtonFromHtml.setChecked(strtobool(From_Html))
                self.ui.ButtonFromLatex.setChecked(strtobool(From_Latex))
                self.ui.ButtonFromOpml.setChecked(strtobool(From_Opml))
                self.ui.ButtonToMarkdown.setChecked(strtobool(To_Markdown))
                self.ui.ButtonToHtml.setChecked(strtobool(To_Html))
                self.ui.ButtonToLatex.setChecked(strtobool(To_Latex))
                self.ui.ButtonToOpml.setChecked(strtobool(To_Opml))
                self.ui.ButtonToLyx.setChecked(strtobool(To_Lyx))
                self.ui.FromParameter.setText(fromParameter)
                self.ui.ToParameter.setText(toParameter)
                self.ui.ExtraParameter.setText(xtraParameter)

if __name__ == "__main__":
    myapp = StartQT5()
    myapp.show()