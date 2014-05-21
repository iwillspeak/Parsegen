# Parsegen

Parsegen is an automatic parser generator. It reads in definitions in BNF and creates a top-down parser with one-symbol lookahead. Currently it supports outputting parsers in *c* and *Ruby*, although the ruby support is in it's early days.

Parsegen reads in files that describe LL(1) grammars and outputs a top-down hand-editable automaton that parses them.

## The Grammar File

Parsegen grammar files are written in a dialect of BNF. There are three main sections in each file, separated by `%%`.

### Header

The first section contains declarations and options. Declarations have the form `TERMINAL = Terminal_Value`. These specify the terminal symbols that are used in the grammar. The left hand side is the way they are referred to in the grammar file and the right hand side is the value to use in the output file (such as an `enum` value or constant). Options begin with `%` and look something like `%option = value`. Options are used to specify things like the function to call in the lexer to get a token, the prefix to use on function names and the language to use for the output automaton. Options specified in the file can be overridden from the command line.

### Body

The second section contains a list of grammar rules. Each line that contains a rule begins with a non-terminal followed by the `:=` symbol. The right hand side of the rule is made up of a mixture of terminals and non-terminals.

	expr := NUMBER expr_prime
	expr_prime := ADD expr_prime
	expr_prime := SUB expr_prime
	expr_prime :=

Lambda transitions are denoted by an empty expansion.

### User Code
The final section contains user code that is written to the output file without any modification. This can be used to provide entry points to the parser or could include a `main` function to make the whole parser standalone.

### Comments

In the first two sections the `#` character can be used as a line comment character. Any text after  the hash is ignored. Within the user code section you are free to use whatever comment system you like, just make sure that it is supported by the target language.

### Example Grammar

An example grammar which parses a properly formatted chain of integers added together:

    NUMBER Tok_NUMBER
    PLUS   Tok_PLUS
    %%
    addition_list := NUMBER addition_list_prime
    addition_list_prime := PLUS NUMBER addition_list_prime
    addition_list_prime := 
    %%
    int main(int argc, const char* argv[])
    {
        printf("%d", addition_list());
    }

## Prerequisites

Parsegen is written in Python 3. To get it up and running you will need a python3 installation and the `pystache` module. If you want to be able to run the tests you will need to have `nose` installed as well. For development you will probably want to use [Snooper][snooper_url] or `nosy` to run the test suites automatically.

# Gimme Gimme Gimme!

Parsegen can be installed with just one command in a Python 3 environment:

    $ pip3 install --pre parsegen

To check that the package installed ok run the following command:

    $ parsegen --version

[snooper_url]: http://github.com/iwillspeak/snooper
