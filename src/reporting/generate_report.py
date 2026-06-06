"""End-to-end pipeline and evidence pack generation."""

from pathlib import Path
import json
import shutil
import pandas as pd

from src.agentic_assistant.evaluator import evaluate_agent_cases, generate_agent_test_cases, save_agent_test_cases
from src.config import CHARTS_DIR, METRICS_DIR, REPORTS_DIR, ensure_directories
from src.credit_model.calibration import calibration_table
from src.credit_model.evaluate import evaluate_models, save_metrics
from src.credit_model.explainability import feature_importance_table
from src.credit_model.fairness import group_fairness_metrics, max_fairness_gap
from src.credit_model.robustness import robustness_report
from src.credit_model.train import train_models
from src.data_generation.generate_credit_data import generate_credit_dataset, save_credit_dataset
from src.genai_assistant.evaluator import evaluate_genai_cases, save_genai_results
from src.genai_assistant.test_cases import generate_genai_test_cases, save_genai_test_cases
from src.reporting.charts import save_credit_metric_chart, save_risk_rating_chart
from src.reporting.supervisory_letter import generate_supervisory_letter
from src.risk.risk_register import RiskRegisterEntry, build_register, save_register

WEB_PUBLIC_DIR = Path(__file__).resolve().parents[2] / "web" / "public"


def build_risk_register(credit_metrics: dict, fairness_gap: float, robustness: dict, genai_results: pd.DataFrame, agent_results: pd.DataFrame) -> pd.DataFrame:
    """Build a supervisory risk register from generated evidence."""
    genai_failures = int((~genai_results["passed"]).sum())
    agent_failures = int((~agent_results["passed"]).sum())
    entries = [
        RiskRegisterEntry("Credit Risk Model", "Model performance risk", "Model discrimination is adequate but requires threshold governance.", f"Best AUC {max(m['auc'] for m in credit_metrics.values()):.3f}", 1, 3, 3, "high", "Model Risk", "Document champion model threshold and validation cadence."),
        RiskRegisterEntry("Credit Risk Model", "Fairness and discrimination risk", "Protected proxy group metrics show measurable outcome gaps.", f"Maximum fairness gap {fairness_gap:.3f}", 2 if fairness_gap > 0.08 else 1, 3, 4, "high", "Fair Lending", "Set group monitoring triggers and remediation workflow."),
        RiskRegisterEntry("Credit Risk Model", "Robustness and drift risk", "Performance shifts under macroeconomic and missing-data stress.", f"Stress AUC delta {robustness['stress_auc_delta']:.3f}", 2, 3, 3, "medium", "Model Risk", "Add stress tests to periodic monitoring."),
        RiskRegisterEntry("GenAI Assistant", "Consumer harm risk", "Automated test suite found residual unsafe-response risk.", f"{genai_failures} failed cases from {len(genai_results)}", 3 if genai_failures else 1, 2, 3, "medium", "Digital Banking", "Expand refusal and vulnerability handling tests."),
        RiskRegisterEntry("GenAI Assistant", "Prompt injection and adversarial misuse risk", "Prompt injection controls require continuous regression testing.", "Dedicated injection cases included in harness.", 2, 3, 4, "medium", "AI Governance", "Maintain attack library and release gates."),
        RiskRegisterEntry("Agentic Loan Assistant", "Agentic tool-use risk", "Tool authorization and escalation behavior need supervisory evidence.", f"{agent_failures} failed cases from {len(agent_results)}", 3 if agent_failures else 1, 3, 4, "high", "Operations", "Restrict tools by purpose and test escalation gates."),
        RiskRegisterEntry("All Systems", "Governance and accountability risk", "Evidence pack should be linked to accountable owners and MI.", "Cross-system register generated.", 2, 3, 3, "medium", "Board Risk", "Add owner attestations and monitoring pack."),
    ]
    return build_register(entries)


def write_evidence_pack(metrics: dict, fairness: pd.DataFrame, robustness: dict, genai: pd.DataFrame, agent: pd.DataFrame, register: pd.DataFrame, path: Path, explainability: pd.DataFrame | None = None) -> None:
    """Write a Markdown supervisory evidence pack."""
    top_risks = register.head(5)[["system", "category", "rating", "finding"]].to_markdown(index=False)
    content = f"""# Supervisory Evidence Pack

## Executive Summary
Emerald Credit Bank's fictional AI estate was assessed across model risk, fairness, consumer harm, explainability, robustness, privacy, prompt injection, agentic tool-use, and governance maturity. The review combines statistical model evaluation, structured GenAI test cases, simulated agent tool-call review, and a risk register.

## AI System Inventory
| System | Purpose | Review focus |
|---|---|---|
| Credit Risk Model | Loan pre-screening | Performance, calibration, fairness, robustness |
| GenAI Consumer Finance Assistant | Customer support and general financial guidance | Harmful advice, hallucination, vulnerable consumers, prompt injection |
| Agentic Loan Assistant | Simulated tool-using loan workflow | Tool authorization, privacy, escalation, over-automation |

## Methodology
The pipeline uses deterministic synthetic data, benchmark ML models, rule-based GenAI scoring with mock-judge rationale, agentic tool logs, and a severity-likelihood-detectability scoring model. Automated results are suitable for triage and portfolio evidence, not as a substitute for legal, conduct, or model validation sign-off.

## Credit Model Findings
```json
{json.dumps(metrics, indent=2)}
```

Fairness summary:
{fairness.to_markdown(index=False)}

Robustness summary:
```json
{json.dumps(robustness, indent=2)}
```

Top feature-importance evidence:
{(explainability if explainability is not None else pd.DataFrame()).to_markdown(index=False)}

## GenAI Findings
- Test cases: {len(genai)}
- Pass rate: {genai['passed'].mean():.1%}
- Highest failed severity: {int(genai['severity_score'].max())}

## Agentic Tool-Use Findings
- Test cases: {len(agent)}
- Pass rate: {agent['passed'].mean():.1%}
- Highest failed severity: {int(agent['severity_score'].max())}

## Risk Register
{top_risks}

## Mitigation Recommendations
- Define risk appetite thresholds for model performance, fairness gaps, and calibration drift.
- Use red-team style GenAI regression suites before assistant releases.
- Restrict agentic tool access by user intent, customer consent, and documented purpose.
- Require human review for vulnerable consumers and high-impact lending outcomes.
- Maintain board-level AI management information and independent validation evidence.

## Mock Supervisory Conclusion
The systems are demonstrable and partially controlled, but supervisory confidence depends on stronger fairness thresholds, continuous adversarial testing, and clearer accountability for agentic tool use.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_react_dashboard_data(
    metrics: dict,
    fairness: pd.DataFrame,
    robustness: dict,
    genai: pd.DataFrame,
    agent: pd.DataFrame,
    register: pd.DataFrame,
    explainability: pd.DataFrame,
) -> Path:
    """Export compact JSON consumed by the React dashboard."""
    dashboard_data = {
        "project": {
            "title": "AI Supervisory Review Simulator for Financial Services",
            "bank": "Emerald Credit Bank",
            "summary": "Regulator-style AI risk assessment across credit ML, GenAI assistant, agentic loan workflows, and governance controls.",
        },
        "inventory": [
            {"system": "Credit Risk Model", "purpose": "Loan pre-screening", "evidence": "AUC, calibration, fairness, robustness, explainability"},
            {"system": "GenAI Consumer Finance Assistant", "purpose": "General customer support", "evidence": "120 structured safety and behavior cases"},
            {"system": "Agentic Loan Assistant", "purpose": "Simulated loan workflow with tools", "evidence": "50 tool-use risk cases and full tool logs"},
        ],
        "creditMetrics": metrics,
        "fairness": fairness.to_dict(orient="records"),
        "robustness": robustness,
        "genaiSummary": {
            "cases": int(len(genai)),
            "passRate": float(genai["passed"].mean()),
            "failedCases": int((~genai["passed"]).sum()),
            "highestSeverity": int(genai["severity_score"].max()),
        },
        "agenticSummary": {
            "cases": int(len(agent)),
            "passRate": float(agent["passed"].mean()),
            "failedCases": int((~agent["passed"]).sum()),
            "highestSeverity": int(agent["severity_score"].max()),
        },
        "riskRegister": register.to_dict(orient="records"),
        "explainability": explainability.to_dict(orient="records"),
    }
    output = REPORTS_DIR / "dashboard_data.json"
    output.write_text(json.dumps(dashboard_data, indent=2), encoding="utf-8")
    return output


def publish_react_dashboard_artifacts(dashboard_data_path: Path, evidence_path: Path) -> None:
    """Copy generated artifacts into the Vite public directory."""
    WEB_PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dashboard_data_path, WEB_PUBLIC_DIR / "dashboard_data.json")
    shutil.copy2(evidence_path, WEB_PUBLIC_DIR / "supervisory_evidence_pack.md")


def _category_summary(results: pd.DataFrame) -> list[dict]:
    rows = []
    for category, group in results.groupby("risk_category"):
        rows.append(
            {
                "risk_category": category,
                "cases": int(len(group)),
                "failures": int((~group["passed"]).sum()),
                "failure_rate": float((~group["passed"]).mean()),
                "highest_severity": int(group["severity_score"].max()),
            }
        )
    return rows


def write_public_static_data(
    metrics: dict,
    fairness: pd.DataFrame,
    robustness: dict,
    genai: pd.DataFrame,
    agent: pd.DataFrame,
    register: pd.DataFrame,
    explainability: pd.DataFrame,
) -> dict[str, Path]:
    """Write deployment-ready static JSON files for the React portfolio site."""
    data_dir = WEB_PUBLIC_DIR / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    champion = metrics["random_forest"]
    genai_failures = genai[~genai["passed"]]
    agent_failures = agent[~agent["passed"]]
    max_fairness_gap_value = float(fairness.filter(like="_gap_to_best").max().max())
    files = {
        "system_inventory": [
            {
                "id": "credit-risk-model",
                "name": "Credit Risk Model",
                "purpose": "Loan pre-screening model trained on synthetic tabular credit data.",
                "users_affected": "Retail borrowers applying for unsecured credit.",
                "risk_level": "High",
                "evaluated_risks": ["Model performance", "Fairness", "Calibration", "Robustness", "Explainability"],
                "key_findings": [
                    f"Champion Random Forest AUC {champion['auc']:.3f} with Brier score {champion['brier_score']:.3f}.",
                    f"Maximum protected-proxy fairness gap {max_fairness_gap_value:.3f}.",
                    f"Stress AUC delta {robustness['stress_auc_delta']:.3f}.",
                ],
            },
            {
                "id": "genai-consumer-assistant",
                "name": "GenAI Consumer Finance Assistant",
                "purpose": "Simulated customer support assistant for loans, debt, affordability, scams, and vulnerable consumer scenarios.",
                "users_affected": "Retail customers seeking financial guidance.",
                "risk_level": "Medium",
                "evaluated_risks": ["Hallucination", "Harmful advice", "Misleading certainty", "Vulnerable consumer handling", "Prompt injection"],
                "key_findings": [
                    f"{int((~genai['passed']).sum())} failed cases from {len(genai)} structured tests.",
                    "Prompt injection cases require continuous regression testing.",
                    "Refusal behavior is the dominant residual issue in the demo harness.",
                ],
            },
            {
                "id": "agentic-loan-assistant",
                "name": "Agentic Loan Assistant",
                "purpose": "Simulated loan workflow that can retrieve policy, check profiles, calculate affordability, recommend next steps, and escalate.",
                "users_affected": "Borrowers whose cases are triaged by automated tool workflows.",
                "risk_level": "High",
                "evaluated_risks": ["Unauthorized tool use", "Privacy leakage", "Policy bypass", "Failure to escalate", "Over-automation"],
                "key_findings": [
                    f"{int((~agent['passed']).sum())} failed cases from {len(agent)} agent-risk tests.",
                    "Unauthorized profile-access scenarios require stronger purpose checks.",
                    "High-risk vulnerability cases are routed to human escalation in the simulated workflow.",
                ],
            },
        ],
        "key_metrics": [
            {"label": "Credit Model AUC", "value": round(champion["auc"], 3), "unit": "", "detail": "Random Forest champion model"},
            {"label": "Fairness Gap", "value": round(max_fairness_gap_value, 3), "unit": "", "detail": "Maximum protected-proxy group gap"},
            {"label": "GenAI Failure Rate", "value": round(float((~genai["passed"]).mean()), 3), "unit": "%", "detail": f"{int((~genai['passed']).sum())}/{len(genai)} cases failed"},
            {"label": "Agent Tool Misuse Rate", "value": round(float((~agent["passed"]).mean()), 3), "unit": "%", "detail": f"{int((~agent['passed']).sum())}/{len(agent)} cases failed"},
        ],
        "risk_register": [
            {"risk_id": f"RR-{i + 1:03d}", **record}
            for i, record in enumerate(register.to_dict(orient="records"))
        ],
        "genai_eval_results": {
            "summary": {
                "total_cases": int(len(genai)),
                "failed_cases": int((~genai["passed"]).sum()),
                "pass_rate": float(genai["passed"].mean()),
                "harmful_advice_rate": float(genai.loc[genai["risk_category"] == "harmful_financial_advice", "severity_score"].gt(0).mean()),
                "hallucination_rate": float(genai.loc[genai["risk_category"] == "hallucination", "severity_score"].gt(0).mean()),
                "prompt_injection_success_rate": float(genai.loc[genai["risk_category"] == "prompt_injection", "severity_score"].gt(0).mean()),
            },
            "by_category": _category_summary(genai),
        },
        "agentic_eval_results": {
            "summary": {
                "total_cases": int(len(agent)),
                "failed_cases": int((~agent["passed"]).sum()),
                "pass_rate": float(agent["passed"].mean()),
                "tool_misuse_rate": float((~agent["passed"]).mean()),
                "unauthorized_tool_use_failure_rate": float(agent.loc[agent["risk_category"] == "unauthorized_tool_use", "severity_score"].gt(0).mean()),
                "prompt_injection_success_rate": float(agent.loc[agent["risk_category"] == "prompt_injection", "severity_score"].gt(0).mean()),
            },
            "by_category": _category_summary(agent),
        },
        "credit_model_metrics": {
            "models": metrics,
            "fairness": fairness.to_dict(orient="records"),
            "robustness": robustness,
            "explainability": explainability.to_dict(orient="records"),
        },
        "failure_examples": [
            *[
                {
                    "id": row["id"],
                    "system": "GenAI Consumer Finance Assistant",
                    "risk_category": row["risk_category"],
                    "severity": int(row["severity_score"]),
                    "failure": row["rationale"],
                    "evidence": row["response"],
                    "expected_control": "Refuse unsafe requests, avoid misleading certainty, and escalate vulnerable consumer cases.",
                }
                for _, row in genai_failures.head(5).iterrows()
            ],
            *[
                {
                    "id": row["id"],
                    "system": "Agentic Loan Assistant",
                    "risk_category": row["risk_category"],
                    "severity": int(row["severity_score"]),
                    "failure": row["rationale"],
                    "evidence": f"Agent decision: {row['decision']}",
                    "expected_control": "Restrict tool use by purpose, preserve privacy, and escalate high-impact cases.",
                }
                for _, row in agent_failures.head(5).iterrows()
            ],
        ],
    }
    written = {}
    for name, payload in files.items():
        path = data_dir / f"{name}.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        written[name] = path
    return written


def run_pipeline() -> dict[str, Path]:
    """Run the full simulator and generate portfolio artifacts."""
    ensure_directories()
    dataset_path = save_credit_dataset()
    df = generate_credit_dataset()
    training = train_models(df)
    metrics = evaluate_models(training.models, training.x_test, training.y_test)
    save_metrics(metrics, METRICS_DIR / "credit_model_metrics.json")

    champion = training.models["random_forest"]
    fairness_df = group_fairness_metrics(champion, training.x_test, training.y_test)
    fairness_df.to_csv(METRICS_DIR / "fairness_metrics.csv", index=False)
    feature_importance_table(champion).to_csv(METRICS_DIR / "feature_importance.csv", index=False)
    calibration_table(champion, training.x_test, training.y_test).to_csv(METRICS_DIR / "calibration_table.csv", index=False)
    robustness = robustness_report(champion, training.x_test, training.y_test)
    (METRICS_DIR / "robustness_metrics.json").write_text(json.dumps(robustness, indent=2), encoding="utf-8")

    save_genai_test_cases()
    genai_results = evaluate_genai_cases(generate_genai_test_cases())
    save_genai_results(genai_results, METRICS_DIR / "genai_results.csv")
    save_agent_test_cases()
    agent_results, tool_log = evaluate_agent_cases(generate_agent_test_cases())
    agent_results.to_csv(METRICS_DIR / "agentic_results.csv", index=False)
    tool_log.to_csv(METRICS_DIR / "agentic_tool_log.csv", index=False)

    register = build_risk_register(metrics, max_fairness_gap(fairness_df), robustness, genai_results, agent_results)
    save_register(register, METRICS_DIR / "risk_register.csv")

    save_credit_metric_chart(metrics, CHARTS_DIR / "credit_model_metrics.png")
    save_risk_rating_chart(register, CHARTS_DIR / "risk_rating_distribution.png")

    evidence_path = REPORTS_DIR / "supervisory_evidence_pack.md"
    explainability = pd.read_csv(METRICS_DIR / "feature_importance.csv")
    write_evidence_pack(metrics, fairness_df, robustness, genai_results, agent_results, register, evidence_path, explainability)
    dashboard_data_path = write_react_dashboard_data(metrics, fairness_df, robustness, genai_results, agent_results, register, explainability)
    publish_react_dashboard_artifacts(dashboard_data_path, evidence_path)
    public_data_paths = write_public_static_data(metrics, fairness_df, robustness, genai_results, agent_results, register, explainability)
    letter_path = REPORTS_DIR / "mock_supervisory_letter.md"
    letter_path.write_text(generate_supervisory_letter(register["finding"].head(5).tolist()), encoding="utf-8")

    return {
        "dataset": dataset_path,
        "credit_metrics": METRICS_DIR / "credit_model_metrics.json",
        "risk_register": METRICS_DIR / "risk_register.csv",
        "evidence_pack": evidence_path,
        "dashboard_data": dashboard_data_path,
        "public_data": public_data_paths["key_metrics"],
        "supervisory_letter": letter_path,
    }


if __name__ == "__main__":
    for name, path in run_pipeline().items():
        print(f"{name}: {path}")
