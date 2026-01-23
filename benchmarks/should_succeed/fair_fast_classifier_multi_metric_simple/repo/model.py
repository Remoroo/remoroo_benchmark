from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class LogisticRegression:
    w: np.ndarray  # (D,)
    b: float

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        z = X @ self.w + self.b
        # NOTE: intentionally naive sigmoid (can overflow for large |z|)
        return 1.0 / (1.0 + np.exp(-z))

    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self.predict_proba(X) >= 0.5).astype(np.int64)


def init_model(n_features: int, seed: int) -> LogisticRegression:
    rng = np.random.RandomState(seed + 2)
    w = (0.01 * rng.randn(n_features)).astype(np.float64)
    b = 0.0
    return LogisticRegression(w=w, b=b)


def step_sgd(
    model: LogisticRegression,
    x: np.ndarray,
    y: int,
    lr: float,
    l2_reg: float,
    fairness_grad: float = 0.0,
) -> None:
    """
    One-sample SGD update (intentionally slow; benchmark expects vectorization).
    fairness_grad is a crude additive term that can destabilize training if misused.
    """
    p = model.predict_proba(x[None, :])[0]
    grad_w = (p - float(y)) * x + l2_reg * model.w + fairness_grad
    grad_b = (p - float(y))
    model.w = model.w - lr * grad_w
    model.b = float(model.b - lr * grad_b)


