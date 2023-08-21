from inspect import isfunction

from frame import Env
from func import Function

global_env = Env(None)


def plus(values):
    result = 0
    for each in values:
        result += each
    return result
global_env.addVar("+", plus)


def minus(values):
    if len(values) == 1:
        return -1 * values[0]
    result = values[0]
    for each in values[1:]:
        result -= each
    return result
global_env.addVar("-", minus)

def mul(values):
    result = 1
    for each in values:
        result *= each
    return result
global_env.addVar("*", mul)

def lt(values):
    if values[0]<values[1]:
        return "#t"
    else:
        return "#f"
global_env.addVar("<", lt)

def gt(values):
    if values[0]>values[1]:
        return "#t"
    else:
        return "#f"
global_env.addVar(">", gt)

def eq(values):
    if values[0]==values[1]:
        return "#t"
    else:
        return "#f"
global_env.addVar("=", eq)


def tokenise_code(code):
    code = code.strip()

    i = 0
    bracket_cntr = 0
    token = []
    newtoken = []
    while (i + 1) <= len(code):
        if code[i] == " " and bracket_cntr == 0:
            if not newtoken:
                i += 1
                continue
            token.append("".join(newtoken))
            newtoken = []
            i += 1
            continue
        if code[i] == "(":
            bracket_cntr += 1
            if bracket_cntr > 1:
                newtoken.append(code[i])
                i += 1
                continue
            if not newtoken:
                newtoken.append(code[i])
                i += 1
                continue
            token.append("".join(newtoken))
            newtoken = []
            newtoken.append(code[i])
            i += 1
        if code[i] == ")":
            bracket_cntr -= 1
            if bracket_cntr > 0:
                newtoken.append(code[i])
                i += 1
                continue
            newtoken.append(code[i])
            token.append("".join(newtoken))
            newtoken = []
            i += 1
            continue
        newtoken.append(code[i])

        i += 1
    if newtoken:
        token.append("".join(newtoken))
    return token


def tokenise_line(code):
    code = code.removeprefix("(")
    code = code.removesuffix(")")
    code = code.strip()

    # removes excessive whitespace
    i = 0
    bracket_cntr = 0
    token = []
    newtoken = []
    while (i + 1) <= len(code):
        if code[i] == " " and bracket_cntr == 0:
            if not newtoken:
                i += 1
                continue
            token.append("".join(newtoken))
            newtoken = []
            i += 1
            continue
        if code[i] == "(":
            bracket_cntr += 1
            if bracket_cntr > 1:
                newtoken.append(code[i])
                i += 1
                continue
            if not newtoken:
                newtoken.append(code[i])
                i += 1
                continue
            token.append("".join(newtoken))
            newtoken = []
            newtoken.append(code[i])
            i += 1
        if code[i] == ")":
            bracket_cntr -= 1
            if bracket_cntr > 0:
                newtoken.append(code[i])
                i += 1
                continue
            newtoken.append(code[i])
            token.append("".join(newtoken))
            newtoken = []
            i += 1
            continue
        newtoken.append(code[i])

        i += 1
    if newtoken:
        token.append("".join(newtoken))
    return token


def isconstant(line):
    tokenised_line = tokenise_line(line)
    if line.startswith("(") or line.endswith(")"):
        return False
    return (tokenised_line[0].isnumeric()) or (tokenised_line[0].startswith("\'"))


def getconstant(tokenised_line):
    if tokenised_line[0].isnumeric():
        return int(tokenised_line[0])
    else:
        return tokenised_line[0].removeprefix("\'")


def isvar(line):
    tokenised_line = tokenise_line(line)
    if line.startswith("(") or line.endswith(")"):
        return False
    return len(
        tokenised_line) == 1  # for the time being the variable predicamet remains at the end and thus need not be implemented


def lookupvar(varname, env):
    return env.lookupvar(varname)


def getvarname(tokenised_line):
    return tokenised_line[0]


def isdefine(line):
    tokenised_line = tokenise_line(line)
    if tokenised_line[0] == "define":
        return True


#  if len(tokenised_line) > 3:
#      raise Exception("define called with illegal number of arguments")

def define_var_name(tokenised_line):
    return tokenised_line[1]


def define_var_value(tokenised_line):
    return tokenised_line[2]


def islambda(tokenised_line):
    if tokenised_line[0] == "lambda":
        return True


def getlambdaargs(tokenised_line):
    return tokenise_line(tokenised_line[1])


def getlambdabody(tokenised_line):
    tokenised_line.reverse()
    tokenised_line.pop()
    tokenised_line.pop()
    tokenised_line.reverse()
    return tokenised_line


def isfunccall(line):
    tokenised_line = tokenise_line(line)
    if line.startswith("(") or line.endswith(")"):
        return True


def lookupfunc(funcname, env):
    return env.lookupvar(funcname)


def getfuncname(tokenised_line):
    return tokenised_line[0]


def getfuncargs(tokenised_line):
    return tokenised_line[1:len(tokenised_line)]


def applyfunc(func, args,env):
    """the args should be a list of values"""
    if isinstance(func, Function):
        func.applyFunc(args,env)
        result = evalbegin(func.getfuncbody(), func.getfuncenv())
        return result
    else:
        if func in global_env.values:
            result = func(args)
        else:
            raise Exception(str(func) + " is not a function")

    return result


def isif(tokenised_line):
    return tokenised_line[0]=="if"

def getpred(tokenised_line):
    return tokenised_line[1]

def getconsequent(tokenised_line):
    return tokenised_line[2]

def getalternative(tokenised_line):
    if len(tokenised_line)>3:
        return tokenised_line[3]
    else:
        return "nil"

def isnil(tokenised_line):
    return tokenised_line[0]=="nil"

def eval(line, env):
    tokenised_line = tokenise_line(line)
    if isdefine(line):  # define
        env.addVar(define_var_name(tokenised_line), eval(define_var_value(tokenised_line), env))
        return None

    if isif(tokenised_line):
        if eval(getpred(tokenised_line),env)=="#t":
            return eval(getconsequent(tokenised_line),env)
        else:
            return eval(getalternative(tokenised_line),env)

    if isnil(tokenised_line):
        return None

    if islambda(tokenised_line):
        return Function(getlambdaargs(tokenised_line), getlambdabody(tokenised_line))

    if isconstant(line):  # constant
        return getconstant(tokenised_line)

    if isvar(line):  # variable
        return lookupvar(getvarname(tokenised_line), env)

    if isfunccall(line):  # functions
        return applyfunc(eval(getfuncname(tokenised_line), env),
                         evalargs(getfuncargs(tokenised_line), env),env)
    """return applyfunc(lookupfunc(getfuncname(tokenised_line), env),
                         evalargs(getfuncargs(tokenised_line), env),env)"""


def evalargs(args, env):
    env_list = []
    for i in range(len(args)):
        env_list.append(env)
    result = list(map(eval, args, env_list))
    return result

def evalbegin(args, env):
    for i in range(len(args)):
        x = eval(args[i],env)
        if x!=None:
            return x
# //////////////////////////////////////////////////

code = "(define fact" \
       "    (lambda (x)" \
       "        (if (= x 0)" \
       "            1" \
       "            (* x (fact (- x 1))))))" \
       "(fact 10)"

#print(tokenise_line(tokenise_code(code)[0]))
# /////////////////////////////////////////////////


tokenised_code = tokenise_code(code)

for i in range(len(tokenised_code)):
    x = eval(tokenised_code[i], global_env)
    if x != None:
        print(x)
