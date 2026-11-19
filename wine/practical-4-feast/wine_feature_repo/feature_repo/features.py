# features.py
"""
Feature definitions for the Wine feature repository:
entity, data source, feature views (schema + TTL) and a feature service.
"""
from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource, FeatureService
from feast.types import Float32, String
from feast.value_type import ValueType

from feature_columns import RAW_COLS

ENGINEERED_NUMERIC = ["flavanoid_ratio", "color_hue_ratio", "alcohol_proline_index"]

# ============================================================
# ENTITY
# ============================================================
sample = Entity(
    name="sample_id",
    join_keys=["sample_id"],
    value_type=ValueType.INT64,
)

# ============================================================
# DATA SOURCE
# ============================================================
wine_source = FileSource(
    name="wine_features_source",
    path="data/wine_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# ============================================================
# FEATURE VIEW 1 - original measurements
# ============================================================
wine_measurements_fv = FeatureView(
    name="wine_measurements",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[Field(name=col, dtype=Float32) for col in RAW_COLS],
    source=wine_source,
    online=True,
)

# ============================================================
# FEATURE VIEW 2 - engineered features
# ============================================================
wine_engineered_fv = FeatureView(
    name="wine_engineered_features",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[Field(name=col, dtype=Float32) for col in ENGINEERED_NUMERIC]
    + [Field(name="alcohol_bin", dtype=String)],
    source=wine_source,
    online=True,
)

# ============================================================
# FEATURE SERVICE
# ============================================================
wine_feature_service = FeatureService(
    name="wine_feature_service",
    features=[wine_measurements_fv, wine_engineered_fv],
)
