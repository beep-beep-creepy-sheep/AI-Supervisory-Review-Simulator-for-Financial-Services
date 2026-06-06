from src.credit_model.fairness import group_fairness_metrics, max_fairness_gap
from src.credit_model.train import train_models
from src.data_generation.generate_credit_data import COLUMNS, generate_credit_dataset


def test_data_generation_shape_and_columns():
    df = generate_credit_dataset(n_rows=200)
    assert df.shape == (200, len(COLUMNS))
    assert list(df.columns) == COLUMNS
    assert set(df["loan_default"].unique()).issubset({0, 1})


def test_credit_training_and_fairness_metrics():
    df = generate_credit_dataset(n_rows=500)
    result = train_models(df)
    fairness = group_fairness_metrics(result.models["logistic_regression"], result.x_test, result.y_test)
    assert {"group", "approval_rate", "false_positive_rate"}.issubset(fairness.columns)
    assert max_fairness_gap(fairness) >= 0

