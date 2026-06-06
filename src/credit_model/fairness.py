"""Fairness metrics for credit-risk models."""

import pandas as pd


def group_fairness_metrics(model, x_test: pd.DataFrame, y_test: pd.Series, group_col: str = "protected_group_proxy", threshold: float = 0.5) -> pd.DataFrame:
    """Calculate group approval, default capture, and false-positive rates."""
    probabilities = model.predict_proba(x_test)[:, 1]
    predicted_default = probabilities >= threshold
    records = []
    for group, idx in x_test.groupby(group_col).groups.items():
        y_group = y_test.loc[idx]
        pred = pd.Series(predicted_default, index=x_test.index).loc[idx]
        approvals = (~pred).mean()
        positives = y_group == 1
        negatives = y_group == 0
        records.append(
            {
                "group": group,
                "n": int(len(idx)),
                "approval_rate": float(approvals),
                "default_capture_rate": float((pred & positives).sum() / max(positives.sum(), 1)),
                "false_positive_rate": float((pred & negatives).sum() / max(negatives.sum(), 1)),
            }
        )
    df = pd.DataFrame(records)
    if len(df) >= 2:
        for metric in ["approval_rate", "default_capture_rate", "false_positive_rate"]:
            df[f"{metric}_gap_to_best"] = float(df[metric].max() - df[metric].min())
    return df


def max_fairness_gap(fairness_df: pd.DataFrame) -> float:
    gap_cols = [col for col in fairness_df.columns if col.endswith("_gap_to_best")]
    return float(fairness_df[gap_cols].max().max()) if gap_cols else 0.0

