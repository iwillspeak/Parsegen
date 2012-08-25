Pine
====

Pine is a simple line-style language project aimed to create a new
object-oriented compiler parser generator.

The Parser
----------

Pine is intended to allow the creation of a new parser generator, similar to
GNU bison or equivalents. It differs in that it is not intended to be able to
create generic parsers but instead parsers that create an Abstract Syntax Tree
for use as the front-end to a programming language compiler. 

The Language
------------

The pine language is a 'line' type programming language. That is it consists
of programs of arithmetic operations with no looping. This is to simplify 
the grammar of the language. The language is not capable of conditional jumps
and therefore is not turing complete. 

An example pine program, a `.cone`, that swaps the values of variables `a`
and `b` follows:


    -- example pine language program
    module example
    
    var a;
    var b;
    
    a = 0;
    b = 10;
    a = a + b; -- (a + b) (b)
    b = b - a; -- (a + b) (a)
    a = a - b; -- (b) (a)

