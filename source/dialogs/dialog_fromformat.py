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

from source.helpers.interface_pandoc import get_pandoc_formats, get_path_pandoc
from source.gui.panconvert_diag_fromformat import Ui_From_Format_Dialog
from source.language.messages import *
from PyQt6.QtWidgets import QMessageBox, QListWidgetItem
from PyQt6.QtCore import QSettings, QSize, QPoint
import os


class FromFormatDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_From_Format_Dialog()
        self.ui.setupUi(self)
        
        # Store formats for filtering
        self.all_formats = []
        self.filtered_formats = []
        
        # Connect signals
        self.ui.formatList.itemClicked.connect(self._on_format_selected)
        self.ui.ButtonCancel.clicked.connect(self.closeEvent)
        self.ui.searchInput.textChanged.connect(self._on_search_text_changed)
        self.ui.searchClearButton.clicked.connect(self._on_clear_search)

        #Initialize Settings
        settings = QSettings('Pandoc', 'PanConvert')
        path_pandoc = settings.value('path_pandoc','')

        self.resize(settings.value("FromFormat_size", QSize(270, 225)))
        self.move(settings.value("FromFormat_pos", QPoint(50, 50)))

        if not os.path.isfile(path_pandoc):
            path_pandoc = get_path_pandoc()
            path_pandoc = settings.value('path_pandoc')

        if os.path.isfile(path_pandoc):
            formats =  get_pandoc_formats()
            fromformats = formats[0]
            
            # Store and populate formats
            self._populate_formats(fromformats)
        else:
            message = error_converter_path()
            QMessageBox.critical(self, 'Pandoc nicht gefunden', message)

    def _populate_formats(self, formats):
        """Populate list with all formats, store for filtering."""
        self.all_formats = list(formats)
        self.filtered_formats = list(formats)
        self._render_list()

    def _render_list(self):
        """Clear and repaint the format list with current filtered_formats."""
        self.ui.formatList.clear()
        for fmt in self.filtered_formats:
            item = QListWidgetItem(fmt)
            self.ui.formatList.addItem(item)

    def _on_search_text_changed(self, text):
        """Filter formats based on search text."""
        search_lower = text.lower()
        if not search_lower:
            self.filtered_formats = list(self.all_formats)
        else:
            self.filtered_formats = [
                fmt for fmt in self.all_formats 
                if search_lower in fmt.lower()
            ]
        self._render_list()
        
        # Auto-select first item if only one match
        if len(self.filtered_formats) == 1:
            self.ui.formatList.setCurrentRow(0)

    def _on_clear_search(self):
        """Clear search field and show all formats."""
        self.ui.searchInput.clear()

    def _on_format_selected(self, item):
        """Called when a format item is clicked."""
        format_name = item.text()
        # Store selected format and close dialog
        settings = QSettings('Pandoc', 'PanConvert')
        settings.setValue('selected_from_format', format_name)
        settings.sync()
        self.accept()

    def get_selected_format(self):
        """Return the selected format."""
        settings = QSettings('Pandoc', 'PanConvert')
        return settings.value('selected_from_format', '')

    def closeEvent(self, event):

        settings = QSettings('Pandoc', 'PanConvert')
        Dialog_Size = settings.value('Dialog_Size')
        if Dialog_Size is True or Dialog_Size == 'true':
            settings.setValue("FromFormat_size", self.size())
            settings.setValue("FromFormat_pos", self.pos())


        settings.sync()
        FromFormatDialog.close(self)