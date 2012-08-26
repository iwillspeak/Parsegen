#include <stdlib.h>
#include <stdio.h>

#include <lex.h>

static const char* tokenName[] = {
	"Lex_eof",
	"Lex_number",
	"Lex_id",
	"Lex_module",
	"Lex_semicolon",
	"Lex_plus",
	"Lex_minus",
	"Lex_equals",
	"Lex_var",
	"Lex_lbrace",
	"Lex_rbrace"
};

void Lex_printToken(Lex_Token* token) {

	fprintf(stdout, "{%s : %s}\n", tokenName[token->type], token->value);
}

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
