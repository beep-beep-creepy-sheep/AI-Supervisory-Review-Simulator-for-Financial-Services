# Supervisory Evidence Pack

## Executive Summary
Emerald Credit Bank's fictional AI estate was assessed across model risk, fairness, consumer harm, explainability, robustness, privacy, prompt injection, agentic tool-use, and governance maturity. The review combines statistical model evaluation, structured GenAI test cases, simulated agent tool-call review, and a risk register.

## AI System Inventory
| System | Purpose | Review focus |
|---|---|---|
| Credit Risk Model | Loan pre-screening | Performance, calibration, fairness, robustness |
| GenAI Consumer Finance Assistant | Customer support and general financial guidance | Harmful advice, hallucination, vulnerable consumers, prompt injection |
| Agentic Loan Assistant | Simulated tool-using loan workflow | Tool authorization, privacy, escalation, over-automation |

## Methodology
The pipeline uses deterministic synthetic data, benchmark ML models, rule-based GenAI scoring with mock-judge rationale, agentic tool logs, and a severity-likelihood-detectability scoring model. Automated results are suitable for triage and supervisory evidence, not as a substitute for legal, conduct, or model validation sign-off.

## Credit Model Findings
```json
{
  "logistic_regression": {
    "auc": 0.738688,
    "roc_auc_integral": 0.738688,
    "precision": 0.3007518796992481,
    "recall": 0.64,
    "f1": 0.4092071611253197,
    "brier_score": 0.20198969324917598,
    "confusion_matrix": [
      [
        439,
        186
      ],
      [
        45,
        80
      ]
    ]
  },
  "random_forest": {
    "auc": 0.7382656,
    "roc_auc_integral": 0.7382656,
    "precision": 0.3592814371257485,
    "recall": 0.48,
    "f1": 0.410958904109589,
    "brier_score": 0.1644077072402183,
    "confusion_matrix": [
      [
        518,
        107
      ],
      [
        65,
        60
      ]
    ]
  }
}
```

Fairness summary:
| group   |   n |   approval_rate |   default_capture_rate |   false_positive_rate |   approval_rate_gap_to_best |   default_capture_rate_gap_to_best |   false_positive_rate_gap_to_best |
|:--------|----:|----------------:|-----------------------:|----------------------:|----------------------------:|-----------------------------------:|----------------------------------:|
| A       | 552 |        0.813406 |               0.421687 |              0.144989 |                    0.136638 |                           0.173551 |                          0.105011 |
| B       | 198 |        0.676768 |               0.595238 |              0.25     |                    0.136638 |                           0.173551 |                          0.105011 |

Robustness summary:
```json
{
  "baseline_auc": 0.7382656,
  "macroeconomic_stress_auc": 0.7287296000000001,
  "missing_value_auc": 0.7080192000000001,
  "stress_auc_delta": -0.009535999999999878,
  "missing_auc_delta": -0.030246399999999896
}
```

Top feature-importance evidence:
| feature                           |   importance |
|:----------------------------------|-------------:|
| num__debt_to_income               |   0.282365   |
| num__existing_debt                |   0.131574   |
| num__credit_history_length        |   0.123054   |
| num__income                       |   0.107759   |
| num__digital_access_score         |   0.0880102  |
| num__missed_payments_12m          |   0.0558145  |
| cat__employment_status_unemployed |   0.0448023  |
| cat__age_band_35-49               |   0.0131527  |
| cat__housing_status_mortgage      |   0.0124428  |
| cat__housing_status_private_rent  |   0.0123711  |
| cat__employment_status_employed   |   0.0121324  |
| cat__region_Dublin                |   0.0112974  |
| cat__employment_status_part_time  |   0.0106337  |
| cat__age_band_25-34               |   0.0102786  |
| cat__housing_status_owner         |   0.00867465 |

## GenAI Findings
- Test cases: 120
- Pass rate: 87.5%
- Highest failed severity: 2

## Agentic Tool-Use Findings
- Test cases: 50
- Pass rate: 82.0%
- Highest failed severity: 2

## Risk Register
| system                 | category                         | rating   | finding                                                               |
|:-----------------------|:---------------------------------|:---------|:----------------------------------------------------------------------|
| Credit Risk Model      | Fairness and discrimination risk | high     | Protected proxy group metrics show measurable outcome gaps.           |
| Agentic Loan Assistant | Agentic tool-use risk            | high     | Tool authorization and escalation behavior need supervisory evidence. |
| Credit Risk Model      | Model performance risk           | medium   | Model discrimination is adequate but requires threshold governance.   |
| Credit Risk Model      | Robustness and drift risk        | medium   | Performance shifts under macroeconomic and missing-data stress.       |
| GenAI Assistant        | Consumer harm risk               | medium   | Automated test suite found residual unsafe-response risk.             |

## Mitigation Recommendations
- Define risk appetite thresholds for model performance, fairness gaps, and calibration drift.
- Use red-team style GenAI regression suites before assistant releases.
- Restrict agentic tool access by user intent, customer consent, and documented purpose.
- Require human review for vulnerable consumers and high-impact lending outcomes.
- Maintain board-level AI management information and independent validation evidence.

## Mock Supervisory Conclusion
The systems are demonstrable and partially controlled, but supervisory confidence depends on stronger fairness thresholds, continuous adversarial testing, and clearer accountability for agentic tool use.
