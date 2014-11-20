# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_prefpane.ui'
#
# Created: Sat Nov 15 16:27:28 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogPreferences(object):
    def setupUi(self, DialogPreferences):
        DialogPreferences.setObjectName("DialogPreferences")
        DialogPreferences.resize(510, 113)
        DialogPreferences.setMinimumSize(QtCore.QSize(400, 100))
        self.label_Pandoc_Path = QtWidgets.QLabel(DialogPreferences)
        self.label_Pandoc_Path.setGeometry(QtCore.QRect(50, 20, 157, 16))
        self.label_Pandoc_Path.setObjectName("label_Pandoc_Path")
        self.Pandoc_Path = QtWidgets.QLineEdit(DialogPreferences)
        self.Pandoc_Path.setGeometry(QtCore.QRect(214, 20, 221, 17))
        self.Pandoc_Path.setText("")
        self.Pandoc_Path.setObjectName("Pandoc_Path")
        self.ButtonSave = QtWidgets.QPushButton(DialogPreferences)
        self.ButtonSave.setGeometry(QtCore.QRect(270, 70, 71, 31))
        self.ButtonSave.setObjectName("ButtonSave")
        self.ButtonCancel = QtWidgets.QPushButton(DialogPreferences)
        self.ButtonCancel.setGeometry(QtCore.QRect(200, 70, 71, 31))
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.Markdown_Path = QtWidgets.QLineEdit(DialogPreferences)
        self.Markdown_Path.setGeometry(QtCore.QRect(214, 44, 221, 17))
        self.Markdown_Path.setText("")
        self.Markdown_Path.setObjectName("Markdown_Path")
        self.label_Markdown_Path = QtWidgets.QLabel(DialogPreferences)
        self.label_Markdown_Path.setGeometry(QtCore.QRect(50, 39, 157, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Markdown_Path.sizePolicy().hasHeightForWidth())
        self.label_Markdown_Path.setSizePolicy(sizePolicy)
        self.label_Markdown_Path.setObjectName("label_Markdown_Path")

        self.retranslateUi(DialogPreferences)
        QtCore.QMetaObject.connectSlotsByName(DialogPreferences)

    def retranslateUi(self, DialogPreferences):
        _translate = QtCore.QCoreApplication.translate
        DialogPreferences.setWindowTitle(_translate("DialogPreferences", "Preferences"))
        self.label_Pandoc_Path.setText(_translate("DialogPreferences", "Path to Pandoc Binary"))
        self.Pandoc_Path.setPlaceholderText(_translate("DialogPreferences", "/usr/local/bin/pandoc"))
        self.ButtonSave.setText(_translate("DialogPreferences", "Save"))
        self.ButtonCancel.setText(_translate("DialogPreferences", "Cancel"))
        self.Markdown_Path.setPlaceholderText(_translate("DialogPreferences", "/usr/local/bin/multimarkdown"))
        self.label_Markdown_Path.setText(_translate("DialogPreferences", "Path to Markdown Binary"))

