#include <stdlib.h>
#include <stdio.h>

#include <lex.h>
#include <parse.h>

int main(int argc, char* argv[]) {
	Lex_Token* tok;
	Lex_TokenType type;
	
	do {
		tok = Lex_getNextToken();
		Lex_printToken(tok);
		type = tok->type;
		Lex_freeToken(tok);
	} while (type != Lex_eof);
}
