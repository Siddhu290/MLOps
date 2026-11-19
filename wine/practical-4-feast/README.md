# Practical 4 — Feast feature store (Wine)

Branch: `wine/practical-4` · Folder: `wine/practical-4-feast/` · Lab manual: Expt 5

Run every command below from inside this folder unless it says otherwise.

```bash
git switch main && git pull origin main
git switch -c wine/practical-4
cd wine/practical-4-feast
```

## Steps

```bash
py -3.11 -m venv .venv-feast
source .venv-feast/Scripts/activate
python -m pip install --upgrade pip
pip install feast pandas pyarrow scikit-learn

# 1. Produce the Expt 4 feature file (this folder carries its own copy of the pipeline)
python src/pipeline/collect.py
python src/pipeline/preprocess.py
python src/pipeline/features.py        # -> data/processed/wine_features.csv

# 2. Feature repository
feast init -t local wine_feature_repo
cd wine_feature_repo/feature_repo
rm -rf feature_definitions.py test_workflow.py __pycache__ data/driver_*.parquet
# create feature_store.yaml, feature_columns.py, features.py, prepare_feature_source.py,
# get_online_features.py, get_historical_features.py, reuse_features_for_clustering.py

python prepare_feature_source.py       # Wrote 178 rows to data/wine_features.parquet
feast apply                            # 1 entity, 2 feature views, 1 feature service
feast entities list
feast feature-views list
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
python get_online_features.py          # Any None values? False
python get_historical_features.py      # 5 rows
python reuse_features_for_clustering.py   # KMeans with 3 clusters
feast feature-services list
cd ../..                               # back to wine/practical-4-feast
```

If `feast init` says the folder already exists (it does when you start from the zip), skip it and the `rm` line.

## Submit

```bash
cd ../..                               # back to the repo root
git status                             # check: no .venv, data CSVs or mlflow.db listed
git add wine/practical-4-feast
git commit -m "feat: complete practical 4 - Feast feature store"
git push -u origin wine/practical-4
```

On GitHub: **Compare & pull request** → base `main`, compare `wine/practical-4` → Create → Merge pull request → Confirm merge.
