# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_help.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Information_Dialog(object):
    def setupUi(self, Information_Dialog):
        Information_Dialog.setObjectName("Information_Dialog")
        Information_Dialog.resize(492, 575)
        self.gridLayout = QtWidgets.QGridLayout(Information_Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonCancel = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.horizontalLayout.addWidget(self.ButtonCancel)
        self.ButtonHelpPanconvert = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonHelpPanconvert.setObjectName("ButtonHelpPanconvert")
        self.horizontalLayout.addWidget(self.ButtonHelpPanconvert)
        self.ButtonHelpPandoc = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonHelpPandoc.setObjectName("ButtonHelpPandoc")
        self.horizontalLayout.addWidget(self.ButtonHelpPandoc)
        self.ButtonBackward = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonBackward.setObjectName("ButtonBackward")
        self.horizontalLayout.addWidget(self.ButtonBackward)
        self.ButtonForward = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonForward.setObjectName("ButtonForward")
        self.horizontalLayout.addWidget(self.ButtonForward)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.textBrowser = QtWebEngineWidgets.QWebEngineView(Information_Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)

        self.retranslateUi(Information_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Information_Dialog)

    def retranslateUi(self, Information_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Information_Dialog.setWindowTitle(_translate("Information_Dialog", "Help"))
        self.ButtonCancel.setText(_translate("Information_Dialog", "Cancel"))
        self.ButtonHelpPanconvert.setText(_translate("Information_Dialog", "Panconvert-Help"))
        self.ButtonHelpPandoc.setText(_translate("Information_Dialog", "Pandoc-Help"))
        self.ButtonBackward.setText(_translate("Information_Dialog", "<"))
        self.ButtonForward.setText(_translate("Information_Dialog", ">"))

from PyQt5 import QtWebEngineWidgets
