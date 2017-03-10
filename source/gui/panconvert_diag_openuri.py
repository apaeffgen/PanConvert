# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'panconvert_diag_openuri.ui'
#
# Created: Fri Mar 10 14:06:45 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogOpenURI(object):
    def setupUi(self, DialogOpenURI):
        DialogOpenURI.setObjectName("DialogOpenURI")
        DialogOpenURI.resize(386, 90)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogOpenURI.sizePolicy().hasHeightForWidth())
        DialogOpenURI.setSizePolicy(sizePolicy)
        DialogOpenURI.setMinimumSize(QtCore.QSize(386, 90))
        DialogOpenURI.setMaximumSize(QtCore.QSize(386, 90))
        self.URI = QtWidgets.QPlainTextEdit(DialogOpenURI)
        self.URI.setGeometry(QtCore.QRect(10, 10, 371, 41))
        self.URI.setObjectName("URI")
        self.widget = QtWidgets.QWidget(DialogOpenURI)
        self.widget.setGeometry(QtCore.QRect(7, 60, 371, 32))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.CheckBoxStayOnTop = QtWidgets.QCheckBox(self.widget)
        self.CheckBoxStayOnTop.setObjectName("CheckBoxStayOnTop")
        self.horizontalLayout.addWidget(self.CheckBoxStayOnTop)
        self.ButtonCancel = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonCancel.sizePolicy().hasHeightForWidth())
        self.ButtonCancel.setSizePolicy(sizePolicy)
        self.ButtonCancel.setMinimumSize(QtCore.QSize(114, 32))
        self.ButtonCancel.setMaximumSize(QtCore.QSize(114, 32))
        self.ButtonCancel.setBaseSize(QtCore.QSize(114, 32))
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.horizontalLayout.addWidget(self.ButtonCancel)
        self.ButtonOpenURI = QtWidgets.QPushButton(self.widget)
        self.ButtonOpenURI.setObjectName("ButtonOpenURI")
        self.horizontalLayout.addWidget(self.ButtonOpenURI)

        self.retranslateUi(DialogOpenURI)
        QtCore.QMetaObject.connectSlotsByName(DialogOpenURI)

    def retranslateUi(self, DialogOpenURI):
        _translate = QtCore.QCoreApplication.translate
        DialogOpenURI.setWindowTitle(_translate("DialogOpenURI", "Open URI"))
        self.CheckBoxStayOnTop.setText(_translate("DialogOpenURI", "Stay on Top"))
        self.ButtonCancel.setText(_translate("DialogOpenURI", "Cancel"))
        self.ButtonOpenURI.setText(_translate("DialogOpenURI", "Open URI"))

