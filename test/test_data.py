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
		