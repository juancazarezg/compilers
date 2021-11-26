import ply.yacc as yacc
import plylexer

tokens = plylexer.tokens
literals = plylexer.literals

precedence = (
    ('right', '='),
    ('left', 'EQUALS', 'NOTEQUALS'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('left', '^'),
    ('left', 'AND', 'OR'),
    ('nonassoc', '<', '>', 'GTREQTHAN', 'LSSEQTHAN'),
    ('right', 'UMINUS')
)

def p_start(p):
    '''ast : statement'''
    global ast
    ast = p[1]

def p_statement(p):
    '''statement : for statement
                 | while statement
                 | if statement
                 | declare ';' statement
                 | print ';' statement
                 | '''
    if len(p) > 2:
        if p[2] == ';':
            p[2] = p[3]
        p[0] = (p[1],) + p[2]
    else:
        p[0] = ()

def p_while(p):
    '''while : WHILE '(' expression ')' '{' statement '}' '''
    p[0] = ('while', p[3], p[6])

def p_for(p):
    '''for : FOR '(' assign ';' expression ';' declareAssign ')' '{' statement '}' '''
    p[0] = ('for', p[3], p[5], p[7], p[10])

def p_if(p):
    '''if : IF '(' expression ')' '{' statement '}' elif else '''
    p[0] = ('if', p[3], p[6])

def p_elif(p):
    '''elif : ELIF '(' expression ')' '{' statement '}' elif
                 | '''
    if len(p) > 2:
        p[0] = (('elif', p[3], p[6]),) + p[8]
    else:
        p[0] = ()

def p_else(p):
    '''else : ELSE '{' statement '}'
            | '''
    if len(p) > 2:
        p[0] = ('else', p[3])

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING
            | BOOL'''
    p[0] = p[1]

def p_declare(p):
    '''declare : declaration
               | assign
               | declareAssign'''
    p[0] = p[1]

def p_declaration(p):
    '''declaration : type ID'''
    p[0] = ('declare', p[1], p[2])

def p_assign(p):
    '''assign : type ID '=' expression'''
    p[0] = ('declareAssign', p[1], p[2], p[4])

def p_declareAssign(p):
    '''declareAssign : ID '=' expression'''
    p[0] = ('assign', p[1], p[3])
    p[0] = ('assign', p[1], p[3])

def p_print(p):
    'print : PRINT expression'
    # print(p[2])
    p[0] = ('print', p[2])

def p_expression_operation(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '^' expression
                  | expression EQUALS expression
                  | expression NOTEQUALS expression
                  | expression GTREQTHAN expression
                  | expression LSSEQTHAN expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = ('operation', p[1], p[2], p[3])

def p_expression_uminus(p):
    '''expression : '-' expression %prec UMINUS'''
    p[0] = -p[2]

def p_expression_group(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

def p_expression_number(p):
    '''expression : INTNUM
                  | FLOATNUM
                  | STRINGVAL
                  | boolval'''
    p[0] = p[1]

def p_boolVal(p):
    '''boolval : TRUE
               | FALSE'''
    if p[1] == "true":
        p[0] = True
    elif p[1] == "false":
        p[0] = False

def p_expression_ID(p):
    "expression : ID"
    p[0] = p[1]

def p_error(t):
    if t:
        print("Syntax error at '%s'" % t.value)
    else:
        print("Syntax error at EOF")

yacc.yacc()
file = open("input.txt", "r")
s = file.read()
yacc.parse(s)

file = open('ast.txt', 'w')
file.write('AST:' + '\n')
file.write('\n')
file.write(str(ast))
file.close()

print('AST generated on ast.txt file')