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
from PyQt5.QtCore import QSettings
from PyQt5 import QtCore
from source.gui.panconvert_diag_prefpane import Ui_DialogPreferences
from distutils.util import strtobool
import platform

global path_pandoc, path_dialog


class PreferenceDialog(QtWidgets.QDialog):

    global path_pandoc, path_dialog

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)
        self.ui.ButtonSave.clicked.connect(self.settings)
        self.ui.ButtonCancel.clicked.connect(self.cancel_dialog)
        self.ui.ButtonPandocPath.clicked.connect(self.DirectoryPandoc)
        self.ui.ButtonMarkdownPath.clicked.connect(self.DirectoryMarkdown)
        self.ui.ButtonOpenSavePath.clicked.connect(self.DirectoryOpenSave)

        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')

        #Paths and Parameters
        path_pandoc = settings.value('path_pandoc')
        self.ui.Pandoc_Path.insert(path_pandoc)
        path_multimarkdown = settings.value('path_multimarkdown')
        self.ui.Markdown_Path.insert(path_multimarkdown)
        path_dialog = settings.value('path_dialog')
        self.ui.Dialog_Path.insert(path_dialog)

        fromParameter = settings.value('fromParameter')
        self.ui.FromParameter.insert(fromParameter)
        toParameter = settings.value('toParameter')
        self.ui.ToParameter.insert(toParameter)
        xtraParameter = settings.value('xtraParameter')
        self.ui.XtraParameter.insert(xtraParameter)


        #Checkboxes
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
                self.ui.ButtonFromMarkdown.setChecked(strtobool(From_Markdown))
                self.ui.ButtonFromHtml.setChecked(strtobool(From_Html))
                self.ui.ButtonFromLatex.setChecked(strtobool(From_Latex))
                self.ui.ButtonFromOpml.setChecked(strtobool(From_Opml))
                self.ui.ButtonToMarkdown.setChecked(strtobool(To_Markdown))
                self.ui.ButtonToHtml.setChecked(strtobool(To_Html))
                self.ui.ButtonToLatex.setChecked(strtobool(To_Latex))
                self.ui.ButtonToOpml.setChecked(strtobool(To_Opml))
                self.ui.ButtonToLyx.setChecked(strtobool(To_Lyx))
                self.ui.StandardConversion.setChecked(strtobool(Standard_Conversion))
                self.ui.BatchConversion.setChecked(strtobool(Batch_Conversion))

            else:
                self.ui.ButtonFromMarkdown.setChecked(From_Markdown)
                self.ui.ButtonFromHtml.setChecked(From_Html)
                self.ui.ButtonFromLatex.setChecked(From_Latex)
                self.ui.ButtonFromOpml.setChecked(From_Opml)
                self.ui.ButtonToMarkdown.setChecked(To_Markdown)
                self.ui.ButtonToHtml.setChecked(To_Html)
                self.ui.ButtonToLatex.setChecked(To_Latex)
                self.ui.ButtonToOpml.setChecked(To_Opml)
                self.ui.ButtonToLyx.setChecked(To_Lyx)
                self.ui.StandardConversion.setChecked(Standard_Conversion)
                self.ui.BatchConversion.setChecked(Batch_Conversion)


    def cancel_dialog(self):
        PreferenceDialog.close(self)

    def settings(self):

        settings = QSettings('Pandoc', 'PanConvert')
        settings.setValue('path_pandoc', self.ui.Pandoc_Path.text())
        settings.setValue('path_multimarkdown', self.ui.Markdown_Path.text())
        settings.setValue('path_dialog', self.ui.Dialog_Path.text())


        settings.setValue('fromParameter', self.ui.FromParameter.text())
        settings.setValue('toParameter', self.ui.ToParameter.text())
        settings.setValue('xtraParameter', self.ui.XtraParameter.text())

        settings.setValue('Standard_Conversion', self.ui.StandardConversion.isChecked())
        settings.setValue('Batch_Conversion', self.ui.BatchConversion.isChecked())

        settings.setValue('From_Markdown', self.ui.ButtonFromMarkdown.isChecked())
        settings.setValue('From_Html', self.ui.ButtonFromHtml.isChecked())
        settings.setValue('From_Latex', self.ui.ButtonFromLatex.isChecked())
        settings.setValue('From_Opml', self.ui.ButtonFromOpml.isChecked())

        settings.setValue('To_Markdown', self.ui.ButtonToMarkdown.isChecked())
        settings.setValue('To_Html', self.ui.ButtonToHtml.isChecked())
        settings.setValue('To_Latex', self.ui.ButtonToLatex.isChecked())
        settings.setValue('To_Opml', self.ui.ButtonToOpml.isChecked())
        settings.setValue('To_Lyx', self.ui.ButtonToLyx.isChecked())

        settings.sync()
        settings.status()


        PreferenceDialog.close(self)

    def DirectoryPandoc(self):
        fd = QtWidgets.QFileDialog(self)
        fd.setDirectory(QtCore.QDir.homePath())
        PandocDirectory = fd.getExistingDirectory()
        self.ui.Pandoc_Path.insert(PandocDirectory)

    def DirectoryMarkdown(self):
        fd = QtWidgets.QFileDialog(self)
        fd.setDirectory(QtCore.QDir.homePath())
        MarkdownDirectory = fd.getExistingDirectory()
        self.ui.Markdown_Path.insert(MarkdownDirectory)

    def DirectoryOpenSave(self):
        fd = QtWidgets.QFileDialog(self)
        fd.setDirectory(QtCore.QDir.homePath())
        OpenSaveDirectory = fd.getExistingDirectory()
        self.ui.Dialog_Path.insert(OpenSaveDirectory)




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = PreferenceDialog()
    myapp.show()
    myapp.exec_()