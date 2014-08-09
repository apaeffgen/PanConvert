__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_
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

