#!/usr/local/bin/python3
__author__ = 'apaeffgen'
# -*- coding: utf-8 -*-

    # This file is part of Panconvert.
    #
    # Panconvert is free software: you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.
    #
    # Panconvert is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with Panconvert.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from PyQt5.QtCore import QPoint, QSize
from source.gui.panconvert_diag_help import Ui_Information_Dialog
#from source.converter.interface_pandoc import get_pandoc_options

class HelpDialog(QtWidgets.QDialog):

     def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Information_Dialog()
        self.ui.setupUi(self)
        self.ui.ButtonHelpPanconvert.clicked.connect(self.helpPanconvert)
        self.ui.ButtonCancel.clicked.connect(self.closeEvent)
        self.ui.ButtonHelpPandoc.clicked.connect(self.helpPandoc)
        self.ui.ButtonBackward.clicked.connect(self.back)
        self.ui.ButtonForward.clicked.connect(self.forward)

        website = 'http://panconvert.readthedocs.io'
        self.ui.textBrowser.load(QtCore.QUrl(website))

        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')

        self.resize(settings.value("Help_size", QSize(270, 225)))
        self.move(settings.value("Help_pos", QPoint(50, 50)))

     def closeEvent(self, event):

        settings = QSettings('Pandoc', 'PanConvert')
        Dialog_Size = settings.value('Dialog_Size')
        if Dialog_Size is True or Dialog_Size == 'true':
            settings.setValue("Help_size", self.size())
            settings.setValue("Help_pos", self.pos())


        settings.sync()
        settings.status()

        HelpDialog.close(self)

     def helpPanconvert(self):
        website = 'http://panconvert.readthedocs.io'
        self.ui.textBrowser.load(QtCore.QUrl(website))

     def helpPandoc(self):
        website = 'http://pandoc.org/README.html'
        self.ui.textBrowser.load(QtCore.QUrl(website))

     def back(self):
         page = self.ui.textBrowser.page()
         history = page.history()
         history.back()


     def forward(self):
         page = self.ui.textBrowser.page()
         history = page.history()
         history.forward()
