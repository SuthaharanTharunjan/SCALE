import operator
import math
import re

NAME = r"""
   __________________     _____  .____     ___________
  /===_____/\_===___ \   /==_==\ |====|    \_===_____/
  \_____==\ /====\  \/  /==/_\==\|====|     |====__)_ 
  /========\\=====\____/====|====\====|___  |========\
 /_______==/ \______==/\____|__==/_______ \/_______==/
         \/         \/         \/        \/        \/ 
"""

RED = "\033[38;2;255;0;127m"  # Hot Magenta (Errors/Exiting)
GREEN = "\033[38;2;46;204;113m"  # Natural Emerald (Startup)
BLUE = "\033[38;2;52;152;219m"  # Clear Sky Blue (Input/Final Answer)
GREY = "\033[38;2;77;77;115m"  # Deep Violet-Slate (Dividers)
VIOLET = "\033[38;2;179;136;255m"  # Electric Violet (Steps)
RESET = "\033[0m"

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
    "d": math.radians,
    "r": math.degrees,
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
    "d": 4,
    "r": 4,
}

single_arg_operators = (
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
    "d",
    "r",
)

TOKEN_PATTERN = re.compile(
    r"\d+\.\d+(?:[eE][-+]?\d+)?|\.\d+(?:[eE][-+]?\d+)?|\d+(?:[eE][-+]?\d+)?|[a-zA-Z]+|[^\s]"
)

FUNC_PATTERN = re.compile(
    r"(?<![a-zA-Z])(?:sin|sinh|asin|asinh|cos|cosh|acos|acosh|tan|tanh|atan|atanh|log|ln|lg|exp|sqrt|abs|d|r)(?![a-zA-Z])|[+/*%^\-]"
)

BRACKET_PATTERN = re.compile(
    r"\)(?=[(a-zA-Z0-9])|(?<![a-zA-Z])(?:e|pi)(?=\()|\d+(?=[(a-df-zA-DF-Z]|(?:e|E)(?![+-]?\d))"
)


def rpn_creator(expression: str):
    output = []
    operlist = []
    tokens = TOKEN_PATTERN.findall(expression)
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
                    raise ValueError(f"Unrecognized mathematical token: '{token}'")

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
            if i in single_arg_operators:
                val = stack.pop()
                stack.append(action[i](val))
            else:
                right = stack.pop()
                left = stack.pop()
                if i == "log":
                    stack.append(action[i](right, left))
                else:
                    stack.append(action[i](left, right))

    if len(stack) > 1:
        raise ValueError("Missing operator between numbers")

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


def colorize_operators(text: str, base_color: str) -> str:
    colored_text = FUNC_PATTERN.sub(lambda m: f"{base_color}{m.group(0)}{RESET}", text)
    return f"{RESET}{colored_text}"


def format_display(val: float) -> str:
    if abs(val) < 1e-12:
        val = 0.0
    elif abs(val - round(val)) < 1e-12:
        val = float(round(val))
    else:
        val = round(val, 12)
    return f"{val:g}"


def main():
    print(NAME)
    print(f"{GREEN}Starting...{RESET}")
    print(f"{GREY}-{RESET}" * 65)

    while True:
        try:
            expression = input(f"Expression : {BLUE}").strip()
            print(RESET, end="")
        except (KeyboardInterrupt, EOFError):
            print(f"{BLUE}quit{RESET}")
            expression = "quit"

        if not expression:
            continue
        expression = expression.lower()

        if expression in ("quit", "exit", "q"):
            print(f"{GREY}-{RESET}" * 65)
            print(f"{RED}Exiting...{RESET}")
            break

        print(f"{GREY}-{RESET}" * 65)

        expression = BRACKET_PATTERN.sub(lambda m: f"{m.group(0)}*", expression)

        print(f"{GREY} = {RESET}{colorize_operators(expression, VIOLET)}")

        try:
            while ("(" in expression) or (")" in expression):
                sub_expression, idx_start, idx_end = peeler(expression)
                sub_expression_m = evaluate_rpn(rpn_creator(sub_expression))
                expression = (
                    expression[:idx_start]
                    + f"{sub_expression_m}"
                    + expression[idx_end + 1 :]
                )
                print(f"{GREY} = {RESET}{colorize_operators(expression, VIOLET)}")

            ans = evaluate_rpn(rpn_creator(expression))
            print(f"{GREY} = {RESET}{ans}")

            formatted_ans = format_display(float(ans))
            print(f"{GREY} ≈ {BLUE}{formatted_ans}{RESET}")

        except IndexError:
            print(f"{RED}Error : Invalid syntax or missing operands{RESET}")

        except Exception as e:
            print(f"{RED}Error : {e}{RESET}")
        print(f"{GREY}-{RESET}" * 65)


if __name__ == "__main__":
    main()
