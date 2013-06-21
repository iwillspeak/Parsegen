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
from parsegen.utils import lazyprop, Namespace

# Dict indexed by uppercase comon name for language
language_hash = {}

def write_grammar(grammar, file=sys.stdout):
	"""Write Grammar
	
	Write a program out to the file that represents an automaton that parses
	the given grammar.
	"""
	
	language = grammar.header.options.get("language", "c")
	ctx = language_hash[_normalise_language_name(language)]
	ctx(grammar).write(file)
	
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
		
		Lazily computes and returns a Namespace containing the options that will
		be used in the output.
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

class CallbackOutputContext(OutputContext):
	"""Callback Output Context
	
	Output context that uses callbacks to write things to a stream. This is
	intended for implementing output contexts where the logic for the context
	is better expressed in python.
	"""
	
	PRE, MAIN, POST = range(3)
	
	def __init__(self, *args):
		OutputContext.__init__(self, *args)
		self.callbacks = {
			self.PRE : [],
			self.MAIN : [],
			self.POST : []
		}
		
	def write(self, file):
		"""Write
		
		Calls the methods that have been registered for each stage to write the
		output to the file.
		"""
		
		for callback in self.callbacks[self.PRE]:
			callback(file)
		
		for callback in self.callbacks[self.MAIN]:
			for name, symbol in self.grammar.expansions.items():
				callback(name, symbol, file)
		
		for callback in self.callbacks[self.POST]:
			callback(file)
	
	def register_callback(self, callback, stage=MAIN):
		
		if not stage in [self.MAIN, self.PRE, self.POST]:
			raise ArgumentError("unknown callback stage '%s'" % stage)
		
		self.callbacks[stage].append(callback)

# Import all the languages here. This is done at the bottom to ensure that all
# the definitions needed are in scope
from . import c
