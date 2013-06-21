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
from parsegen.utils import lazyprop, Namespace

def write_grammar(grammar, file=sys.stdout):
	"""Write Grammar
	
	Write a program out to the file that represents an automaton that parses
	the given grammar.
	"""
	
	COutputContext(grammar).write(file)

class OutputContext(object):
	"""Output Context
	
	Represents the context required to write a grammar out to a file.
	"""
	
	def __init__(self, grammar, option_overrides=None):
		self.grammar = grammar
		self.option_definitions = []
		self.default_prefix = "yy_"
		self._raw_options = self._merged_options(
			grammar.header.options, option_overrides)
		
		# The type that is used to store tokens
		self.register_option("token_type", True, "token_t")
		# The type that is used to store ast nodes, returned from actions
		self.register_option("node_type", True, "node_t*")
		# The function that is used to get the next token from the lexer
		self.register_option("lexer_function", True, "get_next_token()")
		# The header file to include to get the lexer functions
		self.register_option("lexer_include", False, "lexer.h")
		# The code require to access the type of a token, useful if tokens
		# are pointer types.
		self.register_option("token_type_access", False, "")
	
	def write(self, file):
		"""Write
		
		Write the formatted source code for the automaton out to the file.
		"""
		
		self._write_header_to_file(file)
		self._write_helpers_to_file(file)

		self._write_expansions_to_file(self.grammar.expansions, file)
	
		self._write_user_code_to_file(self.grammar.user_code, file)
	
	def register_option(self, option_name, default="", prefix=False):
		self.option_definitions.append((option_name, default, prefix))
	
	@lazyprop
	def options(self):
		"""Options
		
		Lazily computes and returns a Namespace containing the options namespace
		that will be used in the output.
		"""
		
		options = {}
		
		options['prefix'] = self._raw_options.get('prefix', self.default_prefix)
		for option, prefixed, default in self.option_definitions:
			if prefixed:
				default = options['prefix'] + default
			val = self._raw_options.get(option, default)
			options[option] = val
		
		return Namespace(options)
	
	def _merged_options(self, options_base, options_merge):
		"""Merged Options
		
		Merges two sets of options together to create a composite dictionary of
		options.
		"""
		opts = options_base.copy()
		if options_merge:
			opts.update(options_merge)
		return opts
	
class COutputContext(OutputContext):
	"""C Output Context
	
	Represents the context required to write out to a C file.
	"""
	
	def _write_section_header(self, heading, file):
		"""Write Section Header
	
		Prints a commented header to mark a section within the output file.
		"""
	
		file.write('/' + '*' * 77 + '\n')
		file.write(" * {0} *\n".format(heading.center(73)))
		file.write(' ' + '*' * 77 + '/\n\n')

	def _write_header_to_file(self, file):
		"""Write Header to File
	
		Writes the beginning of the file. This is everything that should appear 
		before the utilities.
		"""
	
		self._write_section_header("global includes", file)
	
		file.write('#include <stdio.h>\n#include <stdlib.h>\n#include "{0}"\n\n'
			.format(self.options.lexer_include))

	def _write_helpers_to_file(self, file):
		"""Write Helpers to File
	
		Write out any functions and definitions required for the automaton to
		work. These would usually be the `eat` and `peek` definitions.
		"""
	
		self._write_section_header("utility methods", file)
	
		# Global variables to keep track of tokens from the lexer
		file.write("static " + self.options.token_type + "next_token;\n")
		file.write("static int token_buffered = 0;\n\n")
		
		# Write out the body of the _peek_next_token funciton
		file.write(
			self.options.token_type + " " + self.options.prefix +
			"_peek_next_token(void)\n{\n")
		file.write("\tif (!token_buffered) {\n")
		file.write("\t\tnext_token = " + self.options.lexer_function + ";\n")
		file.write("\t\ttoken_buffered = 1;\n")
		file.write("\t}\n")
		file.write("\treturn next_token;\n")
		file.write("}\n\n")
		
		file.write(
			"int " + self.options.prefix + "_eat_token("+ self.options.token_type +
			" expected_token)\n{\n")
		file.write(
			"\t" + self.options.token_type + " tok = " + self.options.prefix +
			"_peek_next_token();\n")
			
		file.write("\tif (token == expected_token) {\n")
		file.write("\t\ttoken_buffered = 0;\n")
		file.write("\t\treturn 1;\n")
		file.write("\t}\n")
		file.write("\treturn 0;\n")
		file.write("}\n\n")

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

	def _write_symbol_function_begin(self, name, symbol, ofile):
		
		node_count = self._get_counts(symbol)
		
		ofile.write("static {0} {1}(void)\n{{\n".format(
			self.options.node_type, name))
		ofile.write("\t{0} nodes[{1}];\n".format(
			self.options.node_type, node_count))
		ofile.write(
			"\t{0} token {1}_peek_next_token();\n\tswitch(token) {{\n".format(
				self.options.token_type, self.options.prefix))

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
		file.write("\t}\n}\n\n")

	def _write_user_code_to_file(self, code_block, file):
		"""Write User Code to File
	
		Writes a given block of code to the file prefixed with a user code header.
		"""
	
		self._write_section_header('user code', file)
		file.write(code_block)
	