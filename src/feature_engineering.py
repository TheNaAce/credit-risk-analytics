from __future__ import annotations

from typing import Any

import pandas as pd


def available_model_features(loan_data: pd.DataFrame, config: dict[str, Any]) -> list[str]:
    candidates = config["features"]["candidate_predictors"]
    blocked = {"loan_status", "default_flag"}
    return [column for column in candidates if column in loan_data.columns and column not in blocked]


def validate_no_target_leakage(features: list[str]) -> None:
    leakage_terms = {
        "loan_status",
        "default_flag",
        "recoveries",
        "collection_recovery_fee",
        "last_pymnt_amnt",
        "total_pymnt",
        "total_rec_prncp",
        "total_rec_int",
        "total_rec_late_fee",
    }
    overlap = sorted(set(features).intersection(leakage_terms))
    if overlap:
        raise ValueError(f"Potential leakage features selected: {overlap}")
