# Power BI Dashboard Guide

Use the CSV files from `data/powerbi_exports/`.

Recommended pages:

## Executive Overview

Cards: total loans, total loan amount, historical default rate, average loan amount, ROC-AUC, and KS.

## Portfolio Risk

Charts: default rate by grade, purpose, DTI band, income band, and loan amount band. Include loan counts as labels or tooltip fields.

## Model Performance

Charts: ROC curve, precision-recall curve, calibration curve, confusion matrix, precision, recall, F1, and Brier score.

## Risk Segmentation

Charts: loan count by risk segment, total loan exposure by risk segment, and observed default rate versus average predicted PD.

Suggested DAX measures:

```DAX
Total Loans = COUNTROWS('portfolio')
Total Loan Amount = SUM('portfolio'[loan_amnt])
Default Rate = AVERAGE('portfolio'[default_flag])
Average Predicted PD = AVERAGE('predictions'[predicted_pd])
```
