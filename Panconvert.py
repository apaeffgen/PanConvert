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
import platform
import glob
import os

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from source.dialog_preferences import *
from source.dialog_batch import *
from source.dialog_info import *
from source.converter.markdown import *
from source.converter.latex import *
from source.converter.opml import *
from source.converter.html import *
from source.converter.epub import *
from source.converter.lyx import *
from source.converter.manual_converter import *
from source.converter.batch_converter import *
from source.gui.panconvert_gui import Ui_notepad

global openfile, filelist

#TODO: Copy/Paste. In Ui + Function
#TODO: Batch-Conversion. In Ui + Function
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
                    text = 'No Preview of the File-Data possible. Try to manually convert. Good Luck.'
                    data = self.ui.editor_window.setPlainText(text)
                    #QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                    #                          'No Preview of the File-Data possible. Try to manually convert. Good Luck.')

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
        from os.path import isfile
        text = ''
        self.ui.editor_window.setPlainText(text)
        text = self.ui.editor_window(text)
        self.ui.actionSave.setEnabled(True)
        # if isfile(self.filename[0]):
            # self.ui.actionSave.setEnabled(False)

    def buffer_save(self):
        global text, text_undo
        text_undo = text
        text = self.ui.editor_window.toPlainText()

    def undo(self):
        global text,text_undo
        text = text_undo
        self.ui.editor_window.setPlainText(text_undo)

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

    '''Export Functions'''


    def file_export_html2markdown(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_html2markdown(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_markdown2html(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_md2html(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_md2latex(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_md2latex(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_opml2html(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_opml2html(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_opml2latex(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_opml2latex(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_opml2markdown_pandoc(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_opml2markdown(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_html2opml(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_html2opml(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_markdown2opml(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_markdown2opml(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_html2latex(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_html2latex(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_latex2html(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_latex2html(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_latex2opml(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_latex2opml(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_latex2markdown(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_latex2markdown(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_markdown2lyx(self):
        global text, text_undo
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text is not "":
            output_content = convert_markdown2lyx(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')



    def file_export_markdown2epub(self):
        global text
        text = self.ui.editor_window.toPlainText()
        if text is not "":
            output_content = convert_md2epub(text)
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')

    def file_export_manualconverter(self):

        global text, text_undo, openfile
        text = self.ui.editor_window.toPlainText()
        text_undo = text
        if text == '':
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'You have no Data to be converted. Please make an input')
        elif text != 'No Preview of the File-Data possible. Try to manually convert. Good Luck.':
            output_content = convert_universal(text,toFormat,fromFormat,extraParameter)

            if output_content is not '':
                self.ui.editor_window.setPlainText(output_content)
            else:
                QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'There should be a file written to the folder where Panconvert'
                                          ' is stored. Please check at this location. <br><br> If not, somthing'
                                          ' went terribly wrong. Sorry for the inconvenience')



        elif text == 'No Preview of the File-Data possible. Try to manually convert. Good Luck.':
            output_content = convert_binary(openfile,toFormat,fromFormat,extraParameter)
            #self.ui.editor_window.setPlainText("I tried my best to convert. Check if there had been any Output, and if"
            #                                   " so, please check the quality of the created output.")
            self.ui.editor_window.setPlainText(output_content)
            text = output_content
        else:
            QtWidgets.QMessageBox.warning(None, 'Error-Message',
                                          'Something went terribly wrong. Please get some help. Google never was your'
                                          '/ is your friend. Just the NSA is.')

    def file_export_batch_conversion_standard(self):
        # global openfile
        # output_content = batch_convert(openfile,toFormat,fromFormat)
        # self.ui.editor_window.setPlainText(output_content)
        QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'The batch conversion at the moment only works with the manual conversion.<br><br>'
                                          ' Please uncheck the checkbox "Standard Conversion".')


    def file_export_batch_conversion_manual(self):
        global openfile, filelist

        batch_settings = QSettings('Pandoc', 'PanConvert')
        if platform.system() == 'Windows' or platform.system() == 'Linux':
            batch_convert_files = bool(strtobool(batch_settings.value('batch_convert_files')))
            batch_convert_directory = bool(strtobool(batch_settings.value('batch_convert_directory')))
            batch_convert_recursive = bool(strtobool(batch_settings.value('batch_convert_recursive')))
        else:
            batch_convert_files = batch_settings.value('batch_convert_files')
            batch_convert_directory = batch_settings.value('batch_convert_directory')
            batch_convert_recursive = batch_settings.value('batch_convert_recursive')
        data = self.ui.editor_window.toPlainText()



        if data is not '' and batch_convert_files is True:

            for openfiles in filelist:
                if os.path.isfile(openfiles) is True:
                    self.ui.editor_window.setPlainText(data)
                    message = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                    self.ui.editor_window.appendPlainText(message)
                else:
                    errormessage = ('Einige Dateiangaben waren nicht korrekt:')
                    self.ui.editor_window.appendPlainText(errormessage)

        elif batch_convert_recursive is False and batch_convert_directory is True:
            batch_open_path = batch_settings.value('batch_open_path')

            filelist = glob.glob(batch_open_path + '/*')
            for openfiles in filelist:
                if os.path.isfile(openfiles):
                    output_content = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                    self.ui.editor_window.setPlainText(output_content)

        elif batch_convert_recursive is True and batch_convert_directory is True:
            batch_open_path = batch_settings.value('batch_open_path')

            filelistrecursive = create_filelist(batch_open_path)

            for openfiles in filelistrecursive:
                output_content = batch_convert_manual(openfiles,fromFormat,toFormat,extraParameter)
                self.ui.editor_window.setPlainText(output_content)

        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                              'You have to open at least one file in file conversion mode.'
                                              ' <br>Did you put in from / to - formats?'
                                              ' <br>If you are in directory mode, did you specify a directory?'
                                              ' <br> Check your settings.')


    """Gui-Event Definitions"""

    def __init__(self, parent=None):
        global path_dialog, text, text_undo, openfile

        text = ''
        text_undo = ''

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_notepad()
        self.ui.setupUi(self)
        self.ui.actionOpen.triggered.connect(self.file_dialog)
        self.ui.actionSave.triggered.connect(self.buffer_save)
        self.ui.actionSave_AS.triggered.connect(self.file_save_as)
        self.ui.actionNew.triggered.connect(self.file_new)
        self.ui.actionUndo.triggered.connect(self.undo)
        self.ui.ButtonFromFormat.clicked.connect(self.list_from_formats)
        self.ui.ButtonToFormat.clicked.connect(self.list_to_formats)
        self.ui.ButtonOptions.clicked.connect(self.info_dialog)
        self.ui.actionMarkdown2Latex.triggered.connect(self.file_export_md2latex)
        self.ui.actionOpml2latex.triggered.connect(self.file_export_opml2latex)
        self.ui.actionLatex2Opml.triggered.connect(self.file_export_latex2opml)
        self.ui.actionLatex2Markdown.triggered.connect(self.file_export_latex2markdown)
        self.ui.actionOpml2Markdown.triggered.connect(self.file_export_opml2markdown_pandoc)
        self.ui.actionMarkdown2opml.triggered.connect(self.file_export_markdown2opml)
        self.ui.actionHtml2Markdown.triggered.connect(self.file_export_html2markdown)
        self.ui.actionMarkdown2html.triggered.connect(self.file_export_md2latex)
        self.ui.actionOpml2html.triggered.connect(self.file_export_opml2html)
        self.ui.actionHtml2opml.triggered.connect(self.file_export_html2opml)
        self.ui.actionHtml2Latex.triggered.connect(self.file_export_html2latex)
        self.ui.actionLatex2html.triggered.connect(self.file_export_latex2html)
        self.ui.actionMarkdown2Lyx.triggered.connect(self.file_export_markdown2lyx)
        self.ui.ButtonBatch.clicked.connect(self.batch_dialog)
        self.ui.ButtonRevert.clicked.connect(self.undo)
        self.ui.ButtonConvert.clicked.connect(self.event_triggered)
        self.ui.actionPreferences.triggered.connect(self.preference_dialog)
        self.ui.actionHelp.triggered.connect(self.help_dialog)
        self.ui.actionPandoc_Docs.triggered.connect(self.pandocdocs_dialog)
        self.ui.actionSave.setEnabled(True)


        settings = QSettings('Pandoc', 'PanConvert')

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
            if platform.system() == 'Windows' or platform.system() == 'Linux':
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

            else:
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



    """External Dialog Windows - Trigger Functions"""

    def help_dialog(self):
        import webbrowser
        webbrowser.open_new_tab('http://panconvert.sourceforge.net/help')

    def pandocdocs_dialog(self):
        import webbrowser
        webbrowser.open_new_tab('http://pandoc.org/README.html')

    def preference_dialog(self):
        """ References to dialog_preferences.py"""
        self.PreferenceDialog = PreferenceDialog(self)
        self.PreferenceDialog.show()

    def batch_dialog(self):
        """ References to dialog_batch.py"""
        self.BatchDialog = BatchDialog(self)
        self.BatchDialog.show()

    def info_dialog(self):
        """ References to dialog_batch.py"""
        self.InfoDialog = InfoDialog(self)
        self.InfoDialog.show()



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
                self.file_export_md2latex()
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.file_export_markdown2opml()
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToLyx.isChecked() is True:
                self.file_export_markdown2lyx()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.file_export_opml2markdown_pandoc()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.file_export_opml2latex()
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.file_export_latex2markdown()
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToOpml.isChecked()is True:
                self.file_export_latex2opml()
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToMarkdown.isChecked() is True:
                self.file_export_html2markdown()
            elif self.ui.ButtonFromMarkdown.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.file_export_markdown2html()
            elif self.ui.ButtonFromOpml.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.file_export_opml2html()
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToOpml.isChecked() is True:
                self.file_export_html2opml()
            elif self.ui.ButtonFromLatex.isChecked() is True and self.ui.ButtonToHtml.isChecked() is True:
                self.file_export_latex2html()
            elif self.ui.ButtonFromHtml.isChecked() is True and self.ui.ButtonToLatex.isChecked() is True:
                self.file_export_html2latex()
            else:
                QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                              'The from-Format and to-Format should not be identical.<br><br> '
                                              'If you picked to-Lyx, only from-markdown is a valid option.<br><br>'
                                              'Please make a different choice.')

        elif standard_conversion is False and batchConversion is False:# and extraParameter is not "":
            self.file_export_manualconverter()

        elif standard_conversion is True and batchConversion is True:
            self.file_export_batch_conversion_standard()


        elif standard_conversion is False and batchConversion is True:
            self.file_export_batch_conversion_manual()

        elif fromFormat is "" or toFormat is "":
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                          'If you fill in Arguments and uncheck the Box "Standard", you have to '
                                          'provide at least the following Parameters: From, To. <br><br>'
                                          '  Some Formats like odt, epub need an input '
                                          'for "Parameter". Otherwise there will be no output at all')


        else:
            QtWidgets.QMessageBox.warning(None, 'Warning-Message',
                                              'Either is this feature not implemented at the moment,'
                                              ' or you have forgotten the extra Parameter for odt, epub Format. '
                                              ' Please consult the help - System for more Information')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = StartQT5()
    myapp.show()
    sys.exit(app.exec_())
