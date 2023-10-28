# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/gui/panconvert_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_notepad_New(object):
    def setupUi(self, notepad_New):
        notepad_New.setObjectName("notepad_New")
        notepad_New.setWindowModality(QtCore.Qt.NonModal)
        notepad_New.resize(902, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(notepad_New.sizePolicy().hasHeightForWidth())
        notepad_New.setSizePolicy(sizePolicy)
        notepad_New.setMinimumSize(QtCore.QSize(650, 380))
        notepad_New.setSizeIncrement(QtCore.QSize(0, 0))
        notepad_New.setBaseSize(QtCore.QSize(760, 600))
        self.centralwidget = QtWidgets.QWidget(notepad_New)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(650, 300))
        self.centralwidget.setBaseSize(QtCore.QSize(710, 700))
        self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.editor_window = QtWidgets.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editor_window.sizePolicy().hasHeightForWidth())
        self.editor_window.setSizePolicy(sizePolicy)
        self.editor_window.setMinimumSize(QtCore.QSize(0, 80))
        self.editor_window.setBaseSize(QtCore.QSize(0, 266))
        self.editor_window.setAutoFillBackground(True)
        self.editor_window.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.editor_window.setObjectName("editor_window")
        self.gridLayout_2.addWidget(self.editor_window, 0, 0, 4, 1)
        self.WidgetConvert = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.WidgetConvert.sizePolicy().hasHeightForWidth())
        self.WidgetConvert.setSizePolicy(sizePolicy)
        self.WidgetConvert.setMinimumSize(QtCore.QSize(270, 175))
        self.WidgetConvert.setMaximumSize(QtCore.QSize(270, 175))
        self.WidgetConvert.setTabPosition(QtWidgets.QTabWidget.North)
        self.WidgetConvert.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.WidgetConvert.setTabsClosable(False)
        self.WidgetConvert.setObjectName("WidgetConvert")
        self.WidgetConvertStandard = QtWidgets.QWidget()
        self.WidgetConvertStandard.setObjectName("WidgetConvertStandard")
        self.BoxFromFormat = QtWidgets.QGroupBox(self.WidgetConvertStandard)
        self.BoxFromFormat.setGeometry(QtCore.QRect(24, -3, 105, 120))
        self.BoxFromFormat.setMinimumSize(QtCore.QSize(105, 120))
        self.BoxFromFormat.setMaximumSize(QtCore.QSize(105, 100))
        self.BoxFromFormat.setObjectName("BoxFromFormat")
        self.layoutWidget = QtWidgets.QWidget(self.BoxFromFormat)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 92, 77))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ButtonFromLatex = QtWidgets.QRadioButton(self.layoutWidget)
        self.ButtonFromLatex.setObjectName("ButtonFromLatex")
        self.verticalLayout.addWidget(self.ButtonFromLatex)
        self.ButtonFromMarkdown = QtWidgets.QRadioButton(self.layoutWidget)
        self.ButtonFromMarkdown.setChecked(False)
        self.ButtonFromMarkdown.setObjectName("ButtonFromMarkdown")
        self.verticalLayout.addWidget(self.ButtonFromMarkdown)
        self.ButtonFromOpml = QtWidgets.QRadioButton(self.layoutWidget)
        self.ButtonFromOpml.setCheckable(True)
        self.ButtonFromOpml.setChecked(False)
        self.ButtonFromOpml.setObjectName("ButtonFromOpml")
        self.verticalLayout.addWidget(self.ButtonFromOpml)
        self.ButtonFromHtml = QtWidgets.QRadioButton(self.layoutWidget)
        self.ButtonFromHtml.setObjectName("ButtonFromHtml")
        self.verticalLayout.addWidget(self.ButtonFromHtml)
        self.BoxToFormat = QtWidgets.QGroupBox(self.WidgetConvertStandard)
        self.BoxToFormat.setEnabled(True)
        self.BoxToFormat.setGeometry(QtCore.QRect(137, -3, 110, 150))
        self.BoxToFormat.setMinimumSize(QtCore.QSize(110, 150))
        self.BoxToFormat.setMaximumSize(QtCore.QSize(140, 150))
        self.BoxToFormat.setObjectName("BoxToFormat")
        self.layoutWidget1 = QtWidgets.QWidget(self.BoxToFormat)
        self.layoutWidget1.setGeometry(QtCore.QRect(13, 31, 100, 115))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonToEpub = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToEpub.setObjectName("ButtonToEpub")
        self.gridLayout.addWidget(self.ButtonToEpub, 0, 0, 1, 1)
        self.ButtonToMarkdown = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToMarkdown.setCheckable(True)
        self.ButtonToMarkdown.setChecked(False)
        self.ButtonToMarkdown.setObjectName("ButtonToMarkdown")
        self.gridLayout.addWidget(self.ButtonToMarkdown, 2, 0, 1, 1)
        self.ButtonToHtml = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToHtml.setEnabled(True)
        self.ButtonToHtml.setChecked(False)
        self.ButtonToHtml.setObjectName("ButtonToHtml")
        self.gridLayout.addWidget(self.ButtonToHtml, 4, 0, 1, 1)
        self.ButtonToOpml = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToOpml.setObjectName("ButtonToOpml")
        self.gridLayout.addWidget(self.ButtonToOpml, 3, 0, 1, 1)
        self.ButtonToLyx = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToLyx.setEnabled(False)
        self.ButtonToLyx.setObjectName("ButtonToLyx")
        self.gridLayout.addWidget(self.ButtonToLyx, 5, 0, 1, 1)
        self.ButtonToLatex = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToLatex.setObjectName("ButtonToLatex")
        self.gridLayout.addWidget(self.ButtonToLatex, 1, 0, 1, 1)
        self.StandardConversion = QtWidgets.QCheckBox(self.WidgetConvertStandard)
        self.StandardConversion.setGeometry(QtCore.QRect(20, 160, 175, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StandardConversion.sizePolicy().hasHeightForWidth())
        self.StandardConversion.setSizePolicy(sizePolicy)
        self.StandardConversion.setMinimumSize(QtCore.QSize(175, 0))
        self.StandardConversion.setMaximumSize(QtCore.QSize(200, 16777215))
        self.StandardConversion.setChecked(False)
        self.StandardConversion.setAutoRepeat(False)
        self.StandardConversion.setObjectName("StandardConversion")
        self.WidgetConvert.addTab(self.WidgetConvertStandard, "")
        self.WidgetConvertManual = QtWidgets.QWidget()
        self.WidgetConvertManual.setObjectName("WidgetConvertManual")
        self.labelFromBox = QtWidgets.QLabel(self.WidgetConvertManual)
        self.labelFromBox.setGeometry(QtCore.QRect(16, 6, 33, 16))
        self.labelFromBox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.labelFromBox.setObjectName("labelFromBox")
        self.FromParameter = QtWidgets.QLineEdit(self.WidgetConvertManual)
        self.FromParameter.setGeometry(QtCore.QRect(110, 6, 141, 21))
        self.FromParameter.setMinimumSize(QtCore.QSize(50, 0))
        self.FromParameter.setInputMask("")
        self.FromParameter.setText("")
        self.FromParameter.setClearButtonEnabled(True)
        self.FromParameter.setObjectName("FromParameter")
        self.ButtonFromFormat = QtWidgets.QToolButton(self.WidgetConvertManual)
        self.ButtonFromFormat.setGeometry(QtCore.QRect(74, 6, 26, 22))
        self.ButtonFromFormat.setObjectName("ButtonFromFormat")
        self.labelToBox = QtWidgets.QLabel(self.WidgetConvertManual)
        self.labelToBox.setGeometry(QtCore.QRect(16, 38, 40, 16))
        self.labelToBox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.labelToBox.setObjectName("labelToBox")
        self.ToParameter = QtWidgets.QLineEdit(self.WidgetConvertManual)
        self.ToParameter.setGeometry(QtCore.QRect(110, 38, 140, 21))
        self.ToParameter.setText("")
        self.ToParameter.setClearButtonEnabled(True)
        self.ToParameter.setObjectName("ToParameter")
        self.ButtonToFormat = QtWidgets.QToolButton(self.WidgetConvertManual)
        self.ButtonToFormat.setGeometry(QtCore.QRect(74, 38, 26, 22))
        self.ButtonToFormat.setObjectName("ButtonToFormat")
        self.ButtonOptions = QtWidgets.QToolButton(self.WidgetConvertManual)
        self.ButtonOptions.setGeometry(QtCore.QRect(0, 70, 26, 71))
        self.ButtonOptions.setObjectName("ButtonOptions")
        self.ExtraParameter = QtWidgets.QTextEdit(self.WidgetConvertManual)
        self.ExtraParameter.setGeometry(QtCore.QRect(30, 70, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ExtraParameter.setFont(font)
        self.ExtraParameter.setObjectName("ExtraParameter")
        self.WidgetConvert.addTab(self.WidgetConvertManual, "")
        self.gridLayout_2.addWidget(self.WidgetConvert, 0, 1, 1, 1)
        self.WidgetBatch = QtWidgets.QWidget(self.centralwidget)
        self.WidgetBatch.setMinimumSize(QtCore.QSize(270, 0))
        self.WidgetBatch.setBaseSize(QtCore.QSize(270, 230))
        self.WidgetBatch.setObjectName("WidgetBatch")
        self.groupBox_2 = QtWidgets.QGroupBox(self.WidgetBatch)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 0, 270, 230))
        self.groupBox_2.setMinimumSize(QtCore.QSize(270, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(270, 230))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 110, 140, 81))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(120, 75))
        self.groupBox.setMaximumSize(QtCore.QSize(140, 90))
        self.groupBox.setObjectName("groupBox")
        self.ParameterBatchconvertRecursive = QtWidgets.QCheckBox(self.groupBox)
        self.ParameterBatchconvertRecursive.setGeometry(QtCore.QRect(10, 60, 85, 20))
        self.ParameterBatchconvertRecursive.setChecked(True)
        self.ParameterBatchconvertRecursive.setObjectName("ParameterBatchconvertRecursive")
        self.ParameterBatchconvertDirectory = QtWidgets.QRadioButton(self.groupBox)
        self.ParameterBatchconvertDirectory.setGeometry(QtCore.QRect(10, 40, 101, 18))
        self.ParameterBatchconvertDirectory.setChecked(True)
        self.ParameterBatchconvertDirectory.setObjectName("ParameterBatchconvertDirectory")
        self.ParameterBatchconvertFiles = QtWidgets.QRadioButton(self.groupBox)
        self.ParameterBatchconvertFiles.setGeometry(QtCore.QRect(10, 20, 101, 19))
        self.ParameterBatchconvertFiles.setObjectName("ParameterBatchconvertFiles")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(190, 90, 58, 21))
        self.label_4.setObjectName("label_4")
        self.Filter = QtWidgets.QLineEdit(self.groupBox_2)
        self.Filter.setGeometry(QtCore.QRect(10, 90, 171, 21))
        self.Filter.setObjectName("Filter")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 29, 211, 54))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.OpenPath = QtWidgets.QLineEdit(self.layoutWidget2)
        self.OpenPath.setObjectName("OpenPath")
        self.verticalLayout_2.addWidget(self.OpenPath)
        self.OpenPathOutput = QtWidgets.QLineEdit(self.layoutWidget2)
        self.OpenPathOutput.setInputMask("")
        self.OpenPathOutput.setText("")
        self.OpenPathOutput.setObjectName("OpenPathOutput")
        self.verticalLayout_2.addWidget(self.OpenPathOutput)
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget3.setGeometry(QtCore.QRect(225, 29, 27, 54))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.Button_Open_Path = QtWidgets.QToolButton(self.layoutWidget3)
        self.Button_Open_Path.setMaximumSize(QtCore.QSize(25, 23))
        self.Button_Open_Path.setObjectName("Button_Open_Path")
        self.verticalLayout_3.addWidget(self.Button_Open_Path)
        self.Button_Open_Path_Output = QtWidgets.QToolButton(self.layoutWidget3)
        self.Button_Open_Path_Output.setMaximumSize(QtCore.QSize(25, 23))
        self.Button_Open_Path_Output.setObjectName("Button_Open_Path_Output")
        self.verticalLayout_3.addWidget(self.Button_Open_Path_Output)
        self.BatchConversion = QtWidgets.QCheckBox(self.groupBox_2)
        self.BatchConversion.setGeometry(QtCore.QRect(10, 200, 175, 20))
        self.BatchConversion.setMinimumSize(QtCore.QSize(175, 0))
        self.BatchConversion.setObjectName("BatchConversion")
        self.gridLayout_2.addWidget(self.WidgetBatch, 2, 1, 1, 1)
        self.WidgetOK = QtWidgets.QWidget(self.centralwidget)
        self.WidgetOK.setMinimumSize(QtCore.QSize(270, 50))
        self.WidgetOK.setMaximumSize(QtCore.QSize(270, 50))
        self.WidgetOK.setObjectName("WidgetOK")
        self.layoutWidget4 = QtWidgets.QWidget(self.WidgetOK)
        self.layoutWidget4.setGeometry(QtCore.QRect(10, 10, 249, 35))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.MessageNumber = QtWidgets.QLCDNumber(self.layoutWidget4)
        self.MessageNumber.setMinimumSize(QtCore.QSize(50, 0))
        self.MessageNumber.setMaximumSize(QtCore.QSize(100, 16777215))
        self.MessageNumber.setToolTip("")
        self.MessageNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MessageNumber.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MessageNumber.setObjectName("MessageNumber")
        self.horizontalLayout.addWidget(self.MessageNumber)
        self.ButtonRevert = QtWidgets.QPushButton(self.layoutWidget4)
        self.ButtonRevert.setMinimumSize(QtCore.QSize(60, 0))
        self.ButtonRevert.setMaximumSize(QtCore.QSize(110, 16777215))
        self.ButtonRevert.setObjectName("ButtonRevert")
        self.horizontalLayout.addWidget(self.ButtonRevert)
        self.ButtonConvert = QtWidgets.QPushButton(self.layoutWidget4)
        self.ButtonConvert.setMaximumSize(QtCore.QSize(110, 16777215))
        self.ButtonConvert.setObjectName("ButtonConvert")
        self.horizontalLayout.addWidget(self.ButtonConvert)
        self.gridLayout_2.addWidget(self.WidgetOK, 3, 1, 1, 1)
        self.ButtonToggleBatch = QtWidgets.QToolButton(self.centralwidget)
        self.ButtonToggleBatch.setMinimumSize(QtCore.QSize(10, 10))
        self.ButtonToggleBatch.setMaximumSize(QtCore.QSize(16, 16))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/arrow-right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ButtonToggleBatch.setIcon(icon)
        self.ButtonToggleBatch.setObjectName("ButtonToggleBatch")
        self.gridLayout_2.addWidget(self.ButtonToggleBatch, 1, 1, 1, 1)
        notepad_New.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(notepad_New)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 902, 24))
        self.menubar.setAcceptDrops(False)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExtras = QtWidgets.QMenu(self.menubar)
        self.menuExtras.setEnabled(True)
        self.menuExtras.setObjectName("menuExtras")
        self.menuEdit_2 = QtWidgets.QMenu(self.menubar)
        self.menuEdit_2.setObjectName("menuEdit_2")
        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")
        notepad_New.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(notepad_New)
        self.statusbar.setObjectName("statusbar")
        notepad_New.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(notepad_New)
        self.toolBar.setEnabled(True)
        self.toolBar.setMovable(True)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setFloatable(True)
        self.toolBar.setObjectName("toolBar")
        notepad_New.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockLogWindow = QtWidgets.QDockWidget(notepad_New)
        self.dockLogWindow.setMinimumSize(QtCore.QSize(103, 125))
        self.dockLogWindow.setFloating(True)
        self.dockLogWindow.setAllowedAreas(QtCore.Qt.AllDockWidgetAreas)
        self.dockLogWindow.setObjectName("dockLogWindow")
        self.logWindow = QtWidgets.QWidget()
        self.logWindow.setObjectName("logWindow")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.logWindow)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.logBrowser = QtWidgets.QPlainTextEdit(self.logWindow)
        self.logBrowser.setObjectName("logBrowser")
        self.gridLayout_3.addWidget(self.logBrowser, 0, 0, 1, 1)
        self.dockLogWindow.setWidget(self.logWindow)
        notepad_New.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockLogWindow)
        self.actionSave = QtWidgets.QAction(notepad_New)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/save"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon1)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(notepad_New)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/open"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon2)
        self.actionOpen.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_AS = QtWidgets.QAction(notepad_New)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/save_as"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_AS.setIcon(icon3)
        self.actionSave_AS.setObjectName("actionSave_AS")
        self.actionNew = QtWidgets.QAction(notepad_New)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/new"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon4)
        self.actionNew.setObjectName("actionNew")
        self.actionMarkdown2Latex = QtWidgets.QAction(notepad_New)
        self.actionMarkdown2Latex.setObjectName("actionMarkdown2Latex")
        self.actionOpml2latex = QtWidgets.QAction(notepad_New)
        self.actionOpml2latex.setObjectName("actionOpml2latex")
        self.actionOpml2Markdown = QtWidgets.QAction(notepad_New)
        self.actionOpml2Markdown.setObjectName("actionOpml2Markdown")
        self.actionMarkdown2opml = QtWidgets.QAction(notepad_New)
        self.actionMarkdown2opml.setObjectName("actionMarkdown2opml")
        self.actionPreferences = QtWidgets.QAction(notepad_New)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/freferences"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(":/icons/freferences"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionPreferences.setIcon(icon5)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionLatex2Opml = QtWidgets.QAction(notepad_New)
        self.actionLatex2Opml.setObjectName("actionLatex2Opml")
        self.actionLatex2Markdown = QtWidgets.QAction(notepad_New)
        self.actionLatex2Markdown.setObjectName("actionLatex2Markdown")
        self.actionHtml2Markdown = QtWidgets.QAction(notepad_New)
        self.actionHtml2Markdown.setObjectName("actionHtml2Markdown")
        self.actionHtml2Latex = QtWidgets.QAction(notepad_New)
        self.actionHtml2Latex.setObjectName("actionHtml2Latex")
        self.actionHtml2opml = QtWidgets.QAction(notepad_New)
        self.actionHtml2opml.setObjectName("actionHtml2opml")
        self.actionOpml2html = QtWidgets.QAction(notepad_New)
        self.actionOpml2html.setObjectName("actionOpml2html")
        self.actionMarkdown2html = QtWidgets.QAction(notepad_New)
        self.actionMarkdown2html.setObjectName("actionMarkdown2html")
        self.actionLatex2html = QtWidgets.QAction(notepad_New)
        self.actionLatex2html.setObjectName("actionLatex2html")
        self.actionHelp = QtWidgets.QAction(notepad_New)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon6.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionHelp.setIcon(icon6)
        self.actionHelp.setObjectName("actionHelp")
        self.actionMarkdown2Lyx = QtWidgets.QAction(notepad_New)
        self.actionMarkdown2Lyx.setObjectName("actionMarkdown2Lyx")
        self.actionUndo = QtWidgets.QAction(notepad_New)
        self.actionUndo.setObjectName("actionUndo")
        self.actionAbout = QtWidgets.QAction(notepad_New)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSearch = QtWidgets.QAction(notepad_New)
        self.actionSearch.setObjectName("actionSearch")
        self.actionLogViewer = QtWidgets.QAction(notepad_New)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/opml"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLogViewer.setIcon(icon7)
        self.actionLogViewer.setObjectName("actionLogViewer")
        self.actionAbove = QtWidgets.QAction(notepad_New)
        self.actionAbove.setObjectName("actionAbove")
        self.actionBelow = QtWidgets.QAction(notepad_New)
        self.actionBelow.setObjectName("actionBelow")
        self.actionLeft = QtWidgets.QAction(notepad_New)
        self.actionLeft.setObjectName("actionLeft")
        self.actionRight = QtWidgets.QAction(notepad_New)
        self.actionRight.setObjectName("actionRight")
        self.actionBatchModeToggle = QtWidgets.QAction(notepad_New)
        self.actionBatchModeToggle.setObjectName("actionBatchModeToggle")
        self.actionQuit = QtWidgets.QAction(notepad_New)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen_URI = QtWidgets.QAction(notepad_New)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/open_uri.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_URI.setIcon(icon8)
        self.actionOpen_URI.setObjectName("actionOpen_URI")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpen_URI)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_AS)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menuExtras.addAction(self.actionHelp)
        self.menuExtras.addAction(self.actionAbout)
        self.menuEdit_2.addAction(self.actionPreferences)
        self.menuEdit_2.addAction(self.actionUndo)
        self.menuEdit_2.addAction(self.actionSearch)
        self.menuWindow.addAction(self.actionLogViewer)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionAbove)
        self.menuWindow.addAction(self.actionBelow)
        self.menuWindow.addAction(self.actionLeft)
        self.menuWindow.addAction(self.actionRight)
        self.menuWindow.addSeparator()
        self.menuWindow.addAction(self.actionBatchModeToggle)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit_2.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuExtras.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionOpen_URI)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_AS)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)
        self.toolBar.addAction(self.actionLogViewer)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHelp)

        self.retranslateUi(notepad_New)
        self.WidgetConvert.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(notepad_New)

    def retranslateUi(self, notepad_New):
        _translate = QtCore.QCoreApplication.translate
        notepad_New.setWindowTitle(_translate("notepad_New", "PanConvert"))
        self.BoxFromFormat.setTitle(_translate("notepad_New", "From Format"))
        self.ButtonFromLatex.setText(_translate("notepad_New", "Latex"))
        self.ButtonFromMarkdown.setText(_translate("notepad_New", "Markdown"))
        self.ButtonFromOpml.setText(_translate("notepad_New", "Opml"))
        self.ButtonFromHtml.setText(_translate("notepad_New", "Html"))
        self.BoxToFormat.setTitle(_translate("notepad_New", "To Format"))
        self.ButtonToEpub.setText(_translate("notepad_New", "EPub"))
        self.ButtonToMarkdown.setText(_translate("notepad_New", "Markdown"))
        self.ButtonToHtml.setText(_translate("notepad_New", "Html"))
        self.ButtonToOpml.setText(_translate("notepad_New", "Opml"))
        #self.ButtonToLyx.setText(_translate("notepad_New", "Lyx"))
        self.ButtonToLatex.setText(_translate("notepad_New", "Latex"))
        self.StandardConversion.setText(_translate("notepad_New", "Standard Conversion"))
        self.WidgetConvert.setTabText(self.WidgetConvert.indexOf(self.WidgetConvertStandard), _translate("notepad_New", "Standard"))
        self.labelFromBox.setText(_translate("notepad_New", "From"))
        self.ButtonFromFormat.setText(_translate("notepad_New", "..."))
        self.labelToBox.setText(_translate("notepad_New", "To"))
        self.ButtonToFormat.setText(_translate("notepad_New", "..."))
        self.ButtonOptions.setText(_translate("notepad_New", "..."))
        self.ExtraParameter.setPlaceholderText(_translate("notepad_New", "Xtra Pandoc Options"))
        self.WidgetConvert.setTabText(self.WidgetConvert.indexOf(self.WidgetConvertManual), _translate("notepad_New", "Manual"))
        self.groupBox_2.setTitle(_translate("notepad_New", "Batch Mode"))
        self.groupBox.setTitle(_translate("notepad_New", "Conversion Mode"))
        self.ParameterBatchconvertRecursive.setText(_translate("notepad_New", "Recursive"))
        self.ParameterBatchconvertDirectory.setText(_translate("notepad_New", "Directory"))
        self.ParameterBatchconvertFiles.setText(_translate("notepad_New", "Files"))
        self.label_4.setText(_translate("notepad_New", "File Filter"))
        self.Filter.setPlaceholderText(_translate("notepad_New", "optional File Extension Filter (separate with ;)"))
        self.OpenPath.setPlaceholderText(_translate("notepad_New", "Optional Directory Path"))
        self.OpenPathOutput.setPlaceholderText(_translate("notepad_New", "Optional Output Directory Path"))
        self.Button_Open_Path.setText(_translate("notepad_New", "..."))
        self.Button_Open_Path_Output.setText(_translate("notepad_New", "..."))
        self.BatchConversion.setText(_translate("notepad_New", "Batch Conversion"))
        self.MessageNumber.setAccessibleName(_translate("notepad_New", "New Messages"))
        self.ButtonRevert.setText(_translate("notepad_New", "Revert"))
        self.ButtonConvert.setText(_translate("notepad_New", "Convert"))
        self.ButtonToggleBatch.setText(_translate("notepad_New", "..."))
        self.menuFile.setTitle(_translate("notepad_New", "File"))
        self.menuExtras.setTitle(_translate("notepad_New", "Help"))
        self.menuEdit_2.setTitle(_translate("notepad_New", "Edit"))
        self.menuWindow.setTitle(_translate("notepad_New", "Window"))
        self.toolBar.setWindowTitle(_translate("notepad_New", "toolBar"))
        self.actionSave.setText(_translate("notepad_New", "Save Buffer"))
        self.actionOpen.setText(_translate("notepad_New", "Open"))
        self.actionOpen.setShortcut(_translate("notepad_New", "Ctrl+O"))
        self.actionSave_AS.setText(_translate("notepad_New", "Save File"))
        self.actionSave_AS.setShortcut(_translate("notepad_New", "Ctrl+S"))
        self.actionNew.setText(_translate("notepad_New", "New"))
        self.actionNew.setToolTip(_translate("notepad_New", "New"))
        self.actionMarkdown2Latex.setText(_translate("notepad_New", "Markdown2Latex"))
        self.actionOpml2latex.setText(_translate("notepad_New", "opml2latex"))
        self.actionOpml2latex.setToolTip(_translate("notepad_New", "Opml2Latex"))
        self.actionOpml2Markdown.setText(_translate("notepad_New", "Opml2Markdown"))
        self.actionOpml2Markdown.setToolTip(_translate("notepad_New", "Opml2Markdown(Pandoc)"))
        self.actionMarkdown2opml.setText(_translate("notepad_New", "Markdown2opml"))
        self.actionPreferences.setText(_translate("notepad_New", "Preferences"))
        self.actionLatex2Opml.setText(_translate("notepad_New", "Latex2Opml"))
        self.actionLatex2Markdown.setText(_translate("notepad_New", "Latex2Markdown"))
        self.actionHtml2Markdown.setText(_translate("notepad_New", "Html2Markdown"))
        self.actionHtml2Latex.setText(_translate("notepad_New", "Html2Latex"))
        self.actionHtml2opml.setText(_translate("notepad_New", "html2opml"))
        self.actionOpml2html.setText(_translate("notepad_New", "opml2html"))
        self.actionMarkdown2html.setText(_translate("notepad_New", "markdown2html"))
        self.actionLatex2html.setText(_translate("notepad_New", "latex2html"))
        self.actionHelp.setText(_translate("notepad_New", "Help"))
        self.actionMarkdown2Lyx.setText(_translate("notepad_New", "Markdown2Lyx"))
        self.actionUndo.setText(_translate("notepad_New", "Undo"))
        self.actionAbout.setText(_translate("notepad_New", "About"))
        self.actionSearch.setText(_translate("notepad_New", "Search"))
        self.actionLogViewer.setText(_translate("notepad_New", "LogViewer"))
        self.actionAbove.setText(_translate("notepad_New", "Position Above"))
        self.actionBelow.setText(_translate("notepad_New", "Position Below"))
        self.actionLeft.setText(_translate("notepad_New", "Position Left"))
        self.actionRight.setText(_translate("notepad_New", "Position Right"))
        self.actionBatchModeToggle.setText(_translate("notepad_New", "Batch Mode Toggle"))
        self.actionQuit.setText(_translate("notepad_New", "Quit"))
        self.actionOpen_URI.setText(_translate("notepad_New", "Open URI"))
import source.gui.icons_rc
