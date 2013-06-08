#! /usr/bin/env python
import sys
import os

import pystache

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

# -------------------------------------------------------------------
# Class Symbol
#
# Terminal or non-terminal symbol in the grammar. Terminal symbols are strings
# non-terminals are collections of expansions.
# 

class Symbol(object):
	
	def __init__(self, string):
		self.name = string.strip()
		self.expansions = []
		self.am_nullable = True
		
		self._check_identifier(self.name)
	
	def is_term(self):
		return self.name.upper() == self.name
	
	def first(self):
		if self.is_term():
			return set([self.name])
		
		f_set = set()
		for e in self.expansions:
			f_set = f_set.union(self._expansion_first(e))
			
		return f_set
	
	def nullable(self):
		for e in self.expansions:
			for s in e:
				if not s.nullable():
					break
			else:
				return True
		
		return not self.is_term() and not len(self.expansions)
	
	def push_expansion(self, expansion):
		if self.is_term():
			raise TerminalExpansionError
		
		self.expansions.append(expansion)
	
	def _check_identifier(self, identifier):
		
		for s in identifier.split("_"):
			if not s.isalpha():
				raise IdentifierError
	
	def _expansion_first(self, expansion):
		ret = set()
		for sym in expansion:
			ret = ret.union(sym.first())
			if not sym.nullable():
				return ret
		return ret
	

class TerminalExpansionError(Exception):
	pass
	
class IdentifierError(Exception):
	pass

# -------------------------------------------------------------------
# Class Expansion
#
# Represents an expansion of a non-terminal symbo. This is list of Symbols 
# that represent the expansion.
#

class Expansion(list):
	
	def __init__(self, *expansions):
		pass

# --------------------------------------------------------------------

def isTerm(string):
	return string.upper() == string

def getCounts(rule):
	terms = 0
	nterms = 0
	for s in rule:
		if isTerm(s):
			terms += 1
		else:
			nterms += 1
	return (terms, nterms)

class NonTerm(object):
	
	def __init__(self, expansion = None):
		self.nullable = False
		self.expansions = []
		self.first = set()
		self.follow = set()
		if expansion:
			self.addExpansion(expansion)
	
	def addExpansion(self, expansion):
		self.expansions.append(expansion)
		if not expansion:
			self.nullable = True
		if expansion and isTerm(expansion[0]):
			self.addFirst(expansion[0])
	
	def isNullable(self):
		return self.nullable
		
	def setNullable(self):
		self.nullable = True
		
	def addFollow(self, item):
		self.follow.add(item)
	
	def addFirst(self, item):
		self.first.add(item)
	
	def unionFirst(self, set):
		self.first = self.first.union(set)
		
	def unionFollow(self, set):
		self.follow = self.follow.union(set)
	
	def getFirst(self):
		return self.first
	
	def getFollow(self):
		return self.follow
		
	def getExpansions(self):
		return self.expansions
		
	def __str__(self):
		return str(self.nullable) + "(" + str(self.first)+ ")" + str(self.expansions)

def main(argv):
	from argparse import ArgumentParser, FileType
	
	parser = ArgumentParser(description = "Leet-Lang Parser Generator", epilog = 'For more information read the source code...')
	parser.add_argument('-i', '--header', help = '''Create a header file with declarations of all the functions that need
	                                                   to be implemented for the parser to work.''', type = FileType('w'), metavar = 'HEADER')
	parser.add_argument('-s', '--skeleton', help = 'Create a skeleton implementation of the semantic actions for each node', type = FileType('w'))
	parser.add_argument('-o', '--output', help = 'The file name to write the generated parser to.', type = FileType('w'), metavar = 'FILE', default = sys.stdout)
	parser.add_argument('-n', '--notypes', help = "Don't emit type definitions for Par_State and Par_Node", action = 'store_const' , const = True)
	parser.add_argument('file', help = '''The grammar file to generate a parser from.''', type = file)
	options = parser.parse_args(argv)

	# read the file into the map
	rules = {}
	inUser = True
	ourCode = []
	userCode = []
	
	# blocks of code for the parser are enclosed in %{ %}
	for l in options.file:
		if inUser:
			if '%{' in l:
				l = l.partition('%{')
				userCode.append(l[0])
				ourCode.append(l[2])
				inUser = False
			else:
				userCode.append(l)
		else:
			if '%}' in l:
				l = l.partition('%}')
				userCode.append(l[2])
				ourCode.append(l[0])
				inUser = True
			else:
				ourCode.append(l)
				
	options.file.close()
	
	# Filter the code for the parser to remove comments
	ourCode = [ s for s in map(lambda x: x.partition('//')[0].strip(), ourCode) if s]
	
	# Process each declaration
	for dec in ourCode:
		if ':=' in dec:
			nt, _, expansion = dec.partition(':=')
			nt = nt.strip()
			expansion = expansion.split()
		
			if isTerm(nt):
				print "Ignoring expansion for terminal {0}".format(nt)
				continue
		
			try:
				rules[nt].addExpansion(expansion)
			except KeyError:
				rules[nt] = NonTerm(expansion)

	
	# generate the first and follow sets for the symbols
	changed = True
	valid = True
	while changed:
		changed = False
		for name, symbol in rules.iteritems():
			for rule in symbol.getExpansions():
				# calculate the first set of this symbol
				for r in rule:
					if isTerm(r):
						# we have already added terminals to the first set
						break
					if not (rules[r].getFirst().issubset(symbol.getFirst())):
						symbol.unionFirst(rules[r].getFirst())
						changed = True
					if not rules[r].isNullable():
						break
				else:
					# if all of the rules are nullable and 
					# there are no terminals then the symbol
					# is nullable too
					if not symbol.isNullable():
						symbol.setNullable()
						changed = True
				
				# calculate the follow set of this symbol
				for i, r in enumerate(rule):
					if isTerm(r):
						continue
					
					rest = rule[i + 1:]
					allNullable = not len(rest)
					for y in rule[i + 1:]:
						# All the previous have been nullable non terminals so r's follow contains
						# the first of this 
						if isTerm(y):
							if not y in rules[r].getFollow():
								rules[r].addFollow(y)
								changed = True
							break
						else:
							try:
								if not rules[y].getFirst().issubset(rules[r].getFollow()):
									rules[r].unionFollow(rules[y].getFirst())
									changed = True
								if not rules[y].isNullable():
									break
							except KeyError, e:
								valid = False
								print >>sys.stderr, "Reference to undefined non-terminal {0:s} from {1}".format(e, name)
					else:
						allNullable = True
						
					# if every non terminal after is nullable then our follow contains the follow
					# of the parent
					if allNullable:
						try:
							if not symbol.getFollow().issubset(rules[r].getFollow()):
								rules[r].unionFollow(symbol.getFollow())
								changed = True
						except KeyError, e:
							valid = False
							print >>sys.stderr, "Reference to undefined non-terminal {0:s} from {1}".format(e, name)
							
	if not valid:
		return 1
	
	# Create a blank view
	view = { 'options': options }
	
	# print out the resulting automaton
	options.output.write("#include <stdlib.h>\n")
	
	view['module'] = ['lex', 'parse']
	options.output.write("#include <lex.h>\n")
	options.output.write("#include <parse.h>\n")
	options.output.write("\n")
	
	if not options.notypes:
		options.output.write("typedef struct Par_Node_ Par_Node;\n")

	options.output.write("/* Auto generated parser created from {0} */\n".format(options.file.name))
	options.output.write("\n")
	
	options.output.write("// Forward declarations of non terminal symbols\n")
	for name in rules.keys():
		options.output.write("static Par_Node* {0}(void* userPointer);\n".format(name))
	options.output.write("\n")
	
	view['nonterm'] = (map(lambda x: {
		'name': x[0], 'nullable': x[1].isNullable(), 'first': x[1].getFirst(),
		'production': map(lambda x: {'expansion': map(lambda x: {'terminal': isTerm(x), 'token': x}, x), 'prediction': None if not x else ([x[0]] if isTerm(x[0]) else rules[x[0]].getFirst())}, x[1].getExpansions())
	}, rules.iteritems()))
	
	if options.skeleton:
		options.skeleton.write("#include <stdlib.h>\n")
		options.skeleton.write("#include <lex.h>\n")
		options.skeleton.write('\n//structure to contain node values\ntypedef struct Par_Node_ { enum { PAR_NODE_TYPES } type; union { int i; } val; } Par_Node;\n\n')
	
	options.output.write("// Forward declarations of symantic actions\n")
	declarations = []
	for name, symbol in rules.iteritems():
		for rule in symbol.getExpansions():
			if not rule:
				continue
			params = map(lambda x:  ("Lex_Token* tok" + str(x[1])) if isTerm(x[0]) else ("Par_Node* node" + str(x[1])), zip(rule, range(len(rule))))
			declaration = "Par_Node* {0}_sem_{1}({2});\n".format(name, rule[0], ", ".join(params))
			options.output.write(declaration)
			declarations.append(declaration)
			if options.skeleton:
				options.skeleton.write(declaration[:-2] + '{\n\tPar_Node* ret;\n\n\tif (!(ret = malloc(sizeof(Par_Node))))\n\t\treturn NULL;\n\n\treturn ret;\n}\n\n')
	options.output.write("\n")
	
	if options.header:
		modname = os.path.basename(options.file.name).upper().replace('.', '_')
		options.header.write("#ifndef __PARSER_{0}_HEADER__\n".format(modname))
		options.header.write("#define __PARSER_{0}_HEADER__\n".format(modname))
		options.header.write(''.join(declarations))
		options.header.write("#endif\n")
	
	options.output.write("// Helper methods\n")
	options.output.write("static Lex_Token* eatTerminal(Lex_TokenType type) {\n")
	options.output.write("\n")
	options.output.write("\tif (Lex_peekNextToken()->type == type)\n")
	options.output.write("\t\treturn Lex_getNextToken();\n")
	options.output.write("\telse\n")
	options.output.write("\t\treturn NULL;\n")
	options.output.write("}\n")
	options.output.write("\n")
	
	options.output.write("// Terminal symbol implementations\n")
	
	for name, symbol in rules.iteritems():
		options.output.write("//static const Lex_TokenType {0}first[] = {{{1} -1}};\n".format(name, ' '.join(map(lambda x: x + ',', ["Lex_" + s for s in symbol.getFirst()]))))
		options.output.write("static const Lex_TokenType {0}follow[] = {{{1} -1}};\n".format(name, ' '.join(map(lambda x: x + ',', ["Lex_" + s for s in symbol.getFollow()]))))
		
		options.output.write("static Par_Node* {0}(void* userPointer) {{\n".format(name))
		terms = 0
		nterms = 0
		for rule in symbol.getExpansions():
			counts = getCounts(rule)
			terms = max(counts[0], terms)
			nterms = max(counts[1], nterms)
		if nterms:
			options.output.write("\tPar_Node* nterms[{0}];\n".format(nterms))
		if terms:
			options.output.write("\tLex_Token* terms[{0}];\n".format(terms))
		
		options.output.write("\n")
		options.output.write("\tswitch (Lex_peekNextToken()->type) {\n")
		
		seenTerms = []
		
		for rule in symbol.getExpansions():
			
			terms = []
			if rule and isTerm(rule[0]):
				terms.append(rule[0])
			elif rule:
				terms = rules[rule[0]].getFirst()
			else:
				continue
				
			if not terms:
				options.output.write("// TODO: looks like there are no predictions for this expansion yet :-/\n")
			
			options.output.write("\n")
			for t in terms:
				if t in seenTerms:
					options.output.write("#error prediction conflict with terminal {0}\n".format(t))
				else:
					options.output.write("\tcase Lex_{0}:\n".format(t))
			seenTerms.extend(terms)
			
			options.output.write("\t\t// {0}\n".format(" ".join(rule)))
			terms = 0
			nterms = 0
			sems = [] 
			for s in rule:
				if isTerm(s):
					options.output.write("\t\tterms[{0}] = eatTerminal(Lex_{1});\n".format(terms, s))
					options.output.write("\t\tif (terms[{0}] == NULL) {{\n".format(terms))
					options.output.write('\t\t\tprintf("error:%d:%d: Parse error, expecting {0}\\n", Lex_peekNextToken()->position.line, Lex_peekNextToken()->position.column);\n'.format(s))
					options.output.write("\t\t\tgoto error;\n\t\t}\n")
					sems.append("terms[{0}]".format(terms))
					terms += 1
				else:
					options.output.write("\t\tnterms[{0}] = {1}(userPointer);\n".format(nterms, s))
					if not rules[s].isNullable():
						options.output.write("\t\tif (nterms[{0}] == NULL) goto error;\n".format(nterms))
					sems.append("nterms[{0}]".format(nterms))
					nterms += 1
			options.output.write("\t\treturn {0}_sem_{1}({2});\n".format(name, rule[0], ", ".join(sems)))
			options.output.write("\t\tbreak;\n")

		options.output.write("\n\tcase Lex_UNKNOWN:\n")
		options.output.write('\t\tprintf("error:%d:%d unknown token\\n", Lex_peekNextToken()->position.line, Lex_peekNextToken()->position.column);\n')
		options.output.write("\t\tgoto error;\n")
		options.output.write("\t\tbreak;\n")

		options.output.write("\n\tdefault:\n")
		if symbol.isNullable():
			options.output.write("\t\treturn NULL;\n")
		else:
			options.output.write('\t\tprintf("error:%d:%d: Parse error, expecting one of {0} but found %d\\n", Lex_peekNextToken()->position.line, Lex_peekNextToken()->position.column, Lex_peekNextToken()->type);'.format(', '.join(symbol.getFirst())))
			options.output.write("\t\tgoto error;\n")
		options.output.write("\t}\n")
		options.output.write("\n")
		
		options.output.write("error:\n")
		options.output.write("\tLex_peekUntil({0}follow);\n".format(name))
		options.output.write("\treturn NULL;\n")
		options.output.write("}\n\n\n")
		
	options.output.write("// User code section\n")
	options.output.write(''.join(userCode))
	options.output.write('\n')
	
	view['code'] = (s[:-1] for s in userCode)
	print view
	print pystache.render(''.join(open("langs/c.mustache").readlines()), view)


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
