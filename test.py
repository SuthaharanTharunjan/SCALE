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
    "sinh": math.sinh,
    "asin": math.asin,
    "asinh": math.asinh,
    "cos": math.cos,
    "cosh": math.cosh,
    "acos": math.acos,
    "acosh": math.acosh,
    "tan": math.tan,
    "tanh": math.tanh,
    "atan": math.atan,
    # "atan2": math.atan2,
    "atanh": math.atanh,
    "log": math.log,
    "ln": math.log,
    "lg": math.log10,
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
    "abs": 4,
    "sin": 4,
    "sinh": 4,
    "asin": 4,
    "asinh": 4,
    "cos": 4,
    "cosh": 4,
    "acos": 4,
    "acosh": 4,
    "tan": 4,
    "tanh": 4,
    "atan": 4,
    "atanh": 4,
    "log": 4,
    "lg": 4,
    "ln": 4,
}


def rpn_creator(expression: str):
    output = []
    operlist = []
    tokens = re.findall(r"\d+\.\d+|\d+|[a-zA-Z]+|[^\s]", expression)
    prev_token = None
    for token in tokens:
        if token in ("+", "-"):
            if prev_token is None or prev_token in action:
                token = "pos" if token == "+" else "neg"

        if token.replace(".", "").isdigit():
            output.append(float(token))

        elif token in action:
            if precedence[token] == 4 or token == "^":
                while operlist and (precedence[token] < precedence[operlist[-1]]):
                    output.append(operlist.pop())
            else:
                while operlist and (precedence[token] <= precedence[operlist[-1]]):
                    output.append(operlist.pop())

            operlist.append(token)

        prev_token = token

    while operlist:
        output.append(operlist.pop())

    return output


def evaluate_rpn(rpn_list: list):
    stack = []
    for i in rpn_list:
        if isinstance(i, float):
            stack.append(i)
        elif i in action.keys():
            if i in (
                "sin",
                "sinh",
                "asin",
                "asinh",
                "cos",
                "cosh",
                "acos",
                "acosh",
                "tan",
                "tanh",
                "atan",
                "atanh",
                "abs",
                "neg",
                "pos",
                "lg",
                "ln",
            ):
                val = stack.pop()
                stack.append(action[i](val))
            else:
                right = stack.pop()
                left = stack.pop()
                if i == "log":
                    stack.append(action[i](right, left))
                else:
                    stack.append(action[i](left, right))

    return str(stack[0]) if stack else "0.0"


def peeler(expression: str):
    index_1 = None
    index_2 = None
    for i in range(len(expression)):
        if expression[i] == "(":
            index_1 = i
        elif expression[i] == ")":
            index_2 = i
            break
    sub_expression = expression[index_1 + 1 : index_2]
    return sub_expression


def main():
    expression = input("Enter the expression : ").strip()
    while ("(" in expression) or (")" in expression):
        sub_expression = peeler(expression)
        sub_expression_m = evaluate_rpn(rpn_creator(sub_expression))
        expression = expression.replace(f"({sub_expression})", sub_expression_m)
        print(expression)
    print(evaluate_rpn(rpn_creator(expression)))


if __name__ == "__main__":
    main()
