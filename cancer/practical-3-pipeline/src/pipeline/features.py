# src/pipeline/features.py
"""
Stage 3: Feature Engineering.
Derives new, model-useful features from the raw measurements.
"""
import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("features")


def engineer_features(input_path: str, output_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # original features: 30 cell-nucleus measurements (mean / error / worst)
    # creating new features
    df["area_to_perimeter"] = df["mean area"] / df["mean perimeter"].replace(0, pd.NA)
    df["radius_growth_ratio"] = df["worst radius"] / df["mean radius"].replace(0, pd.NA)
    df["texture_smoothness_index"] = df["mean texture"] * df["mean smoothness"]
    df["radius_bin"] = pd.cut(
        df["mean radius"],
        bins=[0, 12, 17, 30],
        labels=["small", "medium", "large"],
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Engineered %d features -> %s", df.shape[1], output_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/cancer_preprocessed.csv")
    parser.add_argument("--output", default="data/processed/cancer_features.csv")
    args = parser.parse_args()
    engineer_features(args.input, args.output)
