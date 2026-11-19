# Practical 2 — DVC dataset versioning (Wine)

Branch: `wine/practical-2` · Folder: `wine/practical-2-dvc/` · Lab manual: Expt 3

Run every command below from inside this folder unless it says otherwise.

```bash
git switch main && git pull origin main
git switch -c wine/practical-2
cd wine/practical-2-dvc
```

## Steps

```bash
python -m pip install dvc pandas scikit-learn
dvc --version

dvc init --subdir                      # --subdir: DVC lives in this folder only
git add .dvc .dvcignore
git commit -m "chore: initialize DVC in practical-2"

mkdir -p ~/dvc-remote-storage
dvc remote add -d myremote ~/dvc-remote-storage
git add .dvc/config
git commit -m "chore: configure local DVC remote"

python src/generate_data.py            # Saved 178 rows
dvc add data/raw/wine_v1.csv
git add data/raw/wine_v1.csv.dvc data/raw/.gitignore src/generate_data.py
git commit -m "data: add wine_v1 raw dataset (178 rows) tracked via DVC"
dvc push

python src/augment_data.py             # Dataset now has 198 rows
dvc add data/raw/wine_v1.csv
git add data/raw/wine_v1.csv.dvc src/augment_data.py
git commit -m "data: augment wine dataset with 20 synthetic rows (178 -> 198)"
dvc push

git log --oneline -- data/raw/wine_v1.csv.dvc    # 2 commits; copy the older hash
dvc diff <v1-hash>                              # Modified: data/raw/wine_v1.csv
git show <v1-hash>:./data/raw/wine_v1.csv.dvc     # v1 md5 + size
git show HEAD:./data/raw/wine_v1.csv.dvc          # v2 md5 + size

git checkout <v1-hash> -- data/raw/wine_v1.csv.dvc
dvc checkout data/raw/wine_v1.csv.dvc
wc -l data/raw/wine_v1.csv                         # 179
git checkout HEAD -- data/raw/wine_v1.csv.dvc
dvc checkout data/raw/wine_v1.csv.dvc
wc -l data/raw/wine_v1.csv                         # 199
```

`git show` needs the `./` in front of the path when you run it from inside this folder.

## Submit

```bash
cd ../..                               # back to the repo root
git status                             # check: no .venv, data CSVs or mlflow.db listed
git add wine/practical-2-dvc
git commit -m "feat: complete practical 2 - DVC dataset versioning"
git push -u origin wine/practical-2
```

On GitHub: **Compare & pull request** → base `main`, compare `wine/practical-2` → Create → Merge pull request → Confirm merge.
