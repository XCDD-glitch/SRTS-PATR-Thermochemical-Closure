"""Evaluate the released symbolic backbones on the public test subset."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.srts_symbolic import predict_cc, predict_gg  # noqa: E402


SPECS = {
    "GG": {
        "file": ROOT / "data" / "gg_test.csv",
        "inputs": ["omr", "Pt4_MPa", "TM3_K"],
        "targets": ["Tt4_K", "kfg", "Rfg_J_per_kgK", "Cp_fg_J_per_kgK"],
        "predict": predict_gg,
    },
    "CC": {
        "file": ROOT / "data" / "cc_test.csv",
        "inputs": ["omr", "Pt4_MPa", "TM3_K", "agr", "Tt51_K", "lambda_T", "Pt7_MPa"],
        "targets": ["Tt7_K", "kfa7", "Rfa7_J_per_kgK", "Cp_fa7_J_per_kgK"],
        "predict": predict_cc,
    },
}


def load_columns(path: Path, names: list[str]) -> np.ndarray:
    table = np.genfromtxt(path, delimiter=",", names=True, dtype=np.float64, encoding="utf-8")
    return np.column_stack([table[name] for name in names])


def metrics(prediction: np.ndarray, target: np.ndarray, names: list[str]) -> dict:
    error = prediction - target
    ape = np.abs(error) / np.maximum(np.abs(target), np.finfo(np.float64).eps) * 100.0
    return {
        "rows": int(len(target)),
        "output_names": names,
        "mape_percent": ape.mean(axis=0).tolist(),
        "p99_ape_percent": np.percentile(ape, 99, axis=0).tolist(),
        "rmse": np.sqrt(np.mean(error**2, axis=0)).tolist(),
        "four_output_mean_mape_percent": float(ape.mean()),
    }


def evaluate(stage: str) -> dict:
    spec = SPECS[stage]
    x = load_columns(spec["file"], spec["inputs"])
    y = load_columns(spec["file"], spec["targets"])
    prediction = spec["predict"](x)
    return metrics(prediction, y, spec["targets"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("GG", "CC", "both"), default="both")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    stages = ("GG", "CC") if args.stage == "both" else (args.stage,)
    results = {stage: evaluate(stage) for stage in stages}
    print(json.dumps(results, indent=2))
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
