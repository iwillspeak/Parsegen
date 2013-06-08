# Parsegen

Parsegen is an automatic parser generator for C. It reads in definitions in BNF and creates a top-down parser with one-symbol lookahead.

In theory Parsegen can generate parsers for LL(1)
grammars.

## The Grammar File

Parsegen grammar files are written in a dialect of BNF. Each line that contains a rule begins with a non-terminal followed by the `:=` symbol. The right hand side of the rule is made up of a mixture of terminals and non-terminals.

	expr := NUMBER expr_prime
	expr_prime := ADD expr_prime
	expr_prime := SUB expr_prime
	expr_prime :=

Non-terminal symbols are designated by uppercase identifiers. The right hand side of a rule can be empty to allow the no-terminal to allow lambda transitions.

## Prerequisites

To get Parsegen working you will need to have these python modules installed: 

 * argparse
