# get_online_features.py
import pandas as pd
from feast import FeatureStore

from feature_columns import RAW_COLS, ENGINEERED_COLS

FEATURES = (
    [f"wine_measurements:{c}" for c in RAW_COLS]
    + [f"wine_engineered_features:{c}" for c in ENGINEERED_COLS]
)

if __name__ == "__main__":
    print("=" * 60)
    print("FEAST ONLINE FEATURE RETRIEVAL TEST")
    print("=" * 60)

    store = FeatureStore(repo_path=".")
    result = store.get_online_features(
        features=FEATURES,
        entity_rows=[{"sample_id": 0}, {"sample_id": 1}, {"sample_id": 2}],
    )

    result_df = pd.DataFrame(result.to_dict())
    print("\nFeatures retrieved for sample_id = 0, 1, 2:")
    print(result_df.T.to_string(header=False))
    print("\nAny None values?", result_df.isnull().any().any())
