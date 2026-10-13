-- Requires a predictions table with predicted_pd and risk_segment.
SELECT
    risk_segment,
    COUNT(*) AS loan_count,
    SUM(loan_amnt) AS total_loan_amount,
    AVG(int_rate) AS average_interest_rate,
    AVG(predicted_pd) AS average_predicted_pd,
    AVG(default_flag) AS observed_default_rate
FROM lending_club_predictions
GROUP BY risk_segment
ORDER BY average_predicted_pd;

SELECT
    grade,
    purpose,
    COUNT(*) AS loan_count,
    AVG(default_flag) AS observed_default_rate,
    AVG(predicted_pd) AS average_predicted_pd
FROM lending_club_predictions
GROUP BY grade, purpose
HAVING COUNT(*) >= 100
ORDER BY observed_default_rate DESC
LIMIT 25;
