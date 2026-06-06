from src.risk.risk_register import RiskRegisterEntry, build_register
from src.risk.scoring_model import score_risk


def test_risk_scoring_logic():
    low = score_risk(1, 1, 1, "medium")
    critical = score_risk(3, 5, 5, "high")
    assert low.rating == "low"
    assert critical.rating == "critical"


def test_risk_register_adds_rating():
    register = build_register(
        [
            RiskRegisterEntry(
                system="GenAI Assistant",
                category="Consumer harm risk",
                finding="Unsafe advice risk",
                evidence="test failure",
                severity=3,
                likelihood=4,
                detectability=4,
                evidence_strength="high",
                owner="AI Governance",
                mitigation="Add release gate",
            )
        ]
    )
    assert register.iloc[0]["rating"] in {"high", "critical"}
    assert "residual_score" in register.columns

