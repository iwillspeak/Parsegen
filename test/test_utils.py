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
from parsegen.utils import *

class TestNamespace(object):
	"""Test Namespace
	
	Tests the Namespacing object. This object is responsible for allowing easier
	read_access to a dict.
	"""
	
	def test_create(self):
		
		n = Namespace({})
		assert n != None
		
		n = Namespace({"foo": "bar"})
		assert n != None
		assert n.foo == "bar"
	
	def test_invalid(self):
		
		assert_raises(TypeError, lambda : Namespace())
	
	def test_dict_access(self):
		
		d = {"foo": 14, "bar": 1243, "baz": "dsaf"}
		
		n = Namespace(d)
		
		for k, v in d.items():
			assert getattr(n, k) == v
	
	def test_compare(self):
		d = {"hello": "2134", "world": "rasdfa"}
		
		n1 = Namespace(d)
		n2 = Namespace(d)
		n3 = Namespace({})
	
		assert n1 == n2
		assert not n1 != n2
		assert n2 != n3
		assert not n1 == n3
	
	def test_contains(self):
		
		n = Namespace({"foo": "", "bar": "string"})
		
		assert "foo" in n
		assert "bar" in n
		assert not "baz" in n