"""
app.py
──────
House Price Prediction – Flask REST API server.

Run:
    python app.py

Endpoints:
    GET  /health            Liveness probe.
    GET  /features          Feature catalogue and defaults.
    POST /predict           Predict price for a single house.
    POST /predict/batch     Predict prices for multiple houses.
"""

import logging
import os
import sys

# Add /project to the path so template_utils can be imported directly.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import template_utils as tu
from flask import Flask, jsonify, request

# ── App setup ─────────────────────────────────────────────────
app = Flask(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
_LOG = logging.getLogger(__name__)

# Eager-load the model at startup so the first request is fast.
try:
    _model = tu.load_model_artifact()
    _LOG.info("Model loaded successfully.")
except FileNotFoundError as exc:
    _LOG.warning("Startup model load failed: %s", exc)
    _model = None


# ── Routes ────────────────────────────────────────────────────
@app.get("/health")
def health():
    """Return API liveness and model status."""
    status = "ok" if _model is not None else "model_unavailable"
    return jsonify({"status": status}), 200 if _model else 503


@app.get("/features")
def features():
    """Return the feature catalogue and default values."""
    return jsonify({
        "numeric_features":     tu.NUMERIC_FEATURES,
        "categorical_features": tu.CATEGORICAL_FEATURES,
        "defaults":             tu.FEATURE_DEFAULTS,
    })


@app.post("/predict")
def predict():
    """
    Predict the sale price for a single house.

    All request fields are optional; missing values use FEATURE_DEFAULTS.
    """
    if _model is None:
        return jsonify({"error": "Model not loaded"}), 503
    try:
        payload = request.get_json(force=True) or {}
        errors = tu.validate_features(payload)
        if errors:
            return jsonify({"error": "Validation failed", "details": errors}), 400
        price = tu.predict_price(payload, model=_model)
        _LOG.info("predict  price=%.2f  payload=%s", price, payload)
        return jsonify({
            "predicted_price": price,
            "model_version":   "1.0",
        })
    except Exception as exc:
        _LOG.exception("Prediction error.")
        return jsonify({"error": str(exc)}), 500


@app.post("/predict/batch")
def predict_batch():
    """Predict prices for multiple houses in one call."""
    if _model is None:
        return jsonify({"error": "Model not loaded"}), 503
    try:
        body      = request.get_json(force=True) or {}
        instances = body.get("instances", [])
        if not instances:
            return jsonify({"error": "No instances provided"}), 400
        prices = [tu.predict_price(inst, model=_model) for inst in instances]
        _LOG.info("batch_predict  count=%d", len(prices))
        return jsonify({"predictions": prices, "count": len(prices)})
    except Exception as exc:
        _LOG.exception("Batch prediction error.")
        return jsonify({"error": str(exc)}), 500


# ── Entry point ───────────────────────────────────────────────
if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)