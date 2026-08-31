import ast
import operator
import math


_ALLOWED_BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv,
}

_ALLOWED_UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


_ALLOWED_FUNCTIONS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs,
    "round": round,
}


_ALLOWED_CONSTANTS = {
    "pi": math.pi,
    "e": math.e,
}


def _evaluate(node: ast.AST) -> float:
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)

        raise ValueError("Invalid constant.")

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_CONSTANTS:
            return _ALLOWED_CONSTANTS[node.id]

        raise ValueError(
            f"Unknown variable: {node.id}"
        )

    if isinstance(node, ast.BinOp):
        operation = _ALLOWED_BINARY_OPERATORS.get(
            type(node.op)
        )

        if operation is None:
            raise ValueError("Operator not allowed.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_UNARY_OPERATORS.get(
            type(node.op)
        )

        if operation is None:
            raise ValueError("Unary operator not allowed.")

        return operation(_evaluate(node.operand))

    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Function not allowed.")

        function = _ALLOWED_FUNCTIONS.get(
            node.func.id
        )

        if function is None:
            raise ValueError(
                f"Function not allowed: {node.func.id}"
            )

        arguments = [
            _evaluate(argument)
            for argument in node.args
        ]

        return float(function(*arguments))

    raise ValueError(
        f"Expression element not allowed: {type(node).__name__}"
    )


def calculate(expression: str) -> str:
    """
    Safely calculate a mathematical expression.

    Examples:
        calculate("2 + 2")
        calculate("sqrt(25) + 10")
        calculate("2 ** 10")
    """

    expression = expression.strip()

    if not expression:
        raise ValueError("Expression cannot be empty.")

    if len(expression) > 500:
        raise ValueError("Expression is too long.")

    try:
        tree = ast.parse(
            expression,
            mode="eval",
        )

        result = _evaluate(tree.body)

    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.")

    except (SyntaxError, ValueError, TypeError) as exc:
        raise ValueError(
            f"Invalid mathematical expression: {exc}"
        ) from exc

    if not math.isfinite(result):
        raise ValueError(
            "The result is not finite."
        )

    if result.is_integer():
        return str(int(result))

    return f"{result:.12g}"
