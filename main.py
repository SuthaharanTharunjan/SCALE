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
    "log": math.log,
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
    if not s or not str(s).strip():
        return []

    s = log_calc(str(s))
    s = trig_calc(s)
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

            while operlist and operlist[-1] != "(":
                prev_op = operlist[-1]
                if op == "^":
                    if precedence.get(prev_op, 0) > precedence.get(op, 0):
                        output.append(operlist.pop())
                    else:
                        break
                else:
                    if precedence.get(prev_op, 0) >= precedence.get(op, 0):
                        output.append(operlist.pop())
                    else:
                        break

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


def value_match_1(match):
    func_name = match.group(1).lower()
    val_stack = calc(match.group(2))
    if not val_stack:
        raise ValueError(f"Empty argument in {func_name}")
    val = val_stack[0]
    result = action[func_name](val)
    return f"{result}"


def trig_calc(string):
    pattern = r"\b(sin|cos|tan)\s*\(([^()]+)\)"
    while re.search(pattern, string):
        string = re.sub(pattern, value_match_1, string)
    return string


def value_match_2(match):
    base_stack = calc(match.group(2))
    val_stack = calc(match.group(3))

    if not base_stack or not val_stack:
        raise ValueError("Invalid logarithmic expression")

    base = base_stack[0]
    val = val_stack[0]

    result = action["log"](val, base)
    return f"{result}"


def log_calc(string):
    pattern = r"\b(log)\s*\(([^()]+)\)\s*\(([^()]+)\)"
    while re.search(pattern, string):
        string = re.sub(pattern, value_match_2, string)
    return string


def main():
    expression = input("Enter the expression: ")
    try:
        result = calc(expression)
        print(result[0] if result else "No input provided.")
    except Exception as e:
        print(f"Error in expression: {e}")


if __name__ == "__main__":
    main()
