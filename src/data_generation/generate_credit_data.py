"""Synthetic credit-risk dataset generation for Emerald Credit Bank."""

from pathlib import Path
import numpy as np
import pandas as pd

from src.config import RAW_DATA_DIR, RANDOM_SEED, ensure_directories


COLUMNS = [
    "customer_id",
    "income",
    "employment_status",
    "age_band",
    "debt_to_income",
    "credit_history_length",
    "existing_debt",
    "missed_payments_12m",
    "housing_status",
    "region",
    "digital_access_score",
    "protected_group_proxy",
    "loan_default",
]


def generate_credit_dataset(n_rows: int = 2500, seed: int = RANDOM_SEED) -> pd.DataFrame:
    """Generate a realistic synthetic loan pre-screening dataset."""
    rng = np.random.default_rng(seed)
    employment = rng.choice(["employed", "self_employed", "part_time", "unemployed"], n_rows, p=[0.56, 0.16, 0.18, 0.10])
    age_band = rng.choice(["18-24", "25-34", "35-49", "50-64", "65+"], n_rows, p=[0.10, 0.26, 0.34, 0.22, 0.08])
    housing = rng.choice(["owner", "mortgage", "private_rent", "social_rent", "living_with_family"], n_rows, p=[0.20, 0.33, 0.28, 0.11, 0.08])
    region = rng.choice(["Dublin", "Cork", "Galway", "Limerick", "Rural"], n_rows, p=[0.34, 0.20, 0.14, 0.12, 0.20])
    protected_proxy = rng.choice(["A", "B"], n_rows, p=[0.72, 0.28])

    income_base = rng.lognormal(mean=10.75, sigma=0.45, size=n_rows)
    income_adjust = np.where(employment == "unemployed", 0.35, np.where(employment == "part_time", 0.62, 1.0))
    group_adjust = np.where(protected_proxy == "B", 0.90, 1.0)
    income = np.clip(income_base * income_adjust * group_adjust, 12000, 160000).round(0)

    missed = rng.poisson(lam=np.where(employment == "unemployed", 1.6, 0.45), size=n_rows)
    dti = np.clip(rng.beta(2.2, 4.2, n_rows) + missed * 0.045 + np.where(protected_proxy == "B", 0.035, 0), 0.03, 0.95)
    existing_debt = np.clip(income * dti * rng.uniform(0.35, 1.15, n_rows), 500, 140000).round(0)
    credit_history = np.clip(rng.normal(8.5, 5.2, n_rows) + np.select([age_band == "18-24", age_band == "65+"], [-4, 5], 0), 0, 35).round(1)
    digital_access = np.clip(rng.normal(68, 18, n_rows) - np.where(age_band == "65+", 16, 0) - np.where(protected_proxy == "B", 5, 0), 5, 100).round(1)

    logit = (
        -2.3
        + dti * 3.2
        + missed * 0.42
        - np.log1p(income) * 0.08
        - credit_history * 0.045
        + np.where(employment == "unemployed", 0.85, 0)
        + np.where(housing == "private_rent", 0.28, 0)
        + np.where(protected_proxy == "B", 0.18, 0)
    )
    probability = 1 / (1 + np.exp(-logit))
    default = rng.binomial(1, probability)

    return pd.DataFrame(
        {
            "customer_id": [f"ECB-{i:05d}" for i in range(n_rows)],
            "income": income,
            "employment_status": employment,
            "age_band": age_band,
            "debt_to_income": dti.round(3),
            "credit_history_length": credit_history,
            "existing_debt": existing_debt,
            "missed_payments_12m": missed,
            "housing_status": housing,
            "region": region,
            "digital_access_score": digital_access,
            "protected_group_proxy": protected_proxy,
            "loan_default": default,
        }
    )


def save_credit_dataset(path: Path | None = None, n_rows: int = 2500) -> Path:
    ensure_directories()
    output = path or RAW_DATA_DIR / "emerald_credit_synthetic.csv"
    generate_credit_dataset(n_rows=n_rows).to_csv(output, index=False)
    return output


if __name__ == "__main__":
    print(save_credit_dataset())

