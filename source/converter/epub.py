__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_
from source.converter.interface_pandoc import convert


def convert_md2epub(text):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(text, 'epub', 'md', '-o test.epub')

    return output
