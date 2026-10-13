-- Example MySQL 8.0 loading flow. Adjust paths for your machine.
CREATE DATABASE IF NOT EXISTS credit_risk;
USE credit_risk;

-- Create table structure by importing data/processed/model_ready_loans.csv with MySQL Workbench
-- Table Data Import Wizard, or define explicit column types after inspecting the CSV.
-- Keep raw borrower-level data out of version control.
