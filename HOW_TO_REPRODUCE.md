# How to Reproduce Results

This document provides **step-by-step instructions** to fully reproduce the
machine learning results of this project, including data preprocessing,
model training, and generation of the trained pipeline artifact.

---

## 🧱 System Requirements

- Python **3.11+** 
- pip or conda
- OS: Windows / Linux / macOS

---

## 📦 Environment Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/loan-prediction-app.git
cd loan-prediction-app
````

### 2. Create a virtual environment

```bash
conda create -n loan_app python=3.11
conda activate loan_app
```

or

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 📊 Dataset

The raw dataset must be located at:

```
data/train.csv
```

Source:

* Analytics Vidhya – Loan Prediction Practice Problem
* [https://www.analyticsvidhya.com/datahack/contest/practice-problem-loan-prediction-iii/](https://www.analyticsvidhya.com/datahack/contest/practice-problem-loan-prediction-iii/)

⚠️ The raw file name **must not be changed**.

---

## 🧹 Data Cleaning & Feature Engineering

Data cleaning and feature engineering are performed **programmatically** inside:

```
scripts/train_model.py
```

Key steps include:

* Type casting categorical variables
* Encoding target variable (`Loan_Status`)
* Dropping invalid rows
* Creating engineered features:

  * Total income
  * Loan installment
  * Income impact ratio

The cleaned dataset is automatically saved as:

```
data/cleaned.csv
```

---

## 🤖 Model Training

### 1. Train the model

Run the following command from the project root:

```bash
python scripts/train_model.py
```

This will:

* Build a full scikit-learn pipeline
* Apply preprocessing and PCA
* Train a CatBoost classifier
* Serialize the trained pipeline

### 2. Output artifact

After successful training, the following file will be created:

```
models/trained_model.pkl
```

This file contains:

* Feature engineering
* Preprocessing
* PCA
* Trained classifier

All encapsulated in a **single pipeline object**.

---

## 🧪 Verification (Optional)

To verify the model loads correctly:

```python
import joblib
model = joblib.load("models/trained_model.pkl")
```

No errors should occur.

---

## 🌐 Run the Streamlit App

Once the model is trained:

```bash
streamlit run app/main.py
```

The application will load the trained pipeline and allow interactive predictions.

---

## 📌 Notes

* The notebooks in `notebooks/` are **experimental only**
* They are not required to reproduce the final model
* All reproducible logic is contained in `scripts/`

---

## ✅ Reproducibility Checklist

* [ ] Environment created
* [ ] Dependencies installed
* [ ] Raw dataset placed in `data/`
* [ ] Training script executed
* [ ] Model artifact generated
* [ ] Application runs successfully

```
