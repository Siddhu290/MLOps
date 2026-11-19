# Practical 4 — Feast feature store (Wine) — what I must do in the exam

Lab manual: **Experiment 5** — create a feature repository, define/register features, ingest
(materialize) them, retrieve online and offline features, reuse them for a second model, analyse benefits.

## Before starting
```bash
git switch main && git pull origin main
git switch -c wine/practical-4
mkdir -p wine/practical-4-feast && cd wine/practical-4-feast
# create .gitignore FIRST (it must contain .venv*/ and data/), then:
python3.11 -m venv .venv-feast            # Windows: py -3.11 -m venv .venv-feast
source .venv-feast/bin/activate           # Windows Git Bash: source .venv-feast/Scripts/activate
python -m pip install --upgrade pip
pip install feast pandas pyarrow scikit-learn
feast version                             # this run: 0.68.0
git status                                # .venv-feast must NOT appear
```

## Steps

### 1. Scaffold
```bash
git add wine/practical-4-feast/.gitignore wine/practical-4-feast/requirements.txt wine/practical-4-feast/README.md
git commit -m "chore: scaffold practical-4 folder"
```

### 2. Produce the Expt 4 feature CSV (local copy of the pipeline)
```bash
mkdir -p src/pipeline && touch src/pipeline/__init__.py   # paste collect.py, preprocess.py, features.py
python src/pipeline/collect.py       # Collected 178 rows
python src/pipeline/preprocess.py    # Preprocessed 178 rows
python src/pipeline/features.py      # Engineered 18 features -> data/processed/wine_features.csv
git add wine/practical-4-feast/src/pipeline/__init__.py wine/practical-4-feast/src/pipeline/collect.py \
        wine/practical-4-feast/src/pipeline/preprocess.py wine/practical-4-feast/src/pipeline/features.py
git commit -m "feat: add local copy of Expt 4 pipeline scripts"
```

### 3. Feature repository + definitions
```bash
feast init -t local wine_feature_repo
cd wine_feature_repo/feature_repo
rm -rf feature_definitions.py test_workflow.py __pycache__ data/driver_*.parquet
# create feature_store.yaml, feature_columns.py, features.py
```
`features.py` defines: Entity `sample_id` (INT64) · FileSource `data/wine_features.parquet` ·
FeatureView `wine_measurements` (13 Float32) · FeatureView `wine_engineered_features` (3 Float32 + `alcohol_bin` String) · FeatureService `wine_feature_service`. TTL 365 days.
```bash
P=wine/practical-4-feast/wine_feature_repo/feature_repo
git add $P/feature_store.yaml $P/feature_columns.py $P/features.py
git commit -m "feat: define entity, feature views and feature service"
```

### 4. Source data, register, ingest
```bash
python prepare_feature_source.py     # Wrote 178 rows to data/wine_features.parquet
feast apply
```
Actual:
```
Created entity sample_id
Created feature view wine_measurements
Created feature view wine_engineered_features
Created feature service wine_feature_service
Created sqlite table wine_feature_repo_wine_engineered_features
Created sqlite table wine_feature_repo_wine_measurements
```
```bash
feast entities list                  # sample_id  ValueType.INT64
feast feature-views list             # wine_measurements, wine_engineered_features
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
git add $P/prepare_feature_source.py
git commit -m "feat: add Feast source preparation"
```

### 5. Retrieval and reuse
```bash
python get_online_features.py
```
```
sample_id                     0         1         2
alcohol                   14.23      13.2     13.16
alcohol_bin                high    medium    medium
flavanoid_ratio        1.092857  1.041509  1.157143
...
Any None values? False
```
```bash
python get_historical_features.py    # Shape: (5, 19) / Number of rows retrieved: 5
python reuse_features_for_clustering.py
```
```
KMeans cluster counts (178 samples, 3 clusters):
0    62
1    47
2    69
```
```bash
feast feature-services list          # wine_feature_service  (17 features)
git add $P/get_online_features.py $P/get_historical_features.py $P/reuse_features_for_clustering.py
git commit -m "feat: add online, historical and reuse retrieval scripts"
cd ../..
```

### 6. Document and log
```bash
git add wine/practical-4-feast/docs/FEATURE_STORE_ANALYSIS.md && git commit -m "docs: add feature store analysis"
git add wine/practical-4-feast/STEPS.md && git commit -m "docs: add practical-4 step log"
```

## Push and PR
```bash
git ls-files | grep -E '\.csv$|\.parquet$|\.db$|\.joblib$|\.pkl$|venv|mlruns|mlartifacts'   # must print nothing
git push -u origin wine/practical-4
```
GitHub: **Pull requests → New** → base `main` ← compare `wine/practical-4` → Create → Merge.

## What the examiner may check
| Check | Command (inside `wine_feature_repo/feature_repo`) |
|---|---|
| Objects registered | `feast entities list`, `feast feature-views list`, `feast feature-services list` |
| Online store filled | `python get_online_features.py` → `Any None values? False` |
| Point-in-time training data | `python get_historical_features.py` → 5 rows |
| Reuse for another model | `python reuse_features_for_clustering.py` → 3 clusters |
| No parquet/db/venv in Git | `git ls-files wine/practical-4-feast` |

## Viva points
- **What is a feature store?** A central registry + storage for features so training (offline) and serving (online) use the same definitions.
- **Offline vs online store?** Offline (Parquet here) holds full history for training via `get_historical_features`; online (SQLite here) holds latest values for low-latency lookups.
- **What does `materialize-incremental` do?** Copies the latest feature values from the offline source into the online store up to the given timestamp.
- **Why event timestamps?** Point-in-time joins: each training row gets feature values as they were at that moment — no future leakage.
- **Why rename `od280/od315_of_diluted_wines`?** A `/` breaks Feast feature references (`view:feature`), so collect.py renames it `od280_od315_ratio`.

## Mistakes to avoid
- Write `.gitignore` (with `.venv*/` and `data/`) **before** creating the venv, or thousands of files appear in `git status`.
- Run `feast` commands from inside `wine_feature_repo/feature_repo` (where `feature_store.yaml` is).
- Run `prepare_feature_source.py` before `feast apply`/retrieval — it needs `wine/practical-4-feast/data/processed/wine_features.csv` from step 2.
- `feast init` also creates `README.md`, `.gitignore` and `__init__.py` files — they are not needed; don't stage them (or delete them).
- Feast 0.68 creates both `driver_stats.parquet` and `driver_quality_labels.parquet`; `rm data/driver_*.parquet` removes both.
