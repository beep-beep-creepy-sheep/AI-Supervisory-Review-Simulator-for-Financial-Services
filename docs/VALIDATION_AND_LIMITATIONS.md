# Validation And Limitations

This project is a self-directed AI-assisted prototype that connects synthetic AI-system evaluation outputs into evidence artifacts. It is not production regulatory tooling and does not claim compliance, deployment readiness, or use of real bank data.

## Synthetic Data Limitations

The bank, customers, prompts, personas, policies, credit records, tool logs, outputs, dashboard data, evidence pack, and mock letter are fictional. Synthetic data is useful for public reproducibility and privacy protection, but it cannot represent the full complexity, distribution, conduct context, or legal obligations of real financial services data.

## Keyword Scoring Limitations

The GenAI scorer uses simple `SAFE_TERMS` and `BAD_TERMS` as a prototype triage layer. These terms are intentionally transparent and easy to inspect, but they are not semantic evaluation. They can miss unsafe paraphrases, indirect privacy leakage, and context-specific harm. They can also flag benign mentions of risky phrases when the response is actually refusing the behaviour.

## Missing Validation Layers

- No human-annotated gold label set is included.
- No real LLM judge is used unless explicitly added in future work.
- No threshold calibration against expert labels is included.
- No live monitoring, drift detection, complaint data, or production incident evidence is included.
- No legal, compliance, conduct-risk, or model-validation sign-off is implied.

## How This Could Be Extended

A stronger validation workflow would add human-reviewed gold labels, semantic similarity checks, calibrated LLM-as-judge experiments, threshold calibration by risk category and severity, adversarial test expansion, monitoring over time, and governance evidence such as ownership, review cadence, escalation paths, and residual risk acceptance.

The automated outputs should be interpreted as repeatable prototype evidence and triage signals. They are useful for learning, regression checks, and structured discussion, but not final assurance.
