# features.py
"""
Feature definitions for the Breast Cancer feature repository:
entity, data source, feature views (schema + TTL) and a feature service.
"""
from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource, FeatureService
from feast.types import Float32, String
from feast.value_type import ValueType

from feature_columns import RAW_COLS

ENGINEERED_NUMERIC = ["area_to_perimeter", "radius_growth_ratio", "texture_smoothness_index"]

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
cancer_source = FileSource(
    name="cancer_features_source",
    path="data/cancer_features.parquet",
    timestamp_field="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# ============================================================
# FEATURE VIEW 1 - original measurements
# ============================================================
cancer_measurements_fv = FeatureView(
    name="cancer_measurements",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[Field(name=col, dtype=Float32) for col in RAW_COLS],
    source=cancer_source,
    online=True,
)

# ============================================================
# FEATURE VIEW 2 - engineered features
# ============================================================
cancer_engineered_fv = FeatureView(
    name="cancer_engineered_features",
    entities=[sample],
    ttl=timedelta(days=365),
    schema=[Field(name=col, dtype=Float32) for col in ENGINEERED_NUMERIC]
    + [Field(name="radius_bin", dtype=String)],
    source=cancer_source,
    online=True,
)

# ============================================================
# FEATURE SERVICE
# ============================================================
cancer_feature_service = FeatureService(
    name="cancer_feature_service",
    features=[cancer_measurements_fv, cancer_engineered_fv],
)
