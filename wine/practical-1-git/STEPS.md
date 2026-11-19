# Practical 1 — Git version control (Wine) — what I must do in the exam

Lab manual: **Experiment 2** — install/configure Git, manage an ML repo, branch and merge,
collaborate through GitHub pull requests, resolve a merge conflict, document the workflow.

## Before starting
```bash
git config --global user.name  "Your Name"          # once per machine
git config --global user.email "you@example.com"
git switch main && git pull origin main
git switch -c wine/practical-1
mkdir -p wine/practical-1-git && cd wine/practical-1-git
python -m pip install scikit-learn pandas numpy joblib
```
Windows Git Bash: use `py -3.11` instead of `python3.11`, and `source .venv/Scripts/activate` instead of `source .venv/bin/activate`.

## Steps

### 1. Scaffold the folder
Purpose: create the project skeleton and ignore generated files *before* anything is generated.
```bash
touch .gitignore requirements.txt README.md     # paste contents
git add wine/practical-1-git/.gitignore wine/practical-1-git/requirements.txt wine/practical-1-git/README.md
git status
git commit -m "chore: scaffold practical-1 folder"
```
`.gitignore` ignores `.venv*/ venv/ __pycache__/ *.pyc data/ models/`.

### 2. Baseline training script
Purpose: first working ML code under version control (RandomForest on `load_wine`, 80/20 stratified split).
```bash
mkdir -p src && touch src/__init__.py src/train.py   # paste train.py (no report print yet)
python src/train.py
```
Expected / actual:
```
Accuracy: 1.0000
Model saved to models/wine_model.joblib
```
```bash
git add wine/practical-1-git/src/__init__.py wine/practical-1-git/src/train.py
git commit -m "feat: add wine baseline training script"
git push -u origin wine/practical-1
```
`models/wine_model.joblib` is NOT committed (ignored by `models/`).

### 3. Feature branch + pull request
Purpose: develop a change in isolation and merge it through a PR.
```bash
git switch -c wine/p1-feature/add-classification-report
# in main(): add  print(report)  after the accuracy print
python src/train.py
```
Actual output:
```
Accuracy: 1.0000
              precision    recall  f1-score   support
           0       1.00      1.00      1.00        12
           1       1.00      1.00      1.00        14
           2       1.00      1.00      1.00        10
    accuracy                           1.00        36
```
```bash
git add wine/practical-1-git/src/train.py
git commit -m "feat: add classification report to training script"
git push -u origin wine/p1-feature/add-classification-report
```
On GitHub: **Compare & pull request** → base `wine/practical-1` ← compare `wine/p1-feature/add-classification-report` → Create → **Merge pull request** → Confirm.
URL: `https://github.com/Siddhu290/MLOps/compare/wine/practical-1...wine/p1-feature/add-classification-report?expand=1`
```bash
git switch wine/practical-1 && git pull origin wine/practical-1
```
(In this rehearsal the merge was done locally with `git merge --no-ff wine/p1-feature/add-classification-report`, which gives the same merge commit GitHub creates.)

### 4. Merge-conflict demo
Purpose: two branches change the same line → Git cannot auto-merge → resolve by hand.
```bash
git switch -c wine/p1-conflict-a          # from wine/practical-1
# line 1 of README.md -> "# Practical 1 — Version A"
git add wine/practical-1-git/README.md && git commit -m "docs: README title (Version A)"
git push -u origin wine/p1-conflict-a

git switch wine/practical-1 && git switch -c wine/p1-conflict-b
# line 1 of README.md -> "# Practical 1 — Version B"
git add wine/practical-1-git/README.md && git commit -m "docs: README title (Version B)"
git push -u origin wine/p1-conflict-b

git merge wine/p1-conflict-a
```
Actual output:
```
CONFLICT (content): Merge conflict in wine/practical-1-git/README.md
Automatic merge failed; fix conflicts and then commit the result.

<<<<<<< HEAD
# Practical 1 — Version B
=======
# Practical 1 — Version A
>>>>>>> wine/p1-conflict-a
```
Fix: replace those 5 lines with `# Practical 1 — Version A + B (resolved)` (VS Code: "Accept Both", then edit).
```bash
git add wine/practical-1-git/README.md
git commit -m "merge: resolve README conflict between version A and B"
git push origin wine/p1-conflict-b
git switch wine/practical-1 && git merge wine/p1-conflict-b     # Fast-forward
python src/train.py                                    # Accuracy: 1.0000 — still works
```

### 5. Document the workflow
```bash
# docs/VERSION_CONTROL_WORKFLOW.md: branching table, commit convention, conflict steps, .gitignore policy
git add wine/practical-1-git/docs/VERSION_CONTROL_WORKFLOW.md
git commit -m "docs: add version control workflow"
git add wine/practical-1-git/STEPS.md
git commit -m "docs: add practical-1 step log"
```

## Push and PR
```bash
git ls-files | grep -E '\.csv$|\.parquet$|\.db$|\.joblib$|\.pkl$|venv|mlruns|mlartifacts'   # must print nothing
git push -u origin wine/practical-1
git log --oneline --graph --all
```
GitHub: **Pull requests → New pull request** → base `main` ← compare `wine/practical-1` → Create pull request → Merge.

## What the examiner may check
| Check | Command |
|---|---|
| Branches exist locally and on GitHub | `git branch -a` |
| History shows feature merge + conflict merge | `git log --oneline --graph --all` |
| Conventional commit messages | `git log --oneline wine/practical-1` |
| No model/data/venv committed | `git ls-files` |
| Code still runs after merges | `python src/train.py` → `Accuracy: 1.0000` |
| No leftover conflict markers | `grep -rn '<<<<<<<' .` prints nothing |

## Viva points
- **Why is Git alone not enough for ML?** Git is built for small text diffs; datasets and model binaries bloat history and can't be diffed — DVC stores pointers in Git and data elsewhere.
- **Why did the README conflict happen?** Both branches changed line 1 relative to the common ancestor; Git's three-way merge cannot pick one, so it inserts `<<<<<<< ======= >>>>>>>` markers.
- **Merge commit vs squash merge?** Merge commit keeps every branch commit plus a joining commit; squash collapses the branch into one commit (cleaner history for noisy experiment branches).
- **Why was the last `git merge wine/p1-conflict-b` a fast-forward?** `wine/practical-1` had no new commits since `wine/p1-conflict-b` branched, so Git just moved the pointer.
- **Why is `models/` in .gitignore?** The `.joblib` model is a generated binary; it is reproduced by running `train.py`.

## Mistakes to avoid
- Never `git add .` from the repo root — stage `wine/practical-1-git/...` paths only, and run `git status` first.
- Create `.gitignore` *before* running `train.py`, otherwise `models/wine_model.joblib` shows up as untracked.
- After resolving a conflict, check no markers remain before `git add`.
- Branch `wine/p1-conflict-b` from `wine/practical-1`, not from `wine/p1-conflict-a`, or there is no conflict.
- Pull `wine/practical-1` after merging the PR on GitHub, before creating the next branch.
