from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_config(config_path: str | Path = "config/config.yaml") -> dict[str, Any]:
    path = PROJECT_ROOT / config_path
    with path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def resolve_project_path(path_value: str | Path) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def get_dataset_path(config: dict[str, Any] | None = None) -> Path:
    config = config or load_config()
    return resolve_project_path(config["paths"]["raw_data"])


def load_loan_data(path: str | Path | None = None) -> pd.DataFrame:
    config = load_config()
    dataset_path = resolve_project_path(path or config["paths"]["raw_data"])
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {dataset_path}. Place loan_data_2007_2014.csv "
            "in data/raw/ or update config/config.yaml."
        )
    loan_data_backup = pd.read_csv(dataset_path, low_memory=False)
    loan_data = loan_data_backup.copy()
    return loan_data


def inspect_dataframe(loan_data: pd.DataFrame) -> dict[str, Any]:
    return {
        "rows": int(loan_data.shape[0]),
        "columns": int(loan_data.shape[1]),
        "duplicate_rows": int(loan_data.duplicated().sum()),
        "column_names": loan_data.columns.tolist(),
        "dtypes": {column: str(dtype) for column, dtype in loan_data.dtypes.items()},
        "missing_values": loan_data.isna().sum().sort_values(ascending=False).to_dict(),
    }


if __name__ == "__main__":
    data = load_loan_data()
    summary = inspect_dataframe(data)
    for key, value in summary.items():
        print(f"{key}: {value}")
