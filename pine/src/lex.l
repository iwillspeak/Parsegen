%{
/**
 * Lexical Tokeniser for Pine
 * 
 * Pine is a simple language to help with parser design for more complex
 * ones.
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <lex.h>

%}

NUMBER  [0-9]+
ID      [a-zA-Z_][a-zA-Z0-9_]*

LINECOM "--"

%option noinput
%option nounput
%%

{NUMBER}    { return Lex_number; } 
"module"    { return Lex_module; }
"var"       { return Lex_var; }
{ID}        { return Lex_id; }
[\ \t\n]    { /* ignore whitespace */ }
";"         { return Lex_semicolon; }
"+"         { return Lex_plus; }
"-"         { return Lex_minus; }
"{"         { return Lex_lbrace; }
"}"         { return Lex_rbrace; }
"="         { return Lex_equals; }

{LINECOM}.* { /* ignore comments */ }

.           { return Lex_eof; }

%%

/**
 * Global token storage to allow the token lookahead functionality
 */
Lex_Token* nextTok = NULL;

/**
 * Perform lexical analysis and return the next token in the input
 * token stream. 
 */
Lex_Token* Lex_getNextToken(void) {
	Lex_Token* tok;
	
	if (nextTok == NULL) {
		tok = malloc(sizeof(Lex_Token));
		if (tok) {
			tok->type = yylex();
			tok->value = strdup(yytext);
		}
	}
	else
		tok = nextTok;

	nextTok = NULL;
	
	return tok;
}

/**
 * Peek at the next token in the queue, without discarding it. This is 
 * used to allow lookaeads in the parser.
 */
Lex_Token* Lex_peekNextToken(void) {

	if (nextTok == NULL)
		nextTok = Lex_getNextToken();
	return nextTok;
}

/**
 * Peek until a token in the token list is found
 */
Lex_Token* Lex_peekUntil(Lex_TokenType* tokenList) {
	Lex_Token* tok;

	do {
		tok = Lex_peekNextToken();
		for (Lex_TokenType* i = tokenList; *i != Lex_TokenListEnd; ++i) {
			if (tok->type == *i)
				return tok;
		}
		Lex_freeToken(tok);
		nextTok = NULL;
	} while (true);
}

/**
 * Free a token, freeing it's internal value buffer too.
 */
void Lex_freeToken(Lex_Token* tok) {

	if (tok != NULL) {
		free(tok->value);
		free(tok);
	}
}