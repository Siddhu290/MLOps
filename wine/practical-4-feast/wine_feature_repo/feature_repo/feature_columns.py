# feature_columns.py
"""
Column lists shared by features.py and the retrieval scripts.
Kept separate so that only features.py defines Feast objects.
"""
RAW_COLS = [
    "alcohol", "malic_acid", "ash", "alcalinity_of_ash", "magnesium",
    "total_phenols", "flavanoids", "nonflavanoid_phenols", "proanthocyanins",
    "color_intensity", "hue", "od280_od315_ratio", "proline",
]

ENGINEERED_COLS = ["flavanoid_ratio", "color_hue_ratio", "alcohol_proline_index", "alcohol_bin"]
