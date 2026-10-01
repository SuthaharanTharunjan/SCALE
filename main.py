import operator
import math
import re

action = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "^": operator.pow,
    "neg": operator.neg,
    "pos": operator.pos,
    "abs": operator.abs,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
}
precedence = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
    "%": 2,
    "^": 3,
}
str = "((5+3)*2-8+2^3*sin(5))*(-1)"


def calc(s):
    output = []
    operlist = []
    temp = ""
    for i in s:
        if i.isdigit() or i == ".":
            temp = temp + i
        elif i == "(":
            operlist.append(i)
        elif i == ")":
            if temp:
                output.append(float(temp))
                temp = ""
            while not operlist[-1] == "(":
                output.append(operlist.pop())
            operlist.pop()
        elif i in action.keys():
            if temp:
                output.append(float(temp))
                temp = ""
            if not operlist:
                operlist.append(i)
                continue
            if not operlist[-1] == "(":
                while operlist and (precedence[operlist[-1]] >= precedence[i]):
                    output.append(operlist.pop())
                else:
                    operlist.append(i)
            else:
                operlist.append(i)
    if temp:
        output.append(float(temp))
    operlist.reverse()
    output = output + operlist

    stack = []
    for i in output:
        if isinstance(i, float):
            stack.append(i)
        elif i in action.keys():
            right = stack.pop()
            left = stack.pop()
            stack.append(action[i](left, right))

    return stack


def value_match(match):
    func_name = match.group(1).lower()
    val = calc(match.group(2))[0]
    result = action[func_name](val)
    if result < 0:
        return f"(0-{abs(result):.2f})"
    return f"{result:.2f}"


def trig_calc(string):
    pattern = r"\b(sin|cos|tan)\s*\(\s*([^)]+?)\s*\)"
    return re.sub(pattern, value_match, string)


str = trig_calc(str)
trig_calc(str)
print(calc(str))
