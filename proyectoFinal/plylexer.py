import ply.lex as lex


reserved = {
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'and': 'AND',
    'or': 'OR',
    'if': 'IF',
    'elif': 'ELIF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'string': 'STRING',
    'bool': 'BOOL',
    'true': 'TRUE',
    'false': 'FALSE',
}
tokens = list(reserved.values()) + [
    'INTNUM',
    'FLOATNUM',
    'ID',
    'STRING',
    'EQUALS',
    'NOTEQUALS',
    'GTREQTHAN',
    'LSSEQTHAN',
    'SENTEND',
    
]

literals = ['+', '-', '*', '/', '=', '^','>', '<', '(', ')', '{', '}', '"']

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    t.type = 'INTNUM'
    return t

def t_FLOATNUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    t.type = 'FLOATNUM'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'ID'
    return t

def t_STRING(t):
    r'"([^"\n]|(\\"))*"'
    t.type = 'STRING'
    return t

t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_GTREQTHAN = r'>='
t_LSSEQTHAN = r'<='
t_SENTEND = r';'
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    errorLine = t.lexer.lineno - 1
    errorToken = t.value[0]

lx = lex.lex()