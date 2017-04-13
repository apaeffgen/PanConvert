# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_fromformat.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_From_Format_Dialog(object):
    def setupUi(self, From_Format_Dialog):
        From_Format_Dialog.setObjectName("From_Format_Dialog")
        From_Format_Dialog.resize(224, 234)
        self.gridLayout = QtWidgets.QGridLayout(From_Format_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ButtonCancel = QtWidgets.QPushButton(From_Format_Dialog)
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.verticalLayout.addWidget(self.ButtonCancel)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.textBrowser = QtWebEngineWidgets.QWebEngineView(From_Format_Dialog)
        self.textBrowser.setMinimumSize(QtCore.QSize(200, 100))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(From_Format_Dialog)
        QtCore.QMetaObject.connectSlotsByName(From_Format_Dialog)

    def retranslateUi(self, From_Format_Dialog):
        _translate = QtCore.QCoreApplication.translate
        From_Format_Dialog.setWindowTitle(_translate("From_Format_Dialog", "Pandoc From Formats"))
        self.ButtonCancel.setText(_translate("From_Format_Dialog", "Cancel"))

from PyQt5 import QtWebEngineWidgets
