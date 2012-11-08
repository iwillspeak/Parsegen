Parsegen
========

This project contains the automatic parser generator for the Leet-Lang 
project. It takes a grammar file that describes the language and generates
a top-down parser for that language. Parsegen can generate parsers for LL(1)
grammars.

The Grammar File
----------------

Parsegen grammar files are written in a dialect of BNF. Each line that 
contains a rule begins with a non-terminal followed by the `:=` symbol. The 
right hand side of the rule is made up of a mixture of terminals and 
non-terminals.

	expr := NUMBER expr_prime
	expr_prime := ADD expr_prime
	expr_prime := SUB expr_prime
	expr_prime :=

Non-terminal symbols are designated by uppercase identifiers. The right hand 
side of a rule can be empty to allow the no-terminal to allow lambda 
transitions.

