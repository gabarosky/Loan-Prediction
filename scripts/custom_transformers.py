from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np

class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Custom transformer that generates new financial features for credit analysis.
    Produces: Income, LoanInstallment, IncomeImpact.
    Safe to call even if some columns are missing or incomes are zero.
    """
    def __init__(self, feature_name='feature_A'):
        self.feature_name = feature_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Work on a copy
        X_transformed = X.copy()

        # Ensure DataFrame
        if not isinstance(X_transformed, pd.DataFrame):
            X_transformed = pd.DataFrame(X_transformed)

        # Provide defaults if columns missing
        for col in ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']:
            if col not in X_transformed.columns:
                X_transformed[col] = 0

        # Replace None/NaN with zeros for numeric ops (but keep original missingness for later pipeline)
        X_transformed[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']] = \
            X_transformed[['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']].fillna(0)

        # Calculate total combined income
        X_transformed['Income'] = X_transformed['ApplicantIncome'] + X_transformed['CoapplicantIncome']

        # Avoid divide-by-zero for Loan_Amount_Term: if zero, use a small epsilon
        loan_term = X_transformed['Loan_Amount_Term'].replace({0: np.nan})
        loan_term = loan_term.fillna(1)  # fallback to 1 if term missing/0 to avoid inf

        # LoanInstallment: LoanAmount is likely in thousands in some datasets; keep consistent with your data
        X_transformed['LoanInstallment'] = X_transformed['LoanAmount'] / loan_term

        # IncomeImpact: protect ApplicantIncome zero -> use Income instead, and if still zero, set NaN
        denom = X_transformed['ApplicantIncome'].replace({0: np.nan})
        denom = denom.fillna(X_transformed['Income'])
        denom = denom.replace({0: np.nan})

        X_transformed['IncomeImpact'] = X_transformed['LoanInstallment'] / denom

        # If IncomeImpact is inf or NaN, set to a large number or NaN (downstream imputer can handle)
        X_transformed['IncomeImpact'] = X_transformed['IncomeImpact'].replace([np.inf, -np.inf], np.nan)

        return X_transformed
