__author__ = 'apaeffgen'
# _*_ coding: utf-8 _*_

import codecs
import sys
from source.converter.markdown import convert_opml2markdown

INPUT = sys.argv[1]
OUTPUT = '.'.join(INPUT.split('.')[:-1] + ['md'])


with codecs.open(INPUT, 'r') as f:
    text = f.read()

output_content = convert_opml2markdown(text)

with codecs.open(OUTPUT, 'w', 'utf-8') as f:
    f.write(output_content)
