"""Credit model performance evaluation."""

from pathlib import Path
import json
import pandas as pd
from sklearn.metrics import auc, brier_score_loss, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score, roc_curve


def evaluate_classifier(model, x_test: pd.DataFrame, y_test: pd.Series, threshold: float = 0.5) -> dict:
    """Compute standard classifier, calibration, and confusion metrics."""
    probabilities = model.predict_proba(x_test)[:, 1]
    predictions = (probabilities >= threshold).astype(int)
    fpr, tpr, _ = roc_curve(y_test, probabilities)
    matrix = confusion_matrix(y_test, predictions).tolist()
    return {
        "auc": float(roc_auc_score(y_test, probabilities)),
        "roc_auc_integral": float(auc(fpr, tpr)),
        "precision": float(precision_score(y_test, predictions, zero_division=0)),
        "recall": float(recall_score(y_test, predictions, zero_division=0)),
        "f1": float(f1_score(y_test, predictions, zero_division=0)),
        "brier_score": float(brier_score_loss(y_test, probabilities)),
        "confusion_matrix": matrix,
    }


def evaluate_models(models: dict, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, dict]:
    return {name: evaluate_classifier(model, x_test, y_test) for name, model in models.items()}


def save_metrics(metrics: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

