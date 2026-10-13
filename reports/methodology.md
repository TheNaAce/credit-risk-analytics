# Methodology

1. Load the Lending Club CSV from the configurable path in `config/config.yaml`.
2. Inspect columns, data types, duplicates, missingness, and the observed `loan_status` categories.
3. Map completed outcomes into `default_flag` and exclude unresolved or ambiguous statuses.
4. Build EDA tables with loan counts, denominators, and observed default rates.
5. Select only candidate predictors expected to be available at the prediction date.
6. Split the data before fitting preprocessing steps. The split is stratified by `default_flag`.
7. Impute missing values, scale numeric variables, and one-hot encode categoricals inside a scikit-learn pipeline.
8. Train Logistic Regression as the only predictive model.
9. Evaluate the test set using ROC-AUC, KS, precision, recall, F1, confusion matrix, Brier score, ROC curve, precision-recall curve, and calibration curve.
10. Use predicted probabilities to create configurable analytical risk bands.

The KS statistic is calculated as the maximum absolute distance between TPR and FPR over ROC thresholds, with `default_flag = 1` as the positive class.
