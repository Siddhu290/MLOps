# src/pipeline/preprocess.py
"""
Stage 2: Data Preprocessing.
Handles missing values, duplicate removal, and type correction.
"""
import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("preprocess")

TARGET_COL = "wine_class"


def preprocess(input_path: str, output_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    initial_rows = len(df)

    # Drop exact duplicate records
    df = df.drop_duplicates()
    logger.info("Dropped %d duplicate rows", initial_rows - len(df))

    # Every column except the label and the timestamp is a numeric feature
    numeric_cols = [c for c in df.columns if c not in (TARGET_COL, "collected_at")]

    # Convert to numbers and fill missing values with the median
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            logger.info("Imputed %d missing values in '%s' with median=%.3f", n_missing, col, median_val)

    # Drop rows with unresolvable missing target
    df = df.dropna(subset=[TARGET_COL])

    df.drop(columns=["collected_at"], inplace=True, errors="ignore")
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Preprocessed %d rows -> %s", len(df), output_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/raw/wine_raw.csv")
    parser.add_argument("--output", default="data/processed/wine_preprocessed.csv")
    args = parser.parse_args()
    preprocess(args.input, args.output)
