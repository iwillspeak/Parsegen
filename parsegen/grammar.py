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

from parsegen.errors import GrammarError

class Grammar(object):
	"""Grammar
	
	Represents a parsed grammar file.
	
	This object is used to collect together the parts of a grammar to allow
	parsed grammars to be passed around more easily. It is also responsible
	for calculating the sets for each expansion in the grammar from the raw
	grammar that it is given.
	"""
	
	def __init__(self, header, expansions, user_code):
		self.header = header
		self.expansions = expansions
		self.user_code = user_code
		self._compute_sets_for_expansions()
	

	def _initialise_expansions_state(self):
		"""Initialise Expansions State
	
		Sets up the expansions ready to have the first and follow sets computed.
		"""
		
		# These strings are long. Define them here to clean things up
		error_nterm_expand = "expansion for nonterminal {0}"
		error_undefined = "{0} is not defined as a terminal or nonterminal"
	
		for symbol in self.expansions.values():
			symbol.set_grammar(self)

			if symbol.name in self.header.terminals:
				raise GrammarError(error_nterm_expand.format(symbol.name))
		
			for exp in symbol.expansions:
				# This creates the initial first sets for each symbol
				if exp.tokens and exp.tokens[0] in self.header.terminals:
					symbol.add_first(exp.tokens[:1])
			
				for e in exp.tokens:
					valid = e in self.header.terminals or e in self.expansions
					if not valid:
						raise GrammarError(error_undefined.format(e))

	def _each_expansion(self):
		"""Each Expansion
	
		Returns an iterator that yields a 3-tuple of name, symbol and expansion
		for each expansion in grammar.
		"""
	
		for symbol in self.expansions.values():
			for expansion in symbol.expansions:
				yield symbol, expansion

	def _update_first_from_expansion(self, symbol, expansion):
		"""Update First from Expansion
	
		Updates the first set from a given symbol based on one of it's
		expansions. Returns true if an update is made to the symbol and false
		otherwise.
		"""
	
		changed = False
	
		for e in expansion.tokens:
			if e in self.header.terminals:
				break
			other_sym = self.expansions[e]
			if not other_sym.first.issubset(symbol.first):
				symbol.add_first(other_sym.first)
				changed = True
			if not other_sym.is_nullable():
				break
		else:
			# if all of the expansions are nullable and there are no terminals
			# then the symbol is nullable too
			if not symbol.is_nullable():
				symbol.set_nullable()
				changed = True
	
		return changed

	def _update_follow_from_expansion(self, symbol, expansion):
		"""Update Follow from Expansion
	
		Updates the follow set for a given symbol based on one of it's
        expansions.	Returns true if an update is made to the symbol and false
        otherwise.
		"""
	
		# TODO: implement follow sets
	
		return False

	def _compute_sets_for_expansions(self):
		"""Compute Sets for Expansions
	
		Iteratively computes the first and follow sets for the grammar. Will
		raise a GrammarError if one of the expansions attempts to use an
		undefined terminal or nonterminal or if an expansion is defined for a
		terminal.
		"""
	
		self._initialise_expansions_state()
		
		# If we don't have any expansions then we don't need to loop
		changed = len(self.expansions)
		
		while changed:
			changed = False
			for symbol, expansion in self._each_expansion():
				r = self._update_first_from_expansion(symbol, expansion)
				s = self._update_follow_from_expansion(symbol, expansion)
				# Changed accumulates 'trueness' with changes
				changed |= r or s
