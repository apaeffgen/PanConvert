# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_prefpane.ui'
#
# Created: Fri Aug  8 08:07:50 2014
#      by: PyQt5 UI code generator 5.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogPreferences(object):
    def setupUi(self, DialogPreferences):
        DialogPreferences.setObjectName("DialogPreferences")
        DialogPreferences.resize(400, 103)
        DialogPreferences.setMinimumSize(QtCore.QSize(400, 100))
        self.label_Pandoc_Path = QtWidgets.QLabel(DialogPreferences)
        self.label_Pandoc_Path.setGeometry(QtCore.QRect(60, 12, 137, 16))
        self.label_Pandoc_Path.setObjectName("label_Pandoc_Path")
        self.Pandoc_Path = QtWidgets.QLineEdit(DialogPreferences)
        self.Pandoc_Path.setGeometry(QtCore.QRect(205, 12, 142, 21))
        self.Pandoc_Path.setText("")
        self.Pandoc_Path.setObjectName("Pandoc_Path")
        self.ButtonSave = QtWidgets.QPushButton(DialogPreferences)
        self.ButtonSave.setGeometry(QtCore.QRect(280, 51, 71, 31))
        self.ButtonSave.setObjectName("ButtonSave")
        self.ButtonCancel = QtWidgets.QPushButton(DialogPreferences)
        self.ButtonCancel.setGeometry(QtCore.QRect(210, 50, 71, 31))
        self.ButtonCancel.setObjectName("ButtonCancel")

        self.retranslateUi(DialogPreferences)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)

    def retranslateUi(self, DialogPreferences):
        _translate = QtCore.QCoreApplication.translate
        DialogPreferences.setWindowTitle(_translate("DialogPreferences", "Preferences"))
        self.label_Pandoc_Path.setText(_translate("DialogPreferences", "Path to Pandoc Binary"))
        self.ButtonSave.setText(_translate("DialogPreferences", "Save"))
        self.ButtonCancel.setText(_translate("DialogPreferences", "Cancel"))

