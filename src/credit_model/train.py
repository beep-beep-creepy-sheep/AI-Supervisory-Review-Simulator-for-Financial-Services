"""Train credit-risk classifiers."""

from dataclasses import dataclass
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.config import RANDOM_SEED


TARGET = "loan_default"
ID_COLUMNS = ["customer_id"]
CATEGORICAL = ["employment_status", "age_band", "housing_status", "region", "protected_group_proxy"]
NUMERIC = ["income", "debt_to_income", "credit_history_length", "existing_debt", "missed_payments_12m", "digital_access_score"]


@dataclass
class TrainingResult:
    models: dict[str, Pipeline]
    x_train: pd.DataFrame
    x_test: pd.DataFrame
    y_train: pd.Series
    y_test: pd.Series


def make_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), NUMERIC),
            ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("encode", OneHotEncoder(handle_unknown="ignore"))]), CATEGORICAL),
        ]
    )


def train_models(df: pd.DataFrame, seed: int = RANDOM_SEED) -> TrainingResult:
    """Train logistic regression and random forest benchmark models."""
    x = df.drop(columns=[TARGET] + ID_COLUMNS)
    y = df[TARGET]
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=seed, stratify=y)
    models = {
        "logistic_regression": Pipeline(
            [("preprocess", make_preprocessor()), ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))]
        ),
        "random_forest": Pipeline(
            [("preprocess", make_preprocessor()), ("model", RandomForestClassifier(n_estimators=120, min_samples_leaf=12, random_state=seed, class_weight="balanced"))]
        ),
    }
    for model in models.values():
        model.fit(x_train, y_train)
    return TrainingResult(models, x_train, x_test, y_train, y_test)
