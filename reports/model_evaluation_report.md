# Model Evaluation Report

The Logistic Regression pipeline was trained and evaluated on the Lending Club CSV placed in `data/raw/`.

```powershell
python -m src.train_model
python -m src.evaluate_model
python -m src.export_results
```

Actual test-set results at the 0.5 reporting threshold:

| Metric | Value |
| --- | ---: |
| ROC-AUC | 0.7007 |
| KS statistic | 0.2978 |
| Precision | 0.3318 |
| Recall | 0.6585 |
| F1-score | 0.4413 |
| Brier score | 0.2203 |

Confusion matrix:

|  | Predicted non-default | Predicted default |
| --- | ---: | ---: |
| Actual non-default | 23,431 | 13,517 |
| Actual default | 3,481 | 6,713 |

Interpretation notes:

- ROC-AUC measures ranking discrimination.
- KS measures the maximum separation between default and non-default score distributions.
- Brier score measures probability calibration error.
- The 0.5 threshold is a reporting baseline, not a recommended credit decision cutoff.
