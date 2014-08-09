__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_

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
        #TODO: Relative Path for preference.txt
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