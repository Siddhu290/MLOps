# Data Pipeline — mlops-wine-classifier

## Pipeline Stages
| Stage | Purpose | Input | Output | Log line (this run) |
|---|---|---|---|---|
| Collect | Obtain raw Wine data | sklearn `load_wine` | `data/raw/wine_raw.csv` | `Collected 178 rows` |
| Preprocess | Remove duplicates, fix types, impute medians | `wine_raw.csv` | `data/processed/wine_preprocessed.csv` | `Dropped 0 duplicate rows`, `Preprocessed 178 rows` |
| Feature Engineering | Add "flavanoid_ratio", "color_hue_ratio", "alcohol_proline_index", "alcohol_bin" | `wine_preprocessed.csv` | `data/processed/wine_features.csv` | `Engineered 18 features` |
| Validate | Check schema, nulls, label values and ranges | `wine_features.csv` | PASS / exit code 1 | `Validation PASSED: 178 rows, 18 columns` |

## Flow
```
collect -> preprocess -> features -> validate
```
- `dvc repro` re-runs only the stages whose dependencies changed (hashes in `dvc.lock`); the second run printed `didn't change, skipping` for all four stages.
- `dvc dag` shows the linear graph above.
- `dvc push` sent the 3 stage outputs to `myremote` (`~/dvc-remote-storage`); tag `wine/p3-pipeline-v1` marks this state.

## Validation failure check
Setting row 1 `alcohol` from 14.23 to 50 in `wine_features.csv` gave:
```
[ERROR] 1 rows out of expected range for 'alcohol' (10.0-16.0)
[ERROR] Pipeline halted: Validation failed with 1 error(s)
```
with exit code 1. Re-running the features stage restored the file.
