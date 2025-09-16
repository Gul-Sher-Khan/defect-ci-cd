from __future__ import annotations
import os
from typing import List, Dict, Any
from flask import Flask, jsonify, request
import pandas as pd
from model import load_model, METRICS

app = Flask(__name__)

MODEL_PATH = os.environ.get("MODEL_PATH", "models/model.pkl")
_model = None


def _ensure_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError(f"Model file not found at {MODEL_PATH}. Train first.")
        _model = load_model(MODEL_PATH)
    return _model


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/predict")
def predict():
    payload = request.get_json(force=True, silent=False)
    instances: List[Dict[str, Any]] = payload.get("instances", [])
    if not instances:
        return jsonify({"error": "No instances provided"}), 400

    df = pd.DataFrame(instances)
    missing = [m for m in METRICS if m not in df.columns]
    if missing:
        return jsonify({"error": f"Missing features: {missing}"}), 400

    df = df[METRICS].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    model = _ensure_model()
    preds = model.predict(df)

    return jsonify({"predictions": preds.tolist()})
