# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/apaeffgen/Programmierung/PanConvert/source/gui/panconvert_diag_help.ui'
#
# Created: Sun Dec 25 12:27:32 2016
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Information_Dialog(object):
    def setupUi(self, Information_Dialog):
        Information_Dialog.setObjectName("Information_Dialog")
        Information_Dialog.resize(707, 575)
        self.gridLayout_2 = QtWidgets.QGridLayout(Information_Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtWebKitWidgets.QWebView(Information_Dialog)
        self.textBrowser.setUrl(QtCore.QUrl("about:blank"))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonCancel = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.gridLayout.addWidget(self.ButtonCancel, 0, 0, 1, 1)
        self.ButtonHelpPandoc = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonHelpPandoc.setObjectName("ButtonHelpPandoc")
        self.gridLayout.addWidget(self.ButtonHelpPandoc, 0, 2, 1, 1)
        self.ButtonHelpPanconvert = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonHelpPanconvert.setObjectName("ButtonHelpPanconvert")
        self.gridLayout.addWidget(self.ButtonHelpPanconvert, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Information_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Information_Dialog)

    def retranslateUi(self, Information_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Information_Dialog.setWindowTitle(_translate("Information_Dialog", "Help"))
        self.ButtonCancel.setText(_translate("Information_Dialog", "Cancel"))
        self.ButtonHelpPandoc.setText(_translate("Information_Dialog", "Pandoc-Help"))
        self.ButtonHelpPanconvert.setText(_translate("Information_Dialog", "Panconvert-Help"))

from PyQt5 import QtWebKitWidgets
