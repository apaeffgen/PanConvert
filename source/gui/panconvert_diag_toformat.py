# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_toformat.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_To_Format_Dialog(object):
    def setupUi(self, To_Format_Dialog):
        To_Format_Dialog.setObjectName("To_Format_Dialog")
        To_Format_Dialog.resize(224, 234)
        self.gridLayout = QtWidgets.QGridLayout(To_Format_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ButtonCancel = QtWidgets.QPushButton(To_Format_Dialog)
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.verticalLayout.addWidget(self.ButtonCancel)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.textBrowser = QtWebEngineWidgets.QWebEngineView(To_Format_Dialog)
        self.textBrowser.setMinimumSize(QtCore.QSize(200, 100))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(To_Format_Dialog)
        QtCore.QMetaObject.connectSlotsByName(To_Format_Dialog)

    def retranslateUi(self, To_Format_Dialog):
        _translate = QtCore.QCoreApplication.translate
        To_Format_Dialog.setWindowTitle(_translate("To_Format_Dialog", "Pandoc To Formats"))
        self.ButtonCancel.setText(_translate("To_Format_Dialog", "Cancel"))

from PyQt5 import QtWebEngineWidgets
