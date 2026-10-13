-- MySQL 8.0 compatible portfolio summary.
-- Load a cleaned/model-ready table named lending_club_loans with default_flag as 0/1.
SELECT
    COUNT(*) AS total_loans,
    SUM(loan_amnt) AS total_loan_amount,
    AVG(loan_amnt) AS average_loan_amount,
    SUM(default_flag) AS default_count,
    AVG(default_flag) AS historical_default_rate
FROM lending_club_loans;
