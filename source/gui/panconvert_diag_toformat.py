# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/gui/panconvert_diag_toformat.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_To_Format_Dialog(object):
    def setupUi(self, To_Format_Dialog):
        To_Format_Dialog.setObjectName("To_Format_Dialog")
        To_Format_Dialog.setWindowModality(QtCore.Qt.NonModal)
        To_Format_Dialog.setEnabled(True)
        To_Format_Dialog.resize(334, 402)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(To_Format_Dialog.sizePolicy().hasHeightForWidth())
        To_Format_Dialog.setSizePolicy(sizePolicy)
        To_Format_Dialog.setMinimumSize(QtCore.QSize(224, 234))
        To_Format_Dialog.setSizeGripEnabled(False)
        To_Format_Dialog.setModal(False)
        self.gridLayout = QtWidgets.QGridLayout(To_Format_Dialog)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
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
