import json
import os
from ast import parse
from ast2json import ast2json

assignStatements=[]
branchConditions=[]
loopConditions=[]

#  ------------- function to check type of expression---------------

def checkExpType(data):
    if data['_type'] == 'BoolOp':
        return handleBoolOp(data)
    elif data['_type'] == 'NamedExpr':
        return handleNamedExpr(data)
    elif data['_type'] == 'BinOp':
        return handleBinOp(data)
    elif data['_type'] == 'UnaryOp':
        return handleUnaryOp(data)
    elif data['_type'] == 'Lambda':
        return handleLambda(data)
    elif data['_type'] == 'IfExp':
        return handleIfExp(data)
    elif data['_type'] == 'Dict':
        return handleDict(data)
    elif data['_type'] == 'Set':
        return handleSet(data)
    elif data['_type'] == 'ListComp':
        return handleListComp(data)
    elif data['_type'] == 'SetComp':
        return handleSetComp(data)
    elif data['_type'] == 'DictComp':
        return handleDictComp(data)
    elif data['_type'] == 'GeneratorExp':
        return handleGeneratorExp(data)
    elif data['_type'] == 'Await':
        return handleAwait()
    elif data['_type'] == 'Yield':
        return handleYield(data)
    elif data['_type'] == 'YieldFrom':
        return handleYieldFrom(data)
    elif data['_type'] == 'Compare':
        return handleCompare(data)
    elif data['_type'] == 'Call':
        return handleCall(data)
    elif data['_type'] == 'FormattedValue':
        return handleFormattedValue(data)
    elif data['_type'] == 'JoinedStr':
        return handleJoinedStr(data)
    elif data['_type'] == 'Constant':
        return handleConstant(data)
    elif data['_type'] == 'Attribute':
        return handleAttribute(data)
    elif data['_type'] == 'Subscript':
        return handleSubscript(data)
    elif data['_type'] == 'Starred':
        return handleStarred(data)
    elif data['_type'] == 'Name':
        return handleName(data)
    elif data['_type'] == 'List':
        return handleList(data)
    elif data['_type'] == 'Tuple':
        return handleTuple(data)
    elif data['_type'] == 'Slice':
        return handleSlice(data)

# ---------------------function to check type of statement---------------------

def checkStmtType(data):
    if data['_type'] == 'FunctionDef':
        return handleFunctionDef(data)
    elif data['_type'] == 'AsyncFunctionDef':
        return handleAsyncFunctionDef(data)
    elif data['_type'] == 'ClassDef':
        return handleClassDef(data)
    elif data['_type'] == 'Return':
        return handleReturn(data)
    elif data['_type'] == 'Assign':
        return handleAssign(data)
    elif data['_type'] == 'AugAssign':
        return handleAugAssign(data)
    elif data['_type'] == 'AnnAssign':
        return handleAnnAssign(data)
    elif data['_type'] == 'For':
        return handleFor(data)
    elif data['_type'] == 'AsyncFor':
        return handleAsyncFor(data)
    elif data['_type'] == 'While':
        return handleWhile(data)
    elif data['_type'] == 'If':
        return handleIf(data)
    elif data['_type'] == 'With':
        return handleAsyncWith(data)
    elif data['_type'] == 'Try':
        return handleTry(data)
    elif data['_type'] == 'Assert':
        return handleAssert(data)
    elif data['_type'] == 'Import':
        return handleImport(data)
    elif data['_type'] == 'ImportFrom':
        return handleImportFrom(data)
    elif data['_type'] == 'Global':
        return handleGlobal(data)
    elif data['_type'] == 'Nonlocal':
        return handleNonLocal(data)
    elif data['_type'] == 'Expr':
        return handleExpr(data)
    elif data['_type'] == 'Pass':
        pass
    elif data['_type'] == 'Break':
        pass
    elif data['_type'] == 'Continue':
        pass

# --------------function to check type of operator--------------------------

def checkOperator(data):
    if data['_type'] == 'Add':
        return '+'
    elif data['_type'] == 'Sub':
        return '-'
    elif data['_type'] == 'Mult':
        return '*'
    elif data['_type'] == 'MatMult':
        return"x"
    elif data['_type'] == 'Div':
        return '/'
    elif data['_type'] == 'Mod':
        return '%'
    elif data['_type'] == 'Pow':
        return '**'
    elif data['_type'] == 'LShift':
        return '<<'
    elif data['_type'] == 'RShift':
        return '>>'
    elif data['_type'] == 'BitOr':
        return '|'
    elif data['_type'] == 'BitXor':
        return '^'
    elif data['_type'] == 'BitAnd':
        return '&'
    elif data['_type'] == 'FloorDiv':
        return '//'

# -------------function to check type of compare operator-----------------

def checkCompareOperator(data):
    if data['_type'] == 'Eq':
        return '=='
    elif data['_type'] == 'NotEq':
        return '!='
    elif data['_type'] == 'Lt':
        return '<'
    elif data['_type'] == 'LtE':
        return '<='
    elif data['_type'] == 'Gt':
        return '>'
    elif data['_type'] == 'GtE':
        return '>='
    elif data['_type'] == 'Is':
        return 'is'
    elif data['_type'] == 'IsNot':
        return 'is not'
    elif data['_type'] == 'In':
        return 'in'
    elif data['_type'] == 'NotIn':
        return 'not in'

# --------------function to check type of unary operator---------------

def checkUnaryOperator(data):
    if data['_type'] == 'Invert':
        return '~'
    elif data['_type'] == 'Not':
        return '!'
    elif data['_type'] == 'UAdd':
        return '+'
    elif data['_type'] == 'USub':
        return '+'

# ------------function to check type of expression context--------------------

def checkExprContext(data):
    if data['_type'] == 'Load':
        return "Load"
    if data['_type'] == 'Store':
        return "Store"
    if data['_type'] == 'Del':
        return "Del"

# ----------------function to check type of boolean operator---------------------------
def checkBoolOp(data):
    if data['_type'] == 'And':
        return 'and'
    if data['_type'] == 'Or':
        return 'or'


# ------------------all experession type functions below----------------------

def handleName(data):
    return data['id']


def handleBoolOp(data):
    values = []
    operator = checkBoolOp(data['op'])
    for value in data['values']:
        values.append(str(checkExpType(value)))
    temp = " "+operator+" "
    return temp.join(values)


def handleConstant(data):
    return data['value']


def handleCompare(data):
    left = str(checkExpType(data['left']))
    operators = []
    comparators = []
    for operator in data['ops']:
        operators.append(str(checkCompareOperator(operator)))
    for comparator in data['comparators']:
        comparators.append(str(checkExpType(comparator)))
    result = left
    for i in range(len(operators)):
        result = result + ' ' + operators[i] + ' ' + comparators[i]
    return result


def handleBinOp(data):
    left = str(checkExpType(data['left']))
    operator = str(checkOperator(data['op']))
    right = str(checkExpType(data['right']))
    return left + operator + right


def handleNamedExpr(data):
    target = str(checkExpType(data['target']))
    value = str(checkExpType(data['value']))
    return target + ':=' + value


def handleUnaryOp(data):
    operator = str(checkUnaryOperator(data['op']))
    operand = str(checkExpType(data['operand']))
    return operator + operand


def handleLambda(data):
    args = str(handleArguments(data['args']))
    body = str(checkExpType(data['body']))
    return 'lambda ' + args + ' : ' + body


def handleIfExp(data):
    test = str(checkExpType(data['test']))
    body = str(checkExpType(data['body']))
    orelsepart = str(checkExpType(data['orelse']))
    return body + ' if ' + test + ' else ' + orelsepart


def handleDict(data):
    keys = []
    values = []
    for key in data['keys']:
        keys.append(checkExpType(key))
    for value in data['values']:
        values.append(checkExpType(value))
    result = []
    for i in range(len(keys)):
        result.append('"' + str(keys[i]) + '"' + ':' + str(values[i]))
    return '{' + ','.join(result) + '}'


def handleSet(data):
    elmts = []
    for elt in data['elts']:
        elmts.append(str(checkExpType(elt)))
    return '{' + ','.join(elmts) + '}'


def handleListComp(data):
    elt = str(checkExpType(data['elt']))
    generators = []
    for generator in data['generators']:
        generators.append(str(handleComprehension(generator)))
    return '[' + elt + ' ' + ' '.join(generators) + ']'


def handleSetComp(data):
    elt = str(checkExpType(data['elt']))
    generators = []
    for generator in data['generators']:
        generators.append(str(handleComprehension(generator)))
    return '{' + elt + ' ' + ' '.join(generators) + '}'


def handleDictComp(data):
    key = str(checkExpType(data['key']))
    value = str(checkExpType(data['value']))
    generators = []
    for generator in data['generators']:
        generators.append(str(handleComprehension(generator)))
    return '{' + key + ' : ' + value + ' ' + ' '.join(generators) + '}'


def handleGeneratorExp(data):
    elt = str(checkExpType(data['elt']))
    generators = []
    for generator in data['generators']:
        generators.append(str(handleComprehension(generator)))
    return '(' + elt + ' ' + ' '.join(generators) + ')'


def handleAwait(data):
    value = checkExpType(data['value'])
    return str(value)


def handleYield(data):
    value = checkExpType(data['value'])
    if value is not None:
        return str(value)
    else:
        return 'None'


def handleYieldFrom(data):
    value = str(checkExpType(data['value']))
    return value


def handleCall(data):
    func = checkExpType(data['func'])
    args = []
    keywords = []
    for arg in data['args']:
        args.append(str(checkExpType(arg)))
    for keyword in data['keywords']:
        keywords.append(str(handleKeyword(keyword)))
    if len(keywords) > 0:
        return func + '(' + ','.join(args) + ',' + ','.join(keywords) \
            + ')'
    else:
        return func + '(' + ','.join(args) + ')'


def handleFormattedValue(data):
    checkExpType(data['value'])


def handleJoinedStr(data):
    values = []
    for value in data['values']:
        values.append(str(checkExpType(value)))
    return ' '.join(values)


def handleAttribute(data):
    value = str(checkExpType(data['value']))
    attr = str(data['attr'])
    return value + '.' + attr


def handleSubscript(data):
    value = str(checkExpType(data['value']))
    slice = str(checkExpType(data['slice']))
    return value + "["+slice+"]"


def handleStarred(data):
    return '*' + str(checkExpType(data['value']))


def handleList(data):
    elts = []
    for elt in data['elts']:
        elts.append(checkExpType(elt))
    return elts


def handleTuple(data):
    elts = []
    for elt in data['elts']:
        elts.append(checkExpType(elt))
    return tuple(elts)


def handleSlice(data):
    lower = ''
    upper = ''
    step = ''
    if data['lower'] is not None:
        lower = str(handleConstant(data['lower']))
    if data['upper'] is not None:
        upper = str(handleConstant(data['upper']))
    if data['step'] is not None:
        step = str(handleConstant(data['step']))
    return '[' + lower + ':' + upper + ':' + step + ']'


# --------------------all statement type functions below------------------------------------------------------

def handleAssign(data):
    global assignStatements
    targets = []
    for target in data['targets']:
        targets.append(str(checkExpType(target)))
    right = checkExpType(data['value'])
    assignStatements.append(','.join(targets) + '=' + str(right))


def handleIf(data):
    global branchConditions
    condition = checkExpType(data['test'])
    for body in data['body']:
        checkStmtType(body)
    for orelse in data['orelse']:
        checkStmtType(orelse)
    branchConditions.append(condition)


def handleExpr(data):
    checkExpType(data['value'])


def handleWhile(data):
    global loopConditions
    condition = checkExpType(data['test'])
    for body in data['body']:
        checkStmtType(body)
    for orelse in data['orelse']:
        checkStmtType(orelse)
    loopConditions.append(condition)


def handleFor(data):
    global loopConditions
    target = checkExpType(data['target'])
    iter = checkExpType(data['iter'])
    for stmt in data['body']:
        checkStmtType(stmt)
    for orelse in data['orelse']:
        checkStmtType(orelse)
    loopConditions.append(target + ' in ' + iter)


def handleAsyncFor(data):
    global loopConditions
    target = checkExpType(data['target'])
    iter = checkExpType(data['iter'])
    for stmt in data['body']:
        checkStmtType(stmt)
    for orelse in data['orelse']:
        checkStmtType(orelse)
    loopConditions.append(target + ' in ' + iter)


def handleFunctionDef(data):
    decoratorLists = []
    f_name = data['name']
    args = handleArguments(data['args'])
    for body in data['body']:
        checkStmtType(body)
    for decoratorList in data['decorator_list']:
        decoratorLists.append(checkExpType(decoratorList))
    if data['returns'] is not None:
        checkExpType(data['returns'])


def handleClassDef(data):
    name = data['name']
    bases = []
    for base in data['bases']:
        bases.append(checkExpType(base))
    keywords = []
    for keyword in data['keywords']:
        keywords.append(checkExpType(keyword))
    for body in data['body']:
        checkStmtType(body)
    decoratorList = []
    for decoratorlist in data['decorator_list']:
        decoratorList.append(checkExpType(decoratorlist))


def handleAsyncFunctionDef(data):
    f_name = data['name']
    args = handleArguments(data['args'])
    for body in data['body']:
        checkStmtType(body)
    for decoratorList in data['decorator_list']:
        checkExpType(decoratorList)
    if data['returns'] is not None:
        checkExpType(data['returns'])


def handleReturn(data):
    if data['value'] is not None:
        return data['value']


def handleDelete(data):
    targets = []
    for target in data['targets']:
        targets.append(checkExpType(target))


def handleAugAssign(data):
    global assignStatements
    target = checkExpType(data['target'])
    op = checkOperator(data['op'])
    value = checkExpType(data['value'])
    assignStatements.append(str(target) + str(op)+ '=' + str(value))



def handleAnnAssign(data):
    target = checkExpType(data['target'])
    simple = data['simple']
    annotation = checkExpType(data['annotation'])
    if data['value'] is not None:
        value = checkExpType(data['value'])


def handleWith(data):
    items = []
    for item in data['items']:
        item.append(handleWith(item))
    for body in data['body']:
        checkExpType(body)


def handleAsyncWith(data):
    items = []
    for item in data['items']:
        item.append(handleWith(item))
    for body in data['body']:
        checkExpType(body)


def handleRaise(data):
    if data['exc'] is not None:
        exc = checkExpType(data['exc'])
    if data['cause'] is not None:
        cause = checkExpType(data['cause'])


def handleTry(data):
    for body in data['body']:
        checkExpType(body)
    for handler in data['handlers']:
        handleExceptHandler(handler)
    for orelse in data['orelse']:
        checkStmtType(orelse)
    for finalBody in data['finalbody']:
        checkExpType(finalBody)


def handleAssert(data):
    test = checkExpType(data['assert'])
    if data['msg'] is not None:
        msg = checkExpType(data['msg'])


def handleImport(data):
    names = []
    for name in data['names']:
        names.append(handleAlias(name))


def handleImportFrom(data):
    names = []
    for name in data['names']:
        names.append(handleAlias(name))
    if data['level'] is not None:
        level = data['level']
    if data['module'] is not None:
        module = data['module']


def handleNonLocal(data):
    names = data['names']


def handleGlobal(data):
    names = data['names']


# -------------------------other functions---------------------------------------------

def handleArguments(data):
    posonlyargs = []
    args = []
    defaults = []
    kwdefaults = []
    kwonlyargs = []
    for arg in data['posonlyargs']:
        posonlyargs.append(str(handleArgument(arg)))
    for arg in data['args']:
        args.append(str(handleArgument(arg)))
    vararg = str(data['vararg'])
    kwarg = str(data['kwarg'])
    for kwonlyarg in data['kwonlyargs']:
        kwonlyargs.append(str(handleArgument(kwonlyarg)))
    for default in data['defaults']:
        defaults.append(str(checkExpType(default)))
    for kwdefault in data['kw_defaults']:
        kwdefaults.append(str(checkExpType(kwdefault)))
    return ','.join(args)


def handleArgument(data):
    return str(data['arg'])


def handleExceptHandler(data):
    if data['type'] is not None:
        checkExpType(data['type'])
    name = data['name']
    for body in data['body']:
        checkExpType(body)


def handleComprehension(data):
    target = str(checkExpType(data['target']))
    iter = str(checkExpType(data['iter']))
    ifs = []
    for i in data['ifs']:
        ifs.append('if ' + str(checkExpType(i)))
    is_asyn = data['is_async']
    return 'for ' + target + ' in ' + iter + ' ' + ' '.join(ifs)


def handleAlias(data):
    name = data['name']
    if data['asname'] is not None:
        asname = data['asname']


def handleKeyword(data):
    value = str(checkExpType(data['value']))
    arg = data['arg']
    if arg is not None:
        return str(arg) + '=' + value
    else:
        return ''


def handleWithItem(data):
    context_expr = checkExpType(data['context_expr'])
    if data['optional_vars'] is not None:
        optional_vars = checkExpType(data['optional_vars'])


def parseAst(data):
    for node in data['body']:
        checkStmtType(node)

# ---------------------------------------------------------------------------------------

temp = True
while(temp):
    path = os.path.dirname(__file__)
    print("Enter the file name of test case that you want to run")
    file_name = input()
    new_path = os.path.join(path,"../testcases/"+file_name)
    node = ast2json(parse(open(new_path).read()))

    parseAst(node)
    
    print("\n")
    print('-------All assignment statements---------')
    print("\n".join(assignStatements))
    print("\n")
    print("---------All branch statements----------")
    print("\n".join(branchConditions))
    print("\n")
    print("----------all loop conditions-----------")
    print("\n".join(loopConditions))
    print("\n")
    
    choice = input("Enter any key to continue or 0 to exit: ")
    if choice=='0':
        temp = False
    else:
        temp = True
    print("\n")
    assignStatements.clear()
    loopConditions.clear()
    branchConditions.clear()