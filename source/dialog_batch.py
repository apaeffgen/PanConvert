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
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from source.gui.panconvert_dialog_batch import Ui_DialogBatch
from distutils.util import strtobool
import platform

global openfiles, batch_open_path

class BatchDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        global batch_open_path, openfile

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogBatch()
        self.ui.setupUi(self)
        self.ui.ButtonSave.clicked.connect(self.batch_settings)
        self.ui.ButtonCancel.clicked.connect(self.cancel_dialog)
        self.ui.Button_Open_Path.clicked.connect(self.directory_dialog)

        #Initialize Settings
        batch_settings = QSettings('Pandoc', 'PanConvert')

        # Path Settings
        batch_open_path = batch_settings.value('batch_open_path')
        self.ui.OpenPath.insert(batch_open_path)


        #Parameter Settings
        parameterBatchconvertDirectory = batch_settings.value('batch_convert_directory',True)
        parameterBatchconvertFiles = batch_settings.value('batch_convert_files', False)
        parameterBatchconvertRecursive = batch_settings.value('batch_convert_recursive', True)

        if platform.system() == 'Windows' or platform.system() == 'Linux':
            self.ui.ParameterBatchconvertDirectory.setChecked(strtobool(parameterBatchconvertDirectory))
            self.ui.ParameterBatchconvertFiles.setChecked(strtobool(parameterBatchconvertFiles))
            self.ui.ParameterBatchconvertRecursive.setChecked(strtobool(parameterBatchconvertRecursive))

        else:
            self.ui.ParameterBatchconvertDirectory.setChecked(parameterBatchconvertDirectory)
            self.ui.ParameterBatchconvertFiles.setChecked(parameterBatchconvertFiles)
            self.ui.ParameterBatchconvertRecursive.setChecked(parameterBatchconvertRecursive)




    def cancel_dialog(self):
        BatchDialog.close(self)

    def batch_settings(self):
        global batch_open_path, openfiles

        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_settings.setValue('batch_convert_directory', self.ui.ParameterBatchconvertDirectory.isChecked())
        batch_settings.setValue('batch_convert_files', self.ui.ParameterBatchconvertFiles.isChecked())
        batch_settings.setValue('batch_convert_recursive', self.ui.ParameterBatchconvertRecursive.isChecked())
        batch_settings.setValue('batch_open_path', self.ui.OpenPath.text())
        batch_settings.sync()
        batch_settings.status()

        BatchDialog.close(self)

    def directory_dialog(self):

        global data, openfiles, batch_open_path


        fd = QtWidgets.QFileDialog(self)

        if batch_open_path == '':
            fd.setDirectory(QtCore.QDir.homePath())
        else:
            fd.setDirectory(batch_open_path)

        batch_directory = fd.getExistingDirectory()
        self.ui.OpenPath.insert(batch_directory)






if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = BatchDialog()
    myapp.show()
    myapp.exec_()