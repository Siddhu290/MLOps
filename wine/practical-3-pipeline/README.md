# Practical 3 — Data pipeline (Wine)

Branch: `wine/practical-3` · Folder: `wine/practical-3-pipeline/` · Lab manual: Expt 4

Run every command below from inside this folder unless it says otherwise.

```bash
git switch main && git pull origin main
git switch -c wine/practical-3
cd wine/practical-3-pipeline
```

## Steps

```bash
python -m pip install dvc pandas scikit-learn pyyaml
dvc init --subdir
git add .dvc .dvcignore
git commit -m "chore: initialize DVC in practical-3"
mkdir -p ~/dvc-remote-storage
dvc remote add -d myremote ~/dvc-remote-storage

# run each stage once by hand
python src/pipeline/collect.py         # Collected 178 rows
python src/pipeline/preprocess.py      # Dropped 0 duplicate rows
python src/pipeline/features.py        # Engineered 18 features
python src/pipeline/validate.py        # Validation PASSED: 178 rows, 18 columns

# then as a DVC pipeline
dvc repro                              # runs collect -> preprocess -> features -> validate
dvc repro                              # every stage: didn't change, skipping
dvc dag
dvc push
```

Validation failure check: open `data/processed/wine_features.csv`, set one `alcohol` value to 50, run `python src/pipeline/validate.py` → range error and exit code 1 (`echo $?`). Then `dvc repro` again to restore the file.

## Submit

```bash
cd ../..                               # back to the repo root
git status                             # check: no .venv, data CSVs or mlflow.db listed
git add wine/practical-3-pipeline
git commit -m "feat: complete practical 3 - DVC data pipeline"
git push -u origin wine/practical-3
```

On GitHub: **Compare & pull request** → base `main`, compare `wine/practical-3` → Create → Merge pull request → Confirm merge.
