#pragma once
#ifndef __PARSE_H__
#define __PARSE_H__

#include "lex.h"

/**
 * Main public parser api
 */

/**
 * Nonterminal Types
 *
 * Each nonterminal is represented by a structure containing terminals and non
 * terminals that make up the semantics of that node
 */
typedef struct _Par_Module      Par_Module;
typedef struct _Par_Program     Par_Program;
typedef struct _Par_Statements  Par_Statements;
typedef struct _Par_Statement   Par_Statement;
typedef struct _Par_Expression  Par_Expression;
typedef struct _Par_Operation   Par_Operation;
typedef struct _Par_Literal     Par_Literal;
typedef struct _Par_Lvalue      Par_Lvalue;
typedef struct _Par_Assign      Par_Assign;
typedef struct _Par_Declaration Par_Declaration;
typedef struct _Par_Block       Par_Block;

struct _Par_Module {
	Lex_Token* identifier;
	Par_Program* program;
};
Par_Module* Par_createModule(Lex_Token* identifier, Par_Program* program);

struct _Par_Program {
	Par_Statements* statements;
};
Par_Program* Par_createProgram(Par_Statements* statements);

struct _Par_Statements {
	Par_Statement* statement;
	Par_Statements* statements;
};
Par_Statements* Par_createStatements(Par_Statement* statement, Par_Statements* statements);

/**
 * Enum for StatementTypes
 */
enum _Par_StatementType {
	Par_StatementExpression,
	Par_StatementAssign,
	Par_StatementDeclaration
};
typedef enum _Par_StatementType Par_StatementType;

struct _Par_Statement {
	Par_StatementType type;
	union {
		Par_Expression*  expression;
		Par_Assign*      assign;
		Par_Declaration* declaration;
	} value;
};
Par_Statement* Par_createExpressionStatement(Par_Expression* expression);
Par_Statement* Par_createAssignStatement(Par_Assign* assign);
Par_Statement* Par_createDeclarationStatement(Par_Declaration* declaration);

/**
 * Enum of Expression Types
 */
enum _Par_ExpressionType {
	Par_ExpressionOperation,
	Par_ExpressionLiteral,
	Par_ExpressionLvalue
};
typedef enum _Par_ExpressionType Par_ExpressionType;

struct _Par_Expression {
	Par_ExpressionType type;
	union {
		Par_Operation* operation;
		Par_Literal*   literal;
		Par_Lvalue*    lvalue;
	} value;
};
Par_Expression* Par_createOperationExpression(Par_Operation* operation);
Par_Expression* Par_createLiteralExpression(Par_Literal* literal);
Par_Expression* Par_createLvalueExpression(Par_Lvalue);

/**
 * Enum of Operation Types
 */
enum _Par_OperationType {
	Par_OperationAdd,
	Par_OperationSub
};
typedef enum _Par_OperationType Par_OperationType;

struct _Par_Operation {
	Par_OperationType type;
	Par_Expression* lhs;
	Par_Expression* rhs;
};
Par_Operation* Par_createAddOperation(Par_Expression* lhs, Par_Expression* rhs);
Par_Operation* Par_createSubOperation(Par_Expression* lhs, Par_Expression* rhs);

struct _Par_Literal {
	Lex_Token* value;
};
Par_Literal* Par_creteLiteral(Lex_Token* value);

struct _Par_Lvalue {
	Lex_Token* identifier;
};
Par_Lvalue* Par_createLvalue(Lex_Token* identifier);

struct _Par_Assign {
	Lex_Token* identifier;
	Par_Expression* expression;
};
Par_Assign* Par_createAssign(Lex_Token* identifier, Par_Expression* expression);

struct _Par_Declaration {
	Lex_Token* identifier;
};
Par_Declaration* Par_createDeclaration(Lex_Token* identifier);

#endif
