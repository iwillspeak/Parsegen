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
from parsegen.errors import *
from parsegen.parse import *

class TestParse(object):
	"""Test Parse
	
	Tests the `parse` submodule.
	"""
	
	def test_parse_buffer(self):
		
		res = parse_buffer(" %% %% ")
		assert res != None
		assert res.user_code == " "
		assert len(res.expansions) == 0
		
		g = parse_buffer(
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
		
		assert type(g.header) == Header
		assert type(g.user_code) == str
		assert type(g.expansions) == dict
		
		h = g.header
		c = g.user_code
		e = g.expansions
		
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
	
	def test_token_extraction(self):
		h = parse_buffer("""
		TOKEN = Token_value
		TOKEN1234 = second_token_value
		AUTOCOPY
		%%
		%%
		""").header
		
		assert h.terminals['TOKEN'] == 'Token_value'
		assert h.terminals['TOKEN1234'] == 'second_token_value'
		assert h.terminals['AUTOCOPY'] == 'AUTOCOPY'
	
	def test_expansion_creation(self):
		exps = parse_buffer(
		"""
		%language = c
		FOO = Tok_FOO
		BAZ = Tok_BAZ
		BAR = Tok_BAR
		%%
		main := baz bar_prime BAZ
		bar  := FOO BAR
		bar_prime := bar bar_prime
		bar_prime := 
		baz := bar_prime
		baz := BAZ
		%%
		// this is a comment
		"""
		).expansions
		
		assert len(exps) == 4
		assert len(exps['main'].expansions) == 1
		assert len(exps['bar'].expansions) == 1
		assert len(exps['bar_prime'].expansions) == 2
		assert len(exps['baz'].expansions) == 2
		
		main = exps['main']
		bar = exps['bar']
		bar_prime = exps['bar_prime']
		baz = exps['baz']
		
		# Check the nullability
		assert not main.is_nullable()
		assert not bar.is_nullable()
		assert bar_prime.is_nullable()
		assert baz.is_nullable()
		
		# Check the first sets
		print(main.first, bar.first, bar_prime.first, baz.first)
		assert main.first == {'FOO', 'BAZ'}
		assert bar.first == {'FOO'}
		assert bar_prime.first == {'FOO'}
		assert baz.first == {'BAZ', 'FOO'}
		
		# Check the follow sets
		print(main.follow, bar.follow, bar_prime.follow, baz.follow)
		assert main.follow == set()
	
	def test_invalid_expansions(self):
		
		assert_raises(
			GrammarError, lambda: parse_buffer(" %% main := TOKEN %% "))
		assert_raises(
			GrammarError, lambda: parse_buffer(" %% main := fdass %% "))
		assert_raises(
			GrammarError, lambda: parse_buffer(
				"TOKEN %% TOKEN := invalid \n invalid := %% "))
