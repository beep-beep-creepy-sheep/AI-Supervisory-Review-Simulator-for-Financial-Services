# Methodology

## Systems Under Evaluation

Emerald Credit Bank is a fictional bank with three AI systems: a credit-risk pre-screening model, a GenAI consumer finance assistant, and an agentic loan assistant that can call simulated tools.

## Evaluation Design

The review combines statistical testing, structured behavioral evaluation, and governance-oriented risk scoring. The synthetic credit dataset is deterministic and includes credit features, affordability indicators, protected-group proxies, and operational context. The GenAI and agentic assistants are evaluated through fixed test suites so results can be reproduced from a clean checkout.

## Metrics

Credit model metrics include AUC, precision, recall, F1, confusion matrix, Brier score, group fairness gaps, calibration tables, missing-value robustness, and macroeconomic stress robustness.

GenAI metrics include pass/fail, severity from 0 to 3, rationale, risk category, and example failure capture. Agentic metrics include pass/fail by tool-use risk category and a complete tool-call log.

## Scoring Rubric

Risk scoring uses severity from 0 to 3, likelihood from 1 to 5, detectability from 1 to 5, and evidence strength of low, medium, or high. Higher detectability means the issue is harder to detect. The residual score maps to low, medium, high, or critical.

## Assumptions

The dataset is synthetic and intentionally includes measurable proxy-risk patterns for demonstration. The GenAI evaluator uses rule-based checks with a mock judge rationale so the project runs without paid API keys.

## Limitations

Automated evaluation is useful for triage and regression testing but does not replace independent model validation, conduct-risk review, legal analysis, or real customer-impact monitoring.

