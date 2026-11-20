# get_historical_features.py
import pandas as pd
from feast import FeatureStore

from feature_columns import RAW_COLS, ENGINEERED_COLS

FEATURES = (
    [f"cancer_measurements:{c}" for c in RAW_COLS]
    + [f"cancer_engineered_features:{c}" for c in ENGINEERED_COLS]
)

if __name__ == "__main__":
    print("=" * 60)
    print("FEAST HISTORICAL FEATURE RETRIEVAL TEST")
    print("=" * 60)

    source_df = pd.read_parquet("data/cancer_features.parquet")

    # Entity dataframe: which samples, and "as of" which time
    entity_df = source_df[["sample_id", "event_timestamp"]].head(5).copy()
    print("\nEntity DataFrame:")
    print(entity_df.to_string(index=False))

    store = FeatureStore(repo_path=".")
    training_df = store.get_historical_features(
        entity_df=entity_df,
        features=FEATURES,
    ).to_df()

    print("\nHistorical Features (engineered columns shown):")
    print(training_df[["sample_id", "event_timestamp"] + ENGINEERED_COLS].to_string(index=False))
    print("\nShape:", training_df.shape)
    print("Number of rows retrieved:", len(training_df))
