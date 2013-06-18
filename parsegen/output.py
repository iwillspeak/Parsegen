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

import sys

def write_grammar(header, expansions, user_code, file=sys.stdout):
	"""Write Grammar
	
	Write a program out to the file that represents an automaton that parses
	the given grammar.
	"""
	
	_write_header_to_file(header, file)
	_write_helpers_to_file(header, file)

	_write_expansions_to_file(header, expansions, file)
	
	_write_user_code_to_file(user_code, file)


def _write_section_header(heading, file):
	"""Write Section Header
	
	Prints a commented header to mark a section within the output file.
	"""
	
	file.write('\n/' + '*' * 77 + '\n')
	file.write(" * {0} *\n".format(heading.center(73)))
	file.write(' ' + '*' * 77 + '/\n')

def _prefixed_default(header, default=None):
	"""Prefixed Default
	
	Returns a the string prefixed with the correct scope. This allows things to
	be namespaced and the user to control what string is used.
	"""
	
	prefix = header.get_option("prefix", 'yy')
	return prefix + '_' + default if default else prefix

def _write_header_to_file(header, file):
	"""Write Header to File
	
	Writes the beginning of the file. This is everything that should appear 
	before the utilities.
	"""
	
	_write_section_header("global includes", file)
	
	file.write("""
#include <stdio.h>
#include <stdlib.h>
#include {0}
	""".format(
		header.get_option("lexer_include", '<lexer.h>')
	))

def _write_helpers_to_file(header, file):
	"""Write Helpers to File
	
	Write out any functions and definitions required for the automaton to work.
	These would usually be the `get` and `peek` definitions.
	"""
	
	_write_section_header("utility methods", file)
	
	file.write("""

static {0} next_token;
static int token_buffered = 0;

{0} {1}_peek_next_token(void)
{{
	
	if (!token_buffered) {{
		next_token = {2};
		token_buffered = 1;
	}}
	
	return next_token;
}}

int {1}_eat_token({0} expected_token)
{{
	{0} token = {1}_peek_next_token();
	
	if (token == expected_token) {{
		token_buffered = 0;
		return 1;
	}}
	
	return 0;
}}
	""".format(
		header.get_option("token_type", _prefixed_default(header, 'token_t')),
		_prefixed_default(header),
		header.get_option(
			'lexer_function', _prefixed_default(header, 'get_next_token'))
	))

def _write_expansions_to_file(header, expansions, file):
	
	_write_section_header('main automaton', file)
	
	for name, symbol in expansions.items():
		_write_symbol_function_begin(header, name, symbol, file)
		for expansion in symbol.expansions:
			_write_body_for_expansion(header, expansions, name, expansion, file)
		_write_symbol_function_end(header, file)

def _get_counts(header, symbol):
	node_count = 0

	for expansion in symbol.expansions:
		n = 0
		for e in expansion:
			if not e in header.terminals:
				n += 1
		if n > node_count: node_count = n
	return node_count

def _write_symbol_function_begin(header, name, symbol, file):
	node_count = _get_counts(header, symbol)
	
	file.write("""
static {0}_node_t* {1}(void)
{{
	{0}_node_t* nodes[{3}];
	{2} token = {0}_peek_next_token();
	
	switch (token) {{
""".format(
		_prefixed_default(header),
		name,
		header.get_option("token_type", _prefixed_default(header, 'token_t')),
		node_count
	))

def _write_body_for_expansion(header, expansions, name, expansion, file):
	
	if not expansion:
		return
	
	terms = None
	if expansion and expansion[0] in header.terminals:
		terms = [expansion[0]]
	else:
		terms = expansions[expansion[0]].first
	
	for term in terms:
		file.write('\tcase {0}:\n'.format(header.terminals[term]))

	params = []
	node = 0
	
	for sym in expansion:
		if sym in header.terminals:
			file.write(
				"\t\tif (!eat_terminal({0}))\n\t\t\tgoto error;\n".format(
					header.terminals[sym]))
			params.append(header.terminals[sym])
		else:
			node_temp = "nodes[{0}]".format(node)
			node += 1
			file.write("\t\t{0} = {1}();\n".format(
				node_temp,
				sym
			))
			params.append(node_temp)
	
	file.write("\t\ttoken_action_{0}({1});\n".format(name, ", ".join(params)))
	file.write('\t\tbreak;\n\n')
	
def _write_symbol_function_end(header, file):
	file.write("\t}\n}\n")

def _write_user_code_to_file(code_block, file):
	"""Write User Code to File
	
	Writes a given block of code to the file prefixed with a user code header.
	"""
	
	_write_section_header('user code', file)
	file.write(code_block)