# Model Card – Loan Pre-Approval Predictor

---

## 📌 Model Overview

**Model Name:** Loan Pre-Approval Prediction Model  
**Model Type:** Binary Classification  
**Framework:** scikit-learn Pipeline with CatBoost  
**Primary Use:** Predicting loan pre-approval likelihood (tentative)

This model estimates whether a loan application is likely to be
**pre-approved** based on applicant financial and demographic features.

⚠️ The output is **non-binding**, **informational only**, and must **not**
be interpreted as an official credit decision.

---

## 🎯 Intended Use

### Intended Use Cases
- Educational demonstration of a full ML pipeline
- Portfolio project
- Exploratory analysis of loan approval patterns
- User-facing *preliminary* loan assessment

### Out-of-Scope Uses
- Automated credit approval
- Legal or financial decision-making
- Replacement of official banking credit processes
- High-stakes decision systems without human review

---

## 📊 Training Data

### Dataset Source
- Analytics Vidhya – Loan Prediction Practice Problem  
- https://www.analyticsvidhya.com/datahack/contest/practice-problem-loan-prediction-iii/

### Dataset Characteristics
- Historical loan application data
- Mixed numerical and categorical features
- Binary target: `Loan_Status` (Approved / Not Approved)

### Data Preprocessing
- Removal of invalid or incomplete records
- Target encoding (`Y → 1`, `N → 0`)
- Categorical variables cast to string
- Feature engineering applied before modeling

---

## 🧮 Features Used

### Raw Input Features
- Gender
- Married
- Dependents
- Education
- Self_Employed
- ApplicantIncome
- CoapplicantIncome
- LoanAmount
- Loan_Amount_Term
- Credit_History
- Property_Area

### Engineered Features
- **Income:** Total household income
- **LoanInstallment:** Approximate monthly installment
- **IncomeImpact:** Loan burden relative to applicant income

---

## ⚙️ Model Architecture

The model is implemented as a single **scikit-learn Pipeline**:

1. Custom Feature Engineering
2. Numerical scaling + PCA (5 components)
3. Categorical imputation and one-hot encoding
4. CatBoost binary classifier

### Hyperparameters (CatBoost)
- Depth: 4
- Iterations: 100
- Learning rate: 0.01
- L2 regularization: 1

---

## 📈 Evaluation Summary

- Evaluation performed using historical data
- Metrics assessed during experimentation:
  - Accuracy: 0.809790
  - Recall: 0.982654
  - f1: 0.878318
  - ROC-AUC: 	0.760504

⚠️ Exact metrics may vary due to data splits and experimental setup.

---

## ⚠️ Limitations

- Dataset size is limited
- Data may not reflect current economic conditions
- Socioeconomic and demographic biases may be present
- PCA reduces interpretability of numerical features
- Predictions should not be used in isolation

---

## ⚖️ Ethical Considerations

- The model may reflect biases present in historical data
- Sensitive attributes are included and may influence predictions
- Outputs should always be reviewed by a human
- Transparency and user disclaimers are required

---

## 🔄 Reproducibility

The full training pipeline and data preprocessing steps are reproducible.

📄 See `HOW_TO_REPRODUCE.md` for exact instructions.

---

## 📅 Versioning

- Model Version: v1.0
- Training Date: 2025-12-16
- Dataset Version: Original Analytics Vidhya dataset
