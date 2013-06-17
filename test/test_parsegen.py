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

# Module to test
from parsegen import *

class TestParsegen(object):
	"""Test Parsegen
	
	Tests the `parsegen` module.
	"""
	
	def test_parse_buffer(self):
		
		res = parse_buffer(" %% %% ")
		assert res != None
		assert res[2] == " "
		
		h, e, c = parse_buffer(
		"""
		TOKEN = Tok_TOKEN
		FUZZBAZ
		%language = c
		%lexer_entry = Lex_getNextToken();
		%%
		# empty grammar section
		%%
		user_code and stuff
		"""
		)
		
		assert type(h) == Header
		assert type(c) == str
		assert type(e) == dict
		
		assert h.options["language"] == "c"
		assert h.options["lexer_entry"] == "Lex_getNextToken();"
		
		assert h.terminals['TOKEN'] == 'Tok_TOKEN'
		assert 'TOKEN' in h.terminals
		assert 'FUZZBAZ' in h.terminals
		
		assert len(e) == 0
		
		assert c == "\n\t\tuser_code and stuff\n\t\t"

	def test_parse_buffer_errors(self):
		
		assert_raises(ParseError, lambda: parse_buffer(" %% %% %% "))
		assert_raises(ParseError, lambda: parse_buffer(" %% "))
	
	def test_expansion_creation(self):
		_, exps, _ = parse_buffer(
		"""
		%language = c
		FOO = Tok_FOO
		BAZ = Tok_BAZ
		%%
		main := bar bar_prime
		bar  := FOO BAR
		bar_prime := bar bar_prime
		bar_prime := 
		%%
		// this is a comment
		"""
		)
		
		assert len(exps) == 3
		assert len(exps['main']) == 1
		assert len(exps['bar']) == 1
		assert len(exps['bar_prime']) == 2
	
