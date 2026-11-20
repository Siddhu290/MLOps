# prepare_feature_source.py
"""
Prepares cancer_features.csv from Experiment 4 into a Feast-ready
Parquet source with entity IDs and event timestamps.
"""
from pathlib import Path

import pandas as pd

# practical-4-feast/ = 2 folders above feature_repo/
PRACTICAL_ROOT = Path(__file__).resolve().parents[2]
input_file = PRACTICAL_ROOT / "data" / "processed" / "cancer_features.csv"
output_file = Path("data/cancer_features.parquet")

if __name__ == "__main__":
    df = pd.read_csv(input_file)

    # Entity ID
    df.insert(0, "sample_id", range(len(df)))

    # Event timestamps (one per minute) for point-in-time correctness
    start_time = pd.Timestamp("2026-08-15 15:20:02", tz="UTC")
    df["event_timestamp"] = pd.date_range(start=start_time, periods=len(df), freq="min")
    df["created_timestamp"] = df["event_timestamp"]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_file, index=False)
    print(f"Wrote {len(df)} rows to {output_file}")
