__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_
from source.converter.interface_pandoc import convert


def convert_markdown2opml(text):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks)
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(text, 'opml', 'md', '--standalone')

    return output


def convert_latex2opml(text):

    output = convert(text, 'opml', 'latex', '--standalone')

    return output


def convert_html2opml(text):

    output = convert(text, 'opml', 'html', '--standalone')

    return output