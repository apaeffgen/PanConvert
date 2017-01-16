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
#import markdown
from PyQt5.QtCore import QPoint, QSize
from source.dialog_preferences import *
from source.dialog_batch import *
from source.dialog_info import *
from source.dialog_help import *
from source.converter.lyx import *
from source.converter.manual_converter import *
from source.converter.batch_converter import *
from source.gui.panconvert_gui_ext import Ui_notepad


global openfile, filelist, actualLanguage

#TODO: Abstraction of Error Functions. Separate Error / Log Window

# noinspection PyStatementEffect,PyAttributeOutsideInit,PyAttributeOutsideInit,PyAttributeOutsideInit
class StartQT5(QtWidgets.QMainWindow):
    global openfile, filelist

    """File Dialog Functions"""

    def file_dialog(self):
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
            from os.path import isfile
            if isfile(self.filename[0]):
                try:
                    text = codecs.open(self.filename[0], 'r', 'utf-8').read()
                    data = self.ui.editor_window.setPlainText(text)

                except:
                    text = error_no_preview()
                    #data = self.ui.editor_window.setPlainText(text)
                    data = self.ui.logBrowser.appendPlainText(text)


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


    def file_save(self):
        from os.path import isfile
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

    def file_new(self):
        global text
        text = ''
        self.ui.editor_window.setPlainText(text)
        self.ui.logBrowser.setPlainText(text)
        self.ui.actionSave.setEnabled(True)



    def buffer_save(self):
        global text, text_undo
        text_undo = text
        text = self.ui.editor_window.toPlainText()

    def undo(self):
        global text,text_undo
        text = text_undo
        self.ui.editor_window.setPlainText(text_undo)


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

    def print_error_messages(self, message):
        message = self.ui.logBrowser.appendPlainText(message)



    def list_from_formats(self):
        from_formats, to_formats = get_pandoc_formats()
        QtWidgets.QMessageBox.information(None, 'Warning-Message',
                                          'List of From-Formats: <br><br>'+ ', '.join(from_formats))

    def list_to_formats(self):
        from_formats, to_formats = get_pandoc_formats()
        QtWidgets.QMessageBox.information(None, 'Warning-Message',
                                          'List of To-Formats: <br><br>'+ ', '.join(to_formats))

    def list_options(self):
        options =  get_pandoc_options()

        QtWidgets.QMessageBox.information(None, 'Warning-Message', 'Detailed-Text'
                                          'List of Options: <br><br>'+ ', '.join(options))


    def check_path(self):
        global error
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')

        if len(path_pandoc) == 0:
            get_path_pandoc()

    def check_path_markdown(self):
        global error
        settings = QSettings('Pandoc', 'PanConvert')
        path_multimarkdown = settings.value('path_multimarkdown','')

        if len(path_multimarkdown) == 0:
            get_path_multimarkdown()

    def check_format(self,FromFormat,ToFormat):
        global error
        error = 0
        get_pandoc_formats()

        from_formats, to_formats = get_pandoc_formats()

        if FromFormat not in from_formats:
            error = 1
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Invalid from format! Expected one of these: ' + ', '.join(from_formats))

        if ToFormat not in to_formats:
            error =2
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'Invalid to format! Expected one of these: ' + ', '.join(to_formats))
        return error



    '''Export Functions'''

    ''' Function for the seperate multimarkdown to lyx converter. Only works, when multimarkdown is installed '''

    def export_markdown2lyx(self):


        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_markdown2lyx(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            message = error_no_input()
            self.ui.logBrowser.appendPlainText(message)

    def export_batch_convert_lyx(self):
        global error
        error = 0
        self.check_path_markdown()
        settings = QSettings('Pandoc', 'PanConvert')
        path_multimarkdown = settings.value('path_multimarkdown','')
        if len(path_multimarkdown) != 0:


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
                        #self.ui.editor_window.appendPlainText(errormessage)
                        self.ui.logBrowser.appendPlainText(errormessage)

                if message == '':
                    message = error_uncatched()
                    #self.ui.editor_window.appendPlainText(message)
                    self.ui.logBrowser.appendPlainText(message)

            elif batch_convert_recursive is False and batch_convert_directory is True:


                filelist = create_simplefilelist()
                for openfiles in filelist:
                    if os.path.isfile(openfiles):
                        message = batch_convert_markdown2lyx(openfiles)

                if message == '':
                    message = error_uncatched()
                    #self.ui.editor_window.appendPlainText(message)
                    self.ui.logBrowser.appendPlainText(message)


            elif batch_convert_recursive is True and batch_convert_directory is True:
                batch_open_path = batch_settings.value('batch_open_path')

                filelistrecursive = create_filelist(batch_open_path)

                for openfiles in filelistrecursive:
                    message = batch_convert_markdown2lyx(openfiles)

                if message == '':
                    message = error_uncatched()
                    #self.ui.editor_window.appendPlainText(message)
                    self.ui.logBrowser.appendPlainText(message)

            else:
                message = error_no_file()
                self.ui.logBrowser.appendPlainText(message)
        else:
            error_converter_path()




    ''' Standard Converter for quick conversion: Parameters are fix coded in the function event_triggered(self) '''

    def export_standardconverter(self, fromFormat, toFormat, extraParameter):


        self.check_path()
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')
        if len(path_pandoc) != 0:

            global text, text_undo, openfile
            text = self.ui.editor_window.toPlainText()
            text_undo = text
            if text == '':
                message = error_no_input()
                self.ui.logBrowser.appendPlainText(message)


            elif text != error_no_preview():
                output_content = convert_universal(text,toFormat,fromFormat,extraParameter)

                if output_content is not None:
                    self.ui.editor_window.setPlainText(output_content)
                else:
                    error_fatal()

            elif text == error_no_preview():
                message = error_binary_file()
                self.ui.logBrowser.appendPlainText(message)
            else:
                error_fatal()




    '''Function for the manual converter. Here the parameters have to be typed in.'''

    def export_manualconverter(self):
        global error
        error = 0
        self.check_path()
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')
        if len(path_pandoc) != 0:
            global text, text_undo, openfil
            text = self.ui.editor_window.toPlainText()
            text_undo = text
            if text == '':
                message = error_no_input()
                self.ui.logBrowser.appendPlainText(message)

            elif text != error_no_preview():

                error = self.check_format(fromFormat,toFormat)

                if error < 1:
                    output_content = convert_universal(text,toFormat,fromFormat,extraParameter)

                    if output_content is not None:
                        self.ui.editor_window.setPlainText(output_content)
                    else:
                        error_fatal()


            elif text == error_no_preview():

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

    ''' Functions for the batch conversion. '''

    def export_batch_conversion_standard(self, fromFormat, toFormat, extraParameter):

        self.check_path()
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')
        if len(path_pandoc) != 0:

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
                        self.ui.editor_window.setPlainText(data)
                        message = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                        #self.ui.editor_window.appendPlainText(message)

                        self.ui.logBrowser.appendPlainText(message)
                    else:

                        errormessage = error_filelist()
                        #self.ui.editor_window.appendPlainText(errormessage)
                        self.ui.logBrowser.appendPlainText(errormessage)

            elif batch_convert_recursive is False and batch_convert_directory is True:


                filelist = create_simplefilelist()
                for openfiles in filelist:
                    if os.path.isfile(openfiles):
                        output_content = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                        #self.ui.editor_window.setPlainText(output_content)
                        self.ui.logBrowser.setPlainText(output_content)

            elif batch_convert_recursive is True and batch_convert_directory is True:
                batch_open_path = batch_settings.value('batch_open_path')

                filelistrecursive = create_filelist(batch_open_path)

                for openfiles in filelistrecursive:
                    output_content = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                    #self.ui.editor_window.setPlainText(output_content)
                    self.ui.logBrowser.setPlainText(output_content)

            else:
                message = error_no_file()
                self.ui.logBrowser.appendPlainText(message)




    def export_batch_conversion_manual(self):
        global error
        error = 0
        self.check_path()
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')
        if len(path_pandoc) != 0:

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

                    for openfiles in filelist:
                        if os.path.isfile(openfiles) is True:
                            self.ui.editor_window.setPlainText(data)
                            message = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                            #self.ui.editor_window.appendPlainText(message)
                            self.ui.logBrowser.appendPlainText(message)
                        else:
                            errormessage = error_filelist()
                            #self.ui.editor_window.appendPlainText(errormessage)
                            self.ui.logBrowser.appendPlainText(errormessage)

                elif batch_convert_recursive is False and batch_convert_directory is True:
                    filelist = create_simplefilelist()
                    for openfiles in filelist:
                        if os.path.isfile(openfiles):
                            output_content = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                            #self.ui.editor_window.setPlainText(output_content)
                            self.ui.logBrowser.setPlainText(output_content)

                elif batch_convert_recursive is True and batch_convert_directory is True:
                    batch_open_path = batch_settings.value('batch_open_path')

                    filelistrecursive = create_filelist(batch_open_path)

                    for openfiles in filelistrecursive:
                        output_content = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                        #self.ui.editor_window.setPlainText(output_content)
                        self.ui.logBrowser.setPlainText(output_content)

                else:
                    message = error_no_file()
                    self.ui.logBrowser.appendPlainText(message)




    def print_error_message(self, message):
        message = error_no_input
        self.ui.logBrowser.setPlainText(message)
        return message



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
        retval = msg.exec_()


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

    def closeEvent(self, event):
        settings = QSettings('Pandoc', 'PanConvert')

        Dock_Size = settings.value('Dock_Size')
        Window_Size = settings.value('Window_Size')
        if Dock_Size is True:
            settings.setValue("geometry", self.saveState())
        if Window_Size is True:
            #settings.setValue('size', self.geometry())
            settings.setValue("size", self.size())
            settings.setValue("pos", self.pos())



    """Gui-Trigger-Function for RadioButtons"""

    def event_triggered(self):
        global fromFormat,toFormat,extraParameter
        fromFormat = self.ui.FromParameter.text()
        toFormat = self.ui.ToParameter.text()
        standard_conversion = self.ui.StandardConversion.isChecked()
        extraParameter = self.ui.ExtraParameter.text()
        batchConversion = self.ui.BatchConversion.isChecked()

        if standard_conversion is True and batchConversion is False:
            if self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_standardconverter("md", "latex", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_standardconverter("md", "opml", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLyx.isChecked() is True:
                self.export_markdown2lyx()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_standardconverter("opml", "md", "--atx-header")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_standardconverter("opml", "latex", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_standardconverter("latex", "md", "--atx-header")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToOpml.isChecked()is True:
                self.export_standardconverter("latex", "opml", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_standardconverter("html", "md", "--atx-header")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_standardconverter("md", "html", "--standalone")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_standardconverter("opml", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_standardconverter("html", "opml", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_standardconverter("latex", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_standardconverter("html", "latex", "--standalone")
            else:
                message = error_equal_formats()
                self.ui.logBrowser.appendPlainText(message)

        elif standard_conversion is True and batchConversion is True:
            if self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_batch_conversion_standard("markdown", "latex", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_batch_conversion_standard("markdown", "opml", "--standalone")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLyx.isChecked() is True:
                self.export_batch_convert_lyx()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_batch_conversion_standard("opml", "markdown", "--atx-header")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_batch_conversion_standard("opml", "latex", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_batch_conversion_standard("latex", "markdown", "--atx-header")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToOpml.isChecked()is True:
                self.export_batch_conversion_standard("latex", "opml", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.export_batch_conversion_standard("html", "markdown", "--atx-header")
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_batch_conversion_standard("markdown", "html", "--standalone")
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_batch_conversion_standard("opml", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.export_batch_conversion_standard("html", "opml", "--standalone")
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.export_batch_conversion_standard("latex", "html", "--standalone")
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.export_batch_conversion_standard("html", "latex", "--standalone")
            else:
                message = error_equal_formats()
                self.ui.logBrowser.appendPlainText(message)

        elif standard_conversion is False and batchConversion is False:# and extraParameter is not "":
            self.export_manualconverter()


        elif standard_conversion is False and batchConversion is True:
            self.export_batch_conversion_manual()

        elif fromFormat is "" or toFormat is "":
            message = error_empty_formats()
            self.ui.logBrowser.appendPlainText(message)


        else:
            error_fatal()



    """Gui-Event Definitions"""

    def __init__(self, parent=None):
        global path_dialog, text, text_undo, openfile, actualLanguage


        text = ''
        text_undo = ''

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_notepad()
        self.ui.setupUi(self)
        self.ui.closeEvent = self.closeEvent



        '''File-Dialog Functions'''
        self.ui.actionOpen.triggered.connect(self.file_dialog)
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
        self.ui.ButtonFromFormat.clicked.connect(self.list_from_formats)
        self.ui.ButtonToFormat.clicked.connect(self.list_to_formats)
        self.ui.ButtonOptions.clicked.connect(self.info_dialog)

        ''' Main Button Functions'''
        self.ui.ButtonBatch.clicked.connect(self.batch_dialog)
        self.ui.ButtonRevert.clicked.connect(self.undo)
        self.ui.ButtonConvert.clicked.connect(self.event_triggered)

        '''Help Menu Functions'''
        self.ui.actionHelp.triggered.connect(self.help_dialog)
        self.ui.actionAbout.triggered.connect(self.about_dialog)

        '''Preference Functions'''
        self.ui.actionPreferences.triggered.connect(self.preference_dialog)
        self.ui.actionSave.setEnabled(True)

        '''Setting-Initialization and Default Settings for the first start'''
        settings = QSettings('Pandoc', 'PanConvert')
        actualLanguage = settings.value('default_language')


        Window_Size = settings.value('Window_Size')
        Dock_Size = settings.value('Dock_Size')
        if Dock_Size is True:
            self.restoreState(settings.value('geometry'))
        if Window_Size is True:
            #self.restoreGeometry(settings.value('size'))
            self.resize(settings.value("size", QSize(270, 225)))
            self.move(settings.value("pos", QPoint(50, 50)))


        path_dialog = settings.value('path_dialog')
        fromParameter = settings.value('fromParameter')
        toParameter = settings.value('toParameter')
        xtraParameter = settings.value('xtraParameter')

        Standard_Conversion = settings.value('Standard_Conversion', False)
        Batch_Conversion = settings.value('Batch_Conversion', False)
        From_Markdown = settings.value('From_Markdown', False)
        From_Html = settings.value('From_Html', False)
        From_Latex = settings.value('From_Latex', False)
        From_Opml = settings.value('From_Opml', False)

        To_Markdown = settings.value('To_Markdown', False)
        To_Html = settings.value('To_Html', False)
        To_Latex = settings.value('To_Latex', False)
        To_Opml = settings.value('To_Opml', False)
        To_Lyx = settings.value('To_Lyx', False)


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
    import sys
    global actualLanguage


    settings = QSettings('Pandoc', 'PanConvert')
    actualLanguage = settings.value('default_language')

    app = QtWidgets.QApplication(sys.argv)

    _translate = QtCore.QTranslator()
    if actualLanguage == 'Deutsch':
        _translate.load("source/language/Panconvert_de.qm") # ,"source/language/Panconvert_es.qm")
    elif actualLanguage == 'Español': # English
        _translate.load("source/language/Panconvert_es.qm")






    app.installTranslator(_translate)
    myapp = StartQT5()
    myapp.show()
    sys.exit(app.exec_())
