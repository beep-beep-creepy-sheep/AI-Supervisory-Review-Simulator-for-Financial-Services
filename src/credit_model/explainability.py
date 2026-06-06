"""Lightweight explainability artifacts for trained credit models."""

import pandas as pd


def feature_importance_table(model, top_n: int = 15) -> pd.DataFrame:
    """Extract transformed feature importances when the estimator supports them."""
    if not hasattr(model.named_steps["model"], "feature_importances_"):
        return pd.DataFrame(columns=["feature", "importance"])
    names = model.named_steps["preprocess"].get_feature_names_out()
    importances = model.named_steps["model"].feature_importances_
    table = pd.DataFrame({"feature": names, "importance": importances})
    return table.sort_values("importance", ascending=False).head(top_n).reset_index(drop=True)

