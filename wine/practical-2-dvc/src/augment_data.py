# src/augment_data.py
import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/wine_v1.csv")

# every column except the label is a numeric feature
feature_cols = [c for c in df.columns if c != "target"]

rng = np.random.default_rng(42)
noise = rng.normal(0, 0.05, size=(20, len(feature_cols)))

sample = df.sample(20, random_state=42).reset_index(drop=True)
sample[feature_cols] = sample[feature_cols].values + noise

augmented = pd.concat([df, sample], ignore_index=True)
augmented.to_csv("data/raw/wine_v1.csv", index=False)
print(f"Dataset now has {len(augmented)} rows")
