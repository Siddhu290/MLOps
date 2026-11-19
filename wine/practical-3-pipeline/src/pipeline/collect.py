# src/pipeline/collect.py
"""
Stage 1: Data Collection.
Ingests the raw Wine dataset and writes it to the raw data zone,
with basic collection-time metadata logging.
"""
import argparse
import logging
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
from sklearn.datasets import load_wine

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("collect")


def collect_data(output_path: str) -> pd.DataFrame:
    wine = load_wine(as_frame=True)
    df = wine.frame.rename(columns={
        "target": "wine_class",
        # "/" in a column name breaks Feast feature references, so rename it
        "od280/od315_of_diluted_wines": "od280_od315_ratio",
    })
    df["wine_class"] = df["wine_class"].map(dict(enumerate(wine.target_names)))  # 0 -> class_0, 1 -> class_1, 2 -> class_2
    df["collected_at"] = datetime.now(timezone.utc).isoformat()  # when the data was collected

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("Collected %d rows -> %s", len(df), output_path)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="data/raw/wine_raw.csv")
    args = parser.parse_args()
    collect_data(args.output)
