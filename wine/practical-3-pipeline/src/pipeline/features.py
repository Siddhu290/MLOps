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

    # original features: 13 chemical measurements of each wine
    # creating new features
    df["flavanoid_ratio"] = df["flavanoids"] / df["total_phenols"].replace(0, pd.NA)
    df["color_hue_ratio"] = df["color_intensity"] / df["hue"].replace(0, pd.NA)
    df["alcohol_proline_index"] = df["alcohol"] * df["proline"] / 1000
    df["alcohol_bin"] = pd.cut(
        df["alcohol"],
        bins=[0, 12.5, 13.5, 16],
        labels=["low", "medium", "high"],
    )

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Engineered %d features -> %s", df.shape[1], output_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/wine_preprocessed.csv")
    parser.add_argument("--output", default="data/processed/wine_features.csv")
    args = parser.parse_args()
    engineer_features(args.input, args.output)
