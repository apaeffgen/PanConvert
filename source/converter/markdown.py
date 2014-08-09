__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_

from source.converter.interface_pandoc import convert


def convert_latex2markdown(text):
    output = convert(text, 'md', 'latex', '--atx-headers')

    return output


def convert_opml2markdown(text):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(text, 'md', 'opml', '--atx-headers')

    return output


def convert_html2markdown(text):

    output = convert(text, 'md', 'html', '--atx-headers')

    return output


