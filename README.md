# Credit Risk Analytics with PD, LGD, EAD and ECL

This is a beginner-friendly Credit Risk Analytics project built in one Jupyter Notebook using the Lending Club loan dataset.

The project uses Python, pandas, NumPy, Matplotlib, Seaborn and scikit-learn. Logistic Regression is the only predictive machine learning model.

## Project Files

- `credit_risk_analysis.ipynb`: complete step-by-step project notebook
- `loan_data_2007_2014.csv`: input dataset, kept out of Git
- `requirements.txt`: Python libraries
- `outputs/`: generated charts, CSV results and model metrics

## What The Notebook Covers

1. Load and inspect the Lending Club dataset.
2. Define `default_flag` from actual `loan_status` values.
3. Run exploratory credit risk analysis.
4. Prepare features manually without scikit-learn Pipeline or ColumnTransformer.
5. Train Logistic Regression.
6. Evaluate accuracy, precision, recall, F1, ROC-AUC, KS and Brier score.
7. Explain PD, LGD, EAD and ECL with simple examples.
8. Calculate illustrative ECL using predicted PD, assumed LGD and loan amount as an exposure proxy.
9. Create risk segments from predicted PD.
10. Save essential outputs to `outputs/`.

## Important Limitations

- The model predicts historical default-related outcomes from the dataset. It is not an IFRS 9 compliant PD model.
- LGD is assumed at 60% for education unless reliable recovery modelling data is available.
- `loan_amnt` is used as an exposure proxy for illustrative ECL. It is not necessarily actual Exposure at Default.
- Risk segment thresholds are examples for learning, not lending approval rules.
- Model relationships show association, not causation.

## Latest Executed Results

The notebook was executed on the local Lending Club dataset.

| Metric | Value |
| --- | ---: |
| Accuracy | 0.7864 |
| Precision | 0.5577 |
| Recall | 0.0588 |
| F1-score | 0.1063 |
| ROC-AUC | 0.6979 |
| KS statistic | 0.2889 |
| Brier score | 0.1550 |

Illustrative risk segmentation uses predicted PD thresholds of 5% and 15%. The ECL section uses a clearly labelled 60% assumed LGD and `loan_amnt` as an exposure proxy.

## How To Run

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Open and run:

```powershell
jupyter notebook credit_risk_analysis.ipynb
```

Or execute the notebook from the terminal:

```powershell
jupyter nbconvert --to notebook --execute credit_risk_analysis.ipynb --inplace
```

After running, check the `outputs/` folder for charts, metrics and CSV exports.
