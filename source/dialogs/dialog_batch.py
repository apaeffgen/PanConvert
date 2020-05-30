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
from PyQt5.QtCore import QPoint, QSize
from source.gui.panconvert_dialog_batch import Ui_DialogBatch
from distutils.util import strtobool as str2bool
import platform

global openfiles, batch_open_path

def strtobool(input):
    """
        safe strtobool : if input is a boolean
        it return the input
    """
    if isinstance(input,bool):
        return input
    try:
        return str2bool(input)
    except:
        print("Dear, we are in trouble ! ;)")

class BatchDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        global batch_open_path, openfile, batch_open_path_output

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogBatch()
        self.ui.setupUi(self)
        self.ui.ButtonSave.clicked.connect(self.batch_settings)
        self.ui.ButtonCancel.clicked.connect(self.closeEvent)
        self.ui.Button_Open_Path.clicked.connect(self.directory_dialog)
        self.ui.Button_Open_Path_Output.clicked.connect(self.directory_dialog_Output)


        #Initialize Settings
        batch_settings = QSettings('Pandoc', 'PanConvert')
        settings = QSettings('Pandoc', 'PanConvert')

        self.resize(settings.value("Batch_size", QSize(270, 225)))
        self.move(settings.value("Batch_pos", QPoint(50, 50)))

        # Path Settings
        batch_open_path = batch_settings.value('batch_open_path')
        self.ui.OpenPath.insert(batch_open_path)
        batch_open_path_output = batch_settings.value('batch_open_path_output')
        self.ui.OpenPath_Output.insert(batch_open_path_output)

        # Filter Settings
        batch_convert_filter = batch_settings.value('batch_convert_filter')
        self.ui.Filter.insert(batch_convert_filter)


        #Parameter Settings

        parameterBatchconvertDirectory = batch_settings.value('batch_convert_directory', True)
        parameterBatchconvertFiles = batch_settings.value('batch_convert_files', False)
        parameterBatchconvertRecursive = batch_settings.value('batch_convert_recursive', True)



        if batch_settings.value('batch_convert_directory') is not None:
            if platform.system() == 'Darwin':
                self.ui.ParameterBatchconvertDirectory.setChecked(parameterBatchconvertDirectory)
                self.ui.ParameterBatchconvertFiles.setChecked(parameterBatchconvertFiles)
                self.ui.ParameterBatchconvertRecursive.setChecked(parameterBatchconvertRecursive)
            else:
                self.ui.ParameterBatchconvertDirectory.setChecked(strtobool(parameterBatchconvertDirectory))
                self.ui.ParameterBatchconvertFiles.setChecked(strtobool(parameterBatchconvertFiles))
                self.ui.ParameterBatchconvertRecursive.setChecked(strtobool(parameterBatchconvertRecursive))







    def closeEvent(self, event):

        settings = QSettings('Pandoc', 'PanConvert')
        Dialog_Size = settings.value('Dialog_Size')
        if Dialog_Size is True or Dialog_Size == 'true':
            settings.setValue("Batch_size", self.size())
            settings.setValue("Batch_pos", self.pos())


        settings.sync()
        settings.status()
        BatchDialog.close(self)

    def batch_settings(self):
        global batch_open_path, openfiles, batch_open_path_output

        batch_settings = QSettings('Pandoc', 'PanConvert')
        batch_settings.setValue('batch_convert_directory', self.ui.ParameterBatchconvertDirectory.isChecked())
        batch_settings.setValue('batch_convert_files', self.ui.ParameterBatchconvertFiles.isChecked())
        batch_settings.setValue('batch_convert_recursive', self.ui.ParameterBatchconvertRecursive.isChecked())
        batch_settings.setValue('batch_open_path', self.ui.OpenPath.text())
        batch_settings.setValue('batch_open_path_output', self.ui.OpenPath_Output.text())
        batch_settings.setValue('batch_convert_filter', self.ui.Filter.text())
        batch_settings.sync()
        batch_settings.status()

        BatchDialog.close(self)

    def directory_dialog(self):

        global data, openfiles, batch_open_path
        self.ui.OpenPath.clear()

        fd = QtWidgets.QFileDialog(self)

        if batch_open_path == '':
            fd.setDirectory(QtCore.QDir.homePath())
        else:
            fd.setDirectory(batch_open_path)

        batch_directory = fd.getExistingDirectory()
        self.ui.OpenPath.insert(batch_directory)

    def directory_dialog_Output(self):

        global data, openfiles, batch_open_path_output
        self.ui.OpenPath_Output.clear()

        fd = QtWidgets.QFileDialog(self)

        if batch_open_path_output == '':
            fd.setDirectory(QtCore.QDir.homePath())
        else:
            fd.setDirectory(batch_open_path_output)

        batch_directory = fd.getExistingDirectory()
        self.ui.OpenPath_Output.insert(batch_directory)






if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myapp = BatchDialog()
    myapp.show()
    myapp.exec_()