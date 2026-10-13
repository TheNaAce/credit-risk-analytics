# Notebook Workflow

Suggested notebook sequence:

1. `01_data_understanding.ipynb`: load data, inspect schema, missingness, duplicates, and loan status values.
2. `02_exploratory_analysis.ipynb`: create default-rate charts and business observations.
3. `03_credit_risk_analysis.ipynb`: compare portfolio risk by grade, purpose, DTI, income, employment length, and loan amount.
4. `04_logistic_regression.ipynb`: train the Logistic Regression pipeline.
5. `05_model_evaluation.ipynb`: evaluate ROC-AUC, KS, calibration, and segmentation.

The production logic lives in `src/` so notebooks can stay readable and reproducible.
