# Credit Risk Analytics and Loan Default Prediction

This project analyzes Lending Club loan data, defines a historical default target, trains a single Logistic Regression model, evaluates model discrimination and calibration, and prepares exports for a Power BI dashboard.

The project is designed for a Data Analyst, Risk Analyst, or credit risk internship portfolio. It avoids tree-based or boosting models by design. Logistic Regression is the only predictive machine learning model.

## Business Problem

Banks and NBFCs need to understand which borrower and loan characteristics are associated with higher historical default risk. This project estimates Probability of Default (PD) for completed historical loans and summarizes risk by grade, purpose, debt-to-income ratio, income, loan amount, and model-based risk segment.

## Dataset

Place the Lending Club file at:

```text
data/raw/loan_data_2007_2014.csv
```

The dataset path is configurable in `config/config.yaml`. Raw data is ignored by Git because it can be large and may contain sensitive borrower-level fields.

If you need a public source, use the Lending Club accepted-loans dataset from Lending Club historical loan data mirrors on Kaggle or similar public archives. Validate licensing and privacy requirements before sharing.

## Target Definition

The target is `default_flag`, where:

- `0` means `Fully Paid`
- `1` means `Charged Off`, `Default`, serious late status, or credit-policy charged-off status
- ongoing or ambiguous statuses such as `Current`, `In Grace Period`, and `Issued` are excluded

This is a historical default proxy, not an IFRS 9 compliant PD model. Charge-offs and defaults are observed outcomes after origination, and the model should not be used as an automated lending decision system.

## Features

Candidate predictors are limited to fields plausibly available at origination:

`loan_amnt`, `annual_inc`, `dti`, `int_rate`, `installment`, `emp_length`, `grade`, `purpose`, `home_ownership`, `verification_status`, and `term`.

`grade` and `int_rate` can already reflect prior underwriting decisions, so coefficient interpretation should be cautious.

## How To Run

```powershell
cd "C:\Users\dines\OneDrive\Documents\New project\credit-risk-analytics"
python -m pip install -r requirements.txt
python -m src.data_loader
python -m src.eda
python -m src.train_model
python -m src.evaluate_model
python -m src.export_results
pytest
```

## Outputs

- `reports/figures/`: EDA and model performance charts
- `reports/model_metrics/model_metrics.json`: ROC-AUC, KS, precision, recall, F1, Brier score, confusion matrix, and classification report
- `models/logistic_regression_pipeline.joblib`: fitted preprocessing and Logistic Regression pipeline
- `models/feature_metadata.json`: selected features and target metadata
- `data/powerbi_exports/`: dashboard-ready CSV exports

## Actual Model Results

Training and evaluation completed on the local Lending Club dataset copied to `data/raw/loan_data_2007_2014.csv`.

Modeling rows after target mapping: 235,709. Test rows: 47,142.

At the reporting threshold of 0.5:

| Metric | Value |
| --- | ---: |
| ROC-AUC | 0.7007 |
| KS statistic | 0.2978 |
| Precision | 0.3318 |
| Recall | 0.6585 |
| F1-score | 0.4413 |
| Brier score | 0.2203 |

Confusion matrix with `default_flag = 1` as the positive class:

|  | Predicted non-default | Predicted default |
| --- | ---: | ---: |
| Actual non-default | 23,431 | 13,517 |
| Actual default | 3,481 | 6,713 |

The threshold is a baseline reporting cutoff. It should not be interpreted as an approval or rejection policy.

## Risk Segmentation Results

Configured thresholds: Low Risk `<= 0.10`, Medium Risk `<= 0.25`, High Risk `> 0.25`.

| Segment | Loans | Observed default rate | Average predicted PD | Total loan amount |
| --- | ---: | ---: | ---: | ---: |
| Low Risk | 133 | 2.26% | 6.44% | 2,361,300 |
| Medium Risk | 6,077 | 6.38% | 19.63% | 75,414,075 |
| High Risk | 40,932 | 23.95% | 50.69% | 558,237,175 |

## Power BI Pages

1. Executive Overview: total loans, total loan amount, default rate, average loan amount, ROC-AUC, and KS.
2. Portfolio Risk: default rate by grade, purpose, DTI band, income band, and loan amount band.
3. Model Performance: ROC curve, precision-recall curve, calibration curve, and confusion matrix.
4. Risk Segmentation: loan count, exposure, observed default rate, and average predicted PD by segment.

## SQL

The `sql/` directory contains MySQL 8.0 compatible scripts for portfolio summaries, default-rate analysis, and risk segmentation. If MySQL is unavailable, `src/eda.py` and `src/export_results.py` produce equivalent pandas outputs.

## Limitations

- The target uses historical observed outcomes and excludes unresolved loans.
- Random holdout validation is used unless reliable origination dates are available and a time split is implemented.
- A 0.5 classification threshold is reported for standard metrics, but credit policy thresholds should be selected using validation data and business cost assumptions.
- Logistic Regression coefficients show association, not causality.
