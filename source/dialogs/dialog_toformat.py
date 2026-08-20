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

from source.helpers.interface_pandoc import get_pandoc_formats
from source.gui.panconvert_diag_toformat import Ui_To_Format_Dialog
from source.language.messages import *
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QSettings, QSize, QPoint
import os


class ToFormatDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_To_Format_Dialog()
        self.ui.setupUi(self)
        
        # Connect list selection signal
        self.ui.formatList.itemClicked.connect(self._on_format_selected)
        self.ui.ButtonCancel.clicked.connect(self.closeEvent)

        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')

        self.resize(settings.value("ToFormat_size", QSize(270, 225)))
        self.move(settings.value("ToFormat_pos", QPoint(50, 50)))

        if os.path.isfile(path_pandoc):
            formats =  get_pandoc_formats()
            toformats = formats[1]
            
            # Populate QListWidget with format items
            for fmt in toformats:
                item = QListWidgetItem(fmt)
                self.ui.formatList.addItem(item)
        else:
            message = error_converter_path()
            self.ui.formatList.addItem(message)

    def _on_format_selected(self, item):
        """Called when a format item is clicked."""
        format_name = item.text()
        # Store selected format and close dialog
        settings = QSettings('Pandoc', 'PanConvert')
        settings.setValue('selected_to_format', format_name)
        settings.sync()
        self.accept()

    def get_selected_format(self):
        """Return the selected format."""
        settings = QSettings('Pandoc', 'PanConvert')
        return settings.value('selected_to_format', '')

    def closeEvent(self, event):

        settings = QSettings('Pandoc', 'PanConvert')
        Dialog_Size = settings.value('Dialog_Size')
        if Dialog_Size is True or Dialog_Size == 'true':
            settings.setValue("ToFormat_size", self.size())
            settings.setValue("ToFormat_pos", self.pos())


        settings.sync()
        ToFormatDialog.close(self)