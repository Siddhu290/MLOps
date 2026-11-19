# Practical 5 — MLflow tracking and registry (Wine)

Branch: `wine/practical-5` · Folder: `wine/practical-5-mlflow/` · Lab manual: Expt 6

Run every command below from inside this folder unless it says otherwise.

```bash
git switch main && git pull origin main
git switch -c wine/practical-5
cd wine/practical-5-mlflow
```

## Steps

```bash
py -3.11 -m venv .venv-mlflow
source .venv-mlflow/Scripts/activate
python -m pip install --upgrade pip
pip install mlflow==2.17.2 "sqlalchemy<2.1" scikit-learn pandas matplotlib

# 1. Produce the Expt 4 feature file (this folder carries its own copy of the pipeline)
python src/pipeline/collect.py
python src/pipeline/preprocess.py
python src/pipeline/features.py        # -> data/processed/wine_features.csv

# 2. Terminal 1 (leave running)
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000
```

Terminal 2:

```bash
cd MLOps/wine/practical-5-mlflow
source .venv-mlflow/Scripts/activate
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
python src/train_with_mlflow.py        # 3 runs in experiment wine-classification-baseline
python src/register_best_model.py      # wine-classifier-prod v1 -> Staging
python src/load_registered_model.py
```

Open http://127.0.0.1:5000 → experiment → select all 3 runs → Compare; Models tab shows `wine-classifier-prod` Version 1 in Staging.
Stop the server (Ctrl+C in Terminal 1) before `git add`, so `mlflow.db` is not locked.

## Submit

```bash
cd ../..                               # back to the repo root
git status                             # check: no .venv, data CSVs or mlflow.db listed
git add wine/practical-5-mlflow
git commit -m "feat: complete practical 5 - MLflow tracking and registry"
git push -u origin wine/practical-5
```

On GitHub: **Compare & pull request** → base `main`, compare `wine/practical-5` → Create → Merge pull request → Confirm merge.
