# Model Card

## Model

The project trains Logistic Regression and Random Forest classifiers for synthetic loan-default pre-screening. The Random Forest is used as the champion model for fairness, calibration, and robustness evidence.

## Intended Use

Supervisory demonstration of model-risk evaluation methods. The model must not be used for real lending.

## Inputs

Income, employment status, age band, debt-to-income ratio, credit history length, existing debt, missed payments, housing status, region, digital access score, and protected-group proxy.

## Evaluation

Generated metrics include AUC, precision, recall, F1, confusion matrix, Brier score, fairness gaps, calibration table, and stress results.

