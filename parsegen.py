#! /usr/bin/env python3

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

##
# Grammar - Parses and represents grammar files

class Grammar():
	
	def __init__(self, definitions, options, expansions, code):
		self.definitions = definitions
		self.options = options
		self.expansions = expansions
		self.code = code
		
	def __repr__(self):
		return "{0}, {1}, {2}, {3}".format(self.definitions, self.options, self.expansions, self.code)

	@classmethod
	def parse_buffer(klass, buff):
		buff = buff.split("%%")
		
		blen = len(buff)
		if blen != 3:
			raise ParseError("Expecting 3 sections but found {0}".format(blen))
			
		defs = []
		opts = {}
		for l in buff[0].split("\n"):
			if l.startswith("%"):
				option, _, value = l[1:].partition(" ")
				option.strip()
				value.strip()
				opts[option] = value.strip()
			elif len(l):
				defs.append(l)	
		
		exps = []
		for e in buff[1].split('\n'):
			if len(e):
				exps.append(e)
		return klass(defs, opts, exps, buff[2])
		

class ParseError(Exception):
	pass