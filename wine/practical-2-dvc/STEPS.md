# Practical 2 — DVC dataset versioning (Wine) — what I must do in the exam

Lab manual: **Experiment 3** — install/configure DVC, track and version a dataset, push it to
remote storage, compare versions, restore an old version, integrate DVC with Git.

## Before starting
```bash
git switch main && git pull origin main
git switch -c wine/practical-2
mkdir -p wine/practical-2-dvc && cd wine/practical-2-dvc
python -m pip install dvc pandas scikit-learn
dvc --version                 # this run: 3.67.1
```

## Steps

### 1. Scaffold
Purpose: folder with a `.gitignore` that does **not** ignore `data/` (the `.dvc` pointer files must be committed).
```bash
git add wine/practical-2-dvc/.gitignore wine/practical-2-dvc/requirements.txt wine/practical-2-dvc/README.md
git commit -m "chore: scaffold practical-2 folder"
```

### 2. Initialise DVC in this folder only
```bash
dvc init --subdir
git status              # A .dvc/.gitignore  A .dvc/config  A .dvcignore
git add .dvc .dvcignore
git commit -m "chore: initialize DVC in practical-2"
```
Never run plain `dvc init` at the repo root.

### 3. Local remote
```bash
mkdir -p ~/dvc-remote-storage
dvc remote add -d myremote ~/dvc-remote-storage     # "Setting 'myremote' as a default remote."
cat .dvc/config
git add .dvc/config
git commit -m "chore: configure local DVC remote"
```
Actual `.dvc/config`:
```
[core]
    remote = myremote
['remote "myremote"']
    url = /home/sm/dvc-remote-storage
```

### 4. Version 1 of the data
```bash
mkdir -p src     # paste src/generate_data.py
python src/generate_data.py          # Saved 178 rows to data/raw/wine_v1.csv
dvc add data/raw/wine_v1.csv         # creates wine_v1.csv.dvc + data/raw/.gitignore
cat data/raw/wine_v1.csv.dvc
git add data/raw/wine_v1.csv.dvc data/raw/.gitignore src/generate_data.py
git commit -m "data: add wine_v1 raw dataset (178 rows) tracked via DVC"
git tag wine/p2-data-v1
dvc push                             # 1 file pushed
```
Actual `.dvc` file: `md5: 2925c4a8cd201c79d97d3d283429ef23`, `size: 12261`.

### 5. Version 2 of the data
```bash
# paste src/augment_data.py (adds 20 noisy copies of random rows)
python src/augment_data.py           # Dataset now has 198 rows
dvc add data/raw/wine_v1.csv
git add data/raw/wine_v1.csv.dvc src/augment_data.py
git commit -m "data: augment wine dataset with 20 synthetic rows"
git tag wine/p2-data-v2
dvc push                             # 1 file pushed
```
Actual `.dvc` file: `md5: 2d8d2352eca13e70355307236da99f25`, `size: 17133`.

### 6. Compare and restore (no commits)
```bash
git log --oneline -- data/raw/wine_v1.csv.dvc     # 2 commits
dvc diff wine/p2-data-v1                               # Modified: data/raw/wine_v1.csv
git show wine/p2-data-v1:./data/raw/wine_v1.csv.dvc    # md5 2925c4a8...  size 12261
git show wine/p2-data-v2:./data/raw/wine_v1.csv.dvc    # md5 2d8d2352...  size 17133

git checkout wine/p2-data-v1 -- data/raw/wine_v1.csv.dvc
dvc checkout data/raw/wine_v1.csv.dvc
wc -l data/raw/wine_v1.csv                        # 179  (178 rows + header)

git checkout HEAD -- data/raw/wine_v1.csv.dvc
dvc checkout data/raw/wine_v1.csv.dvc
wc -l data/raw/wine_v1.csv                        # 199

ls ~/dvc-remote-storage/files/md5                 # 29  2d   (one folder per version)
git status                                        # clean
```
`git show` needs `./` in front of the path when run from inside the subfolder.

### 7. Document and log
```bash
git add wine/practical-2-dvc/docs/DVC_WORKFLOW.md && git commit -m "docs: add DVC workflow"
git add wine/practical-2-dvc/STEPS.md && git commit -m "docs: add practical-2 step log"
```

## Push and PR
```bash
git ls-files | grep -E '\.csv$|\.parquet$|\.db$|\.joblib$|\.pkl$|venv|mlruns|mlartifacts'   # must print nothing
git push -u origin wine/practical-2
git push origin wine/p2-data-v1 wine/p2-data-v2
```
GitHub: **Pull requests → New** → base `main` ← compare `wine/practical-2` → Create → Merge. Tags are visible under **Code → Tags**.

## What the examiner may check
| Check | Command |
|---|---|
| CSV is not in Git, only its pointer | `git ls-files wine/practical-2-dvc` (shows `.dvc` file, no `.csv`) |
| Two data versions in history | `git log --oneline -- data/raw/wine_v1.csv.dvc` |
| Versions differ | `dvc diff wine/p2-data-v1` |
| Restore works | `git checkout wine/p2-data-v1 -- data/raw/wine_v1.csv.dvc && dvc checkout data/raw/wine_v1.csv.dvc && wc -l data/raw/wine_v1.csv` → 179 |
| Remote in sync | `dvc status -c` → "Cache and remote 'myremote' are in sync." |
| Tags pushed | `git ls-remote --tags origin` |

## Viva points
- **How does DVC keep big files out of Git?** Content-addressable storage: the file's MD5 decides where it lives in cache/remote; Git only stores the small `.dvc` file with the hash and size.
- **Why both `git checkout` and `dvc checkout`?** `git checkout` restores the pointer (old hash); `dvc checkout` makes the real CSV on disk match that hash from the cache.
- **Why not commit `wine_v1.csv`, `wine_v2.csv` to Git?** Every copy stays in Git history forever and nothing ties a commit to the data it used; DVC dedups by hash and pins data per commit.
- **What is `data/raw/.gitignore`?** Written by `dvc add` so Git ignores the real CSV.
- **Why `--subdir`?** The repo holds several practicals; DVC must be scoped to this folder.

## Mistakes to avoid
- Do not put `data/` in this folder's `.gitignore` — the `.dvc` files would be ignored too.
- Run `dvc add` **again** after changing the CSV, otherwise the pointer keeps the old hash.
- `dvc push` after every data commit, otherwise a teammate can't `dvc pull` that version.
- After the restore demo, go back to HEAD (`git checkout HEAD -- ...` + `dvc checkout`) so `git status` is clean.
- Push the tags separately: `git push origin wine/p2-data-v1 wine/p2-data-v2` (`git push` alone doesn't send tags).
