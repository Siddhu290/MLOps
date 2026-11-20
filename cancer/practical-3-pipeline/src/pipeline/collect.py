# src/pipeline/collect.py
"""
Stage 1: Data Collection.
Ingests the raw Breast Cancer dataset and writes it to the raw data zone,
with basic collection-time metadata logging.
"""
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
from sklearn.datasets import load_breast_cancer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("collect")


def collect_data(output_path: str) -> pd.DataFrame:
    cancer = load_breast_cancer(as_frame=True)
    df = cancer.frame.rename(columns={"target": "diagnosis"})
    df["diagnosis"] = df["diagnosis"].map(dict(enumerate(cancer.target_names)))  # 0 -> malignant, 1 -> benign
    df["collected_at"] = datetime.now(timezone.utc).isoformat()  # when the data was collected

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Collected %d rows -> %s", len(df), output_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/cancer_raw.csv")
    args = parser.parse_args()
    collect_data(args.output)
