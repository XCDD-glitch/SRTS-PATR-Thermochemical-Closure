"""Inference-only evaluator for the released GG and CC symbolic backbones."""

from __future__ import annotations

import ast
import json
from functools import lru_cache
from pathlib import Path

import numpy as np


MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "final_symbolic_models.json"


@lru_cache(maxsize=1)
def _models() -> dict:
    return json.loads(MODEL_PATH.read_text(encoding="utf-8"))


def _evaluate_ast(node: ast.AST, variables: dict[str, np.ndarray]) -> np.ndarray | float:
    if isinstance(node, ast.Expression):
        return _evaluate_ast(node.body, variables)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _evaluate_ast(node.operand, variables)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left = _evaluate_ast(node.left, variables)
        right = _evaluate_ast(node.right, variables)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left**right
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "sqrt"
        and len(node.args) == 1
        and not node.keywords
    ):
        return np.sqrt(_evaluate_ast(node.args[0], variables))
    raise ValueError(f"Unsupported symbolic term: {ast.dump(node, include_attributes=False)}")


@lru_cache(maxsize=None)
def _parsed(expression: str) -> ast.Expression:
    return ast.parse(expression, mode="eval")


def _predict(stage: str, physical_inputs: np.ndarray, *, strict: bool) -> np.ndarray:
    config = _models()["stages"][stage]
    x = np.asarray(physical_inputs, dtype=np.float64)
    if x.ndim == 1:
        x = x.reshape(1, -1)
    expected = len(config["input_names"])
    if x.ndim != 2 or x.shape[1] != expected:
        raise ValueError(f"{stage} expects shape (n, {expected}); received {x.shape}")
    low = np.asarray(config["domain_low"], dtype=np.float64)
    high = np.asarray(config["domain_high"], dtype=np.float64)
    if strict and (np.any(x < low) or np.any(x > high)):
        bad = np.argwhere((x < low) | (x > high))[0]
        row, column = int(bad[0]), int(bad[1])
        name = config["input_names"][column]
        raise ValueError(
            f"Input outside released design range: row={row}, variable={name}, "
            f"value={x[row, column]:.12g}, range=[{low[column]:.12g}, {high[column]:.12g}]"
        )
    u = (x - low) / (high - low)
    variables = {f"u{i}": u[:, i] for i in range(u.shape[1])}
    columns = []
    for output_name in config["output_order"]:
        model = config["outputs"][output_name]
        prediction = np.full(x.shape[0], float(model["intercept"]), dtype=np.float64)
        for term in model["terms"]:
            prediction += float(term["coefficient"]) * _evaluate_ast(
                _parsed(term["expression"]), variables
            )
        columns.append(prediction)
    return np.column_stack(columns)


def predict_gg(physical_inputs: np.ndarray, *, strict: bool = True) -> np.ndarray:
    """Return [Tt4_K, kfg, Rfg_J_per_kgK, Cp_fg_J_per_kgK]."""
    return _predict("GG", physical_inputs, strict=strict)


def predict_cc(physical_inputs: np.ndarray, *, strict: bool = True) -> np.ndarray:
    """Return [Tt7_K, kfa7, Rfa7_J_per_kgK, Cp_fa7_J_per_kgK]."""
    return _predict("CC", physical_inputs, strict=strict)
