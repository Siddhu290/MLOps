# reuse_features_for_clustering.py
"""
Demonstrates a completely different model (unsupervised KMeans clustering)
reusing the SAME registered features through the feature service.
"""
import pandas as pd
from feast import FeatureStore
from sklearn.cluster import KMeans

N_CLUSTERS = 3

if __name__ == "__main__":
    print("=" * 60)
    print("FEAST FEATURE SERVICE TEST")
    print("=" * 60)

    store = FeatureStore(repo_path=".")
    feature_service = store.get_feature_service("wine_feature_service")

    # 1. Online lookup for one sample through the feature service
    result = store.get_online_features(
        features=feature_service,
        entity_rows=[{"sample_id": 1}],
    )
    print("\nFeatures retrieved using Feature Service (sample_id = 1):")
    print(result.to_dict())

    # 2. Reuse the same features for a different model: clustering
    source_df = pd.read_parquet("data/wine_features.parquet")
    entity_df = source_df[["sample_id", "event_timestamp"]]
    df = store.get_historical_features(entity_df=entity_df, features=feature_service).to_df()

    X = df.drop(columns=["sample_id", "event_timestamp", "alcohol_bin"])
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(X)

    print(f"\nKMeans cluster counts ({len(df)} samples, {N_CLUSTERS} clusters):")
    print(df["cluster"].value_counts().sort_index().to_string())
