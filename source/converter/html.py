__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_
from source.converter.interface_pandoc import convert


def convert_md2html(text):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(text, 'html', 'md', '--standalone')

    return output


def convert_opml2html(text):

    output = convert(text, 'html', 'opml', '--standalone')

    return output


def convert_latex2html(text):

    output = convert(text, 'html', 'latex', '--standalone')

    return output