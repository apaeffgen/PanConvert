# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_info.ui'
#
# Created: Sat May 16 19:57:46 2015
#      by: PyQt5 UI code generator 5.3.1
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
        self.ButtonInfo = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonInfo.setObjectName("ButtonInfo")
        self.gridLayout.addWidget(self.ButtonInfo, 0, 2, 1, 1)
        self.ButtonMoreInfo = QtWidgets.QPushButton(Information_Dialog)
        self.ButtonMoreInfo.setObjectName("ButtonMoreInfo")
        self.gridLayout.addWidget(self.ButtonMoreInfo, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Information_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Information_Dialog)

    def retranslateUi(self, Information_Dialog):
        _translate = QtCore.QCoreApplication.translate
        Information_Dialog.setWindowTitle(_translate("Information_Dialog", "Information"))
        self.ButtonCancel.setText(_translate("Information_Dialog", "Cancel"))
        self.ButtonInfo.setText(_translate("Information_Dialog", "Pandoc-Options"))
        self.ButtonMoreInfo.setText(_translate("Information_Dialog", "More Information"))

from PyQt5 import QtWebKitWidgets
