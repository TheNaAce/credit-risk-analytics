from __future__ import annotations

import pandas as pd


GOOD_STATUSES = {"Fully Paid"}
BAD_STATUSES = {
    "Charged Off",
    "Default",
    "Does not meet the credit policy. Status:Charged Off",
    "Late (31-120 days)",
}
EXCLUDED_STATUSES = {
    "Current",
    "In Grace Period",
    "Late (16-30 days)",
    "Issued",
    "Does not meet the credit policy. Status:Fully Paid",
}


def map_loan_status_to_default(status: object) -> float | None:
    if pd.isna(status):
        return None
    status_text = str(status).strip()
    if status_text in GOOD_STATUSES:
        return 0
    if status_text in BAD_STATUSES:
        return 1
    if status_text in EXCLUDED_STATUSES:
        return None
    return None


def add_default_target(loan_data: pd.DataFrame) -> pd.DataFrame:
    if "loan_status" not in loan_data.columns:
        raise KeyError("loan_status column is required to define the binary default target.")
    mapped = loan_data["loan_status"].map(map_loan_status_to_default)
    model_data = loan_data.assign(default_flag=mapped).dropna(subset=["default_flag"]).copy()
    model_data["default_flag"] = model_data["default_flag"].astype(int)
    unique_values = set(model_data["default_flag"].unique())
    if not unique_values.issubset({0, 1}):
        raise ValueError(f"default_flag must be binary, found {unique_values}.")
    return model_data


def target_mapping_table(loan_data: pd.DataFrame) -> pd.DataFrame:
    if "loan_status" not in loan_data.columns:
        raise KeyError("loan_status column is required to inspect target mapping.")
    table = loan_data["loan_status"].value_counts(dropna=False).rename_axis("loan_status").reset_index(name="loan_count")
    table["default_flag"] = table["loan_status"].map(map_loan_status_to_default)
    table["mapping_decision"] = table["default_flag"].map({0: "non_default", 1: "default"}).fillna("excluded")
    return table
