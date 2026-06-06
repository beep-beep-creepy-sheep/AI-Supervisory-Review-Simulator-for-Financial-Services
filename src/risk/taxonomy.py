"""Risk taxonomy for supervisory AI review."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskCategory:
    name: str
    description: str


RISK_TAXONOMY = [
    RiskCategory("Model performance risk", "Predictive failures, weak discrimination, or unstable accuracy."),
    RiskCategory("Fairness and discrimination risk", "Unequal outcomes or proxies affecting protected groups."),
    RiskCategory("Consumer harm risk", "Advice or automation that worsens customer financial outcomes."),
    RiskCategory("Hallucination and misinformation risk", "Unsupported or fabricated financial claims."),
    RiskCategory("Explainability and transparency risk", "Insufficient reasons for model or assistant outputs."),
    RiskCategory("Robustness and drift risk", "Performance degradation under missing data or stress scenarios."),
    RiskCategory("Privacy and data access risk", "Unnecessary disclosure, retention, or use of personal data."),
    RiskCategory("Prompt injection and adversarial misuse risk", "Instruction override or malicious input success."),
    RiskCategory("Agentic tool-use risk", "Unsafe, unauthorized, or poorly logged automated tool actions."),
    RiskCategory("Governance and accountability risk", "Weak ownership, controls, monitoring, or escalation."),
]


def category_names() -> list[str]:
    return [item.name for item in RISK_TAXONOMY]

