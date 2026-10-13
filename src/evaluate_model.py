from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[1] / ".matplotlib_cache"))

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import CalibrationDisplay
from sklearn.metrics import (
    brier_score_loss,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)

from src.data_loader import load_config, resolve_project_path
from src.metrics import ks_statistic


def evaluate_saved_model(threshold: float = 0.5) -> dict:
    config = load_config()
    artifact_path = resolve_project_path(config["paths"]["model_pipeline"])
    if not artifact_path.exists():
        raise FileNotFoundError("Model artifact not found. Run python -m src.train_model first.")
    artifact = joblib.load(artifact_path)
    pipeline = artifact["pipeline"]
    x_test = artifact["x_test"]
    y_test = artifact["y_test"]
    y_score = pipeline.predict_proba(x_test)[:, 1]
    y_pred = (y_score >= threshold).astype(int)

    metrics = {
        "threshold": threshold,
        "positive_class": "default_flag = 1",
        "roc_auc": float(roc_auc_score(y_test, y_score)),
        "ks_statistic": ks_statistic(y_test, y_score),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "brier_score": float(brier_score_loss(y_test, y_score)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(y_test, y_pred, zero_division=0, output_dict=True),
    }

    metrics_path = resolve_project_path(config["paths"]["metrics"])
    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    _save_curves(y_test, y_score, config)
    return metrics


def _save_curves(y_test: pd.Series, y_score, config: dict) -> None:
    figures_dir = resolve_project_path(config["paths"]["figures"])
    figures_dir.mkdir(parents=True, exist_ok=True)

    fpr, tpr, _ = roc_curve(y_test, y_score)
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, label="Logistic Regression")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random baseline")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "roc_curve.png", dpi=160)
    plt.close()

    precision, recall, _ = precision_recall_curve(y_test, y_score)
    plt.figure(figsize=(7, 5))
    plt.plot(recall, precision)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.tight_layout()
    plt.savefig(figures_dir / "precision_recall_curve.png", dpi=160)
    plt.close()

    CalibrationDisplay.from_predictions(y_test, y_score, n_bins=10)
    plt.title("Calibration Curve")
    plt.tight_layout()
    plt.savefig(figures_dir / "calibration_curve.png", dpi=160)
    plt.close()


if __name__ == "__main__":
    print(json.dumps(evaluate_saved_model(), indent=2))
