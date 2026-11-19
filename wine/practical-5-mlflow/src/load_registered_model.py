# src/load_registered_model.py
import os

import mlflow
import mlflow.sklearn
import pandas as pd

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))

MODEL_URI = "models:/wine-classifier-prod/Staging"
DATA_PATH = "data/processed/wine_features.csv"
TARGET_COL = "wine_class"
BIN_COL = "alcohol_bin"

print("=" * 60)
print("LOADING REGISTERED MODEL")
print("=" * 60)
print("Model URI:", MODEL_URI)

# Load from the Model Registry (no retraining, no run ID, no file path)
model = mlflow.sklearn.load_model(MODEL_URI)
print("\nModel loaded successfully!")
print("Model type:", type(model))
print("\nLoaded Model:")
print(model)

# Quick inference check on 5 rows
df = pd.read_csv(DATA_PATH)
X = df.drop(columns=[TARGET_COL, BIN_COL]).head(5)
# LabelEncoder sorted the class names alphabetically during training
classes = sorted(df[TARGET_COL].unique())
predicted = [classes[i] for i in model.predict(X)]
print("\nPredicted labels for first 5 rows:", predicted)
print("Actual labels for first 5 rows   :", df[TARGET_COL].head(5).tolist())
