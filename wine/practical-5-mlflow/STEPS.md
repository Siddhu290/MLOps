# Practical 5 — MLflow tracking + model registry (Wine) — what I must do in the exam

Lab manual: **Experiment 6** — configure MLflow, train models, log parameters/metrics/artifacts,
compare runs, register the best model, move it to Staging and load it back from the registry.

## Before starting
```bash
git switch main && git pull origin main
git switch -c wine/practical-5
mkdir -p wine/practical-5-mlflow && cd wine/practical-5-mlflow
# .gitignore FIRST: .venv*/ data/ models/ mlruns/ mlartifacts/ mlflow.db confusion_matrix_*.png
python3.11 -m venv .venv-mlflow           # Windows: py -3.11 -m venv .venv-mlflow
source .venv-mlflow/bin/activate          # Windows Git Bash: source .venv-mlflow/Scripts/activate
python -m pip install --upgrade pip
pip install mlflow==2.17.2 "sqlalchemy<2.1" scikit-learn pandas matplotlib
mlflow --version                          # mlflow, version 2.17.2
```

## Steps

### 1. Scaffold
```bash
git add wine/practical-5-mlflow/.gitignore wine/practical-5-mlflow/requirements.txt wine/practical-5-mlflow/README.md
git commit -m "chore: scaffold practical-5 folder"
```

### 2. Produce the feature CSV (local copy of Expt 4 pipeline)
```bash
mkdir -p src/pipeline && touch src/pipeline/__init__.py   # paste collect.py, preprocess.py, features.py
python src/pipeline/collect.py && python src/pipeline/preprocess.py && python src/pipeline/features.py
# -> data/processed/wine_features.csv (178 rows, 18 columns)
git add wine/practical-5-mlflow/src/pipeline/__init__.py wine/practical-5-mlflow/src/pipeline/collect.py \
        wine/practical-5-mlflow/src/pipeline/preprocess.py wine/practical-5-mlflow/src/pipeline/features.py
git commit -m "feat: add local copy of Expt 4 pipeline scripts"
```

### 3. Start the tracking server — Terminal 1 (leave it running)
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --port 5000
```
Ready when it prints `Booting worker with pid: ...` (check: `curl http://127.0.0.1:5000/health` → `OK`).

### 4. Train and track 3 models — Terminal 2
```bash
cd wine/practical-5-mlflow && source .venv-mlflow/bin/activate
export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
python src/train_with_mlflow.py
```
Each run logs params (`model_type`, `C`/`max_iter` or `n_estimators`/`max_depth`), metrics
(`accuracy`, `precision_macro`, `recall_macro`, `f1_macro`), a confusion-matrix PNG and the model.
Actual comparison table:
```
                 model  accuracy  precision_macro  recall_macro  f1_macro
   logistic_regression  0.972222         0.977778      0.966667  0.970962
 random_forest_shallow  1.000000         1.000000      1.000000  1.000000
    random_forest_deep  1.000000         1.000000      1.000000  1.000000
Best model based on F1 score: random_forest_shallow
```
```bash
git add wine/practical-5-mlflow/src/train_with_mlflow.py
git commit -m "feat: track 3 model runs with MLflow"
```

### 5. Register the best run and move it to Staging
```bash
python src/register_best_model.py
```
```
Best Run   Model: random_forest_shallow   F1 Score: 1.0
Successfully registered model 'wine-classifier-prod'.
Version: 1
Model moved to Staging successfully.
Model URI: models:/wine-classifier-prod/Staging
```
```bash
git add wine/practical-5-mlflow/src/register_best_model.py
git commit -m "feat: register best model to Staging"
```

### 6. Load the model from the registry
```bash
python src/load_registered_model.py
```
```
Model type: <class 'sklearn.ensemble._forest.RandomForestClassifier'>
RandomForestClassifier(max_depth=3, n_estimators=50, random_state=42)
Predicted labels for first 5 rows: ['class_0', 'class_0', 'class_0', 'class_0', 'class_0']
Actual labels for first 5 rows   : ['class_0', 'class_0', 'class_0', 'class_0', 'class_0']
```
```bash
git add wine/practical-5-mlflow/src/load_registered_model.py
git commit -m "feat: load registered model from registry"
```

### 7. Show the UI, then stop the server
Open http://127.0.0.1:5000:
1. **Experiments** (left) → `wine-classification-baseline` → 3 runs listed.
2. Tick all 3 runs → **Compare** → parallel-coordinates / scatter of `f1_macro`, params table side by side.
3. Click a run → **Artifacts** → `confusion_matrix_<model>.png` and the `model/` folder.
4. **Models** tab (top) → `wine-classifier-prod` → Version 1 → Stage **Staging**.

Then Ctrl+C in Terminal 1 so `mlflow.db` is not locked.
```bash
git add wine/practical-5-mlflow/STEPS.md && git commit -m "docs: add practical-5 step log"
```

## Push and PR
```bash
git ls-files | grep -E '\.csv$|\.parquet$|\.db$|\.joblib$|\.pkl$|venv|mlruns|mlartifacts'   # must print nothing
git push -u origin wine/practical-5
```
GitHub: **Pull requests → New** → base `main` ← compare `wine/practical-5` → Create → Merge.

## What the examiner may check
| Check | How |
|---|---|
| 3 runs with params + metrics | UI → experiment → Compare |
| Artifacts logged | UI → run → Artifacts (confusion matrix + model) |
| Model registered in Staging | UI → Models → `wine-classifier-prod` v1 Staging |
| Loading by name works | `python src/load_registered_model.py` |
| No db/artifacts in Git | `git ls-files wine/practical-5-mlflow` |

## Viva points
- **Param vs metric vs artifact?** Param = input setting (C, max_depth); metric = numeric result (f1_macro); artifact = file (PNG, model).
- **Why a tracking server with SQLite?** The Model Registry needs a database backend; the plain file store (`mlruns/`) does not support registration.
- **How was the best model chosen?** `search_runs` ordered by `f1_macro DESC, start_time ASC` — both random forests scored 1.0, so the earlier run (`random_forest_shallow`) won the tie.
- **Why load via `models:/wine-classifier-prod/Staging`?** Consumers refer to a name + stage, not a run ID or file path, so a new version can be promoted without changing code.
- **Why LabelEncoder classes sorted?** `LabelEncoder` sorts labels alphabetically, so `class_0, class_1, class_2` map to 0, 1, 2; the load script reverses that mapping.

## Mistakes to avoid
- Export `MLFLOW_TRACKING_URI` in **every** new terminal before running the scripts.
- Start the server from inside `wine/practical-5-mlflow/` so `mlflow.db` and `mlartifacts/` land there (both ignored).
- Running `train_with_mlflow.py` twice creates 6 runs; `register_best_model.py` twice creates Version 2.
- MLflow 2.17 prints FutureWarnings about stages (`transition_model_version_stage`) and LogisticRegression prints a convergence warning — both are harmless.
- Stop the server before `git add` / switching branches.
