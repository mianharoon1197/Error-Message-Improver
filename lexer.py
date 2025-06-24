import ply.lex as lex
from errors import record

# --- Global cache to avoid repeated lexer errors ---
_seen_lexer_errors = set()

reserved = {
    'int': 'INT',
    'float': 'FLOAT_TYPE',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'return': 'RETURN'
}

tokens = [
    'ID', 'NUMBER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS',
    'LT', 'GT', 'EQ',
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'SEMICOLON', 'COMMA'
] + list(reserved.values())

t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUALS     = r'='
t_LT         = r'<'
t_GT         = r'>'
t_EQ         = r'=='
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_LBRACE     = r'\{'
t_RBRACE     = r'\}'
t_SEMICOLON  = r';'
t_COMMA      = r','

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t\r'

def t_error(t):
    char = t.value[0]
    key = (t.lineno, char)
    if key not in _seen_lexer_errors:
        _seen_lexer_errors.add(key)
        record(
            t.lineno,
            f"Invalid character '{char}'",
            "Syntax",
            f"Remove or replace '{char}' with a valid symbol or identifier."
        )
    t.lexer.skip(1)

lexer = lex.lex()
