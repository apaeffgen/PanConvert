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
from source.gui.panconvert_diag_prefpane import Ui_DialogPreferences
import os


class PreferenceDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogPreferences()
        self.ui.setupUi(self)
        self.ui.ButtonSave.clicked.connect(self.input_path)
        self.ui.ButtonCancel.clicked.connect(self.cancel_dialog)

    def cancel_dialog(self):
        PreferenceDialog.close(self)

    def input_path(self):
        systempath = os.getcwd()
        d = open(systempath + "/source/preferences.txt", "w")
        outputpath = self.ui.Pandoc_Path.text()

        d.writelines(outputpath)
        d.close()

        PreferenceDialog.close(self)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = PreferenceDialog()
    myapp.show()
    myapp.exec_()