import streamlit as st
import sys
import os

# Allow imports from repo root
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.form import show_prediction_form
from app.prediction import load_model

def main():
    st.set_page_config(
        page_title="ML Predictor",
        page_icon="🎯",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    @st.cache_resource
    def load_ml_model():
        return load_model()

    pipeline = load_ml_model()

    if pipeline is None:
        st.error("El modelo no está disponible. Revisa mensajes anteriores o ejecuta `python scripts/train_model.py`.")
        return

    show_prediction_form(pipeline)

if __name__ == "__main__":
    main()
