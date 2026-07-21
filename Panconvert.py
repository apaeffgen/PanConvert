#!/usr/bin/env python3
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

import sys
import os
from PyQt6 import QtWidgets
from PyQt6.QtCore import QSettings
from source.main_gui import StartQT5, get_path_pandoc
from source.language import load_language, get_available_languages


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Load saved language setting
    settings = QSettings('Pandoc', 'PanConvert')
    actual_language = settings.value('default_language', 'en')

    # Install the translator
    load_language(app, actual_language)

    myapp = StartQT5()
    myapp.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # Check for pandoc path on first run
    settings = QSettings('Pandoc', 'PanConvert')
    path_pandoc = settings.value('path_pandoc', '')

    if not os.path.isfile(str(path_pandoc)):
        get_path_pandoc()

    main()
