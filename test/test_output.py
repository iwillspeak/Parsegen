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

# Test helpers
from nose.tools import *
import sys

# Module to test
from parsegen.utils import Struct
from parsegen.parse import parse_buffer
from parsegen.output import *

class TestOutput(object):
	"""Test Output
	
	Test the `output` submodule.
	"""
	
	def test_write_grammar(self):
		g = parse_buffer("""
		
		WORLD
		
		%prefix = yy
		%lexer_function = Lex_getNextToken()
		%token_type = Lex_Token
		
		%%
		
		main := hello main
		main := 
		
		hello := WORLD
		
		%%
		
		hello world
		
		""")
		
		write_grammar(g, sys.stdout, language="pretty_print")
		write_grammar(g, sys.stdout, language="c")
		
	def test_options(self):

		g = parse_buffer("""
		
		WORLD
		
		%language = C
		%prefix = yy
		%lexer_function = Lex_getNextToken()
		%token_type = Lex_Token
		
		%%
		
		main := hello
		
		hello := WORLD
		
		%%
		
		hello world
		
		""")
		
		ctx = OutputFormatter(g, {"prefix": "bar_"})
		
		opts = {
			"prefix": "bar_",
			"lexer_function": "Lex_getNextToken()",
			"token_type": "Lex_Token",
			"node_type": "bar_node_t*",
			"token_type_access": '',
			"lexer_include": "lexer.h"
		}
		
		assert ctx.options == Struct(opts)
