"""Stress and missing-value robustness checks."""

import pandas as pd

from src.credit_model.evaluate import evaluate_classifier


def missing_value_stress(x_test: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    stressed = x_test.copy()
    for col in columns:
        if col in stressed.columns:
            stressed[col] = None
    return stressed


def macroeconomic_stress(x_test: pd.DataFrame) -> pd.DataFrame:
    stressed = x_test.copy()
    if "debt_to_income" in stressed:
        stressed["debt_to_income"] = (stressed["debt_to_income"] * 1.18).clip(upper=0.98)
    if "income" in stressed:
        stressed["income"] = (stressed["income"] * 0.92).clip(lower=10000)
    if "missed_payments_12m" in stressed:
        stressed["missed_payments_12m"] = stressed["missed_payments_12m"] + 1
    return stressed


def robustness_report(model, x_test: pd.DataFrame, y_test: pd.Series) -> dict:
    baseline = evaluate_classifier(model, x_test, y_test)
    stress = evaluate_classifier(model, macroeconomic_stress(x_test), y_test)
    missing = evaluate_classifier(model, missing_value_stress(x_test, ["income", "credit_history_length"]), y_test)
    return {
        "baseline_auc": baseline["auc"],
        "macroeconomic_stress_auc": stress["auc"],
        "missing_value_auc": missing["auc"],
        "stress_auc_delta": stress["auc"] - baseline["auc"],
        "missing_auc_delta": missing["auc"] - baseline["auc"],
    }

