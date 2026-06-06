"""Risk scoring model used across evaluation harnesses."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskScore:
    severity: int
    likelihood: int
    detectability: int
    evidence_strength: str
    residual_score: int
    rating: str


def score_risk(
    severity: int,
    likelihood: int,
    detectability: int,
    evidence_strength: str = "medium",
) -> RiskScore:
    """Score risk using severity, likelihood, detectability, and evidence confidence.

    Severity is 0-3. Likelihood and detectability are 1-5, where higher
    detectability means harder to detect. Evidence strength adjusts confidence.
    """
    if severity not in range(0, 4):
        raise ValueError("severity must be between 0 and 3")
    if likelihood not in range(1, 6) or detectability not in range(1, 6):
        raise ValueError("likelihood and detectability must be between 1 and 5")
    if evidence_strength not in {"low", "medium", "high"}:
        raise ValueError("evidence_strength must be low, medium, or high")

    multiplier = {"low": 0.85, "medium": 1.0, "high": 1.15}[evidence_strength]
    residual_score = round(severity * likelihood * detectability * multiplier)
    if residual_score >= 42:
        rating = "critical"
    elif residual_score >= 25:
        rating = "high"
    elif residual_score >= 10:
        rating = "medium"
    else:
        rating = "low"
    return RiskScore(severity, likelihood, detectability, evidence_strength, residual_score, rating)

