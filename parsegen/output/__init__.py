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
import re
from parsegen.utils import lazyprop, Struct

# Dict indexed by uppercase comon name for language
language_hash = {}

def write_grammar(grammar, file=sys.stdout, options=None, language=None):
	"""Write Grammar
	
	Write a program out to the file that represents an automaton that parses
	the given grammar.
	"""

	if not language:
		language = grammar.header.options.get("language", "pretty_print")
	ctx = language_hash[_normalise_language_name(language)]
	ctx(grammar, options).write(file)
	
def _normalise_language_name(name):
	return re.sub("[\-_\ ]", "-", name.strip()).upper()
	
def register_context(language, context):
	language_hash[_normalise_language_name(language)] = context

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
		self.register_option("token_type", "token_t", True)
		# The type that is used to store ast nodes, returned from actions
		self.register_option("node_type", "node_t*", True)
		# The function that is used to get the next token from the lexer
		self.register_option("lexer_function", "get_next_token()", True)
		# The header file to include to get the lexer functions
		self.register_option("lexer_include", "lexer.h")
		# The code require to access the type of a token, useful if tokens
		# are pointer types.
		self.register_option("token_type_access", "")
	
	def predictions_for_expansion(self, expansion):
		"""Predictions for Expansion
		
		Returns a list of tokens that predict the given expansion. This can be
		empty if the expansion is a lambda transition, otherwise it will be
		the first set of the first symbol in the expansion.
		"""
		
		if not expansion:
			return set()
		elif expansion[0] in self.grammar.header.terminals:
			return {expansion[0]}
		else:
			return self.grammar.expansions[expansion[0]].first
	
	def register_option(self, option_name, default="", prefix=False):
		self.option_definitions.append((option_name, default, prefix))
	
	@lazyprop
	def options(self):
		"""Options
		
		Lazily computes and returns a Struct containing the options that will
		be used in the output.
		"""
		
		options = {}
		
		options['prefix'] = self._raw_options.get('prefix', self.default_prefix)
		for option, default, prefixed in self.option_definitions:
			if prefixed:
				default = options['prefix'] + default
			val = self._raw_options.get(option, default)
			options[option] = val
		
		return Struct(options)
	
	def _merged_options(self, options_base, options_merge):
		"""Merged Options
		
		Merges two sets of options together to create a composite dictionary of
		options.
		"""
		opts = options_base.copy()
		if options_merge:
			opts.update(options_merge)
		return opts

	def _get_counts(self, symbol):
		"""Get Counts
		
		Returns the number of nodes in a given symbol that are nonterminals and
		terminals.
		"""
		node_count, term_count = 0, 0

		for expansion in symbol.expansions:
			n,t = 0,0
			for e in expansion:
				if e in self.grammar.header.terminals:
					t += 1
				else:
					n += 1
			if n > node_count: node_count = n
			if t > term_count: term_count = t
		return node_count, term_count

# Import all the languages here. This is done at the bottom to ensure that all
# the definitions needed are in scope
from . import c, pretty_print, ruby
