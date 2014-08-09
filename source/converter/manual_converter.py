__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_
from source.converter.interface_pandoc import convert


def convert_universal(text,ToFormat,FromFormat,arg):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(text, ToFormat, FromFormat, arg)

    return output

def convert_binary(openfile,ToFormat,FromFormat,arg):
    # ReturnValues: OpenedText, ToFormat, FromFormat, ExtraArguments (divided by blanks, if empty, use '')
    # output = convert('/Users/apaeffgen/Downloads/test.md', 'latex') # For debugging purpose only

    output = convert(openfile, ToFormat, FromFormat, arg)

    return output

