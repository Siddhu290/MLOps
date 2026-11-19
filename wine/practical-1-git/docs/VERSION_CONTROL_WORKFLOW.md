# Version Control Workflow — mlops-wine-classifier

## Branching Strategy
| Branch | Purpose |
|---|---|
| `main` | Stable code; only changed through reviewed pull requests |
| `wine/practical-1` | Integration branch for this practical (plays the role of `develop`) |
| `wine/p1-feature/add-classification-report` | Feature branch, merged back into `wine/practical-1` via pull request |
| `wine/p1-conflict-a`, `wine/p1-conflict-b` | Branches created to practise merge-conflict resolution |

Rule: no direct commits to `main`. Flow: `wine/p1-feature/*` → Pull Request → `wine/practical-1` → Pull Request → `main`.

## Commit Convention
`feat:` new functionality · `fix:` bug fix · `docs:` documentation · `chore:` tooling/config · `refactor:` no behaviour change · `merge:` conflict resolution

## Merge Conflict Resolution
1. Merge (`git merge wine/p1-conflict-a` while on `wine/p1-conflict-b`); Git flags `README.md`.
2. Find the `<<<<<<<` / `=======` / `>>>>>>>` markers.
3. Keep current, incoming, or a combination; remove all markers.
4. `git add <file>` then `git commit`.
5. Run `python src/train.py` before pushing.

## .gitignore Policy
Datasets (`data/`), models (`models/*.joblib`), virtual environments and
Python caches are excluded from Git; datasets are tracked with DVC instead.
