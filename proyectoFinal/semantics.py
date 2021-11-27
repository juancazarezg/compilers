from parser import ast

code = []

def assign(expr):
    res = "" + expr[2] + " = "
    if expr[1] == 'int' or expr[1] == 'float':
        if type(expr[3]) is not tuple:
            res = res + str(float(expr[3]))
        else:
            res = res + str(operation(expr[3]))
    else:
        res = res + str(expr[3])

    code.append(res)

def declare(expr):
    res = "" + expr[1] + " = " + expr[2]
    code.append(res)

def id_assign(expr):
    res = "" + expr[1] + " = "

    if type(expr[2]) is not tuple:
        res = res + str(expr[2])
    else:
        res = res + str(operation(expr[2]))
    code.append(res)

def operation(expr):
    res = ""

    if expr[2] == '>' or expr[2] == '>=' or expr[2] == '<' or expr[2] == '>=' or expr[2] == 'and' or expr[2] == 'or' or expr[2] == '==':
        if type(expr[1]) is not tuple:
            res = res + str(expr[1])
        else:
            res = res + str(operation(expr[1]))

        res = res + ' ' + expr[2] + ' '

        if type(expr[3]) is not tuple:
            res = res + str(expr[3])
        else:
            res = res + str(operation(expr[3]))

        code.append(res)

    else:
        resultExpr = 0
        if type(expr[1]) is not tuple:
            if type(expr[1]) is int or float:
                resultExpr = expr[1]

            res = res + str(expr[1])
        else:
            resultExpr = operation(expr[1])
            res = res + str(resultExpr)

        if expr[2] == '+':
            res = res + ' + '
        elif expr[2] == '-':
            res = res + ' - '
        elif expr[2] == '*':
            res = res + ' * '
        elif expr[2] == '/':
            res = res + ' / '
        elif expr[2] == '^':
            res = res + ' ^ '

        if type(expr[3]) is not tuple:
            if expr[2] == '+' and type(expr[3]) is not str:
                if type(resultExpr) is not str:
                    resultExpr = resultExpr + expr[3]
                else:
                    resultExpr = expr[3]
            elif expr[2] == '-' and type(expr[3]) is not str:
                if type(resultExpr) is not str:
                    resultExpr = resultExpr - expr[3]
                else:
                    resultExpr = expr[3]
            elif expr[2] == '*' and type(expr[3]) is not str:
                if type(resultExpr) is not str:
                    resultExpr = resultExpr * expr[3]
                else:
                    resultExpr = expr[3]
            elif expr[2] == '/' and type(expr[3]) is not str:
                if type(resultExpr) is not str:
                    resultExpr = resultExpr / expr[3]
                else:
                    resultExpr = expr[3]
            elif expr[2] == '^' and type(expr[3]) is not str:
                if type(resultExpr) is not str:
                    resultExpr = resultExpr ** expr[3]
                else:
                    resultExpr = expr[3]

            res = res + str(expr[3])

        elif type(expr[3]) is str:
            res = res + expr[3]
            code.append(res)
            return res

        else:
            opRes = 0

            if expr[2] == '+':
                op = operation(expr[3])
                resultExpr = resultExpr + op
                opRes = op
            elif expr[2] == '-':
                op = operation(expr[3])
                resultExpr = resultExpr - op
                opRes = op
            elif expr[2] == '*':
                op = operation(expr[3])
                resultExpr = resultExpr * op
                opRes = op
            elif expr[2] == '/':
                op = operation(expr[3])
                resultExpr = resultExpr / op
                opRes = op
            elif expr[2] == '^':
                op = operation(expr[3])
                resultExpr = resultExpr ** op
                opRes = op

            res = res + str(opRes)

        code.append(res)
        return resultExpr


def print_sem(expr):
    if type(expr[1]) is not tuple:
        res = expr[0] + ' = ' + expr[1]
        code.append(res)
    else:
        res = expr[0] + ' = ' + str(operation(expr[1]))
        code.append(res)

def for_sem(expr):
    code.append('for')
    assign(expr[1])
    operation(expr[2])
    id_assign(expr[3])
    for stm in expr[4]:
        callMethod(stm)
    code.append('end for')

def if_sem(expr):
    code.append('if')
    operation(expr[1])
    for stm in expr[2]:
        callMethod(stm)
    index = 2
    code.append('end if')

def while_sem(expr):
    code.append('while')
    operation(expr[1])
    for stm in expr[2]:
        callMethod(stm)
    code.append('end while')

def callMethod(expr):
    if expr[0] == 'idAssign':
        id_assign(expr)
    elif expr[0] == 'declare':
        declare(expr)
    elif expr[0] == 'assign':
        assign(expr)
    elif expr[0] == 'for':
        for_sem(expr)
    elif expr[0] == 'print':
        print_sem(expr)
    elif expr[0] == 'if':
        if_sem(expr)
    elif expr[0] == 'while':
        while_sem(expr)

for expr in ast:
    callMethod(expr)

print()
print("TAC: ")
print()

file = open('tac.txt', 'w')
for expr in code:
    print(expr)
    file.write(expr + '\n')
file.close()

print()
print('TAC generated on tac.txt file')
print()