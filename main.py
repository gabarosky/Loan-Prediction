import streamlit as st
from app.form import show_prediction_form
from app.prediction import load_model

def main():
    st.title("Loan Prediction App")

    pipeline = load_model()
    show_prediction_form(pipeline)

if __name__ == "__main__":
    main()
