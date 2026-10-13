-- MySQL 8.0 compatible default-rate analysis queries.
SELECT grade, COUNT(*) AS loan_count, SUM(default_flag) AS default_count, AVG(default_flag) AS default_rate
FROM lending_club_loans
GROUP BY grade
ORDER BY default_rate DESC;

SELECT purpose, COUNT(*) AS loan_count, SUM(default_flag) AS default_count, AVG(default_flag) AS default_rate
FROM lending_club_loans
GROUP BY purpose
ORDER BY default_rate DESC;

SELECT
    CASE
        WHEN dti < 10 THEN '00-10'
        WHEN dti < 20 THEN '10-20'
        WHEN dti < 30 THEN '20-30'
        WHEN dti < 40 THEN '30-40'
        ELSE '40+'
    END AS dti_band,
    COUNT(*) AS loan_count,
    SUM(default_flag) AS default_count,
    AVG(default_flag) AS default_rate
FROM lending_club_loans
GROUP BY dti_band
ORDER BY dti_band;
