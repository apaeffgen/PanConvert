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

from source.gui.panconvert_diag_openuri import Ui_DialogOpenURI
from source.language.messages import *
from source.main_gui import *
from source.helpers.helper_functions import save_dialog_position
import builtins
import codecs
from os.path import isfile



class OpenURIDialog(QtWidgets.QDialog):
    global uri

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_DialogOpenURI()
        self.ui.setupUi(self)
        self.ui.ButtonOpenURI.clicked.connect(self.openuri)
        self.ui.ButtonCancel.clicked.connect(self._on_cancel)
        self.ui.CheckBoxStayOnTop.stateChanged.connect(self.stayOnTop)

        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')

        self.resize(settings.value("OpenURI_size", QSize(270, 225)))
        # Position restored in showEvent, NOT here
        uri = ''


    def showEvent(self, event):
        """Restore position when dialog is shown (fixed timing)."""
        super().showEvent(event)
        
        settings = QSettings('Pandoc', 'PanConvert')
        pos = settings.value("OpenURI_pos", None)
        
        if pos:
            self.move(pos)

    def stayOnTop(self):
        if self.ui.CheckBoxStayOnTop.isChecked():
            self.setWindowFlags(
                self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(
                self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def _on_cancel(self):
        """Handle Cancel button click."""
        save_dialog_position(self, "OpenURI_size", "OpenURI_pos")
        self.close()

    def closeEvent(self, event):
        save_dialog_position(self, "OpenURI_size", "OpenURI_pos")
        OpenURIDialog.close(self)

    def openuri(self):
        uri = self.ui.URI.toPlainText()
        builtins.uri = uri

        # Save position and size BEFORE closing
        save_dialog_position(self, "OpenURI_size", "OpenURI_pos")

        OpenURIDialog.close(self)