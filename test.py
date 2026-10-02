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
    "abs": 4,
    "sin": 4,
    "cos": 4,
    "tan": 4,
    "log": 4,
}


def rpn_creator(expression: str):
    expression = expression.replace(" ", "")
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
            if i in ("sin", "cos", "tan", "abs", "neg", "pos"):
                val = stack.pop()
                stack.append(action[i](val))
            else:
                right = stack.pop()
                left = stack.pop()
                stack.append(action[i](left, right))

    return str(stack[0]) if stack else "0.0"


def peeler(expression: str):
    expression = expression.replace(" ", "")
    depth = 0
    index_1 = None
    index_2 = None
    for i in range(len(expression)):
        if expression[i] == "(":
            depth += 1
            index_1 = i
        elif expression[i] == ")":
            depth -= 1
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
