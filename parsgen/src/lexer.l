%{
/**
 * Lexical Tokeniser for Parser Gnerator
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <lexer.h>

%}

ARROW      "->"
BAR        "|"
STAR       "*"
LAMBDA     "$"
OBRACKET   "("
CBRACKET   ")"
IDENTIFIER [a-z][a-z0-9_\-']*
TOKEN_REF  <[a-z][a-z0-9_\-']*>

LINECOM    "--"
WS         [\ \n\t]+

%option noinput
%option nounput
%%

{ARROW}       { return Lex_arrow; }
{BAR}         { return Lex_bar; }
{STAR}        { return Lex_star; }
{LAMBDA}      { return Lex_lambda; }
{OBRACKET}    { return Lex_obracket; }
{CBRACKET}    { return Lex_cbracket; }
{IDENTIFIER}  { return Lex_identifier; }
{TOKEN_REF}   { return Lex_token_ref; }

{LINECOM}.*   { /* ignore comments */ }
{WS}          { /* ignore whitespace */ }

.             { return Lex_eof; }

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
			tok->value = yytext;
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