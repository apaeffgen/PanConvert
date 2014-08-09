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

from source.converter.interface_pandoc import convert


def convert_md2latex(text):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(text, 'latex', 'md', '--standalone')

    return output


def convert_opml2latex(text):

    output = convert(text, 'latex', 'opml', '--standalone')

    return output


def convert_html2latex(text):

    output = convert(text, 'latex', 'html', '--standalone')

    return output

