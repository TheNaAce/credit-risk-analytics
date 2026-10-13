from __future__ import annotations

import re
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


PERCENT_COLUMNS = {"int_rate", "revol_util"}


def clean_percentage(value: object) -> float:
    if pd.isna(value):
        return np.nan
    if isinstance(value, str):
        value = value.replace("%", "").strip()
    return pd.to_numeric(value, errors="coerce")


def clean_emp_length(value: object) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).strip().lower()
    if text in {"n/a", "nan", ""}:
        return np.nan
    if "< 1" in text:
        return 0.5
    if "10+" in text:
        return 10.0
    match = re.search(r"\d+", text)
    return float(match.group()) if match else np.nan


def clean_term(value: object) -> float:
    if pd.isna(value):
        return np.nan
    match = re.search(r"\d+", str(value))
    return float(match.group()) if match else np.nan


def prepare_feature_frame(loan_data: pd.DataFrame, feature_columns: Iterable[str]) -> pd.DataFrame:
    available = [column for column in feature_columns if column in loan_data.columns]
    features = loan_data[available].copy()
    for column in features.columns:
        if column in PERCENT_COLUMNS:
            features[column] = features[column].map(clean_percentage)
        elif column == "emp_length":
            features[column] = features[column].map(clean_emp_length)
        elif column == "term":
            features[column] = features[column].map(clean_term)
        elif column in {"loan_amnt", "annual_inc", "dti", "installment"}:
            features[column] = pd.to_numeric(features[column], errors="coerce")
    return features


def split_feature_types(features: pd.DataFrame) -> tuple[list[str], list[str]]:
    numeric_features = features.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_features = [column for column in features.columns if column not in numeric_features]
    return numeric_features, categorical_features


def build_preprocessor(numeric_features: list[str], categorical_features: list[str]) -> ColumnTransformer:
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric_features),
            ("categorical", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )
