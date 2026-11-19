# Feature Store Analysis — mlops-wine-classifier

## Setup
Feast 0.68.0, local provider, SQLite online store, Parquet offline source
(`data/wine_features.parquet`, 178 rows), entity `sample_id` (INT64).

| Object | Name |
|---|---|
| Entity | `sample_id` |
| Feature view 1 | `wine_measurements` (13 original measurements) |
| Feature view 2 | `wine_engineered_features` ("flavanoid_ratio", "color_hue_ratio", "alcohol_proline_index", "alcohol_bin") |
| Feature service | `wine_feature_service` (both views, 17 features) |

`feast apply` created 1 entity, 2 feature views, 1 feature service and 2 SQLite tables;
`feast materialize-incremental` loaded both views into the online store.

## Results from this run
| Script | Result |
|---|---|
| `get_online_features.py` | 17 features for sample_id 0, 1, 2; `Any None values? False` |
| `get_historical_features.py` | 5 rows, shape (5, 19), joined as of each event timestamp |
| `reuse_features_for_clustering.py` | KMeans on all 178 samples → cluster sizes 62 / 47 / 69 |

## Observed benefits
- **No training-serving skew:** the same feature definitions were served online
  (`get_online_features.py`) and offline (`get_historical_features.py`) with identical values
  (e.g. sample 0 `flavanoid_ratio` = 1.092857 in both).
- **Reusability:** `reuse_features_for_clustering.py` trained a KMeans model on the
  same registered features with zero re-implementation.
- **Point-in-time correctness:** historical retrieval joins features "as of" each
  entity's event timestamp, preventing future-data leakage.
- **Centralised governance:** `features.py` is the single source of truth for all
  consuming models.
