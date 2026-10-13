from __future__ import annotations

import pandas as pd


def assign_risk_segment(predicted_pd: float, low_max: float = 0.10, medium_max: float = 0.25) -> str:
    if predicted_pd <= low_max:
        return "Low Risk"
    if predicted_pd <= medium_max:
        return "Medium Risk"
    return "High Risk"


def summarize_segments(
    data: pd.DataFrame,
    probability_column: str = "predicted_pd",
    target_column: str = "default_flag",
    loan_amount_column: str = "loan_amnt",
    low_max: float = 0.10,
    medium_max: float = 0.25,
) -> pd.DataFrame:
    output = data.copy()
    output["risk_segment"] = output[probability_column].map(lambda value: assign_risk_segment(value, low_max, medium_max))
    aggregations = {
        "loan_count": (target_column, "size"),
        "observed_default_rate": (target_column, "mean"),
        "average_predicted_pd": (probability_column, "mean"),
    }
    if loan_amount_column in output.columns:
        aggregations["total_loan_amount"] = (loan_amount_column, "sum")
    return output.groupby("risk_segment").agg(**aggregations).reset_index()
