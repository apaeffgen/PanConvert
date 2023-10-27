# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source/gui/panconvert_gui_old.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_notepad(object):
    def setupUi(self, notepad):
        notepad.setObjectName("notepad")
        notepad.setWindowModality(QtCore.Qt.NonModal)
        notepad.resize(820, 576)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(notepad.sizePolicy().hasHeightForWidth())
        notepad.setSizePolicy(sizePolicy)
        notepad.setMinimumSize(QtCore.QSize(820, 550))
        notepad.setBaseSize(QtCore.QSize(760, 550))
        self.centralwidget = QtWidgets.QWidget(notepad)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QtCore.QSize(710, 500))
        self.centralwidget.setBaseSize(QtCore.QSize(710, 700))
        self.centralwidget.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.BoxFromFormat = QtWidgets.QGroupBox(self.centralwidget)
        self.BoxFromFormat.setMinimumSize(QtCore.QSize(120, 120))
        self.BoxFromFormat.setMaximumSize(QtCore.QSize(120, 100))
        self.BoxFromFormat.setObjectName("BoxFromFormat")
        self.layoutWidget = QtWidgets.QWidget(self.BoxFromFormat)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 92, 77))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
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
        self.ButtonFromLatex = QtWidgets.QRadioButton(self.layoutWidget)
        self.ButtonFromLatex.setObjectName("ButtonFromLatex")
        self.verticalLayout.addWidget(self.ButtonFromLatex)
        self.gridLayout_2.addWidget(self.BoxFromFormat, 0, 0, 3, 1)
        self.BoxToFormat = QtWidgets.QGroupBox(self.centralwidget)
        self.BoxToFormat.setMinimumSize(QtCore.QSize(120, 135))
        self.BoxToFormat.setMaximumSize(QtCore.QSize(140, 135))
        self.BoxToFormat.setObjectName("BoxToFormat")
        self.layoutWidget1 = QtWidgets.QWidget(self.BoxToFormat)
        self.layoutWidget1.setGeometry(QtCore.QRect(13, 31, 92, 115))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.ButtonToHtml = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToHtml.setChecked(False)
        self.ButtonToHtml.setObjectName("ButtonToHtml")
        self.gridLayout.addWidget(self.ButtonToHtml, 4, 0, 1, 1)
        self.ButtonToMarkdown = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToMarkdown.setCheckable(True)
        self.ButtonToMarkdown.setChecked(False)
        self.ButtonToMarkdown.setObjectName("ButtonToMarkdown")
        self.gridLayout.addWidget(self.ButtonToMarkdown, 1, 0, 1, 1)
        self.ButtonToOpml = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToOpml.setObjectName("ButtonToOpml")
        self.gridLayout.addWidget(self.ButtonToOpml, 3, 0, 1, 1)
        self.ButtonToLyx = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToLyx.setObjectName("ButtonToLyx")
        #self.gridLayout.addWidget(self.ButtonToLyx, 6, 0, 1, 1)
        self.ButtonToLatex = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToLatex.setObjectName("ButtonToLatex")
        self.gridLayout.addWidget(self.ButtonToLatex, 5, 0, 1, 1)
        self.ButtonToEpub = QtWidgets.QRadioButton(self.layoutWidget1)
        self.ButtonToEpub.setCheckable(True)
        self.ButtonToEpub.setChecked(False)
        self.ButtonToEpub.setObjectName("ButtonToEpub")
        self.gridLayout.addWidget(self.ButtonToEpub, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.BoxToFormat, 0, 1, 4, 1)
        self.labelFromBox = QtWidgets.QLabel(self.centralwidget)
        self.labelFromBox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.labelFromBox.setObjectName("labelFromBox")
        self.gridLayout_2.addWidget(self.labelFromBox, 0, 2, 1, 2)
        self.FromParameter = QtWidgets.QLineEdit(self.centralwidget)
        self.FromParameter.setInputMask("")
        self.FromParameter.setText("")
        self.FromParameter.setClearButtonEnabled(True)
        self.FromParameter.setObjectName("FromParameter")
        self.gridLayout_2.addWidget(self.FromParameter, 0, 4, 1, 1)
        self.ButtonFromFormat = QtWidgets.QToolButton(self.centralwidget)
        self.ButtonFromFormat.setObjectName("ButtonFromFormat")
        self.gridLayout_2.addWidget(self.ButtonFromFormat, 0, 5, 1, 1)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ButtonBatch = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonBatch.setObjectName("ButtonBatch")
        self.verticalLayout_3.addWidget(self.ButtonBatch)
        self.ButtonRevert = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonRevert.setObjectName("ButtonRevert")
        self.verticalLayout_3.addWidget(self.ButtonRevert)
        self.ButtonConvert = QtWidgets.QPushButton(self.centralwidget)
        self.ButtonConvert.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ButtonConvert.setObjectName("ButtonConvert")
        self.verticalLayout_3.addWidget(self.ButtonConvert)
        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 6, 3, 1)
        self.labelToBox = QtWidgets.QLabel(self.centralwidget)
        self.labelToBox.setMaximumSize(QtCore.QSize(40, 16777215))
        self.labelToBox.setObjectName("labelToBox")
        self.gridLayout_2.addWidget(self.labelToBox, 1, 2, 1, 1)
        self.ToParameter = QtWidgets.QLineEdit(self.centralwidget)
        self.ToParameter.setText("")
        self.ToParameter.setClearButtonEnabled(True)
        self.ToParameter.setObjectName("ToParameter")
        self.gridLayout_2.addWidget(self.ToParameter, 1, 4, 1, 1)
        self.ButtonToFormat = QtWidgets.QToolButton(self.centralwidget)
        self.ButtonToFormat.setObjectName("ButtonToFormat")
        self.gridLayout_2.addWidget(self.ButtonToFormat, 1, 5, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 2, 2, 1, 2)
        self.ExtraParameter = QtWidgets.QLineEdit(self.centralwidget)
        self.ExtraParameter.setToolTip("")
        self.ExtraParameter.setText("")
        self.ExtraParameter.setClearButtonEnabled(True)
        self.ExtraParameter.setObjectName("ExtraParameter")
        self.gridLayout_2.addWidget(self.ExtraParameter, 2, 4, 1, 1)
        self.ButtonOptions = QtWidgets.QToolButton(self.centralwidget)
        self.ButtonOptions.setObjectName("ButtonOptions")
        self.gridLayout_2.addWidget(self.ButtonOptions, 2, 5, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.StandardConversion = QtWidgets.QCheckBox(self.centralwidget)
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
        self.horizontalLayout.addWidget(self.StandardConversion)
        self.BatchConversion = QtWidgets.QCheckBox(self.centralwidget)
        self.BatchConversion.setMinimumSize(QtCore.QSize(175, 0))
        self.BatchConversion.setObjectName("BatchConversion")
        self.horizontalLayout.addWidget(self.BatchConversion)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.MessageNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.MessageNumber.setToolTip("")
        self.MessageNumber.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.MessageNumber.setFrameShadow(QtWidgets.QFrame.Plain)
        self.MessageNumber.setObjectName("MessageNumber")
        self.horizontalLayout_2.addWidget(self.MessageNumber)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 3, 1, 4)
        self.editor_window = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.editor_window.setMinimumSize(QtCore.QSize(0, 120))
        self.editor_window.setBaseSize(QtCore.QSize(0, 266))
        self.editor_window.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.editor_window.setObjectName("editor_window")
        self.gridLayout_2.addWidget(self.editor_window, 4, 0, 1, 7)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        notepad.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(notepad)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 820, 24))
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
        notepad.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(notepad)
        self.statusbar.setObjectName("statusbar")
        notepad.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(notepad)
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QtCore.QSize(24, 24))
        self.toolBar.setObjectName("toolBar")
        notepad.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.dockLogWindow = QtWidgets.QDockWidget(notepad)
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
        notepad.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockLogWindow)
        self.actionSave = QtWidgets.QAction(notepad)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/save"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon)
        self.actionSave.setObjectName("actionSave")
        self.actionOpen = QtWidgets.QAction(notepad)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/open"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen.setIcon(icon1)
        self.actionOpen.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionOpen.setIconVisibleInMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave_AS = QtWidgets.QAction(notepad)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/save_as"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_AS.setIcon(icon2)
        self.actionSave_AS.setObjectName("actionSave_AS")
        self.actionNew = QtWidgets.QAction(notepad)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/new"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionNew.setIcon(icon3)
        self.actionNew.setObjectName("actionNew")
        self.actionMarkdown2Latex = QtWidgets.QAction(notepad)
        self.actionMarkdown2Latex.setObjectName("actionMarkdown2Latex")
        self.actionOpml2latex = QtWidgets.QAction(notepad)
        self.actionOpml2latex.setObjectName("actionOpml2latex")
        self.actionOpml2Markdown = QtWidgets.QAction(notepad)
        self.actionOpml2Markdown.setObjectName("actionOpml2Markdown")
        self.actionMarkdown2opml = QtWidgets.QAction(notepad)
        self.actionMarkdown2opml.setObjectName("actionMarkdown2opml")
        self.actionPreferences = QtWidgets.QAction(notepad)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/freferences"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon4.addPixmap(QtGui.QPixmap(":/icons/freferences"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionPreferences.setIcon(icon4)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actionLatex2Opml = QtWidgets.QAction(notepad)
        self.actionLatex2Opml.setObjectName("actionLatex2Opml")
        self.actionLatex2Markdown = QtWidgets.QAction(notepad)
        self.actionLatex2Markdown.setObjectName("actionLatex2Markdown")
        self.actionHtml2Markdown = QtWidgets.QAction(notepad)
        self.actionHtml2Markdown.setObjectName("actionHtml2Markdown")
        self.actionHtml2Latex = QtWidgets.QAction(notepad)
        self.actionHtml2Latex.setObjectName("actionHtml2Latex")
        self.actionHtml2opml = QtWidgets.QAction(notepad)
        self.actionHtml2opml.setObjectName("actionHtml2opml")
        self.actionOpml2html = QtWidgets.QAction(notepad)
        self.actionOpml2html.setObjectName("actionOpml2html")
        self.actionMarkdown2html = QtWidgets.QAction(notepad)
        self.actionMarkdown2html.setObjectName("actionMarkdown2html")
        self.actionLatex2html = QtWidgets.QAction(notepad)
        self.actionLatex2html.setObjectName("actionLatex2html")
        self.actionHelp = QtWidgets.QAction(notepad)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon5.addPixmap(QtGui.QPixmap(":/icons/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionHelp.setIcon(icon5)
        self.actionHelp.setObjectName("actionHelp")
        self.actionMarkdown2Lyx = QtWidgets.QAction(notepad)
        self.actionMarkdown2Lyx.setObjectName("actionMarkdown2Lyx")
        self.actionUndo = QtWidgets.QAction(notepad)
        self.actionUndo.setObjectName("actionUndo")
        self.actionAbout = QtWidgets.QAction(notepad)
        self.actionAbout.setObjectName("actionAbout")
        self.actionSearch = QtWidgets.QAction(notepad)
        self.actionSearch.setObjectName("actionSearch")
        self.actionLogViewer = QtWidgets.QAction(notepad)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/opml"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLogViewer.setIcon(icon6)
        self.actionLogViewer.setObjectName("actionLogViewer")
        self.actionAbove = QtWidgets.QAction(notepad)
        self.actionAbove.setObjectName("actionAbove")
        self.actionBelow = QtWidgets.QAction(notepad)
        self.actionBelow.setObjectName("actionBelow")
        self.actionLeft = QtWidgets.QAction(notepad)
        self.actionLeft.setObjectName("actionLeft")
        self.actionRight = QtWidgets.QAction(notepad)
        self.actionRight.setObjectName("actionRight")
        self.actionQuit = QtWidgets.QAction(notepad)
        self.actionQuit.setObjectName("actionQuit")
        self.actionOpen_URI = QtWidgets.QAction(notepad)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/open_uri.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_URI.setIcon(icon7)
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
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit_2.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuExtras.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addAction(self.actionSave_AS)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPreferences)
        self.toolBar.addAction(self.actionLogViewer)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionHelp)

        self.retranslateUi(notepad)
        QtCore.QMetaObject.connectSlotsByName(notepad)

    def retranslateUi(self, notepad):
        _translate = QtCore.QCoreApplication.translate
        notepad.setWindowTitle(_translate("notepad", "PanConvert"))
        self.BoxFromFormat.setTitle(_translate("notepad", "From Format"))
        self.ButtonFromMarkdown.setText(_translate("notepad", "Markdown"))
        self.ButtonFromOpml.setText(_translate("notepad", "Opml"))
        self.ButtonFromHtml.setText(_translate("notepad", "Html"))
        self.ButtonFromLatex.setText(_translate("notepad", "Latex"))
        self.BoxToFormat.setTitle(_translate("notepad", "To Format"))
        self.ButtonToHtml.setText(_translate("notepad", "Html"))
        self.ButtonToMarkdown.setText(_translate("notepad", "Epub"))
        self.ButtonToOpml.setText(_translate("notepad", "Opml"))
        #self.ButtonToLyx.setText(_translate("notepad", "Lyx"))
        self.ButtonToLatex.setText(_translate("notepad", "Latex"))
        self.ButtonToEpub.setText(_translate("notepad", "Markdown"))
        self.labelFromBox.setText(_translate("notepad", "From"))
        self.ButtonFromFormat.setText(_translate("notepad", "..."))
        self.ButtonBatch.setText(_translate("notepad", "Batch"))
        self.ButtonRevert.setText(_translate("notepad", "Revert"))
        self.ButtonConvert.setText(_translate("notepad", "Convert"))
        self.labelToBox.setText(_translate("notepad", "To"))
        self.ButtonToFormat.setText(_translate("notepad", "..."))
        self.label.setText(_translate("notepad", "Options"))
        self.ButtonOptions.setText(_translate("notepad", "..."))
        self.StandardConversion.setText(_translate("notepad", "Standard Conversion"))
        self.BatchConversion.setText(_translate("notepad", "Batch Conversion"))
        self.MessageNumber.setAccessibleName(_translate("notepad", "New Messages"))
        self.menuFile.setTitle(_translate("notepad", "File"))
        self.menuExtras.setTitle(_translate("notepad", "Help"))
        self.menuEdit_2.setTitle(_translate("notepad", "Edit"))
        self.menuWindow.setTitle(_translate("notepad", "Window"))
        self.toolBar.setWindowTitle(_translate("notepad", "toolBar"))
        self.actionSave.setText(_translate("notepad", "Save Buffer"))
        self.actionOpen.setText(_translate("notepad", "Open"))
        self.actionOpen.setShortcut(_translate("notepad", "Ctrl+O"))
        self.actionSave_AS.setText(_translate("notepad", "Save File"))
        self.actionSave_AS.setShortcut(_translate("notepad", "Ctrl+S"))
        self.actionNew.setText(_translate("notepad", "New"))
        self.actionNew.setToolTip(_translate("notepad", "New"))
        self.actionMarkdown2Latex.setText(_translate("notepad", "Markdown2Latex"))
        self.actionOpml2latex.setText(_translate("notepad", "opml2latex"))
        self.actionOpml2latex.setToolTip(_translate("notepad", "Opml2Latex"))
        self.actionOpml2Markdown.setText(_translate("notepad", "Opml2Markdown"))
        self.actionOpml2Markdown.setToolTip(_translate("notepad", "Opml2Markdown(Pandoc)"))
        self.actionMarkdown2opml.setText(_translate("notepad", "Markdown2opml"))
        self.actionPreferences.setText(_translate("notepad", "Preferences"))
        self.actionLatex2Opml.setText(_translate("notepad", "Latex2Opml"))
        self.actionLatex2Markdown.setText(_translate("notepad", "Latex2Markdown"))
        self.actionHtml2Markdown.setText(_translate("notepad", "Html2Markdown"))
        self.actionHtml2Latex.setText(_translate("notepad", "Html2Latex"))
        self.actionHtml2opml.setText(_translate("notepad", "html2opml"))
        self.actionOpml2html.setText(_translate("notepad", "opml2html"))
        self.actionMarkdown2html.setText(_translate("notepad", "markdown2html"))
        self.actionLatex2html.setText(_translate("notepad", "latex2html"))
        self.actionHelp.setText(_translate("notepad", "Help"))
        self.actionMarkdown2Lyx.setText(_translate("notepad", "Markdown2Lyx"))
        self.actionUndo.setText(_translate("notepad", "Undo"))
        self.actionAbout.setText(_translate("notepad", "About"))
        self.actionSearch.setText(_translate("notepad", "Search"))
        self.actionLogViewer.setText(_translate("notepad", "LogViewer"))
        self.actionAbove.setText(_translate("notepad", "Position Above"))
        self.actionBelow.setText(_translate("notepad", "Position Below"))
        self.actionLeft.setText(_translate("notepad", "Position Left"))
        self.actionRight.setText(_translate("notepad", "Position Right"))
        self.actionQuit.setText(_translate("notepad", "Quit"))
        self.actionOpen_URI.setText(_translate("notepad", "Open Uri"))
import source.gui.icons_rc
