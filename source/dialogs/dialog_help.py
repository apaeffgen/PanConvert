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

from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtCore import QSettings
from PyQt6.QtCore import QPoint, QSize
from source.gui.panconvert_diag_help import Ui_Information_Dialog
from source.helpers.helper_functions import save_dialog_position
#from source.converter.interface_pandoc import get_pandoc_options

class HelpDialog(QtWidgets.QDialog):

     def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_Information_Dialog()
        self.ui.setupUi(self)
        self.ui.ButtonHelpPanconvert.clicked.connect(self.helpPanconvert)
        self.ui.ButtonCancel.clicked.connect(self._on_cancel)
        self.ui.ButtonHelpPandoc.clicked.connect(self.helpPandoc)
        self.ui.ButtonBackward.clicked.connect(self.back)
        self.ui.ButtonForward.clicked.connect(self.forward)


        website = 'https://panconvert.readthedocs.io'
        self.ui.textBrowser.load(QtCore.QUrl(website))

        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')

        self.resize(settings.value("Help_size", QSize(270, 225)))
        # Position restored in showEvent, NOT here

     def showEvent(self, event):
        """Restore position when dialog is shown (fixed timing)."""
        super().showEvent(event)
        
        settings = QSettings('Pandoc', 'PanConvert')
        pos = settings.value("Help_pos", None)
        
        if pos:
            self.move(pos)

     def _on_cancel(self):
        """Handle Cancel button click."""
        save_dialog_position(self, "Help_size", "Help_pos")
        self.close()

     def closeEvent(self, event):
        save_dialog_position(self, "Help_size", "Help_pos")
        event.accept()

     def helpPanconvert(self):

        website = 'https://panconvert.readthedocs.io'
        self.ui.textBrowser.load(QtCore.QUrl(website))

     def helpPandoc(self):

        website = 'https://pandoc.org/MANUAL.html'
        self.ui.textBrowser.load(QtCore.QUrl(website))

     def back(self):
         page = self.ui.textBrowser.page()
         history = page.history()
         history.back()


     def forward(self):
         page = self.ui.textBrowser.page()
         history = page.history()
         history.forward()
