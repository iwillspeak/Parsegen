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
	
	def test_errors(self):
		e_str = "dummy string"
		
		e = ParseError(e_str)
		assert str(e).startswith('parsegen:')
		assert 'parse error' in str(e)
		assert e_str in str(e)
		
		e = GrammarError(e_str)
		assert str(e).startswith('parsegen:')
		assert 'grammar error' in str(e)
		assert e_str in str(e)

	
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
		BAR = Tok_BAR
		%%
		main := baz bar_prime
		bar  := FOO BAR
		bar_prime := bar bar_prime
		bar_prime := 
		baz := bar_prime
		%%
		// this is a comment
		"""
		)
		
		assert len(exps) == 4
		assert len(exps['main']) == 1
		assert len(exps['bar']) == 1
		assert len(exps['bar_prime']) == 2
		assert len(exps['baz']) == 1
		
		main = exps['main']
		bar = exps['bar']
		bar_prime = exps['bar_prime']
		baz = exps['baz']
		
		assert not main.is_nullable()
		assert not bar.is_nullable()
		assert bar_prime.is_nullable()
		assert baz.is_nullable()
	
	def test_invalid_expansions(self):
		
		assert_raises(
			GrammarError, lambda: parse_buffer(" %% main := TOKEN %% "))
		assert_raises(
			GrammarError, lambda: parse_buffer(" %% main := fdass %% "))
		assert_raises(
			GrammarError, lambda: parse_buffer(
				"TOKEN %% TOKEN := invalid \n invalid := %% "))

class TestHeader(object):
	"""Test Header
	
	Test the Header object. This is responsible for representing the options
	and the terminals used for the grammar. Options can be accessed with the
	`get_option` method to allow accessing options with a default value.
	"""
	
	def test_create(self):
		
		h = Header({}, {})
		assert h != None
		assert len(h.options) == 0
		assert len(h.terminals) == 0
		
		h = Header({'TERM': 'definition'}, {'option': 'value'})
		assert h != None
		assert len(h.options) == 1
		assert h.options['option'] == 'value'
		
		assert len(h.terminals) == 1
		assert h.terminals['TERM'] == 'definition'
		
	def test_get_option(self):
		
		h = Header({'TERM': 'definition'}, {'option': 'value'})
		
		assert hasattr(h, 'get_option')
		
		assert h.get_option('option') == 'value'
		assert h.get_option('option', 'default') == 'value'
		assert h.get_option('notinhahs') == ''
		assert h.get_option('notinhash', 'default') == 'default'

class TestSymbol(object):
	"""Test Symbol
	
	Test the Symbol object. This is responsible for representing a given
	symbol and all of it's expansions. It is responsible for holding information
	about the nullability of the symbol and the first and follow sets of the 
	symbol.
	"""
	
	def test_create(self):
		s = Symbol()
		
		assert s != None
		
		assert_raises(TypeError, lambda: Symbol("some test string"))
		
		assert hasattr(s, "expansions")

		
	def test_add_expansion(self):
		
		s = Symbol()
		
		assert len(s.expansions) == 0
		
		s.add_expansion(["this", "is", "an", "expansion"])
		
		assert len(s.expansions) == 1
		
		s.add_expansion(["shorter", "expansion"])
		
		assert len(s.expansions) == 2
		
		s.add_expansion([])
		
		assert len(s.expansions) == 3
		
		assert len(s.expansions) == len(s)

	def test_nullable(self):
		
		s = Symbol()
		
		assert s.is_nullable()
		
		s.add_expansion(["not", "nullable"])
		
		assert not s.is_nullable()
		
		s.add_expansion([])
		
		assert s.is_nullable()
		
	def test_first_set(self):
		
		s = Symbol()
		
		assert s.first == set()
		
		s.add_first({'foo', 'bar'})
		
		assert s.first == {'foo', 'bar'}
		
		s.add_first(['bar', 'baz'])
		
		assert s.first == {'foo', 'bar', 'baz'}
		
	def test_follow_set(self):
		
		s = Symbol()
		
		assert s.follow == set()
		
		s.add_follow({'foo', 'bar'})
		
		assert s.follow == {'foo', 'bar'}
		
		s.add_follow(['bar', 'baz'])
		
		assert s.follow == {'foo', 'bar', 'baz'}
		
		