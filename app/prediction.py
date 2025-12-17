import joblib
import pandas as pd
import os
import sys
import streamlit as st

# Ensure scripts path for FeatureEngineer import
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(current_dir, '..', 'scripts')
if scripts_path not in sys.path:
    sys.path.insert(0, scripts_path)
try:
    from custom_transformers import FeatureEngineer
except Exception:
    # If it fails, app still should show error when loading model
    pass

# Try to import config.get_model_path, else fallback
try:
    from config import get_model_path
except Exception:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def get_model_path(filename):
        return os.path.join(PROJECT_ROOT, 'models', filename)

def load_model():
    """Load the pipeline (or return None)"""
    model_file = get_model_path('trained_model.pkl')
    if not os.path.exists(model_file):
        st.error("❌ Missing model file: trained_model.pkl")
        st.info("Run training: `python scripts/train_model.py`")
        return None

    try:
        pipeline = joblib.load(model_file)
        return pipeline
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

def make_prediction(pipeline, user_input):
    """Make prediction using pipeline. Returns (label:int, prob:float)."""
    if pipeline is None:
        raise ValueError("Model pipeline is None")

    input_df = pd.DataFrame([user_input])
    # pipeline.predict returns array([1]) — return scalar
    pred_array = pipeline.predict(input_df)
    try:
        pred = int(pred_array[0])
    except Exception:
        # Fallback
        pred = int(pred_array)

    # Try probability if available
    prob = None
    if hasattr(pipeline, "predict_proba"):
        try:
            prob_array = pipeline.predict_proba(input_df)
            # If binary, take probability for class 1
            if prob_array.shape[1] >= 2:
                prob = float(prob_array[0, 1])
        except Exception:
            prob = None

    return pred, prob
