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
from source.gui.panconvert_diag_prefpane import Ui_DialogPreferences
from distutils.util import strtobool
import platform

global path_pandoc


class PreferenceDialog(QtWidgets.QDialog):

    global path_pandoc

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)
        self.ui.ButtonSave.clicked.connect(self.settings)
        self.ui.ButtonCancel.clicked.connect(self.cancel_dialog)
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc')
        self.ui.Pandoc_Path.insert(path_pandoc)
        path_multimarkdown = settings.value('path_multimarkdown')
        self.ui.Markdown_Path.insert(path_multimarkdown)

        From_Markdown = settings.value('From_Markdown', False)
        From_Html = settings.value('From_Html', False)
        From_Latex = settings.value('From_Latex', False)
        From_Opml = settings.value('From_Opml', False)

        To_Markdown = settings.value('To_Markdown', False)
        To_Html = settings.value('To_Html', False)
        To_Latex = settings.value('To_Latex', False)
        To_Opml = settings.value('To_Opml', False)
        To_Lyx = settings.value('To_Lyx', False)


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







    def cancel_dialog(self):
        PreferenceDialog.close(self)

    def settings(self):


        settings = QSettings('Pandoc', 'PanConvert')
        settings.setValue('path_pandoc', self.ui.Pandoc_Path.text())
        settings.setValue('path_multimarkdown', self.ui.Markdown_Path.text())

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



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = PreferenceDialog()
    myapp.show()
    myapp.exec_()