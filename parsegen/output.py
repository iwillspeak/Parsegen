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
import parsegen.data as data

def write_grammar(grammar, file=sys.stdout):
	"""Write Grammar
	
	Write a program out to the file that represents an automaton that parses
	the given grammar.
	"""
	
	OutputContext(grammar).write(file)

class OutputContext(object):
	"""Output Context
	
	Represents the context required to write a grammar out to a file.
	"""
	
	def __init__(self, grammar, option_overrides={}):
		self.grammar = grammar
		options = grammar.header.options.copy()
		options.update(option_overrides)
		self.options = self._process_options(options)
	
	def write(self, file):
		"""Write
		
		Write the formatted source code for the automaton out to the file.
		"""
		
		self._write_header_to_file(file)
		self._write_helpers_to_file(file)

		self._write_expansions_to_file(self.grammar.expansions, file)
	
		self._write_user_code_to_file(self.grammar.user_code, file)
		

	def _write_section_header(self, heading, file):
		"""Write Section Header
	
		Prints a commented header to mark a section within the output file.
		"""
	
		file.write('\n/' + '*' * 77 + '\n')
		file.write(" * {0} *\n".format(heading.center(73)))
		file.write(' ' + '*' * 77 + '/\n')

	def _prefixed_default(self, default=None):
		"""Prefixed Default
	
		Returns a the string prefixed with the correct scope. This allows things to
		be namespaced and the user to control what string is used.
		"""
	
		prefix = self.grammar.header.get_option("prefix", 'yy')
		return prefix + '_' + default if default else prefix

	def _write_header_to_file(self, file):
		"""Write Header to File
	
		Writes the beginning of the file. This is everything that should appear 
		before the utilities.
		"""
	
		self._write_section_header("global includes", file)
	
		file.write("""
	#include <stdio.h>
	#include <stdlib.h>
	#include {0}
		""".format(
			self.grammar.header.get_option("lexer_include", '<lexer.h>')
		))

	def _write_helpers_to_file(self, file):
		"""Write Helpers to File
	
		Write out any functions and definitions required for the automaton to work.
		These would usually be the `get` and `peek` definitions.
		"""
	
		self._write_section_header("utility methods", file)
	
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
			self.grammar.header.get_option("token_type", self._prefixed_default('token_t')),
			self._prefixed_default(),
			self.grammar.header.get_option(
				'lexer_function', self._prefixed_default('get_next_token'))
		))

	def _write_expansions_to_file(self, expansions, file):
	
		self._write_section_header('main automaton', file)
	
		for name, symbol in expansions.items():
			self._write_symbol_function_begin(name, symbol, file)
			for expansion in symbol.expansions:
				self._write_body_for_expansion(expansions, name, expansion, file)
			self._write_symbol_function_end(file)

	def _get_counts(self, symbol):
		node_count = 0

		for expansion in symbol.expansions:
			n = 0
			for e in expansion:
				if not e in self.grammar.header.terminals:
					n += 1
			if n > node_count: node_count = n
		return node_count

	def _write_symbol_function_begin(self, name, symbol, file):
		node_count = self._get_counts(symbol)
	
		file.write("""
	static {0}_node_t* {1}(void)
	{{
		{0}_node_t* nodes[{3}];
		{2} token = {0}_peek_next_token();
	
		switch (token) {{
	""".format(
			self._prefixed_default(),
			name,
			self.grammar.header.get_option("token_type", self._prefixed_default('token_t')),
			node_count
		))

	def _write_body_for_expansion(self, expansions, name, expansion, file):
	
		if not expansion:
			return
	
		terms = None
		if expansion and expansion[0] in self.grammar.header.terminals:
			terms = [expansion[0]]
		else:
			terms = expansions[expansion[0]].first
	
		for term in terms:
			file.write('\tcase {0}:\n'.format(self.grammar.header.terminals[term]))

		params = []
		node = 0
	
		for sym in expansion:
			if sym in self.grammar.header.terminals:
				file.write(
					"\t\tif (!eat_terminal({0}))\n\t\t\tgoto error;\n".format(
						self.grammar.header.terminals[sym]))
				params.append(self.grammar.header.terminals[sym])
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
	
	def _write_symbol_function_end(self, file):
		file.write("\t}\n}\n")

	def _write_user_code_to_file(self, code_block, file):
		"""Write User Code to File
	
		Writes a given block of code to the file prefixed with a user code header.
		"""
	
		self._write_section_header('user code', file)
		file.write(code_block)
	
	def get_option_definitions(self):
		"""Get Option Definitions
		
		Returns an iterable containing tuples that define the options that this
		output context accepts.
		
		Options are of the form (option_key, prefixed, default) where
		option_key is the string that identifies the option, prefixed states if
		the option should have a prefix appended to it's default value and
		default is the value to use if no option is provided for this key. 
		"""
		return [
			# The prefix to use on default values and parser functions
			("prefix", False, "yy_"),
			# The type that is used to store tokens
			("token_type", True, "token_t"),
			# The type that is used to store ast nodes, returned from actions
			("node_type", True, "node_t"),
			# The function that is used to get the next token from the lexer
			("lexer_function", True, "get_next_token()"),
			# The code require to access the type of a token, useful if tokens
			# are pointer types.
			("token_type_access", False, "")
		]
	
	def _process_options(self, options_hash):
		"""Process Options
		
		Takes a hash of options and returns a Namespace containing the values
		that will be used in the output.
		"""
		
		options = {}
		
		for option, prefixed, default in self.get_option_definitions():
			if prefixed:
				default = options['prefix'] + default
			val = options_hash.get(option, default)
			options[option] = val
		
		return data.Namespace(options)