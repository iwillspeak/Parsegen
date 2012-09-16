#include <stdlib.h>
#include <stdio.h>

#include <parse.h>

static void* amalloc(size_t size) {
	void* block;
	
	block = malloc(size);
	
	if (block == NULL)
		exit(EXIT_FAILURE);
	
	return block;
}

/**
 * Parser Object Allocators 
 */
Par_Module* Par_createModule(Lex_Token* identifier, Par_Program* program) {
	Par_Module* ret = amalloc(sizeof(Par_Module));
	
	ret->identifier = identifier;
	ret->program = program;
	
	return ret;
}

Par_Program* Par_createProgram(Par_Statements* statements) {
	Par_Program* ret = amalloc(sizeof(Par_Program));
	
	ret->statements = statements;
	
	return ret;
}

Par_Statements* Par_createStatements(Par_Statement* statement, Par_Statements* statements) {
	Par_Statements* ret = amalloc(sizeof(Par_Statements));
	
	ret->statement = statement;
	ret->statements = statements;
	
	return ret;
}

Par_Statement* Par_createExpressionStatement(Par_Expression* expression) {
	Par_Statement* ret = amalloc(sizeof(Par_Statement));
	
	ret->type = Par_StatementExpression;
	ret->value.expression = expression;
	
	return ret;
}

Par_Statement* Par_createAssigStatement(Par_Assign* assign) {
	Par_Statement* ret = amalloc(sizeof(Par_Statement));
	
	ret->type = Par_StatementAssign;
	ret->value.assign = assign;
	
	return ret;
}

Par_Statement* Par_createDeclarationStatement(Par_Declaration* declaration) {
	Par_Statement* ret = amalloc(sizeof(Par_Statement));
	
	ret->type = Par_StatementDeclaration;
	ret->value.declaration = declaration;
	
	return ret;
}

Par_Expression* Par_createOperationExpression(Par_Operation* operation) {
	Par_Expression* ret = amalloc(sizeof(Par_Expression));
	
	ret.type = Par_ExpressionOperation;
	ret.value.operation = operation;
	
	return ret;
}

Par_Expression* Par_createLiteralExpression(Par_Literal* literal) {
	Par_Expression* ret = amalloc(sizeof(Par_Expression));
	
	ret.type = Par_ExpressionLiteral;
	ret.value.literal = literal;
	
	return ret;
}

Par_Expression* Par_createLvalueExpression(Par_Lvalue* lvalue) {
	Par_Expression* ret = amalloc(sizeof(Par_Expression));
	
	ret.type = Par_ExpressionLvalue;
	ret.value.lvalue = lvalue;
	
	return ret;
}



//TODO: continue from here
