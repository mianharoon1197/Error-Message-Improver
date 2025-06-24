# ✅ Fully working parser.py (fixed for AST compatibility)
import ply.yacc as yacc
from lexer import tokens
from semantic import (
    declare_var, assign_var, get_var_type,
    declare_func, call_func,
    begin_scope, end_scope
)

source_code = ""

class ASTNode:
    def __init__(self, nodetype, value=None, children=None):
        self.nodetype = nodetype
        self.value = value
        self.children = children or []

precedence = (
    ('left', 'LT', 'GT', 'EQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# --- Program ---
def p_program(p):
    'program : statement_list'
    p[0] = ASTNode('program', children=p[1])

# --- Statement list ---
def p_statement_list_multi(p):
    'statement_list : statement_list statement'
    p[0] = p[1] + [p[2]]

def p_statement_list_single(p):
    'statement_list : statement'
    p[0] = [p[1]]

# --- Block ---
def p_block(p):
    'block : LBRACE statement_list RBRACE'
    begin_scope()
    stmts = p[2]
    end_scope()
    p[0] = ASTNode('block', children=stmts)

# --- Declarations ---
def p_statement_decl_assign(p):
    '''statement : INT ID EQUALS expression SEMICOLON
                 | FLOAT_TYPE ID EQUALS expression SEMICOLON'''
    declare_var(p[2], p[1], line=p.lineno(2))
    assign_var(p[2], p[4].value, line=p.lineno(2))
    p[0] = ASTNode('declare_assign', p[2], [p[4]])

def p_statement_decl(p):
    '''statement : INT ID SEMICOLON
                 | FLOAT_TYPE ID SEMICOLON'''
    declare_var(p[2], p[1], line=p.lineno(2))
    p[0] = ASTNode('declare', p[2])

# --- Assignments ---
def p_statement_assign(p):
    'statement : ID EQUALS expression SEMICOLON'
    assign_var(p[1], p[3].value, line=p.lineno(1))
    p[0] = ASTNode('assign', p[1], [p[3]])

# --- Function Declaration ---
def p_function_decl(p):
    'statement : INT ID LPAREN params RPAREN block'
    declare_func(p[2], 'int', p[4], line=p.lineno(2))

    begin_scope()
    for name, typ in p[4]:
        declare_var(name, typ, line=p.lineno(2))
    body = p[6]
    end_scope()

    # ✅ Wrap raw (name, type) tuples into ASTNodes for visualization
    param_nodes = [ASTNode('param', f'{typ} {name}') for name, typ in p[4]]

    p[0] = ASTNode('func_decl', p[2], [ASTNode('params', children=param_nodes), body])



# --- Function Call ---
def p_statement_func_call(p):
    'statement : ID LPAREN args RPAREN SEMICOLON'
    call_func(p[1], p[3], line=p.lineno(1))
    p[0] = ASTNode('func_call', p[1], p[3])

# --- Return ---
def p_statement_return(p):
    'statement : RETURN expression SEMICOLON'
    p[0] = ASTNode('return', children=[p[2]])

# --- If / Else ---
def p_statement_if(p):
    'statement : IF LPAREN expression RPAREN block'
    p[0] = ASTNode('if', children=[p[3], p[5]])

def p_statement_if_else(p):
    'statement : IF LPAREN expression RPAREN block ELSE block'
    p[0] = ASTNode('if_else', children=[p[3], p[5], p[7]])

# --- While ---
def p_statement_while(p):
    'statement : WHILE LPAREN expression RPAREN block'
    p[0] = ASTNode('while', children=[p[3], p[5]])

# --- For loop ---
def p_statement_for(p):
    'statement : FOR LPAREN statement expression SEMICOLON statement RPAREN block'
    begin_scope()
    init, cond, incr = p[3], p[4], p[6]
    body = ASTNode('block', children=p[8].children + [incr])
    p[0] = ASTNode('block', children=[init, ASTNode('while', children=[cond, body])])
    end_scope()


# --- Parameters and Arguments ---
def p_params_multiple(p):
    'params : params COMMA param'
    p[0] = p[1] + [p[3]]

def p_params_single(p):
    'params : param'
    p[0] = [p[1]]

def p_params_empty(p):
    'params : '
    p[0] = []

def p_param(p):
    '''param : INT ID
             | FLOAT_TYPE ID'''
    p[0] = (p[2], p[1])  # ✅ Returns a tuple (name, type)

def p_args_multiple(p):
    'args : args COMMA expression'
    p[0] = p[1] + [p[3]]

def p_args_single(p):
    'args : expression'
    p[0] = [p[1]]

def p_args_empty(p):
    'args : '
    p[0] = []

# --- Expressions ---
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ASTNode('binop', p[2], [p[1], p[3]])
    p[0].value = 'float' if 'float' in (p[1].value, p[3].value) else 'int'

def p_expression_cmpop(p):
    '''expression : expression LT expression
                  | expression GT expression
                  | expression EQ expression'''
    p[0] = ASTNode('cmpop', p[2], [p[1], p[3]])
    p[0].value = 'bool'

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = ASTNode('number', p[1])
    p[0].value = 'float' if isinstance(p[1], float) else 'int'

def p_expression_id(p):
    'expression : ID'
    p[0] = ASTNode('id', p[1])
    p[0].value = get_var_type(p[1], line=p.lineno(1))

# --- Error ---
def p_error(p):
    if p:
        print(f"\n🔴 Syntax error at token '{p.value}' (line {p.lineno})")
    else:
        print("\n🔴 Syntax error at EOF")

parser = yacc.yacc()