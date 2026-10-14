# SRTS-PATR Thermochemical Closure

This pre-publication package contains the eight final **symbolic thermochemical backbones**, a deterministic inference-only evaluator, and held-out CEA test data for the GG and CC closures of the PATR model.

The neural residual, trained residual-DNN weights, checkpoints, and serialized neural-network models are not included. Consequently, errors computed with this package describe the symbolic backbones only and must not be presented as the accuracy of the complete SRTS model.

## Contents

- `models/final_symbolic_models.json`: exact coefficients, retained terms, transformations, and input ranges.
- `docs/FORMULAE.md`: all eight expressions in readable form.
- `src/srts_symbolic.py`: inference-only NumPy evaluator.
- `data/gg_test.csv` and `data/cc_test.csv`: 1,000-row held-out CEA test subsets used only for verification.
- `examples/evaluate_test_data.py`: computes symbolic-only error metrics on the test subsets.

## Quick start

```bash
python -m pip install -r requirements.txt
python examples/evaluate_test_data.py --stage both
```

Programmatic use:

```python
import numpy as np
from src.srts_symbolic import predict_gg, predict_cc

gg_y = predict_gg(np.array([[0.70, 5.0, 600.0]]))
cc_y = predict_cc(np.array([[0.70, 5.0, 600.0, 4.0, 700.0, 0.85, 0.50]]))
```

The evaluator rejects inputs outside the released design ranges by default. Pass `strict=False` only if extrapolation is intentional; extrapolated predictions are not validated.

## Input ranges

| Closure | Variable | Unit | Minimum | Maximum |
|---|---|---:|---:|---:|
| GG | `omr` | 1 | 0.1 | 1.3 |
| GG | `Pt4_MPa` | MPa | 1.0 | 10.0 |
| GG | `TM3_K` | K | 180 | 1080 |
| CC | `omr` | 1 | 0.1 | 1.3 |
| CC | `Pt4_MPa` | MPa | 1.0 | 10.0 |
| CC | `TM3_K` | K | 180 | 1080 |
| CC | `agr` | 1 | 1.0 | 10.0 |
| CC | `Tt51_K` | K | 200 | 1200 |
| CC | `lambda_T` | 1 | 0.7 | 1.0 |
| CC | `Pt7_MPa` | MPa | 0.1 | 1.0 |

The final CC `TM3_K` range is 180–1080 K.

## Test data and package scope

`gg_test.csv` and `cc_test.csv` are 1,000-row held-out NASA CEA test subsets provided only for verification. The complete training dataset and the training pipeline are intentionally not released in this pre-publication package.
