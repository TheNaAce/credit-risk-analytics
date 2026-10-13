from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".matplotlib_cache"))

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.data_loader import load_config, load_loan_data, resolve_project_path
from src.preprocessing import clean_percentage
from src.target import add_default_target, target_mapping_table


def rate_table(data: pd.DataFrame, group_column: str) -> pd.DataFrame:
    grouped = data.groupby(group_column, dropna=False).agg(
        loan_count=("default_flag", "size"),
        default_count=("default_flag", "sum"),
        observed_default_rate=("default_flag", "mean"),
        total_loan_amount=("loan_amnt", "sum") if "loan_amnt" in data.columns else ("default_flag", "size"),
    )
    return grouped.reset_index().sort_values("observed_default_rate", ascending=False)


def add_bands(data: pd.DataFrame) -> pd.DataFrame:
    output = data.copy()
    if "int_rate" in output.columns:
        output["int_rate_numeric"] = output["int_rate"].map(clean_percentage)
        output["int_rate_band"] = pd.cut(output["int_rate_numeric"], bins=[0, 8, 12, 16, 20, 100], include_lowest=True)
    if "dti" in output.columns:
        output["dti_band"] = pd.cut(pd.to_numeric(output["dti"], errors="coerce"), bins=[0, 10, 20, 30, 40, 100], include_lowest=True)
    if "annual_inc" in output.columns:
        output["income_band"] = pd.cut(pd.to_numeric(output["annual_inc"], errors="coerce"), bins=[0, 30000, 60000, 100000, 150000, float("inf")], include_lowest=True)
    if "loan_amnt" in output.columns:
        output["loan_amount_band"] = pd.cut(pd.to_numeric(output["loan_amnt"], errors="coerce"), bins=[0, 5000, 10000, 15000, 25000, 40000], include_lowest=True)
    return output


def run_eda_exports() -> None:
    config = load_config()
    loan_data = load_loan_data()
    model_data = add_bands(add_default_target(loan_data))
    export_dir = resolve_project_path(config["paths"]["powerbi_exports"])
    figure_dir = resolve_project_path(config["paths"]["figures"])
    export_dir.mkdir(parents=True, exist_ok=True)
    figure_dir.mkdir(parents=True, exist_ok=True)

    target_mapping_table(loan_data).to_csv(export_dir / "target_mapping.csv", index=False)
    overall = pd.DataFrame(
        {
            "metric": ["loan_count", "default_count", "observed_default_rate"],
            "value": [len(model_data), model_data["default_flag"].sum(), model_data["default_flag"].mean()],
        }
    )
    overall.to_csv(export_dir / "portfolio_summary.csv", index=False)

    dimensions = ["grade", "purpose", "emp_length", "int_rate_band", "dti_band", "income_band", "loan_amount_band"]
    for column in dimensions:
        if column in model_data.columns:
            table = rate_table(model_data, column)
            table.to_csv(export_dir / f"default_rate_by_{column}.csv", index=False)
            plt.figure(figsize=(9, 5))
            sns.barplot(data=table, x=column, y="observed_default_rate")
            plt.xticks(rotation=45, ha="right")
            plt.title(f"Default Rate by {column}")
            plt.ylabel("Observed Default Rate")
            plt.tight_layout()
            plt.savefig(figure_dir / f"default_rate_by_{column}.png", dpi=160)
            plt.close()


if __name__ == "__main__":
    run_eda_exports()
    print("EDA tables and figures exported.")
