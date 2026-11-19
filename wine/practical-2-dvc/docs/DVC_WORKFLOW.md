# DVC Workflow — mlops-wine-classifier

## Setup
- DVC initialised with `dvc init --subdir` (DVC lives in `wine/practical-2-dvc/` only).
- Remote `myremote` → `~/dvc-remote-storage` (local folder, set as default with `dvc remote add -d`).

## Cycle followed for every data change
`dvc add data/raw/wine_v1.csv` → `git add data/raw/wine_v1.csv.dvc` → `git commit` → `git tag` → `dvc push`

## Dataset versions
| Version | Git tag | Rows | Lines (`wc -l`) | MD5 | Size | Change |
|---|---|---|---|---|---|---|
| v1 | `wine/p2-data-v1` | 178 | 179 | `2925c4a8cd201c79d97d3d283429ef23` | 12261 B | Original `load_wine` dataset |
| v2 | `wine/p2-data-v2` | 198 | 199 | `2d8d2352eca13e70355307236da99f25` | 17133 B | +20 noisy synthetic rows (`src/augment_data.py`) |

Remote storage holds one object per version, addressed by hash:
`files/md5/29/25c4a8cd201c79d97d3d283429ef23` and `files/md5/2d/8d2352eca13e70355307236da99f25`.

## Comparing and restoring versions
- `dvc diff wine/p2-data-v1` shows `data/raw/wine_v1.csv` as Modified.
- `git show wine/p2-data-v1:./data/raw/wine_v1.csv.dvc` / `git show wine/p2-data-v2:./data/raw/wine_v1.csv.dvc` show the two hashes.
- Restore v1: `git checkout wine/p2-data-v1 -- data/raw/wine_v1.csv.dvc` then `dvc checkout data/raw/wine_v1.csv.dvc` (`wc -l` → 179).
- Back to latest: `git checkout HEAD -- data/raw/wine_v1.csv.dvc` then `dvc checkout data/raw/wine_v1.csv.dvc` (`wc -l` → 199).
