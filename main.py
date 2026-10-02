import operator
import math
import re

NAME = r"""
  __________________     _____  .____     ___________
 /   _____/\_   ___ \   /  _  \ |    |    \_   _____/
 \_____  \ /    \  \/  /  /_\  \|    |     |    __)_ 
 /        \\     \____/    |    \    |___  |        \
/_______  / \______  /\____|__  /_______ \/_______  /
        \/         \/         \/        \/        \/ 
"""

GREEN = "\033[92m"
RESET = "\033[0m"
RED = "\033[91m"
GREEN2 = "\033[38;2;70;185;155m"
BLUE1 = "\033[38;5;67m"
BLUE2 = "\033[38;5;75m"
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
    "exp": math.exp,
    "sqrt": math.sqrt,
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
    "exp": 4,
    "sqrt": 4,
}


def rpn_creator(expression: str):
    output = []
    operlist = []
    pattern = r"\d+\.\d+(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|\d+(?:[eE][-+]?\d+)?|[a-zA-Z]+|[^\s]"
    tokens = re.findall(pattern, expression)
    prev_token = None
    for token in tokens:
        if token in ("+", "-"):
            if prev_token is None or prev_token in action:
                token = "pos" if token == "+" else "neg"

        if token in action:
            if precedence[token] == 4 or token == "^":
                while operlist and (precedence[token] < precedence[operlist[-1]]):
                    output.append(operlist.pop())
            else:
                while operlist and (precedence[token] <= precedence[operlist[-1]]):
                    output.append(operlist.pop())

            operlist.append(token)
        else:
            if token == "e":
                output.append(math.e)
            elif token == "pi":
                output.append(math.pi)
            else:
                try:
                    output.append(float(token))
                except ValueError:
                    pass

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
                "exp",
                "sqrt",
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

    if index_1 is None or index_2 is None:
        raise ValueError("Unbalanced parentheses in expression")

    sub_expression = expression[index_1 + 1 : index_2]
    return sub_expression, index_1, index_2


def main():
    print(NAME)
    print("-" * 60)

    while True:
        try:
            expression = input(f"{BLUE2}Expression{RESET} : {BLUE1}").strip()
        except KeyboardInterrupt, EOFError:
            print(f"{RED}Exiting...{RESET}")
            break
        print(RESET, end="")

        if expression.lower() in ("quit", "exit", "q"):
            print(f"{RED}Exiting...{RESET}")
            break

        print("-" * 65)
        try:
            while ("(" in expression) or (")" in expression):
                sub_expression, idx_start, idx_end = peeler(expression)
                sub_expression_m = evaluate_rpn(rpn_creator(sub_expression))
                expression = (
                    expression[:idx_start]
                    + sub_expression_m
                    + expression[idx_end + 1 :]
                )
                print(f"{GREEN2} = {expression}{RESET}")
            print(f"{GREEN} = {evaluate_rpn(rpn_creator(expression))}{RESET}")
        except Exception as e:
            print(f"{RED}Error : {e}{RESET}")
        print("-" * 65)


if __name__ == "__main__":
    main()
