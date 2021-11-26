from parser import ast

code = []

def id_assign(expr):
    res = "" + expr[2] + " = "
    if expr[1] == 'int' or expr[1] == 'float':
        if type(expr[3]) is not tuple:
            res = res + str(float(expr[3]))
        else:
            res = res + operation(expr[3])
    else:
        res = res + str(expr[3])

    code.append(res)

def declare(expr):
    res = "" + expr[1] + " = " + expr[2]
    code.append(res)

def operation(expr):
    res = ""

    if expr[2] == '>' or expr[2] == '>=' or expr[2] == '<' or expr[2] == '>=' or expr[2] == 'and' or expr[2] == 'or' or expr[2] == '==':
        if type(expr[1]) is not tuple:
            res = res + str(expr[1])
        else:
            res = res + str(operation(expr[1]))

        res = res + ' = ' + expr[2] + ' '

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

def assign(expr):
    res = "" + expr[1] + " = "

    if type(expr[2]) is not tuple:
        res = res + str(expr[2])
    else:
        res = res + str(operation(expr[2]))

    code.append(res)

def print_sem(expr):
    res = expr[0] + ' = ' + expr[1]
    code.append(res)

def for_sem(expr):
    code.append('for')
    id_assign(expr[1])
    operation(expr[2])
    assign(expr[3])
    for stm in expr[4]:
        if stm[0] == 'idAssign':
            id_assign(stm)
        elif stm[0] == 'declare':
            declare(stm)
        elif stm[0] == 'assign':
            assign(stm)
        elif stm[0] == 'print':
            print_sem(stm)
        elif stm[0] == 'if':
            if_sem(stm[1])
        elif stm[0] == 'while':
            while_sem(stm)
    code.append('end for')

def if_sem(expr):
    code.append('if')
    operation(expr[1][1])
    for stm in expr[1][2]:
        if stm[0] == 'idAssign':
            id_assign(stm)
        elif stm[0] == 'declare':
            declare(stm)
        elif stm[0] == 'assign':
            assign(stm)
        elif stm[0] == 'for':
            for_sem(stm)
        elif stm[0] == 'print':
            print_sem(stm)
        elif stm[0] == 'if':
            if_sem(stm[1])
        elif stm[0] == 'while':
            while_sem(stm)
    code.append('end if')
    index = 2
    while index < len(expr):
        if len(expr[index]) > 0:
            if expr[index][0][0] == 'elif':
                code.append('elif')
                operation(expr[index][0][1])
                for stm in expr[index][0][2]:
                    if stm[0] == 'idAssign':
                        id_assign(stm)
                    elif stm[0] == 'declare':
                        declare(stm)
                    elif stm[0] == 'assign':
                        assign(stm)
                    elif stm[0] == 'for':
                        for_sem(stm)
                    elif stm[0] == 'print':
                        print_sem(stm)
                    elif stm[0] == 'if':
                        if_sem(stm[1])
                    elif stm[0] == 'while':
                        while_sem(stm)
                code.append('end elif')
            else:
                code.append('else')
                for stm in expr[index][1]:
                    if stm[0] == 'idAssign':
                        id_assign(stm)
                    elif stm[0] == 'declare':
                        declare(stm)
                    elif stm[0] == 'assign':
                        assign(stm)
                    elif stm[0] == 'for':
                        for_sem(stm)
                    elif stm[0] == 'print':
                        print_sem(stm)
                    elif stm[0] == 'if':
                        if_sem(stm[1])
                    elif stm[0] == 'while':
                        while_sem(stm)
                code.append('end else')

        index = index + 1

def while_sem(expr):
    code.append('while')
    operation(expr[1])
    for stm in expr[2]:
        if stm[0] == 'idAssign':
            id_assign(stm)
        elif stm[0] == 'declare':
            declare(stm)
        elif stm[0] == 'assign':
            assign(stm)
        elif stm[0] == 'for':
            for_sem(stm)
        elif stm[0] == 'print':
            print_sem(stm)
        elif stm[0] == 'if':
            if_sem(stm)
        elif stm[0] == 'while':
            while_sem(stm)
    code.append('end while')

for expr in ast:
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