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

test_file_1 = """
SAMPLE_TOKEN = Tok_SAMPLE
%%
main := SAMPLE_TOKEN
%%
"""

test_file_2 = """
%language C
%%
%%
"""

class TestParsegen():
    
	def test_parse_buffer(self):
		state = Grammar.parse_buffer(test_file_1)
		assert type(state) == Grammar
		
		assert getattr(state, "definitions", None) != None
		assert getattr(state, "options", None) != None
		assert getattr(state, "expansions", None) != None
		assert getattr(state, "code", None) != None
		
		assert type(state.definitions) == list
		assert type(state.options) == dict
		assert type(state.expansions) == list
		assert type(state.code) == str
		
		assert len(state.definitions) == 1
		assert len(state.options) == 0
		assert len(state.expansions) == 1
		assert state.code.strip() == ""
		
		state = Grammar.parse_buffer(test_file_2)
		assert type(state) == Grammar

		assert getattr(state, "definitions", None) != None
		assert getattr(state, "options", None) != None
		assert getattr(state, "expansions", None) != None
		assert getattr(state, "code", None) != None
		
		assert type(state.definitions) == list
		assert type(state.options) == dict
		assert type(state.expansions) == list
		assert type(state.code) == str
		
		assert len(state.definitions) == 0
		assert len(state.options) == 1
		assert len(state.expansions) == 0
		assert state.code.strip() == ""
	
		assert state.options["language"] == "C"
		