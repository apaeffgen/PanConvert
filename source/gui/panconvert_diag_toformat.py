# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_toformat.ui'
#
# Created: Tue Jan 17 09:00:06 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_To_Format_Dialog(object):
    def setupUi(self, To_Format_Dialog):
        To_Format_Dialog.setObjectName("To_Format_Dialog")
        To_Format_Dialog.resize(274, 402)
        self.gridLayout_2 = QtWidgets.QGridLayout(To_Format_Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonCancel = QtWidgets.QPushButton(To_Format_Dialog)
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.gridLayout.addWidget(self.ButtonCancel, 0, 0, 1, 1)
        self.ButtonInfo = QtWidgets.QPushButton(To_Format_Dialog)
        self.ButtonInfo.setObjectName("ButtonInfo")
        self.gridLayout.addWidget(self.ButtonInfo, 0, 2, 1, 1)
        self.ButtonMoreInfo = QtWidgets.QPushButton(To_Format_Dialog)
        self.ButtonMoreInfo.setObjectName("ButtonMoreInfo")
        self.gridLayout.addWidget(self.ButtonMoreInfo, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 2, 0, 1, 1)
        self.textBrowser = QtWebKitWidgets.QWebView(To_Format_Dialog)
        self.textBrowser.setUrl(QtCore.QUrl("about:blank"))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 1, 0, 1, 1)

        self.retranslateUi(To_Format_Dialog)
        QtCore.QMetaObject.connectSlotsByName(To_Format_Dialog)

    def retranslateUi(self, To_Format_Dialog):
        _translate = QtCore.QCoreApplication.translate
        To_Format_Dialog.setWindowTitle(_translate("To_Format_Dialog", "Pandoc To Formats"))
        self.ButtonCancel.setText(_translate("To_Format_Dialog", "Cancel"))
        self.ButtonInfo.setText(_translate("To_Format_Dialog", "Formats"))
        self.ButtonMoreInfo.setText(_translate("To_Format_Dialog", "Help"))

from PyQt5 import QtWebKitWidgets
