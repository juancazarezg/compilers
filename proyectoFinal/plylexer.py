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
    'STRINGVAL',
    'EQUALS',
    'NOTEQUALS',
    'GTREQTHAN',
    'LSSEQTHAN',
]

literals = ['=', '+', '-', '*', '/', '^', '(', ')', '{', '}', '<', '>', ';']

t_EQUALS = r'=='
t_NOTEQUALS = r'!='
t_GTREQTHAN = r'>='
t_LSSEQTHAN = r'<='

def t_FLOATNUM(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t):
    r'".*"'
    t.value = t.value.replace("\"", "")
    t.type = reserved.get(t.value, 'STRINGVAL') 
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lx = lex.lex()