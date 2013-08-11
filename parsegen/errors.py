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

class ParsegenError(Exception):
	"""Parsegen Error
	
	Root class for all exceptions in this module
	"""
	
	def __init__(self, error_name, string):
		string = "parsegen: {0}: {1}".format(error_name, string)
		Exception.__init__(self, string)
	
class ParseError(ParsegenError):
	"""Parse Error
	
	Represents a failure to parse a grammar file. The reason for the failure is
	provided as a string.
	"""
	
	def __init__(self, string):
		"""ParseError Constructor
		
		Create a new parse error from a string. The string is automatically
		formatted for pretty printing in context with other errors.
		"""
		
		ParsegenError.__init__(self, 'parse error', string)

class GrammarError(ParsegenError):
	"""Grammar Error
	
	Represent a logical error in one of the grammar expansions. The reason for
	the failure is provided as a string.
	"""
	
	def __init__(self, string):
		"""GrammarError Constructor
		
		Create a new grammar error from a string. The string is automatically
		formatted.
		"""
		
		ParsegenError.__init__(self, 'grammar error', string)

class SymbolNameError(ParsegenError):
	"""Symbol Name Error
	
	Represents an invalid token or symbol name.
	"""
	
	def __init__(self, name):
		"""SymbolNameError Constructor
		
		Takes the string that represents the invalid name and constructs an
		error string from it.
		"""
		
		err = "invalid token or symbol name %s" % name
		ParsegenError.__init__(self, "name error", err)
