# Data dictionary

## GG test data

| Column | Unit | Meaning |
|---|---:|---|
| `omr` | 1 | LOX/LCH₄ mixture ratio |
| `Pt4_MPa` | MPa | Gas-generator chamber pressure |
| `TM3_K` | K | Methane inlet temperature |
| `Tt4_K` | K | CEA reference gas-generator temperature |
| `kfg` | 1 | CEA reference specific-heat ratio |
| `Rfg_J_per_kgK` | J/(kg K) | CEA reference gas constant |
| `Cp_fg_J_per_kgK` | J/(kg K) | CEA reference constant-pressure specific heat |

## CC test data

| Column | Unit | Meaning |
|---|---:|---|
| `omr` | 1 | LOX/LCH₄ mixture ratio |
| `Pt4_MPa` | MPa | Upstream pressure input used by the CC closure |
| `TM3_K` | K | Methane inlet temperature |
| `agr` | 1 | Air-to-rich-gas ratio |
| `Tt51_K` | K | Turbine-exit total temperature |
| `lambda_T` | 1 | Turbine temperature-ratio variable supplied to the closure |
| `Pt7_MPa` | MPa | Combustor total pressure |
| `Tt7_K` | K | CEA reference combustor temperature |
| `kfa7` | 1 | CEA reference specific-heat ratio |
| `Rfa7_J_per_kgK` | J/(kg K) | CEA reference gas constant |
| `Cp_fa7_J_per_kgK` | J/(kg K) | CEA reference constant-pressure specific heat |

The files contain 1,000 held-out CEA samples for verification of the released symbolic backbones.
