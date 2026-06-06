"""Calibration summaries for credit-risk models."""

import pandas as pd
from sklearn.calibration import calibration_curve


def calibration_table(model, x_test: pd.DataFrame, y_test: pd.Series, bins: int = 8) -> pd.DataFrame:
    probabilities = model.predict_proba(x_test)[:, 1]
    frac_pos, mean_pred = calibration_curve(y_test, probabilities, n_bins=bins, strategy="quantile")
    return pd.DataFrame({"mean_predicted_probability": mean_pred, "observed_default_rate": frac_pos})

