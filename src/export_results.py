from __future__ import annotations

import json

import joblib
import pandas as pd

from src.data_loader import load_config, resolve_project_path
from src.risk_segmentation import summarize_segments


def export_model_results() -> None:
    config = load_config()
    artifact = joblib.load(resolve_project_path(config["paths"]["model_pipeline"]))
    pipeline = artifact["pipeline"]
    x_test = artifact["x_test"].copy()
    y_test = artifact["y_test"].copy()
    predicted_pd = pipeline.predict_proba(x_test)[:, 1]

    scoring = x_test.copy()
    scoring["default_flag"] = y_test.values
    scoring["predicted_pd"] = predicted_pd
    thresholds = config["model"]["risk_thresholds"]
    segments = summarize_segments(
        scoring,
        low_max=thresholds["low_max"],
        medium_max=thresholds["medium_max"],
    )

    export_dir = resolve_project_path(config["paths"]["powerbi_exports"])
    export_dir.mkdir(parents=True, exist_ok=True)
    scoring.to_csv(export_dir / "test_set_predictions.csv", index=False)
    segments.to_csv(export_dir / "risk_segment_summary.csv", index=False)

    metrics_path = resolve_project_path(config["paths"]["metrics"])
    if metrics_path.exists():
        metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        pd.DataFrame([metrics]).drop(columns=["classification_report"], errors="ignore").to_csv(
            export_dir / "model_metrics.csv", index=False
        )


if __name__ == "__main__":
    export_model_results()
    print("Power BI model exports created.")
