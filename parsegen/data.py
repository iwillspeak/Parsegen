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

from parsegen.errors import SymbolNameError
from parsegen.utils import lazyprop, Struct

class Header(object):
	"""Grammar File Header
	
	Represents the header section of the grammar file. Contains two mappings
	that represent the options and the terminal definitions.
	"""
	
	def __init__(self, terms, opts):
		"""Header Constructor
		
		Creates a new header from a given set of terminals and options. Both of
		these should be `dict`s containing mappings from the option/terminal
		names to their values.
		"""
		
		self.options = opts
		self.terminals = terms
		
	def get_option(self, option, default=""):
		return self.options.get(option, default)

class Symbol(object):
	"""Grammar Symbol
	
	Represents the expansions of a given symbol.
	"""
	
	def __init__(self, name):
		self.name = self._process_name(name)
		self.expansions = []
		self.nullable = False
		self.first = set()
		self.follow = set()
		self.grammar = None
	
	def _process_name(self, name):
		name = name.strip()
		if name and len(name.split()) != 1:
			raise SymbolNameError(name)
		return name

	@lazyprop
	def counts(self):
		"""Counts

		Returns the maximum number of terminals and nonterminals that this
		symbol has in any of its expansions
		"""
		node_count, term_count = 0, 0

		for expansion in self.expansions:
			n,t = 0,0
			for e in expansion:
				if e in self.grammar.header.terminals:
					t += 1
				else:
					n += 1
			if n > node_count: node_count = n
			if t > term_count: term_count = t
		return node_count, term_count

	def nonterminal_count(self):
		return self.counts[0]

	def terminal_count(self):
		return self.counts[1]
	
	def add_expansion(self, expansion):
		"""Add Expansion
		
		Adds a list of token names to the expansions of this symbol. This method
		automatically sets the symbol to nullable if a null expansion is passed
		in.
		"""

		self.expansions.append(Expansion(self, expansion))
		if not expansion:
			# We _know_ this symbol is nullable now, so set it
			self.set_nullable()

	def set_nullable(self):
		"""Set Nullable
		
		Mark the symbol as nullable. Nullable symbols are those that can expand
		to an empty string.
		"""
		
		self.nullable = True
	
	def is_nullable(self):
		"""Is Nullable
		
		Returns true if the symbol is nullable and false otherwise. A symbol
        with no expansions is considered nullable.
		"""
		
		if len(self.expansions) == 0:
			return True
		else:
			return self.nullable
			
	def _union_set_with_values(self, set_ref, values):
		"""Union Set With Values
		
		Set union helper method
		"""
		
		values = set(values)
		set_ref = set_ref.union(values)
		return set_ref
		
	def add_first(self, values):
		"""Add First
		
		Adds values to the first set. If any of the values are in the first set.
		This is a *set union* operation. `values` can be a set or a list.
		"""
		
		self.first = self._union_set_with_values(self.first, values)
		
	def add_follow(self, values):
		"""Add Follow
		
		Adds values to the follow set. If any of the values are in the first
		set. This is a *set union* operation. `values` can be a set or a list.
		"""
		
		self.follow = self._union_set_with_values(self.follow, values)

	def set_grammar(self, grammar):
		"""Set Grammar

		Attach the symbol to a grammar
		"""

		self.grammar = grammar

class Expansion(object):
	"""Expansion
	
	Represents a series of tokens in a grammar expansion.
	"""

	def __init__(self, symbol, tokens):
		self.symbol = symbol
		self.tokens = tokens

	@lazyprop
	def predictions(self):
		predictions = []
		if not self.tokens:
			pass
		elif self.tokens[0] in self.symbol.grammar.header.terminals:
			predictions = [self.tokens[0]]
		else:
			predictions = self.symbol.grammar.expansions[self.tokens[0]].first

		return [self.symbol.grammar.header.terminals[t] for t in predictions]
