# src/pipeline/validate.py
"""
Stage 4: Data Validation.
Schema and statistical checks that must pass before data can
flow downstream to training. Raises on failure to hard-stop the pipeline.
"""
import argparse
import logging
import sys

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("validate")

RAW_COLS = [
    "alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
    "total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins",
    "color_intensity", "hue", "od280_od315_ratio", "proline",
]

TARGET_COL = "wine_class"
ENGINEERED_COLS = ["flavanoid_ratio", "color_hue_ratio", "alcohol_proline_index", "alcohol_bin"]
EXPECTED_COLUMNS = set(RAW_COLS) | {TARGET_COL} | set(ENGINEERED_COLS)

VALID_TARGETS = {"class_0", "class_1", "class_2"}

RANGE_CHECKS = {
    "alcohol": (10.0, 16.0),
    "malic_acid": (0.5, 6.5),
    "color_intensity": (1.0, 14.0),
    "proline": (250, 1800),
}


class DataValidationError(Exception):
    pass


def validate(input_path: str) -> pd.DataFrame:
    df = pd.read_csv(input_path)
    errors = []

    missing_cols = EXPECTED_COLUMNS - set(df.columns)
    if missing_cols:
        errors.append(f"Missing expected columns: {missing_cols}")

    if df.isnull().any().any():
        null_cols = df.columns[df.isnull().any()].tolist()
        errors.append(f"Unexpected null values in columns: {null_cols}")

    invalid_targets = set(df[TARGET_COL].unique()) - VALID_TARGETS
    if invalid_targets:
        errors.append(f"Unexpected {TARGET_COL} values: {invalid_targets}")

    for col, (low, high) in RANGE_CHECKS.items():
        out_of_range = df[(df[col] < low) | (df[col] > high)]
        if not out_of_range.empty:
            errors.append(f"{len(out_of_range)} rows out of expected range for '{col}' ({low}-{high})")

    if errors:
        for e in errors:
            logger.error(e)
        raise DataValidationError(f"Validation failed with {len(errors)} error(s)")

    logger.info("Validation PASSED: %d rows, %d columns, all checks satisfied", len(df), df.shape[1])
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/processed/wine_features.csv")
    args = parser.parse_args()
    try:
        validate(args.input)
    except DataValidationError as e:
        logger.error("Pipeline halted: %s", e)
        sys.exit(1)
