from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import numpy as np


def log_loss(y_true: np.ndarray, y_prob: np.ndarray, eps: float = 1e-12) -> float:
    y_true = y_true.astype(np.float64)
    y_prob = np.clip(y_prob.astype(np.float64), eps, 1.0 - eps)
    return float(-np.mean(y_true * np.log(y_prob) + (1.0 - y_true) * np.log(1.0 - y_prob)))


def accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = y_true.astype(np.int64)
    y_pred = y_pred.astype(np.int64)
    return float(np.mean(y_true == y_pred))


def fairness_gap(y_true: np.ndarray, y_pred: np.ndarray, g: np.ndarray) -> float:
    """
    Absolute difference in accuracy across groups (0 vs 1).
    """
    g = g.astype(np.int64)
    mask0 = g == 0
    mask1 = g == 1
    # Avoid division by zero in edge cases
    acc0 = accuracy(y_true[mask0], y_pred[mask0]) if np.any(mask0) else 0.0
    acc1 = accuracy(y_true[mask1], y_pred[mask1]) if np.any(mask1) else 0.0
    return float(abs(acc0 - acc1))


def compute_all(y_true: np.ndarray, y_prob: np.ndarray, y_pred: np.ndarray, g: np.ndarray) -> Dict[str, float]:
    return {
        "accuracy": accuracy(y_true, y_pred),
        "loss": log_loss(y_true, y_prob),
        "fairness_gap": fairness_gap(y_true, y_pred, g),
    }


