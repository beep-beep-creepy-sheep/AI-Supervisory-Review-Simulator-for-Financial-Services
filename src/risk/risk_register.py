"""Structured risk register assembled from evaluation evidence."""

from dataclasses import asdict, dataclass
from pathlib import Path
import pandas as pd

from src.risk.scoring_model import score_risk


@dataclass
class RiskRegisterEntry:
    system: str
    category: str
    finding: str
    evidence: str
    severity: int
    likelihood: int
    detectability: int
    evidence_strength: str
    owner: str
    mitigation: str

    def to_record(self) -> dict:
        scored = score_risk(self.severity, self.likelihood, self.detectability, self.evidence_strength)
        record = asdict(self)
        record.update({"residual_score": scored.residual_score, "rating": scored.rating})
        return record


def build_register(entries: list[RiskRegisterEntry]) -> pd.DataFrame:
    """Convert risk entries to a sorted DataFrame."""
    df = pd.DataFrame([entry.to_record() for entry in entries])
    if df.empty:
        return df
    order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return df.sort_values(by="rating", key=lambda s: s.map(order)).reset_index(drop=True)


def save_register(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)

