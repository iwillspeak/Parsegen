# This file is part of Parsegen and is licensed as follows:
#
# Copyright (c) 2012 Will Speak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import sys
import argparse

from parsegen.utils import Struct
from parsegen.version import VERSION
import parsegen.parse

def parse(args):

    # Using argparse to get all the options, not that there are many
    parser = argparse.ArgumentParser(description="LL(1) parser generator")
    parser.add_argument('-o', '--output',
                        help="File to write the generated grammar to.",
                        type=argparse.FileType('w'),
                        metavar='FILE',
                        default=sys.stdout)
    parser.add_argument('-l', '--language',
                        help="The language to use to generate the parser.")
    parser.add_argument('file',
                        help="Input grammar file",
                        type=argparse.FileType('r'))
    parser.add_argument('options',
                        help="option=value pairs to override values " \
                        "specified in the grammar",
                        nargs="*")
    parser.add_argument('--version', action='version',
                        help="Print out the version information",
                        version="Parsegen version {0}".format(VERSION))
    
    options = parser.parse_args(args)

    options_dict = {}
    for opt in options.options:
        opt, val = parsegen.parse.parse_option(opt)
        options_dict[opt] = val

    return Struct(output_file=options.output, input_file=options.file,
                  options=options_dict, language=options.language)
