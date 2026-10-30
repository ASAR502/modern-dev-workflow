"""Lightweight, dependency-free tools the agent can call on demand.

Each function has a docstring describing when it should be used — the model
reads these to decide which tool to call for a given query.
"""

import ast
import math
import operator
import random
import re
from datetime import datetime

__all__ = [
    "calculate",
    "get_current_time",
    "text_stats",
    "estimate_tokens",
    "pick_random",
]

_CALC_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}
_CALC_FUNCS = {
    "sqrt": math.sqrt,
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
}
_CALC_CONSTS = {"pi": math.pi, "e": math.e, "tau": math.tau}


def _eval_math(node: ast.AST) -> float:
    if isinstance(node, ast.Expression):
        return _eval_math(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _CALC_OPS:
        left, right = _eval_math(node.left), _eval_math(node.right)
        if isinstance(node.op, ast.Pow) and (abs(right) > 100 or abs(left) > 1_000_000):
            raise ValueError("exponent too large")
        return _CALC_OPS[type(node.op)](left, right)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _CALC_OPS:
        return _CALC_OPS[type(node.op)](_eval_math(node.operand))
    if isinstance(node, ast.Name) and node.id in _CALC_CONSTS:
        return _CALC_CONSTS[node.id]
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in _CALC_FUNCS
    ):
        return _CALC_FUNCS[node.func.id](*[_eval_math(arg) for arg in node.args])
    raise ValueError("unsupported expression")


def calculate(expression: str) -> str:
    """Evaluate a math expression exactly, e.g. '12 * (3 + 4)' or 'sqrt(144) + pi'.
    Use whenever the user asks an arithmetic, percentage, or math question."""
    try:
        result = _eval_math(ast.parse(expression, mode="eval"))
    except Exception:
        return (
            f"Could not evaluate '{expression}'. Supported: numbers, + - * / // % **, "
            "sqrt, abs, round, min, max, log, log10, exp, sin, cos, tan, pi, e, tau."
        )
    return f"{expression} = {result}"


def get_current_time() -> str:
    """Get the current date and time on this machine.
    Use when the user asks about today's date, the current time, or needs 'now' as context."""
    return datetime.now().strftime("%A, %B %d, %Y — %I:%M:%S %p")


def text_stats(text: str) -> str:
    """Count words, characters, and sentences in a piece of text.
    Use when the user asks how long a text is or wants word or character counts."""
    words = text.split()
    sentences = [s for s in re.split(r"[.!?]+", text) if s.strip()]
    return f"Words: {len(words)} | Characters: {len(text)} | Sentences: {len(sentences)}"


def estimate_tokens(text: str) -> str:
    """Roughly estimate how many LLM tokens a text would use (~4 characters per token).
    Use when the user asks about token counts, prompt size, or context-window usage."""
    return f"~{max(1, round(len(text) / 4))} tokens (rule of thumb: ~4 characters per token)"


def pick_random(options: str) -> str:
    """Pick one option at random from a comma-separated list.
    Use when the user asks you to choose or randomly pick between given options."""
    choices = [option.strip() for option in options.split(",") if option.strip()]
    if not choices:
        return "No options given — pass a comma-separated list."
    return f"I picked: {random.choice(choices)}"
