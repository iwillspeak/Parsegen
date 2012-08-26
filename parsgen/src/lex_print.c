#include <stdlib.h>
#include <stdio.h>

#include <lexer.h>

static const char* tokNames[] = {
   	"Lex_eof",
   	"Lex_arrow",
   	"Lex_bar",
   	"Lex_star",
   	"Lex_lambda",
   	"Lex_obracket",
   	"Lex_cbracket",
   	"Lex_identifier",
   	"Lex_token_ref"
};

void Lex_printToken(Lex_Token* tok) {

	fprintf(stdout, "{%s: %s}\n", tokNames[tok->type], tok->value);
}
