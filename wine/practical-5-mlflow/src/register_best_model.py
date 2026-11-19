# src/register_best_model.py
"""
Queries MLflow for the best run in the experiment by f1_macro
and registers it under a named, versioned entry in the Model Registry.
"""
import os

import mlflow
from mlflow.tracking import MlflowClient

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
client = MlflowClient()

EXPERIMENT_NAME = "wine-classification-baseline"
REGISTERED_MODEL_NAME = "wine-classifier-prod"

# 1. Find the experiment
experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    raise RuntimeError(f"Experiment '{EXPERIMENT_NAME}' not found.")
experiment_id = experiment.experiment_id
print("Experiment ID:", experiment_id)

# 2. Find the best run
# highest F1 first; on a tie, the earliest run wins (same as the comparison table)
runs = client.search_runs(
    experiment_ids=[experiment_id],
    order_by=["metrics.f1_macro DESC", "attributes.start_time ASC"],
)
if not runs:
    raise RuntimeError("No runs found in the experiment.")

best_run = runs[0]
best_run_id = best_run.info.run_id
print("\nBest Run")
print("Run ID:", best_run_id)
print("Model:", best_run.data.params["model_type"])
print("F1 Score:", best_run.data.metrics["f1_macro"])

# 3. Register the best model
model_uri = f"runs:/{best_run_id}/model"
print("\nRegistering model...")
print("Model URI:", model_uri)
model_version = mlflow.register_model(model_uri=model_uri, name=REGISTERED_MODEL_NAME)
print("\nModel Registered Successfully")
print("Model Name:", REGISTERED_MODEL_NAME)
print("Version:", model_version.version)

# 4. Move it to Staging
client.transition_model_version_stage(
    name=REGISTERED_MODEL_NAME,
    version=model_version.version,
    stage="Staging",
)
print("\nModel moved to Staging successfully.")
print(f"Model URI: models:/{REGISTERED_MODEL_NAME}/Staging")
