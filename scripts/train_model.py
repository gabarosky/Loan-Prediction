import joblib
import os
import sys
import pandas as pd

# allow importing local modules when executed from repo root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# now import custom transformer
from custom_transformers import FeatureEngineer

from sklearn.impute import SimpleImputer
from catboost import CatBoostClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Try to import config for paths; fallback to computed paths
try:
    from config import get_model_path, get_data_path
except Exception:
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    def get_data_path(filename): return os.path.join(PROJECT_ROOT, 'data', filename)
    def get_model_path(filename): return os.path.join(PROJECT_ROOT, 'models', filename)


def create_full_pipeline(numeric_features, categorical_features, model_estimator):
    numeric_pipeline = Pipeline(steps=[
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=min(5, len(numeric_features))))
    ])

    categorical_pipeline = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='DK')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_pipeline, numeric_features),
            ('cat', categorical_pipeline, categorical_features)
        ],
        remainder='passthrough'
    )

    full_pipeline = Pipeline(steps=[
        ('feature_engineer', FeatureEngineer()),
        ('preprocessor', preprocessor),
        ('estimator', model_estimator)
    ])

    return full_pipeline

def load_and_clean_data():
    file_path = get_data_path('train.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    print("📥 Loading original data...")
    df = pd.read_csv(file_path)

    cols_to_str = ['Gender', 'Married', 'Education', 'Self_Employed',
                   'Dependents', 'Property_Area', 'Credit_History']

    for col in cols_to_str:
        if col in df.columns:
            df[col] = df[col].astype(str)

    if 'Loan_Status' in df.columns:
        df['Loan_Status'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

    # drop entries with missing values in 'LoanAmount' and 'Loan_Amount_Term'
    if 'LoanAmount' in df.columns and 'Loan_Amount_Term' in df.columns:
        df = df.dropna(subset=['LoanAmount', 'Loan_Amount_Term'])

    if 'Loan_ID' in df.columns:
        df.drop(columns='Loan_ID', inplace=True)

    cleaned_path = get_data_path('cleaned.csv')
    df.to_csv(cleaned_path, index=False)
    print(f"✅ Cleaned data saved: {cleaned_path}  shape: {df.shape}")
    return df

def train_model():
    numerical_cols = [
        'Income', 'ApplicantIncome', 'CoapplicantIncome',
        'LoanInstallment', 'LoanAmount', 'Loan_Amount_Term',
        'IncomeImpact'
    ]
    categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Dependents',
                        'Property_Area', 'Credit_History']

    model = CatBoostClassifier(
        verbose=0,
        depth=4,
        iterations=100,
        l2_leaf_reg=1,
        learning_rate=0.01
    )

    pipeline = create_full_pipeline(numerical_cols, categorical_cols, model)

    df = load_and_clean_data()

    target = 'Loan_Status'
    if target not in df.columns:
        raise KeyError(f"Target column '{target}' not found in cleaned data")

    X = df.drop(target, axis=1)
    y = df[target]

    print("🚀 Initiating Pipeline training...")
    pipeline.fit(X, y)
    print("✅ Pipeline successfully trained.")

    model_path = get_model_path('trained_model.pkl')
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipeline, model_path)
    print(f"💾 Pipeline saved to: {model_path}")

if __name__ == "__main__":
    train_model()
