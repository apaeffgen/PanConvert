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
import os

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
        path_multimarkdown = settings.value('path_multimarkdown')
        self.ui.Pandoc_Path.insert(path_pandoc)
        self.ui.Markdown_Path.insert(path_multimarkdown)



    def cancel_dialog(self):
        PreferenceDialog.close(self)

    def settings(self):


        settings = QSettings('Pandoc', 'PanConvert')
        settings.setValue('path_pandoc', self.ui.Pandoc_Path.text())
        settings.setValue('path_multimarkdown', self.ui.Markdown_Path.text())
        settings.sync()
        settings.status()

        PreferenceDialog.close(self)



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = PreferenceDialog()
    myapp.show()
    myapp.exec_()