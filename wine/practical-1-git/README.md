# Practical 1 — Version A + B (resolved)

Branch: `wine/practical-1` · Folder: `wine/practical-1-git/` · Lab manual: Expt 2

Run every command below from inside this folder unless it says otherwise.

```bash
git switch main && git pull origin main
git switch -c wine/practical-1
cd wine/practical-1-git
```

## Steps

```bash
mkdir -p src docs
touch src/__init__.py src/train.py README.md requirements.txt .gitignore
# paste src/train.py, requirements.txt, .gitignore
python src/train.py                    # Accuracy: 1.0000
git add .
git commit -m "chore: add wine baseline training script"
```

Branching and PR practice (names prefixed so they don't clash with teammates' branches):

```bash
git push -u origin wine/practical-1
git switch -c wine/p1-feature/add-classification-report
# edit src/train.py (e.g. print the classification report), then:
git add src/train.py
git commit -m "feat: add classification report to training script"
git push -u origin wine/p1-feature/add-classification-report
# GitHub PR: base wine/practical-1 <- compare wine/p1-feature/add-classification-report, merge it
git switch wine/practical-1 && git pull origin wine/practical-1
```

Merge-conflict demo (edits only this folder's README.md):

```bash
git switch -c wine/p1-conflict-a
# change line 1 of README.md to "# Practical 1 — Version A"
git commit -am "docs: README title (Version A)"
git switch wine/practical-1
git switch -c wine/p1-conflict-b
# change line 1 of README.md to "# Practical 1 — Version B"
git commit -am "docs: README title (Version B)"
git merge wine/p1-conflict-a                # CONFLICT in README.md
# fix the markers in VS Code, keep "# Practical 1 — Version A + B (resolved)"
git add README.md
git commit -m "merge: resolve README conflict between version A and B"
git switch wine/practical-1 && git merge wine/p1-conflict-b
python src/train.py
git log --oneline --graph --all
```

## Submit

```bash
cd ../..                               # back to the repo root
git status                             # check: no .venv, data CSVs or mlflow.db listed
git add wine/practical-1-git
git commit -m "feat: complete practical 1 - git workflow"
git push -u origin wine/practical-1
```

On GitHub: **Compare & pull request** → base `main`, compare `wine/practical-1` → Create → Merge pull request → Confirm merge.
