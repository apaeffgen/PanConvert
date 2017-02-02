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
from PyQt5.QtCore import QPoint, QSize
from source.gui.panconvert_diag_prefpane_ext import Ui_DialogPreferences
from distutils.util import strtobool
import platform, os

global path_pandoc, path_dialog, actualLanguage





class PreferenceDialog(QtWidgets.QDialog):

    global path_pandoc, path_dialog

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)
        self.ui.ButtonSave.clicked.connect(self.settings)
        self.ui.ButtonSave_2.clicked.connect(self.settings)
        self.ui.ButtonCancel.clicked.connect(self.cancel_dialog)
        self.ui.ButtonCancel_2.clicked.connect(self.cancel_dialog)
        self.ui.ButtonPandocPath.clicked.connect(self.DirectoryPandoc)
        self.ui.ButtonMarkdownPath.clicked.connect(self.DirectoryMarkdown)
        self.ui.ButtonOpenSavePath.clicked.connect(self.DirectoryOpenSave)



        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')

        #Language Settings
        default_language = settings.value('default_language')
        self.ui.comboBoxLanguageSelector.addItem('')
        self.ui.comboBoxLanguageSelector.addItem('English')
        self.ui.comboBoxLanguageSelector.addItem('Deutsch')
        self.ui.comboBoxLanguageSelector.addItem('Español')
        self.ui.comboBoxLanguageSelector.currentIndexChanged.connect(self.SetLanguage)

        #Checkbox Size of Main Window and DockWindow
        Window_Size = settings.value('Window_Size', True)
        Dock_Size = settings.value('Dock_Size', True)
        Dialog_Size = settings.value('Dialog_Size', True)

        #Checkbox Gui Old / New
        Button_OldGui = settings.value('Button_OldGui', False)
        Button_NewGui = settings.value('Button_NewGui', True)

        #Standard Tab of the New Gui
        Tab_StandardConverter = settings.value('Tab_StandardConverter', True)
        Tab_ManualConverter = settings.value('Tab_ManualConverter', False)
        Tab_BatchConverter = settings.value('Tab_BatchConverter', False)


        #Size of Dialog Windows
        self.resize(settings.value("Preference_size", QSize(270, 225)))
        self.move(settings.value("Preference_pos", QPoint(50, 50)))


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
            if platform.system() == 'Darwin':
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
                self.ui.Window_Size.setChecked(Window_Size)
                self.ui.Dock_Size.setChecked(Dock_Size)
                self.ui.Dialog_Size.setChecked(Dialog_Size)
                self.ui.Button_OldGui.setChecked(Button_OldGui)
                self.ui.Button_NewGui.setChecked(Button_NewGui)
                self.ui.Tab_StandardConverter.setChecked(Tab_StandardConverter)
                self.ui.Tab_ManualConverter.setChecked(Tab_ManualConverter)
                self.ui.Tab_BatchConverter.setChecked(Tab_BatchConverter)

            else:
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
                self.ui.Window_Size.setChecked(strtobool(Window_Size))
                self.ui.Dock_Size.setChecked(strtobool(Dock_Size))
                self.ui.Dialog_Size.setChecked(strtobool(Dialog_Size))
                self.ui.Button_OldGui.setChecked(strtobool(Button_OldGui))
                self.ui.Button_NewGui.setChecked(strtobool(Button_NewGui))
                self.ui.Tab_StandardConverter.setChecked(strtobool(Tab_StandardConverter))
                self.ui.Tab_ManualConverter.setChecked(strtobool(Tab_ManualConverter))
                self.ui.Tab_BatchConverter.setChecked(strtobool(Tab_BatchConverter))





    def cancel_dialog(self):
        PreferenceDialog.close(self)

    def settings(self):

        settings = QSettings('Pandoc', 'PanConvert')

        settings.setValue('Window_Size', self.ui.Window_Size.isChecked())
        settings.setValue('Dock_Size', self.ui.Dock_Size.isChecked())
        settings.setValue('Dialog_Size', self.ui.Dialog_Size.isChecked())

        settings.setValue('Button_OldGui', self.ui.Button_OldGui.isChecked())
        settings.setValue('Button_NewGui', self.ui.Button_NewGui.isChecked())
        settings.setValue('Tab_StandardConverter', self.ui.Tab_StandardConverter.isChecked())
        settings.setValue('Tab_ManualConverter', self.ui.Tab_ManualConverter.isChecked())
        settings.setValue('Tab_BatchConverter', self.ui.Tab_BatchConverter.isChecked())

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

        Dialog_Size = settings.value('Dialog_Size')
        if Dialog_Size is True or Dialog_Size == 'true':
            settings.setValue("Preference_size", self.size())
            settings.setValue("Preference_pos", self.pos())





        settings.sync()
        settings.status()






        PreferenceDialog.close(self)

    def DirectoryPandoc(self):
        self.ui.Pandoc_Path.clear()
        fd = QtWidgets.QFileDialog(self)
        fd.setDirectory(QtCore.QDir.homePath())
        PandocDirectory = fd.getExistingDirectory()
        self.ui.Pandoc_Path.insert(PandocDirectory)

    def DirectoryMarkdown(self):
        self.ui.Markdown_Path.clear()
        fd = QtWidgets.QFileDialog(self)
        fd.setDirectory(QtCore.QDir.homePath())
        MarkdownDirectory = fd.getExistingDirectory()
        self.ui.Markdown_Path.insert(MarkdownDirectory)

    def DirectoryOpenSave(self):
        self.ui.Dialog_Path.clear()
        fd = QtWidgets.QFileDialog(self)
        fd.setDirectory(QtCore.QDir.homePath())
        OpenSaveDirectory = fd.getExistingDirectory()
        self.ui.Dialog_Path.insert(OpenSaveDirectory)

    def SetLanguage(self):
        global actualLanguage
        settings = QSettings('Pandoc', 'PanConvert')
        settings.setValue('default_language', str(self.ui.comboBoxLanguageSelector.currentText()))
        actualLanguage = str(self.ui.comboBoxLanguageSelector.currentText())
        settings.sync()
        settings.status()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = PreferenceDialog()
    myapp.show()
    myapp.exec_()