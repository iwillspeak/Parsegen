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

from parsegen.errors import ParseError
from parsegen.data import Header, Symbol
from parsegen.grammar import Grammar

def parse_buffer(buffer):
	"""Parse Buffer
	
	Parse the given buffer and return a 3-tuple of the contents. The first
	element of the tuple is a Header object representing the definitions
	and options used, the second is a list of expansions and the third is a
	string containing the contents of the user code section.
	"""
	
	try:
		sects = buffer.split("%%")
		header, expansions, user_code = sects
	except ValueError:
		raise ParseError("expected 3 sections but found {0}".format(len(sects)))
		
	# process the header section, to extract the options and stuff
	header = _process_header(header)
	
	# now we can process the expansions
	expansions = _process_expansions(expansions)
	
	# Return the processed parts
	return Grammar(header, expansions, user_code)

def parse_file(file):
	"""Parse File
	
	Reads the contents of the file and parses the contents. Returns the same
	as `parse_buffer`.
	"""
	
	try:
		return parse_buffer(file.read())
	except AttributeError:
		pass
	
	with open(file, "r") as file:
		return parse_buffer(file.read())

def _processed_lines(text):
	"""Processed Lines
	
	Returns an iterable containing all non-empty lines within the text with
	comments removed.
	"""
	
	for l in text.split("\n"):
		l, _, _ = l.partition("#")
		l = l.strip()
		if len(l):
			yield l

def parse_option(opt_line):
	"""Parse Option

	Allows other parts of the program to use the option parsing in this file. If
	the code is updated it should make things simpler if this is used to process
	options.
	"""

	return _kv_with_sep(opt_line, "=")

def _kv_with_sep(opt_line, sep="="):
	"""Key Value Pair
	
	Extracts a key-value pair from the `opt_line` using the separator, if given.
	"""
	
	key, _, val = opt_line.partition(sep)
	
	return key.strip(), val.strip()

def _add_opt_to_dict(opt_line, dict, sep="=", mirror_empty=False):
	"""Add Option to Dictionary
	
	Extracts a `key = value` pair from the `opt_line` and adds the pair to the
	`dict`, uaing the optional separator `sep` to separate them.
	"""
	
	key, val = _kv_with_sep(opt_line, sep)
	
	if mirror_empty and not val:
		val = key
	
	dict[key] = val

def _process_header(header):
	"""Process Header
	
	Process the header section, splits the header definitions into two `dict`s
	so that they can be looked up later.
	"""
	
	terms = {}
	opts = {}
	
	for l in _processed_lines(header):
		if l[:1] == "%":
			_add_opt_to_dict(l[1:], opts)
		else:
			_add_opt_to_dict(l, terms, mirror_empty=True)
	
	return Header(terms, opts)

def _process_expansions(expansions):
	"""Process Expansions
	
	Processes a block of text containing grammar expansions into a `dict`
	containing mappings from symbol names to Symbol objects.
	"""
	
	exps = {}
	
	for l in _processed_lines(expansions):
		sym, exp = _kv_with_sep(l, ":=")
		
		s = exps.get(sym, Symbol(sym))
		s.add_expansion(exp.split())
		exps[sym] = s
		
	return exps
