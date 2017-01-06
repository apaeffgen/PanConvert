# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/apaeffgen/Programmierung/PanConvert/source/gui/panconvert_dialog_batch.ui'
#
# Created: Mon Jan  2 14:52:08 2017
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DialogBatch(object):
    def setupUi(self, DialogBatch):
        DialogBatch.setObjectName("DialogBatch")
        DialogBatch.resize(386, 220)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DialogBatch.sizePolicy().hasHeightForWidth())
        DialogBatch.setSizePolicy(sizePolicy)
        DialogBatch.setMinimumSize(QtCore.QSize(386, 220))
        DialogBatch.setMaximumSize(QtCore.QSize(386, 220))
        self.OpenPath = QtWidgets.QLineEdit(DialogBatch)
        self.OpenPath.setGeometry(QtCore.QRect(47, 12, 311, 21))
        self.OpenPath.setObjectName("OpenPath")
        self.Button_Open_Path = QtWidgets.QToolButton(DialogBatch)
        self.Button_Open_Path.setGeometry(QtCore.QRect(12, 12, 25, 22))
        self.Button_Open_Path.setMaximumSize(QtCore.QSize(25, 23))
        self.Button_Open_Path.setObjectName("Button_Open_Path")
        self.ButtonSave = QtWidgets.QPushButton(DialogBatch)
        self.ButtonSave.setGeometry(QtCore.QRect(250, 160, 114, 32))
        self.ButtonSave.setObjectName("ButtonSave")
        self.ButtonCancel = QtWidgets.QPushButton(DialogBatch)
        self.ButtonCancel.setGeometry(QtCore.QRect(250, 120, 114, 32))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ButtonCancel.sizePolicy().hasHeightForWidth())
        self.ButtonCancel.setSizePolicy(sizePolicy)
        self.ButtonCancel.setMinimumSize(QtCore.QSize(114, 32))
        self.ButtonCancel.setMaximumSize(QtCore.QSize(114, 32))
        self.ButtonCancel.setBaseSize(QtCore.QSize(114, 32))
        self.ButtonCancel.setObjectName("ButtonCancel")
        self.Filter = QtWidgets.QLineEdit(DialogBatch)
        self.Filter.setGeometry(QtCore.QRect(10, 50, 350, 21))
        self.Filter.setObjectName("Filter")
        self.layoutWidget = QtWidgets.QWidget(DialogBatch)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 90, 204, 102))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.layoutWidget)
        self.groupBox.setMinimumSize(QtCore.QSize(200, 100))
        self.groupBox.setMaximumSize(QtCore.QSize(200, 100))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ParameterBatchconvertRecursive = QtWidgets.QCheckBox(self.groupBox)
        self.ParameterBatchconvertRecursive.setChecked(True)
        self.ParameterBatchconvertRecursive.setObjectName("ParameterBatchconvertRecursive")
        self.gridLayout_2.addWidget(self.ParameterBatchconvertRecursive, 3, 0, 1, 1)
        self.ParameterBatchconvertDirectory = QtWidgets.QRadioButton(self.groupBox)
        self.ParameterBatchconvertDirectory.setChecked(True)
        self.ParameterBatchconvertDirectory.setObjectName("ParameterBatchconvertDirectory")
        self.gridLayout_2.addWidget(self.ParameterBatchconvertDirectory, 2, 0, 1, 1)
        self.ParameterBatchconvertFiles = QtWidgets.QRadioButton(self.groupBox)
        self.ParameterBatchconvertFiles.setObjectName("ParameterBatchconvertFiles")
        self.gridLayout_2.addWidget(self.ParameterBatchconvertFiles, 1, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.retranslateUi(DialogBatch)
        QtCore.QMetaObject.connectSlotsByName(DialogBatch)

    def retranslateUi(self, DialogBatch):
        _translate = QtCore.QCoreApplication.translate
        DialogBatch.setWindowTitle(_translate("DialogBatch", "Batch Preferences"))
        self.OpenPath.setPlaceholderText(_translate("DialogBatch", "Optional Directory Path"))
        self.Button_Open_Path.setText(_translate("DialogBatch", "..."))
        self.ButtonSave.setText(_translate("DialogBatch", "Save"))
        self.ButtonCancel.setText(_translate("DialogBatch", "Cancel"))
        self.Filter.setPlaceholderText(_translate("DialogBatch", "optional File Extension Filter (separate with ;)"))
        self.groupBox.setTitle(_translate("DialogBatch", "Conversion Mode"))
        self.ParameterBatchconvertRecursive.setText(_translate("DialogBatch", "Recursive"))
        self.ParameterBatchconvertDirectory.setText(_translate("DialogBatch", "Directory"))
        self.ParameterBatchconvertFiles.setText(_translate("DialogBatch", "Files"))

