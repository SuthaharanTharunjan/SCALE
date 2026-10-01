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
    "neg": 4,
    "pos": 4,
}


def calc(s):
    output = []
    operlist = []
    temp = ""
    expect_operand = True
    for i in s.replace(" ", ""):
        if i.isdigit() or i == ".":
            temp += i
            expect_operand = False
        elif i == "(":
            operlist.append(i)
            expect_operand = True
        elif i == ")":
            if temp:
                output.append(float(temp))
                temp = ""
            while operlist and operlist[-1] != "(":
                output.append(operlist.pop())
            if operlist and operlist[-1] == "(":
                operlist.pop()
            expect_operand = False
        elif i in action.keys():
            if temp:
                output.append(float(temp))
                temp = ""

            if expect_operand and i in ["-", "+"]:
                op = "neg" if i == "-" else "pos"
            else:
                op = i

            while (
                operlist
                and operlist[-1] != "("
                and precedence.get(operlist[-1], 0) >= precedence.get(op, 0)
            ):
                output.append(operlist.pop())

            operlist.append(op)
            expect_operand = True

    if temp:
        output.append(float(temp))

    while operlist:
        output.append(operlist.pop())

    stack = []
    for i in output:
        if isinstance(i, float):
            stack.append(i)
        elif i in action.keys():
            if i in ["neg", "pos", "abs"]:
                val = stack.pop()
                stack.append(action[i](val))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(action[i](left, right))

    return stack


def value_match(match):
    func_name = match.group(1).lower()
    val = calc(match.group(2))[0]
    result = action[func_name](val)
    return f"{result:.2f}"


def trig_calc(string):
    pattern = r"\b(sin|cos|tan)\s*\(\s*([^)]+?)\s*\)"
    return re.sub(pattern, value_match, string)


expression = "(((5+3)*2-8+2^3*sin(5))*(-1))*(-1)"
expression = trig_calc(expression)

print(calc(expression))
