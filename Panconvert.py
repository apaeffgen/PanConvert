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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtCore import QT_VERSION_STR
from source.main_gui import *
import sys

def main():

    app = QtWidgets.QApplication(sys.argv)
    app.installTranslator(_translate)
    myapp = StartQT5()
    myapp.show ()
    sys.exit (app.exec_ () )


if __name__ == '__main__':
    import sys
    global actualLanguage

    settings = QSettings('Pandoc', 'PanConvert')
    actualLanguage = settings.value('default_language')


    _translate = QtCore.QTranslator()
    script_dir = os.path.dirname(sys.argv[0])

    if actualLanguage == 'Deutsch':
        german_language = script_dir + "/Panconvert_de.qm"
        if os.path.isfile(german_language):
            _translate.load(german_language)
        else:
            _translate.load(script_dir + "/source/language/Panconvert_de.qm")

    elif actualLanguage == 'Español':
        spanish_language = script_dir + "/Panconvert_es.qm"
        if os.path.isfile(spanish_language):
            _translate.load(spanish_language)
        else:
            _translate.load(script_dir + "source/language/Panconvert_es.qm")

    if not os.path.isfile(path_pandoc):
        get_path_pandoc()

    main()
