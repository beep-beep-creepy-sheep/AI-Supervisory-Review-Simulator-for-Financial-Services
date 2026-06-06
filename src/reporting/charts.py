"""Chart generation for supervisory evidence."""

from pathlib import Path
import os
import pandas as pd

_MPL_CACHE = Path(__file__).resolve().parents[2] / "outputs" / ".matplotlib"
_MPL_CACHE.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_MPL_CACHE))
os.environ.setdefault("XDG_CACHE_HOME", str(_MPL_CACHE))

import matplotlib.pyplot as plt


def save_credit_metric_chart(metrics: dict[str, dict], path: Path) -> None:
    """Save a compact model comparison chart."""
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(metrics).T[["auc", "precision", "recall", "f1", "brier_score"]]
    ax = frame.plot(kind="bar", figsize=(9, 4), rot=0)
    ax.set_title("Credit Model Evaluation Metrics")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def save_risk_rating_chart(register: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts = register["rating"].value_counts().reindex(["critical", "high", "medium", "low"]).fillna(0)
    ax = counts.plot(kind="bar", color=["#7f1d1d", "#b91c1c", "#d97706", "#047857"], figsize=(7, 4), rot=0)
    ax.set_title("Risk Register Rating Distribution")
    ax.set_ylabel("Number of findings")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()
