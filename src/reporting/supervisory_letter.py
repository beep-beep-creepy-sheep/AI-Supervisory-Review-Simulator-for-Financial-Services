"""Generate a fictional supervisory letter."""

from src.config import BANK_NAME


def generate_supervisory_letter(top_findings: list[str]) -> str:
    findings = "\n".join(f"- {finding}" for finding in top_findings[:5])
    return f"""# Mock Supervisory Letter to {BANK_NAME}

To: Board Risk Committee and Chief Risk Officer, {BANK_NAME}

This fictional supervisory letter summarizes the AI risk review of the bank's credit risk model, consumer finance assistant, and agentic loan assistant.

## Key Findings
{findings}

## Required Remediation Actions
- Strengthen fairness monitoring for credit pre-screening and document thresholds for management action.
- Add periodic calibration, robustness, and drift monitoring with accountable owners.
- Maintain a controlled GenAI evaluation suite covering harmful advice, uncertainty, vulnerable consumers, and prompt injection.
- Require human escalation for vulnerability, hardship, policy-bypass, and high-impact lending scenarios.
- Evidence tool authorization, privacy controls, and complete tool-call logging for agentic workflows.

## Governance Expectations
The bank should provide named owners, management information, risk appetite limits, independent validation, and board-level reporting for all material AI systems.

## Timeline Placeholders
- 30 days: remediation plan and accountable owners.
- 60 days: enhanced monitoring evidence and revised controls.
- 90 days: independent validation report and board attestation.
"""

