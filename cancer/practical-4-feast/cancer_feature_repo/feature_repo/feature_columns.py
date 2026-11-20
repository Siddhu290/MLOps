# feature_columns.py
"""
Column lists shared by features.py and the retrieval scripts.
Kept separate so that only features.py defines Feast objects.
"""
# 10 base measurements x 3 statistics (mean / error / worst) = 30 columns
BASE = [
    "radius", "texture", "perimeter", "area", "smoothness",
    "compactness", "concavity", "concave points", "symmetry", "fractal dimension",
]
RAW_COLS = (
    [f"mean {b}" for b in BASE]
    + [f"{b} error" for b in BASE]
    + [f"worst {b}" for b in BASE]
)

ENGINEERED_COLS = ["area_to_perimeter", "radius_growth_ratio", "texture_smoothness_index", "radius_bin"]
