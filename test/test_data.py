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
from parsegen.data import *
from parsegen.errors import *

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
	
	def setup(self):
		self.sym = Symbol("foo")
	
	def test_create(self):
		
		assert self.sym != None
		
		assert_raises(SymbolNameError, lambda: Symbol("some test string"))
		assert_raises(SymbolNameError, lambda: Symbol("hello\tworld"))
		
		assert hasattr(self.sym, "expansions")
		assert self.sym.name == "foo"
		assert Symbol("foo-bar").name == "foo-bar"
		assert Symbol("hello_world").name == 'hello_world'
		
		assert Symbol("    whitespace_before").name == "whitespace_before"
		assert Symbol("whitespace_after\t\t").name == "whitespace_after"

		
	def test_add_expansion(self):
		
		assert len(self.sym.expansions) == 0
		
		self.sym.add_expansion(["this", "is", "an", "expansion"])
		
		assert len(self.sym.expansions) == 1
		
		self.sym.add_expansion(["shorter", "expansion"])
		
		assert len(self.sym.expansions) == 2
		
		self.sym.add_expansion([])
		
		assert len(self.sym.expansions) == 3

	def test_nullable(self):
		
		assert self.sym.is_nullable()
		
		self.sym.add_expansion(["not", "nullable"])
		
		assert not self.sym.is_nullable()
		
		self.sym.add_expansion([])
		
		assert self.sym.is_nullable()
		
	def test_first_set(self):
		
		assert self.sym.first == set()
		
		self.sym.add_first({'foo', 'bar'})
		
		assert self.sym.first == {'foo', 'bar'}
		
		self.sym.add_first(['bar', 'baz'])
		
		assert self.sym.first == {'foo', 'bar', 'baz'}
		
	def test_follow_set(self):
		
		assert self.sym.follow == set()
		
		self.sym.add_follow({'foo', 'bar'})
		
		assert self.sym.follow == {'foo', 'bar'}
		
		self.sym.add_follow(['bar', 'baz'])
		
		assert self.sym.follow == {'foo', 'bar', 'baz'}
