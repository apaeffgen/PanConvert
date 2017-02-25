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

from helpers.interface_pandoc import get_pandoc_formats, get_path_pandoc
from source.gui.panconvert_diag_fromformat import Ui_From_Format_Dialog
from source.language.messages import *


class FromFormatDialog(QtWidgets.QDialog):

     def __init__(self, parent=None):

        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_From_Format_Dialog()
        self.ui.setupUi(self)
        #self.ui.ButtonInfo.clicked.connect(self.info)
        self.ui.ButtonCancel.clicked.connect(self.closeEvent)
        #self.ui.ButtonMoreInfo.clicked.connect(self.moreinfo)

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
            data = '<br>'.join(fromformats)
            self.ui.textBrowser.setContent(data)
        else:
                message = error_converter_path()
                return message

     def closeEvent(self, event):

        settings = QSettings('Pandoc', 'PanConvert')
        Dialog_Size = settings.value('Dialog_Size')
        if Dialog_Size is True or Dialog_Size == 'true':
            settings.setValue("FromFormat_size", self.size())
            settings.setValue("FromFormat_pos", self.pos())


        settings.sync()
        settings.status()
        FromFormatDialog.close(self)

     def info(self):
        formats =  get_pandoc_formats()
        fromformats = formats[0]
        data = '<br>'.join(fromformats)
        self.ui.textBrowser.setContent(data)

     def moreinfo(self):
        website = 'http://pandoc.org/README.html'
        self.ui.textBrowser.load(QtCore.QUrl(website))

     def back(self):
         back = 'href="javascript:history.go(-1)'
         self.ui.textBrowser.load(QtCore.QUrl(back))