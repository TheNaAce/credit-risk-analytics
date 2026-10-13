# Data Dictionary

| Field | Description | Role |
| --- | --- | --- |
| loan_amnt | Requested or funded loan amount, depending on source definition | Predictor and exposure |
| annual_inc | Borrower annual income | Predictor |
| dti | Debt-to-income ratio | Predictor |
| int_rate | Loan interest rate | Predictor, with underwriting caveat |
| installment | Monthly installment amount | Predictor |
| emp_length | Employment length converted to numeric years | Predictor |
| grade | Lending Club loan grade | Predictor, with underwriting caveat |
| purpose | Borrower-stated loan purpose | Predictor and segment |
| home_ownership | Borrower home ownership category | Predictor |
| verification_status | Income verification status | Predictor |
| term | Loan term in months | Predictor |
| loan_status | Original Lending Club outcome/status | Target source only |
| default_flag | Binary modeled target, where 1 is default-related outcome | Target |
| predicted_pd | Logistic Regression predicted probability of `default_flag = 1` | Model output |
| risk_segment | Analytical low, medium, or high risk band | Reporting output |
