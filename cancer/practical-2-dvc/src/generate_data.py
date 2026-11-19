# src/generate_data.py
import os

import pandas as pd
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer(as_frame=True)
df = data.frame

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/cancer_v1.csv", index=False)
print(f"Saved {len(df)} rows to data/raw/cancer_v1.csv")
