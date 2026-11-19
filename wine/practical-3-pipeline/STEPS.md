# Practical 3 — DVC data pipeline (Wine) — what I must do in the exam

Lab manual: **Experiment 4** — data collection, preprocessing, feature engineering, validation,
and automating them as a reproducible DVC pipeline (`dvc.yaml` + `dvc.lock`).

## Before starting
```bash
git switch main && git pull origin main
git switch -c wine/practical-3
mkdir -p wine/practical-3-pipeline && cd wine/practical-3-pipeline
python -m pip install dvc pandas scikit-learn pyyaml
```

## Steps

### 1. Scaffold
`.gitignore` must **not** ignore `data/` (DVC writes its own `data/*/.gitignore`).
```bash
git add wine/practical-3-pipeline/.gitignore wine/practical-3-pipeline/requirements.txt wine/practical-3-pipeline/README.md
git commit -m "chore: scaffold practical-3 folder"
```

### 2. DVC + remote
```bash
dvc init --subdir
git add .dvc .dvcignore && git commit -m "chore: initialize DVC in practical-3"
mkdir -p ~/dvc-remote-storage
dvc remote add -d myremote ~/dvc-remote-storage
git add .dvc/config && git commit -m "chore: configure local DVC remote"
```

### 3. Add each stage, run it, commit it (never the CSV)
```bash
mkdir -p src/pipeline && touch src/pipeline/__init__.py
python src/pipeline/collect.py      # [INFO] Collected 178 rows -> data/raw/wine_raw.csv
git add src/pipeline/__init__.py src/pipeline/collect.py && git commit -m "feat: add collect stage"

python src/pipeline/preprocess.py   # [INFO] Dropped 0 duplicate rows / Preprocessed 178 rows
git add src/pipeline/preprocess.py && git commit -m "feat: add preprocess stage"

python src/pipeline/features.py     # [INFO] Engineered 18 features -> data/processed/wine_features.csv
git add src/pipeline/features.py && git commit -m "feat: add features stage"

python src/pipeline/validate.py     # [INFO] Validation PASSED: 178 rows, 18 columns, all checks satisfied
git add src/pipeline/validate.py && git commit -m "feat: add validate stage"
```
`git status` shows `?? data/` here — that's correct, don't add it.

### 4. Validation failure demo (no commit)
Open `data/processed/wine_features.csv`, change one `alcohol` value (row 1: 14.23) to `50`, save.
```bash
python src/pipeline/validate.py
echo $?
```
Actual:
```
[ERROR] 1 rows out of expected range for 'alcohol' (10.0-16.0)
[ERROR] Pipeline halted: Validation failed with 1 error(s)
1
```
Restore: `python src/pipeline/features.py` (or `dvc repro` once `dvc.yaml` exists).

### 5. Wire the pipeline
```bash
# dvc.yaml: 4 stages, each with cmd / deps / outs (validate has no outs)
git add dvc.yaml && git commit -m "feat: wire pipeline stages in dvc.yaml"
```

### 6. Reproduce
```bash
dvc repro            # Running stage 'collect' ... 'preprocess' ... 'features' ... 'validate'
git add dvc.lock data/raw/.gitignore data/processed/.gitignore
git commit -m "feat: add dvc.lock for reproducible pipeline"
dvc repro            # Stage 'collect' didn't change, skipping  (x4) / Data and pipelines are up to date.
dvc dag              # collect -> preprocess -> features -> validate
dvc push             # 3 files pushed
git tag wine/p3-pipeline-v1
```

### 7. Document and log
```bash
git add wine/practical-3-pipeline/docs/DATA_PIPELINE.md && git commit -m "docs: add data pipeline documentation"
git add wine/practical-3-pipeline/STEPS.md && git commit -m "docs: add practical-3 step log"
```

## Push and PR
```bash
git ls-files | grep -E '\.csv$|\.parquet$|\.db$|\.joblib$|\.pkl$|venv|mlruns|mlartifacts'   # must print nothing
git push -u origin wine/practical-3
git push origin wine/p3-pipeline-v1
```
GitHub: **Pull requests → New** → base `main` ← compare `wine/practical-3` → Create → Merge.

## What the examiner may check
| Check | Command |
|---|---|
| Pipeline runs end to end | `dvc repro` (or `dvc repro -f` to force all stages) |
| Caching works | second `dvc repro` → all stages skipped |
| Stage graph | `dvc dag` |
| Exact hashes recorded | `cat dvc.lock` |
| Validation halts bad data | corrupt a value → `python src/pipeline/validate.py; echo $?` → 1 |
| Outputs on remote | `dvc status -c` → in sync |

## Viva points
- **How does `dvc repro` decide what to re-run?** It compares current MD5s of each stage's `deps` with `dvc.lock`; only stages with a changed dependency (and everything downstream) re-run.
- **Why does validate exit with code 1 instead of warning?** A non-zero exit stops `dvc repro`/CI, so bad data never reaches training.
- **Why is feature logic a pipeline stage, not notebook code?** Versioned, hash-tracked, re-run automatically, and reusable by serving code — avoids training-serving skew.
- **What does `dvc.lock` contain?** The cmd plus md5/size of every dep and out from the last successful run.
- **Why does collect re-run if forced but not otherwise?** Its only dep is `collect.py`; the output changes each run (`collected_at` timestamp) but that doesn't matter unless the stage is triggered.

## Mistakes to avoid
- Don't `git add data/` — the CSVs are DVC outputs; only commit the `data/*/.gitignore` DVC creates.
- `dvc repro` prints `git add dvc.lock data/processed/.gitignore data/raw/.gitignore` — commit exactly those.
- pandas 3.x prints a `Pandas4Warning` about `inplace=True` in preprocess.py — it's only a warning, the stage still succeeds.
- Restore the corrupted CSV after the failure demo, or the next `dvc repro` will re-run features (hash changed).
- The remote is shared with practical 2 (`~/dvc-remote-storage`) — that is fine, objects are addressed by hash.
