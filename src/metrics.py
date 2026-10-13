from __future__ import annotations

import numpy as np
from sklearn.metrics import roc_curve


def ks_statistic(y_true, y_score) -> float:
    fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=1)
    return float(np.max(np.abs(tpr - fpr)))
