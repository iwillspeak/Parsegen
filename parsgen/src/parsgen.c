#include <stdlib.h>
#include <stdio.h>

#include <lexer.h>

int main(int argc, char* argv[]) {
	Lex_Token* tok;
	
	do {
		tok = Lex_getNextToken();
		Lex_printToken(tok);
	} while (tok->type != Lex_eof);
}
