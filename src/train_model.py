from __future__ import annotations

import json

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.data_loader import load_config, load_loan_data, resolve_project_path
from src.feature_engineering import available_model_features, validate_no_target_leakage
from src.preprocessing import build_preprocessor, prepare_feature_frame, split_feature_types
from src.target import add_default_target


def train_logistic_regression() -> Pipeline:
    config = load_config()
    loan_data = load_loan_data()
    model_data = add_default_target(loan_data)
    feature_columns = available_model_features(model_data, config)
    validate_no_target_leakage(feature_columns)
    if not feature_columns:
        raise ValueError("No configured candidate predictors are available in the dataset.")

    features = prepare_feature_frame(model_data, feature_columns)
    target = model_data["default_flag"]
    assert set(target.unique()).issubset({0, 1})

    numeric_features, categorical_features = split_feature_types(features)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config["model"]["test_size"],
        random_state=config["project"]["random_seed"],
        stratify=target,
    )
    assert set(y_train.unique()) == {0, 1}
    assert set(y_test.unique()) == {0, 1}

    preprocessor = build_preprocessor(numeric_features, categorical_features)
    classifier = LogisticRegression(
        max_iter=config["model"]["max_iter"],
        class_weight=config["model"].get("class_weight"),
        random_state=config["project"]["random_seed"],
    )
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("model", classifier)])
    pipeline.fit(x_train, y_train)

    model_path = resolve_project_path(config["paths"]["model_pipeline"])
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "x_test": x_test, "y_test": y_test}, model_path)

    metadata = {
        "features": feature_columns,
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "target": "default_flag",
        "positive_class": "default_flag = 1",
        "class_weight": config["model"].get("class_weight"),
        "note": "Only Logistic Regression is trained. Grade and interest rate may reflect prior underwriting.",
    }
    metadata_path = resolve_project_path(config["paths"]["feature_metadata"])
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    processed_path = resolve_project_path(config["paths"]["processed_data"])
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    pd.concat([features, target], axis=1).to_csv(processed_path, index=False)
    return pipeline


if __name__ == "__main__":
    train_logistic_regression()
    print("Saved Logistic Regression pipeline and feature metadata.")
